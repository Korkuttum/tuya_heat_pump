"""
Tuya RAW Payload Explorer
=========================
Live-updating GUI for reverse-engineering `raw` type Tuya data-points.

If the GUI ever freezes, run from a terminal (cmd / powershell) instead
of double-clicking — the script prints a full trace to stdout so you
can see exactly where it got stuck.

Dependencies auto-installed on first run: requests
"""

import time
import hmac
import hashlib
import json
import base64
import struct
import os
import sys
import subprocess
import threading
import queue
import traceback
from datetime import datetime


# ------------------------------------------------------------------ #
# Debug logger — writes to raw_explorer.log next to the script,
# and also to stdout when a real console is attached (i.e. when
# launched from cmd/terminal, or when the .py extension is used
# instead of .pyw). No console → no noise for the end user.
# ------------------------------------------------------------------ #
_LOG_LOCK = threading.Lock()

# Log file lives next to the script (or in cwd if we can't determine that)
try:
    _LOG_PATH = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "raw_explorer.log"
    )
except NameError:
    _LOG_PATH = "raw_explorer.log"

try:
    _LOG_FILE = open(_LOG_PATH, "a", encoding="utf-8")
    _LOG_FILE.write(f"\n\n=== Session start {datetime.now().isoformat()} ===\n")
    _LOG_FILE.flush()
except Exception:
    _LOG_FILE = None

# stdout is None (or broken) when launched via pythonw.exe / .pyw on Windows
_HAS_CONSOLE = sys.stdout is not None and hasattr(sys.stdout, "write")


def log(msg):
    ts = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    line = f"[{ts}] {msg}"
    with _LOG_LOCK:
        if _LOG_FILE is not None:
            try:
                _LOG_FILE.write(line + "\n")
                _LOG_FILE.flush()
            except Exception:
                pass
        if _HAS_CONSOLE:
            try:
                print(line, flush=True)
            except Exception:
                pass


log("Script starting...")


def log_exception(prefix=""):
    """Log the current exception traceback safely (works under pythonw.exe)."""
    try:
        import io
        buf = io.StringIO()
        traceback.print_exc(file=buf)
        log(f"{prefix}\n{buf.getvalue()}")
    except Exception:
        pass


# ------------------------------------------------------------------ #
# Package bootstrap
# ------------------------------------------------------------------ #
def _ensure(pkg, imp=None):
    """Install a Python package via pip if it can't be imported.
    Cross-platform: works on Windows, macOS, and Linux.
    Handles PEP 668 'externally-managed-environment' by retrying with
    --break-system-packages (common on modern Ubuntu / Homebrew Python).
    """
    imp = imp or pkg
    try:
        __import__(imp)
        return
    except ImportError:
        pass

    log(f"Installing '{pkg}'...")
    cmd = [sys.executable, "-m", "pip", "install", "--quiet", pkg]
    try:
        subprocess.check_call(cmd)
        return
    except subprocess.CalledProcessError as e:
        # PEP 668 lockout on Debian/Ubuntu 23+ and Homebrew Python
        log(f"pip install failed ({e}). Retrying with --user...")
        try:
            subprocess.check_call(cmd + ["--user"])
            return
        except subprocess.CalledProcessError:
            pass
        log("Retrying with --break-system-packages...")
        try:
            subprocess.check_call(cmd + ["--break-system-packages"])
            return
        except subprocess.CalledProcessError as e2:
            msg = (
                f"Could not install '{pkg}' automatically.\n\n"
                f"Please run this command manually and try again:\n\n"
                f"    {sys.executable} -m pip install {pkg}\n"
            )
            log(f"FATAL: {msg}")
            # If we have a display, show a message box so the user knows what happened.
            try:
                import tkinter.messagebox as _mb
                import tkinter as _tk
                r = _tk.Tk(); r.withdraw()
                _mb.showerror("Missing package", msg)
                r.destroy()
            except Exception:
                pass
            sys.exit(1)


_ensure("requests")

import requests  # noqa: E402
import tkinter as tk  # noqa: E402
from tkinter import ttk, messagebox, filedialog  # noqa: E402

log("Imports done.")


# ------------------------------------------------------------------ #
# HTTP session — reuse TCP+TLS connection across polls
# ------------------------------------------------------------------ #
_SESSION = requests.Session()


# ------------------------------------------------------------------ #
# Tuya API helpers
# ------------------------------------------------------------------ #
def resolve_api_endpoint(x):
    return {
        "cn": "https://openapi.tuyacn.com",
        "us": "https://openapi.tuyaus.com",
        "eu": "https://openapi.tuyaeu.com",
        "in": "https://openapi.tuyain.com",
    }.get(x.strip().lower(), x.strip())


def _sign(access_id, access_key, method, path, t, token=None, body=""):
    csha = hashlib.sha256(body.encode("utf8")).hexdigest()
    stringToSign = f"{method}\n{csha}\n\n{path}"
    msg = access_id + (token or "") + t + stringToSign
    return hmac.new(
        access_key.encode("utf-8"), msg.encode("utf-8"), hashlib.sha256
    ).hexdigest().upper()


def api_get_token(access_id, access_key, api_endpoint):
    path = "/v1.0/token?grant_type=1"
    t = str(int(time.time() * 1000))
    sign = _sign(access_id, access_key, "GET", path, t)
    hdrs = {"client_id": access_id, "sign": sign, "t": t, "sign_method": "HMAC-SHA256"}
    log(f"HTTP GET {api_endpoint}{path}")
    r = _SESSION.get(f"{api_endpoint}{path}", headers=hdrs, timeout=10)
    log(f"HTTP GET token → {r.status_code}")
    r.raise_for_status()
    return r.json()["result"]["access_token"]


def api_get_properties(access_id, access_key, api_endpoint, token, device_id):
    path = f"/v2.0/cloud/thing/{device_id}/shadow/properties"
    t = str(int(time.time() * 1000))
    sign = _sign(access_id, access_key, "GET", path, t, token)
    hdrs = {
        "client_id": access_id, "sign": sign, "t": t,
        "sign_method": "HMAC-SHA256", "mode": "cors",
        "Content-Type": "application/json", "access_token": token,
    }
    r = _SESSION.get(f"{api_endpoint}{path}", headers=hdrs, timeout=10)
    r.raise_for_status()
    return r.json()


def api_get_model(access_id, access_key, api_endpoint, token, device_id):
    path = f"/v2.0/cloud/thing/{device_id}/model"
    t = str(int(time.time() * 1000))
    sign = _sign(access_id, access_key, "GET", path, t, token)
    hdrs = {
        "client_id": access_id, "sign": sign, "t": t,
        "sign_method": "HMAC-SHA256", "mode": "cors",
        "Content-Type": "application/json", "access_token": token,
    }
    r = _SESSION.get(f"{api_endpoint}{path}", headers=hdrs, timeout=10)
    r.raise_for_status()
    d = r.json()
    result = {}
    try:
        mj = json.loads(d["result"]["model"])
        for s in mj.get("services", []):
            for p in s.get("properties", []):
                if p.get("abilityId") is not None:
                    result[int(p["abilityId"])] = p.get("accessMode", "?")
    except Exception:
        pass
    return result


# ------------------------------------------------------------------ #
# Decoders
# ------------------------------------------------------------------ #
def decode_int32_fields(b64_str):
    if not b64_str:
        return []
    try:
        data = base64.b64decode(b64_str)
    except Exception:
        return []
    n = len(data) // 4
    if n == 0:
        return []
    try:
        return list(struct.unpack_from(">" + "i" * n, data, 0))
    except struct.error:
        return []


def ascii_hint(value):
    try:
        b = struct.pack(">i", value)
    except struct.error:
        return "...."
    return "".join(chr(x) if 32 <= x <= 126 else "." for x in b)


def detect_string_sequences(rows_by_dp):
    """Find consecutive fields whose bytes form a printable ASCII string.
    Returns { (dp_id, start_field_idx): decoded_string }.

    A field only starts a candidate string if ALL its bytes are printable
    or null (and the first byte is not null). This guards against fields
    like 0x2D11AA1E where only the first byte happens to be printable —
    treating that as a string start led to an infinite loop in an earlier
    version because the inner loop broke without advancing `i`.
    """
    hits = {}
    for dp_id, items in rows_by_dp.items():
        i = 0
        while i < len(items):
            b0 = struct.pack(">i", items[i][1])
            first_is_printable = 32 <= b0[0] <= 126
            all_ok = all(byte == 0 or 32 <= byte <= 126 for byte in b0)
            if first_is_printable and all_ok:
                start = i
                collected = b""
                while i < len(items):
                    b = struct.pack(">i", items[i][1])
                    if b == b"\x00\x00\x00\x00":
                        i += 1
                        break
                    if not all(byte == 0 or 32 <= byte <= 126 for byte in b):
                        break
                    collected += b
                    i += 1
                # Guarantee forward progress even if the inner loop broke
                # without incrementing i (shouldn't happen given the outer
                # guard above, but belt-and-suspenders against future edits)
                if i == start:
                    i += 1
                    continue
                if len(collected) >= 4:
                    s = collected.rstrip(b"\x00").decode("ascii", errors="replace")
                    if any(c.isalnum() for c in s) and len(s) >= 2:
                        hits[(dp_id, items[start][0])] = s
            else:
                i += 1
    return hits


# ------------------------------------------------------------------ #
# Snippet export
# ------------------------------------------------------------------ #
UNIT_TO_DEVICE_CLASS = {
    "°C": "temperature", "C": "temperature",
    "°F": "temperature", "F": "temperature",
    "A": "current", "V": "voltage",
    "W": "power", "kW": "power",
    "Wh": "energy", "kWh": "energy",
    "Hz": "frequency",
    "%": "", "rpm": "", "step": "", "P": "",
}


def _norm_unit(u):
    if not u:
        return ""
    u = u.strip()
    return {"C": "°C", "F": "°F"}.get(u, u)


def _snake(name):
    import re
    s = re.sub(r"[^\w\s]", "", str(name)).strip()
    s = re.sub(r"\s+", "_", s)
    return s.lower()


def export_snippet(path, labels, device_id):
    lines = [
        '"""RAW field mapping generated by raw_explorer.py',
        f'Device: {device_id}',
        f'Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}',
        'Encoding: int32 big-endian, signed',
        '"""',
        '',
        'RAW_FIELD_TYPES = {',
    ]
    for key, info in sorted(labels.items(),
                            key=lambda kv: (int(kv[0].split(":")[0]),
                                            int(kv[0].split(":")[1]))):
        if not info["name"]:
            continue
        dp_id, idx = key.split(":")
        raw_name = info["name"].strip()
        name = _snake(raw_name)
        unit = _norm_unit(info.get("unit", ""))
        dc = UNIT_TO_DEVICE_CLASS.get(unit, "")
        lines.append(f'    "{name}": {{')
        lines.append(f'        "dp_id": {dp_id},')
        lines.append(f'        "field_index": {idx},')
        lines.append(f'        "encoding": "int32_be",')
        lines.append(f'        "name": "{raw_name}",')
        if unit:
            lines.append(f'        "unit": "{unit}",')
        if dc:
            lines.append(f'        "device_class": "{dc}",')
            lines.append('        "state_class": "measurement",')
        lines.append('    },')
    lines.append('}')
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


# ------------------------------------------------------------------ #
# Background poller
# ------------------------------------------------------------------ #
class Poller(threading.Thread):
    def __init__(self, creds, q, interval=3.0):
        super().__init__(daemon=True)
        self.creds = creds
        self.q = q
        self.interval = interval
        self.stop_event = threading.Event()
        self.token = None

    def stop(self):
        self.stop_event.set()

    def run(self):
        log("Poller thread started.")
        c = self.creds
        try:
            self.q.put(("info", "Authenticating..."))
            log("Calling api_get_token()...")
            self.token = api_get_token(c["access_id"], c["access_key"], c["api_endpoint"])
            log(f"Token OK (len={len(self.token)}).")
        except Exception as e:
            log(f"Auth error: {e}")
            log_exception()
            self.q.put(("error", f"Auth failed: {e}"))
            return

        # Fetch model in background thread — never blocks properties
        def _load_model_bg():
            log("Model thread: starting api_get_model()...")
            try:
                am = api_get_model(
                    c["access_id"], c["access_key"], c["api_endpoint"],
                    self.token, c["device_id"],
                )
                log(f"Model OK ({len(am)} DPs).")
                self.q.put(("access_map", am))
            except Exception as e:
                log(f"Model failed (non-fatal): {e}")

        threading.Thread(target=_load_model_bg, daemon=True).start()

        self.q.put(("info", "Fetching first data..."))
        log("Starting property polling loop.")

        while not self.stop_event.is_set():
            try:
                log("Poll: calling api_get_properties()...")
                t0 = time.time()
                data = api_get_properties(
                    c["access_id"], c["access_key"], c["api_endpoint"],
                    self.token, c["device_id"],
                )
                log(f"Poll: got response in {time.time()-t0:.2f}s.")
                self.q.put(("props", data))
            except requests.HTTPError as e:
                if e.response is not None and e.response.status_code in (401, 403):
                    log("Token expired, re-authing...")
                    try:
                        self.token = api_get_token(
                            c["access_id"], c["access_key"], c["api_endpoint"]
                        )
                        continue
                    except Exception as ex:
                        log(f"Re-auth failed: {ex}")
                        self.q.put(("error", f"Re-auth failed: {ex}"))
                        return
                log(f"HTTP error: {e}")
                self.q.put(("error", f"HTTP {e}"))
            except requests.RequestException as e:
                log(f"Network error: {e}")
                self.q.put(("error", f"Network: {e}"))
            except Exception as e:
                log(f"Unexpected error: {e}")
                log_exception()
                self.q.put(("error", str(e)))

            # Interruptible sleep
            for _ in range(int(self.interval * 10)):
                if self.stop_event.is_set():
                    log("Poller stopping.")
                    return
                time.sleep(0.1)


# ------------------------------------------------------------------ #
# Connect dialog
# ------------------------------------------------------------------ #
class ConnectDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Tuya API Connection")
        self.result = None
        self.resizable(False, False)
        self.grab_set()
        frm = ttk.Frame(self, padding=20)
        frm.pack(fill="both", expand=True)
        for i, (label, attr, is_pw) in enumerate([
            ("ACCESS_ID", "e_id", False),
            ("ACCESS_KEY", "e_key", True),
            ("API_ENDPOINT", "cb_ep", False),
            ("DEVICE_ID", "e_dev", False),
        ]):
            ttk.Label(frm, text=label + ":").grid(row=i, column=0, sticky="e", pady=4)
            if attr == "cb_ep":
                w = ttk.Combobox(frm, values=["eu", "us", "cn", "in"], width=38)
                w.set("eu")
            else:
                w = ttk.Entry(frm, width=40, show="*" if is_pw else "")
            w.grid(row=i, column=1, pady=4, padx=6, sticky="w")
            setattr(self, attr, w)
        btns = ttk.Frame(frm)
        btns.grid(row=4, column=0, columnspan=2, pady=(14, 0))
        ttk.Button(btns, text="Connect", command=self._ok).pack(side="left", padx=6)
        ttk.Button(btns, text="Cancel", command=self._cancel).pack(side="left", padx=6)
        self.bind("<Return>", lambda e: self._ok())
        self.bind("<Escape>", lambda e: self._cancel())
        self.e_id.focus_set()

    def _ok(self):
        access_id = self.e_id.get().strip()
        access_key = self.e_key.get().strip()
        api_endpoint = resolve_api_endpoint(self.cb_ep.get())
        device_id = self.e_dev.get().strip()
        if not (access_id and access_key and api_endpoint and device_id):
            messagebox.showwarning("Missing", "Fill in all fields.", parent=self)
            return
        self.result = {
            "access_id": access_id, "access_key": access_key,
            "api_endpoint": api_endpoint, "device_id": device_id,
        }
        self.grab_release()  # important on Windows
        self.destroy()

    def _cancel(self):
        self.result = None
        self.grab_release()
        self.destroy()


# ------------------------------------------------------------------ #
# Main app
# ------------------------------------------------------------------ #
COMMON_UNITS = ["", "°C", "°F", "A", "V", "W", "kW", "kWh", "Wh",
                "Hz", "%", "rpm", "step", "P"]


class ExplorerApp:
    def __init__(self, root, creds):
        log("ExplorerApp __init__")
        self.root = root
        self.creds = creds
        self.access_by_dp = {}
        self.labels = {}
        self.iid_by_key = {}
        self.prev_values = {}
        self.stats = {}
        self.string_hints = {}
        self.strings_detected = False
        self.first_poll_done = False
        self.poll_count = 0
        self._build_ui()
        log("UI built. Starting Poller.")
        self.q = queue.Queue()
        self.poller = Poller(creds, self.q, interval=3.0)
        self.poller.start()
        self.root.after(150, self._drain_queue)
        log("Main loop starting.")

    def _build_ui(self):
        self.root.title(f"Tuya RAW Explorer — {self.creds['device_id']}")
        self.root.geometry("1100x720")

        toolbar = ttk.Frame(self.root, padding=(10, 8))
        toolbar.pack(fill="x")
        ttk.Button(toolbar, text="Export RAW_FIELD_TYPES",
                   command=self._export).pack(side="right")
        ttk.Label(toolbar,
                  text="Fill Name and Unit for fields you recognize, then click Export.",
                  foreground="#555").pack(side="left")

        main = ttk.Frame(self.root, padding=(10, 0))
        main.pack(fill="both", expand=True)

        table_wrap = ttk.Frame(main)
        table_wrap.pack(fill="both", expand=True, pady=(0, 8))

        columns = ("dp_id", "dp_code", "access", "field_idx",
                   "int32", "ascii", "string", "min", "max", "name", "unit")
        self.tree = ttk.Treeview(table_wrap, columns=columns,
                                 show="headings", selectmode="browse", height=18)
        for col, text, w, anchor in [
            ("dp_id", "DP", 50, "center"),
            ("dp_code", "Code", 160, "w"),
            ("access", "Acc", 45, "center"),
            ("field_idx", "Idx", 45, "center"),
            ("int32", "int32", 110, "e"),
            ("ascii", "ASCII", 65, "w"),
            ("string", "String", 150, "w"),
            ("min", "min", 90, "e"),
            ("max", "max", 90, "e"),
            ("name", "Name", 200, "w"),
            ("unit", "Unit", 60, "center"),
        ]:
            self.tree.heading(col, text=text)
            self.tree.column(col, width=w, anchor=anchor, stretch=False)

        self.tree.tag_configure("labeled", background="#DCF3D1")
        self.tree.tag_configure("string_hint", background="#DFEEFF")
        self.tree.tag_configure("dynamic", background="#FFF7C2")
        self.tree.tag_configure("zero", foreground="#B0B0B0")

        vs = ttk.Scrollbar(table_wrap, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vs.set)
        self.tree.grid(row=0, column=0, sticky="nsew")
        vs.grid(row=0, column=1, sticky="ns")
        table_wrap.rowconfigure(0, weight=1)
        table_wrap.columnconfigure(0, weight=1)

        self.tree.bind("<<TreeviewSelect>>", self._on_select)

        editor = ttk.LabelFrame(main, text="Selected field", padding=10)
        editor.pack(fill="x")

        self.sel_info = tk.StringVar(value="Select a row to edit.")
        ttk.Label(editor, textvariable=self.sel_info,
                  foreground="#333").grid(row=0, column=0, columnspan=6,
                                          sticky="w", pady=(0, 8))

        ttk.Label(editor, text="Name:").grid(row=1, column=0, sticky="e", padx=(0, 6))
        self.name_var = tk.StringVar()
        self.name_entry = ttk.Entry(editor, textvariable=self.name_var, width=38)
        self.name_entry.grid(row=1, column=1, sticky="w")

        ttk.Label(editor, text="Unit:").grid(row=1, column=2, sticky="e", padx=(18, 6))
        self.unit_var = tk.StringVar()
        self.unit_combo = ttk.Combobox(editor, textvariable=self.unit_var,
                                       values=COMMON_UNITS, width=10)
        self.unit_combo.grid(row=1, column=3, sticky="w")

        ttk.Button(editor, text="Save (Enter)",
                   command=self._save).grid(row=1, column=4, padx=(18, 4))
        ttk.Button(editor, text="Clear", command=self._clear).grid(row=1, column=5)

        self.name_entry.bind("<Return>", lambda e: self._save())
        self.unit_combo.bind("<Return>", lambda e: self._save())

        self.status = tk.StringVar(value="Starting...")
        ttk.Label(self.root, textvariable=self.status, relief="sunken",
                  anchor="w", padding=(8, 3)).pack(fill="x", side="bottom")

    # ------------------------- queue -------------------------
    def _drain_queue(self):
        try:
            while True:
                kind, payload = self.q.get_nowait()
                if kind == "access_map":
                    log(f"UI: got access_map ({len(payload)} DPs)")
                    self.access_by_dp = payload
                    # Retro-fill access column for already-populated rows
                    for key, iid in self.iid_by_key.items():
                        dp_id = int(key.split(":")[0])
                        self.tree.set(iid, "access", payload.get(dp_id, "?"))
                elif kind == "props":
                    log("UI: got props")
                    self._ingest(payload)
                elif kind == "info":
                    self.status.set(payload)
                    log(f"UI: info → {payload}")
                elif kind == "error":
                    self.status.set(f"ERROR: {payload}")
                    log(f"UI: error → {payload}")
        except queue.Empty:
            pass
        except Exception as e:
            log(f"UI drain error: {e}")
            log_exception()
        self.root.after(150, self._drain_queue)

    # ------------------------- ingest -------------------------
    def _ingest(self, data):
        try:
            props = data.get("result", {}).get("properties", [])
            log(f"Ingest: {len(props)} total DPs, filtering raw...")
            rows_by_dp = {}
            rows_flat = []
            for p in props:
                if p.get("type") != "raw":
                    continue
                fields = decode_int32_fields(p["value"])
                rows_by_dp[p["dp_id"]] = [(i, v) for i, v in enumerate(fields)]
                for i, v in enumerate(fields):
                    rows_flat.append({
                        "dp_id": p["dp_id"], "dp_code": p["code"],
                        "field_idx": i, "value": v,
                    })

            log(f"Ingest: {len(rows_flat)} raw fields, {len(rows_by_dp)} raw DPs")

            if not self.strings_detected and rows_by_dp:
                self.string_hints = detect_string_sequences(rows_by_dp)
                self.strings_detected = True
                log(f"Ingest: detected {len(self.string_hints)} string hints")

            if not self.first_poll_done:
                self.first_poll_done = True
                self.status.set(f"Loading {len(rows_flat)} fields...")
                log("Ingest: first poll → starting chunked populate")
                # Yield to the event loop *first* so the status update paints
                self.root.after(1, self._populate_chunked, rows_flat, 0)
            else:
                log("Ingest: subsequent poll → in-place update")
                self._update_tree(rows_flat)
                self.poll_count += 1
                self.status.set(
                    f"Poll #{self.poll_count} · {datetime.now().strftime('%H:%M:%S')} · "
                    f"{len(rows_flat)} fields · {len(self.labels)} labeled"
                )
        except Exception as e:
            log(f"Ingest error: {e}")
            log_exception()

    def _populate_chunked(self, rows_flat, start, chunk_size=5):
        end = min(start + chunk_size, len(rows_flat))
        for r in rows_flat[start:end]:
            dp = r["dp_id"]
            idx = r["field_idx"]
            key = f"{dp}:{idx}"
            self.stats[key] = {"min": r["value"], "max": r["value"]}
            self.prev_values[key] = r["value"]
            access = self.access_by_dp.get(dp, "?")
            s_hint = self.string_hints.get((dp, idx), "")
            tags = self._tags_for(key, r["value"], s_hint)
            iid = self.tree.insert(
                "", "end",
                values=(dp, r["dp_code"], access, idx,
                        r["value"], ascii_hint(r["value"]), s_hint,
                        r["value"], r["value"], "", ""),
                tags=tags,
            )
            self.iid_by_key[key] = iid

        if end < len(rows_flat):
            self.status.set(f"Loading {end}/{len(rows_flat)} fields...")
            self.root.after(1, self._populate_chunked, rows_flat, end, chunk_size)
        else:
            self.poll_count = 1
            log(f"Populate finished: {end} rows.")
            self.status.set(
                f"Poll #1 · {datetime.now().strftime('%H:%M:%S')} · "
                f"{end} fields · {len(self.labels)} labeled · "
                f"{len(self.string_hints)} string hints"
            )

    def _update_tree(self, rows_flat):
        changed_count = 0
        for r in rows_flat:
            key = f"{r['dp_id']}:{r['field_idx']}"
            iid = self.iid_by_key.get(key)
            if iid is None:
                continue
            new_val = r["value"]
            old_val = self.prev_values.get(key)
            if new_val == old_val:
                continue
            changed_count += 1
            self.prev_values[key] = new_val

            st = self.stats.setdefault(key, {"min": new_val, "max": new_val})
            old_min, old_max = st["min"], st["max"]
            st["min"] = min(old_min, new_val)
            st["max"] = max(old_max, new_val)

            self.tree.set(iid, "int32", new_val)
            self.tree.set(iid, "ascii", ascii_hint(new_val))
            if st["min"] != old_min:
                self.tree.set(iid, "min", st["min"])
            if st["max"] != old_max:
                self.tree.set(iid, "max", st["max"])

            s_hint = self.string_hints.get((r["dp_id"], r["field_idx"]), "")
            self.tree.item(iid, tags=self._tags_for(key, new_val, s_hint))
        if changed_count:
            log(f"Update: {changed_count} rows changed.")

    def _tags_for(self, key, value, s_hint):
        tags = []
        if key in self.labels and self.labels[key]["name"]:
            tags.append("labeled")
        elif s_hint:
            tags.append("string_hint")
        elif value != 0:
            st = self.stats.get(key, {})
            if st.get("min") != st.get("max"):
                tags.append("dynamic")
        if value == 0 and self.stats.get(key, {}).get("max") == 0:
            tags.append("zero")
        return tuple(tags)

    # ------------------------- editor -------------------------
    def _on_select(self, event=None):
        sel = self.tree.selection()
        if not sel:
            return
        vals = self.tree.item(sel[0], "values")
        if not vals:
            return
        dp, code, access, idx = vals[0], vals[1], vals[2], vals[3]
        int32_val, ascii_val, s_hint = vals[4], vals[5], vals[6]
        key = f"{dp}:{idx}"
        info = f"DP {dp} · {code} · acc={access}   |   field {idx}   |   int32={int32_val}   |   ASCII='{ascii_val}'"
        if s_hint:
            info += f"   |   suggested: '{s_hint}'"
        self.sel_info.set(info)
        lbl = self.labels.get(key, {"name": "", "unit": ""})
        self.name_var.set(lbl["name"] if lbl["name"] else s_hint)
        self.unit_var.set(lbl["unit"])
        self.name_entry.focus_set()
        self.name_entry.select_range(0, tk.END)

    def _save(self):
        sel = self.tree.selection()
        if not sel:
            return
        iid = sel[0]
        vals = self.tree.item(iid, "values")
        if not vals:
            return
        key = f"{vals[0]}:{vals[3]}"
        name = self.name_var.get().strip()
        unit = self.unit_var.get().strip()
        if name:
            self.labels[key] = {"name": name, "unit": unit}
            self.tree.set(iid, "name", name)
            self.tree.set(iid, "unit", unit)
        else:
            self.labels.pop(key, None)
            self.tree.set(iid, "name", "")
            self.tree.set(iid, "unit", "")
        s_hint = self.string_hints.get((int(vals[0]), int(vals[3])), "")
        self.tree.item(iid, tags=self._tags_for(key, int(vals[4]), s_hint))
        nxt = self.tree.next(iid)
        if nxt:
            self.tree.selection_set(nxt)
            self.tree.see(nxt)
            self._on_select()

    def _clear(self):
        sel = self.tree.selection()
        if not sel:
            return
        iid = sel[0]
        vals = self.tree.item(iid, "values")
        if not vals:
            return
        key = f"{vals[0]}:{vals[3]}"
        self.labels.pop(key, None)
        self.tree.set(iid, "name", "")
        self.tree.set(iid, "unit", "")
        self.name_var.set("")
        self.unit_var.set("")
        s_hint = self.string_hints.get((int(vals[0]), int(vals[3])), "")
        self.tree.item(iid, tags=self._tags_for(key, int(vals[4]), s_hint))

    # ------------------------- export -------------------------
    def _export(self):
        if not self.labels:
            messagebox.showwarning("Nothing to export",
                                   "No fields have been labeled yet.")
            return
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        default = f"RAW_FIELD_TYPES_{self.creds['device_id'][:8]}_{ts}.py"
        path = filedialog.asksaveasfilename(
            defaultextension=".py",
            initialfile=default,
            filetypes=[("Python", "*.py"), ("Text", "*.txt")],
        )
        if not path:
            return
        try:
            export_snippet(path, self.labels, self.creds["device_id"])
            messagebox.showinfo(
                "Exported",
                f"Saved {len(self.labels)} field(s) to:\n{path}"
            )
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save: {e}")

    def on_close(self):
        log("on_close: stopping poller")
        self.poller.stop()
        self.root.destroy()


# ------------------------------------------------------------------ #
# Entry
# ------------------------------------------------------------------ #
def main():
    log("main() starting")
    root = tk.Tk()
    root.withdraw()
    dlg = ConnectDialog(root)
    root.wait_window(dlg)
    if dlg.result is None:
        log("Cancelled by user.")
        root.destroy()
        return
    log(f"Credentials entered: device_id={dlg.result['device_id']}, endpoint={dlg.result['api_endpoint']}")
    root.deiconify()
    app = ExplorerApp(root, dlg.result)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()
    log("main() exited")


if __name__ == "__main__":
    try:
        main()
    except Exception:
        log("Fatal error at top level:")
        log_exception()
        try:
            import tkinter.messagebox as _mb
            import tkinter as _tk
            r = _tk.Tk(); r.withdraw()
            _mb.showerror(
                "Fatal error",
                f"Something went wrong. See log file:\n{_LOG_PATH}"
            )
            r.destroy()
        except Exception:
            pass
        if _HAS_CONSOLE:
            try:
                input("Press ENTER to exit...")
            except Exception:
                pass