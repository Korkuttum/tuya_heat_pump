"""Device "last seen" tracking and the online/offline decision for cloud and
MQTT connections.

Why this exists
---------------
Tuya's own `online` flag cannot be trusted (devices show online while they
are not, and the cloud keeps returning old DP values for devices that are
long gone). The only fact we can establish ourselves is *when we last got a
real signal from the device*:

- a cloud poll returns the time each DP was last reported by the device,
- an MQTT push carries the time the device reported the DP (`t`),
- in local mode a successful status/receive proves the device answered.

The online decision is derived from that single `last_seen` value:

    online  <=>  now - last_seen <= timeout

The timeout depends on how talkative the device is:

- chatty devices (heat pumps push a measurement roughly every second) get a
  short timeout, so a device that really went away is noticed within
  minutes,
- quiet devices (a thermostat that only reports when something changes, a
  machine that is idle for days) get a long timeout, so they are not
  reported as offline just because nothing changed.

"Chatty" is learned from observation and then latched: once a device has
shown a sustained high message rate it stays chatty until Home Assistant is
restarted (it is re-learned within minutes). Latching matters: a chatty
device that falls silent must NOT slip back to the long quiet timeout.

A user supplied timeout (minutes, 0 = automatic) overrides both.

Known limit: a quiet device that is plugged in and a quiet device that is
unplugged look identical until the timeout elapses. Nothing we can observe
distinguishes them.

This module has no Home Assistant imports so it can be unit tested on its
own. All times are epoch seconds; callers pass `now` explicitly.
"""
from __future__ import annotations

from collections import deque

# Timeout for devices that are not chatty (seconds).
QUIET_TIMEOUT_S = 12 * 3600
# Floor of the timeout for chatty devices (seconds).
CHATTY_MIN_TIMEOUT_S = 600
# Latch "chatty" after this many messages inside the sliding window ...
CHATTY_MIN_MESSAGES = 60
CHATTY_WINDOW_S = 600
# ... provided they are spread over at least this long (a short burst, for
# example the settings dump after a user changed something, is not chatty).
CHATTY_MIN_SPAN_S = 300
# Cloud-only: latch "chatty" when the newest DP time advanced in this many
# polls in a row.
CLOUD_ADVANCE_POLLS = 6
# A chatty device silent this long gets a verification poll (is the MQTT
# stream broken, or is the device really gone?).
SILENCE_VERIFY_S = 300
VERIFY_COOLDOWN_S = 600
# Ignore absurd timestamps from a device clock far in the future.
MAX_FUTURE_SKEW_S = 5


def _normalise_ts(ts: float | int | None) -> float | None:
    """Tuya timestamps are milliseconds; accept seconds too."""
    if ts is None:
        return None
    try:
        ts = float(ts)
    except (TypeError, ValueError):
        return None
    if ts <= 0:
        return None
    if ts > 1e11:  # milliseconds
        ts /= 1000.0
    return ts


class OnlineTracker:
    """Tracks the last time a device was seen and derives online state."""

    def __init__(self, override_minutes: float = 0, poll_interval_s: float = 180) -> None:
        self.override_minutes = float(override_minutes or 0)
        self.poll_interval_s = float(poll_interval_s or 180)
        self.last_seen: float | None = None
        self.last_seen_source: str | None = None
        self.chatty: bool = False
        # True only when the MQTT message RATE latched chatty (not the cloud
        # poll heuristic): this is what decides whether to drop the MQTT
        # subscription to protect the Tuya message quota.
        self.stream_chatty: bool = False
        self._msg_times: deque[float] = deque(maxlen=2000)
        self._last_cloud_stamp: float = 0.0
        self._cloud_streak: int = 0
        self._last_verify: float = 0.0

    # ------------------------------------------------------------------
    # signals
    # ------------------------------------------------------------------
    def _see(self, ts: float, now: float, source: str) -> None:
        ts = min(ts, now + MAX_FUTURE_SKEW_S)
        ts = min(ts, now)
        if self.last_seen is None or ts > self.last_seen:
            self.last_seen = ts
            self.last_seen_source = source

    def note_message(self, ts: float | int | None, now: float, count: int = 1) -> None:
        """An MQTT message from this device arrived (`ts` = device report time;
        `count` = number of DPs in it, informational only)."""
        stamp = _normalise_ts(ts)
        self._see(stamp if stamp is not None else now, now, "mqtt")
        # One entry per MESSAGE, not per DP in it: a heat pump message carries
        # many DPs, and counting them individually filled the window so fast
        # that its span never reached CHATTY_MIN_SPAN_S.
        self._msg_times.append(now)
        cutoff = now - CHATTY_WINDOW_S
        while self._msg_times and self._msg_times[0] < cutoff:
            self._msg_times.popleft()
        if (
            not self.chatty
            and len(self._msg_times) >= CHATTY_MIN_MESSAGES
            and self._msg_times[-1] - self._msg_times[0] >= CHATTY_MIN_SPAN_S
        ):
            self.chatty = True
            self.stream_chatty = True

    def note_cloud(self, stamp: float | int | None, now: float) -> None:
        """A cloud poll finished; `stamp` is the newest DP report time in it."""
        ts = _normalise_ts(stamp)
        if ts is None:
            return
        self._see(ts, now, "cloud")
        if ts > self._last_cloud_stamp + 0.5:
            self._cloud_streak += 1
        else:
            self._cloud_streak = 0
        self._last_cloud_stamp = max(self._last_cloud_stamp, ts)
        if self._cloud_streak >= CLOUD_ADVANCE_POLLS:
            self.chatty = True

    def note_local(self, now: float) -> None:
        """Local mode: the device answered (status, receive)."""
        self._see(now, now, "local")

    # ------------------------------------------------------------------
    # decision
    # ------------------------------------------------------------------
    def timeout_s(self) -> float:
        if self.override_minutes > 0:
            return self.override_minutes * 60.0
        if self.chatty:
            return max(CHATTY_MIN_TIMEOUT_S, 3.0 * self.poll_interval_s)
        return float(QUIET_TIMEOUT_S)

    def silence_s(self, now: float) -> float | None:
        if self.last_seen is None:
            return None
        return max(0.0, now - self.last_seen)

    def is_online(self, now: float) -> bool | None:
        """True/False once the device has been seen at least once, else None
        (unknown: the caller should keep whatever state it has)."""
        silence = self.silence_s(now)
        if silence is None:
            return None
        return silence <= self.timeout_s()

    def should_verify(self, now: float) -> bool:
        """Chatty device unusually silent: worth one verification poll."""
        silence = self.silence_s(now)
        if silence is None or not self.chatty:
            return False
        if silence < SILENCE_VERIFY_S:
            return False
        return now - self._last_verify >= VERIFY_COOLDOWN_S

    def mark_verified(self, now: float) -> None:
        self._last_verify = now

    # ------------------------------------------------------------------
    # presentation
    # ------------------------------------------------------------------
    def attributes(self, now: float) -> dict:
        """State attributes, deliberately rounded to whole minutes so that a
        1 Hz MQTT stream does not rewrite the entity state every second."""
        from datetime import datetime, timezone

        out: dict = {"chatty": self.chatty}
        if self.last_seen is not None:
            minute = int(self.last_seen // 60) * 60
            out["last_seen"] = datetime.fromtimestamp(minute, timezone.utc).isoformat()
            out["last_seen_source"] = self.last_seen_source
            out["silence_minutes"] = int((now - self.last_seen) // 60)
        out["offline_timeout_minutes"] = int(self.timeout_s() // 60)
        return out
