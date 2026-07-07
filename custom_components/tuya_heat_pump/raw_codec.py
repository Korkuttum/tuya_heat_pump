"""Shared raw-payload field encode/decode helpers for Tuya Heatpump.

A single Tuya `raw`-type DP (base64) often packs several logical values
(int32/int16/uint8) at fixed byte offsets. Sensor, switch, number, and
select entities that read/write an individual packed field all use these
same helpers, so decode and encode stay in lock-step and there's only
one place to fix if the byte math is ever wrong.
"""
from __future__ import annotations
import base64
import logging
import struct

_LOGGER = logging.getLogger(__name__)

# (struct format, size in bytes) per supported encoding.
_STRUCT_FORMAT = {
    "int32_be": (">i", 4),
    "int16_be": (">h", 2),
    "uint8": (">B", 1),
}


def decode_raw_field(b64_string: str | None, field_index: int,
                      encoding: str = "int32_be") -> int | None:
    """Decode a single field out of a base64-encoded raw payload.

    Supports:
        - int32_be : 4-byte big-endian signed  (large status blobs)
        - int16_be : 2-byte big-endian signed  (small counters/timers)
        - uint8    : 1-byte unsigned            (single-byte flags)
    """
    if not b64_string:
        return None
    fmt_size = _STRUCT_FORMAT.get(encoding)
    if fmt_size is None:
        _LOGGER.warning("Unknown raw encoding: %s", encoding)
        return None
    fmt, size = fmt_size
    try:
        payload = base64.b64decode(b64_string)
        return struct.unpack_from(fmt, payload, field_index * size)[0]
    except Exception as err:
        _LOGGER.debug("Raw decode failed at field_index=%s (%s): %s",
                      field_index, encoding, err)
        return None


def encode_raw_field(b64_string: str | None, field_index: int,
                      encoding: str, value) -> str | None:
    """Patch a single field inside a base64 raw payload and return the
    new full payload as base64 — the inverse of decode_raw_field.

    Tuya raw DPs are opaque byte blobs: there is no partial write. Only
    the bytes for this one field change here; every other packed field
    already in the payload is preserved untouched, and the caller sends
    the whole patched payload back as a normal DP write.
    """
    if not b64_string:
        _LOGGER.error("Cannot encode raw field: no existing payload to patch")
        return None
    fmt_size = _STRUCT_FORMAT.get(encoding)
    if fmt_size is None:
        _LOGGER.warning("Unknown raw encoding: %s", encoding)
        return None
    fmt, size = fmt_size
    try:
        payload = bytearray(base64.b64decode(b64_string))
        offset = field_index * size
        if offset + size > len(payload):
            _LOGGER.error(
                "field_index %s (%s, %s bytes) is out of range for a "
                "%s-byte payload — refusing to write out of bounds",
                field_index, encoding, size, len(payload),
            )
            return None
        struct.pack_into(fmt, payload, offset, int(round(value)))
        return base64.b64encode(bytes(payload)).decode("ascii")
    except Exception as err:
        _LOGGER.error("Raw encode failed at field_index=%s (%s): %s",
                       field_index, encoding, err)
        return None


def resolve_raw_source(coordinator, config: dict) -> str | None:
    """Return the coordinator.data key that holds the raw payload for
    this entity. Uses explicit `raw_source` from the model if provided,
    otherwise falls back to a dp_id lookup against the coordinator's
    raw-DP cache. This lets model files omit `raw_source` when the
    dp_id alone is enough to identify the payload."""
    explicit = config.get("raw_source")
    if explicit:
        return explicit
    dp_id = config.get("dp_id")
    if dp_id is None:
        return None
    return getattr(coordinator, "raw_code_by_dp_id", {}).get(dp_id)


def watch_pending_raw_entities(config_entry, coordinator, async_add_entities,
                                 pending, entity_class, logger):
    """Retry adding raw-field entities whose payload wasn't available yet
    at platform setup time.

    Cloud's single `/shadow/properties` call tends to return every DP in
    one shot, but local (LAN) connections sometimes don't include large
    "raw" DPs in the very first `.status()` poll — they arrive a bit
    later over the persistent socket. Without this, an entity whose raw
    source wasn't ready on the first pass would be skipped forever.

    This registers a coordinator listener that re-checks the pending
    list on every update, adds any entity whose raw_source has since
    become resolvable, and stops watching it once added. `pending` is a
    plain list of (code, config) tuples, mutated in place so the caller
    doesn't need to manage its own bookkeeping. `entity_class` must have
    the same (coordinator, code, config) constructor signature used by
    every entity class in this integration.
    """
    if not pending:
        return

    def _check_pending():
        if not pending:
            return
        newly_ready = []
        still_pending = []
        for code, config in pending:
            raw_source = resolve_raw_source(coordinator, config)
            if raw_source and coordinator.data and raw_source in coordinator.data:
                resolved_config = {**config, "raw_source": raw_source}
                newly_ready.append(entity_class(coordinator, code, resolved_config))
                logger.info(
                    "Raw source now available, adding delayed entity: %s (%s)",
                    resolved_config.get('name', code), code,
                )
            else:
                still_pending.append((code, config))
        pending[:] = still_pending
        if newly_ready:
            async_add_entities(newly_ready)

    remove_listener = coordinator.async_add_listener(_check_pending)
    config_entry.async_on_unload(remove_listener)
