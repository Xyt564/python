import threading
import socket
import ssl
import json
import time
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urljoin
import requests
import os

try:
    import customtkinter as ctk
    from tkinter import filedialog, messagebox
except Exception as e:
    raise SystemExit("This script requires customtkinter. Install with: pip install customtkinter")

# Try to import nmap (python-nmap)
try:
    import nmap
    HAVE_NMAP = True
except Exception:
    HAVE_NMAP = False

# ---------- Config ----------
COMMON_PORTS = [21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143, 443, 445, 465,
                587, 636, 993, 995, 1080, 1433, 1521, 1723, 3306, 3389, 5900, 8080]
SOCKET_TIMEOUT = 3.0
MAX_THREADS = 60
DEFAULT_WORDLIST = ["admin", "login", "robots.txt", "backup", "config", "uploads", ".git/"]

# ---------- Scanning helpers (same logic as CLI scanner) ----------

def tcp_connect_banner(host, port, timeout=SOCKET_TIMEOUT):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        s.connect((host, port))

        # Try a tiny HTTP probe for HTTP-like ports
        try:
            if port in (80, 8080, 8000, 8888, 5000):
                s.send(b"HEAD / HTTP/1.0\r\n\r\n")
        except Exception:
            pass

        # Try to read banner
        try:
            data = s.recv(4096)
            banner = data.decode(errors="ignore").strip()
        except Exception:
            banner = ""
        s.close()
        return True, banner
    except Exception:
        return False, ""


def scan_port(host, port):
    open_, banner = tcp_connect_banner(host, port)
    return {"port": port, "open": open_, "banner": banner}


def http_header_check(url, timeout=5):
    results = {}
    try:
        resp = requests.get(url, timeout=timeout, allow_redirects=True)
        results["status_code"] = resp.status_code
        headers = {k.lower(): v for k, v in resp.headers.items()}
        results["server_header"] = headers.get("server")
        sec_headers = {
            "strict-transport-security": "HSTS",
            "content-security-policy": "CSP",
            "x-frame-options": "X-Frame-Options",
            "x-content-type-options": "X-Content-Type-Options",
            "referrer-policy": "Referrer-Policy",
            "x-xss-protection": "X-XSS-Protection",
        }
        missing = []
        present = {}
        for h in sec_headers:
            if h in headers:
                present[sec_headers[h]] = headers[h]
            else:
                missing.append(sec_headers[h])
        results["missing_security_headers"] = missing
        results["present_security_headers"] = present
    except Exception as e:
        results["error"] = str(e)
    return results


def dir_probe(base_url, paths, timeout=4, rate_delay=0.2):
    found = []
    for p in paths:
        url = urljoin(base_url.rstrip('/') + '/', p.lstrip('/'))
        try:
            r = requests.get(url, timeout=timeout, allow_redirects=True)
            if r.status_code < 400:
                found.append({"path": p, "status": r.status_code})
        except Exception:
            pass
        time.sleep(rate_delay)
    return found


def run_nmap_scan(host, ports_str=None):
    if not HAVE_NMAP:
        return {"error": "python-nmap not installed"}
    nm = nmap.PortScanner()
    args = "-sV -Pn"
    if ports_str:
        args += f" -p {ports_str}"
    try:
        nm.scan(hosts=host, arguments=args)
        return nm[host]
    except Exception as e:
        return {"error": str(e)}

# ---------- GUI Application ----------

class VulnScannerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Vuln Scanner (CTk)")
        self.geometry("900x650")

        # Layout frames
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        left = ctk.CTkFrame(self, width=300, corner_radius=8)
        left.grid(row=0, column=0, padx=12, pady=12, sticky="ns")

        right = ctk.CTkFrame(self, corner_radius=8)
        right.grid(row=0, column=1, padx=12, pady=12, sticky="nsew")

        # Left (controls)
        ctk.CTkLabel(left, text="Target").pack(pady=(12, 4), anchor="w")
        self.entry_target = ctk.CTkEntry(left, placeholder_text="example.com or 10.0.0.5")
        self.entry_target.pack(fill="x", padx=12)

        ctk.CTkLabel(left, text="Ports (comma separated) -- leave blank for default").pack(pady=(12, 4), anchor="w")
        self.entry_ports = ctk.CTkEntry(left, placeholder_text=",".join(str(p) for p in COMMON_PORTS))
        self.entry_ports.pack(fill="x", padx=12)

        self.var_nmap = ctk.BooleanVar(value=HAVE_NMAP)
        self.chk_nmap = ctk.CTkCheckBox(left, text=f"Use python-nmap (installed: {HAVE_NMAP})", variable=self.var_nmap)
        self.chk_nmap.pack(pady=(12, 0), padx=12, anchor="w")

        self.var_dir = ctk.BooleanVar(value=True)
        self.chk_dir = ctk.CTkCheckBox(left, text="Directory probe", variable=self.var_dir)
        self.chk_dir.pack(pady=(8, 0), padx=12, anchor="w")

        ctk.CTkLabel(left, text="Dir wordlist (optional file)").pack(pady=(12, 4), anchor="w")
        self.lbl_wordlist = ctk.CTkLabel(left, text="(default small built-in list)")
        self.lbl_wordlist.pack(padx=12, anchor="w")
        btn_choose = ctk.CTkButton(left, text="Choose wordlist file", command=self.choose_wordlist)
        btn_choose.pack(padx=12, pady=(6, 0), fill="x")

        ctk.CTkLabel(left, text="Rate delay between dir requests (s)").pack(pady=(12, 4), anchor="w")
        self.entry_delay = ctk.CTkEntry(left, placeholder_text="0.2")
        self.entry_delay.pack(fill="x", padx=12)

        btn_start = ctk.CTkButton(left, text="Start Scan", fg_color="#0ea5ae", command=self.start_scan)
        btn_start.pack(pady=18, padx=12, fill="x")

        btn_save = ctk.CTkButton(left, text="Save Last Report", command=self.save_report)
        btn_save.pack(padx=12, fill="x")

        # Right (results)
        topbar = ctk.CTkFrame(right, height=40)
        topbar.pack(fill="x", padx=8, pady=8)
        self.lbl_status = ctk.CTkLabel(topbar, text="Idle")
        self.lbl_status.pack(side="left", padx=8)

        # Results text box
        self.txt = ctk.CTkTextbox(right, width=600, height=520)
        self.txt.pack(fill="both", expand=True, padx=8, pady=(0,8))
        self.txt.configure(state="disabled")

        # Internal state
        self.wordlist = None
        self.last_report = None
        self.scan_thread = None

    def choose_wordlist(self):
        path = filedialog.askopenfilename(title="Choose wordlist file", filetypes=[("Text files","*.txt"), ("All files","*")])
        if path:
            self.wordlist = path
            self.lbl_wordlist.configure(text=os.path.basename(path))

    def append_text(self, txt):
        self.txt.configure(state="normal")
        self.txt.insert("end", txt+"\n")
        self.txt.see("end")
        self.txt.configure(state="disabled")

    def save_report(self):
        if not self.last_report:
            messagebox.showinfo("No report", "No report to save yet. Run a scan first.")
            return
        path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON","*.json")])
        if not path:
            return
        with open(path, "w") as f:
            json.dump(self.last_report, f, indent=2)
        messagebox.showinfo("Saved", f"Report saved to {path}")

    def start_scan(self):
        target = self.entry_target.get().strip()
        if not target:
            messagebox.showwarning("Target required", "Enter a hostname or IP to scan")
            return

        ports_text = self.entry_ports.get().strip()
        ports = None
        if ports_text:
            try:
                ports = [int(p.strip()) for p in ports_text.split(",") if p.strip()]
            except Exception:
                messagebox.showerror("Invalid ports", "Ports must be comma separated integers")
                return

        try:
            delay = float(self.entry_delay.get().strip() or "0.2")
        except Exception:
            delay = 0.2

        do_nmap = bool(self.var_nmap.get()) and HAVE_NMAP
        do_dir = bool(self.var_dir.get())

        # Load wordlist if provided
        if self.wordlist:
            try:
                with open(self.wordlist, "r", errors="ignore") as f:
                    wl = [l.strip() for l in f if l.strip()]
            except Exception:
                wl = DEFAULT_WORDLIST
        else:
            wl = DEFAULT_WORDLIST

        # Start scan in background thread to keep GUI responsive
        if self.scan_thread and self.scan_thread.is_alive():
            messagebox.showinfo("Scan running", "A scan is already running")
            return

        self.txt.configure(state="normal")
        self.txt.delete("0.0", "end")
        self.txt.configure(state="disabled")
        self.lbl_status.configure(text=f"Scanning {target}...")
        self.append_text(f"[+] Starting scan against {target}")

        self.scan_thread = threading.Thread(target=self.perform_scan, args=(target, ports, do_nmap, do_dir, wl, delay), daemon=True)
        self.scan_thread.start()

    def perform_scan(self, target, ports, do_nmap, do_dir, wordlist, rate_delay):
        report = {"target": target, "scanned_at": time.strftime("%Y-%m-%d %H:%M:%S"), "ports": [], "http_checks": [], "dir_probe": []}

        # Resolve
        try:
            ip = socket.gethostbyname(target)
            report["ip"] = ip
            self.append_text(f"Resolved {target} -> {ip}")
        except Exception:
            report["ip"] = None
            self.append_text("[!] Failed to resolve target")

        # Ports
        scan_ports = ports if ports else COMMON_PORTS
        self.append_text(f"[+] Scanning ports: {scan_ports}")
        with ThreadPoolExecutor(max_workers=min(MAX_THREADS, len(scan_ports))) as ex:
            futures = {ex.submit(scan_port, target, p): p for p in scan_ports}
            for fut in as_completed(futures):
                p = futures[fut]
                try:
                    res = fut.result()
                except Exception as e:
                    res = {"port": p, "open": False, "banner": "", "error": str(e)}
                report["ports"].append(res)
                if res.get("open"):
                    self.append_text(f"    Port {p} OPEN  banner: {res.get('banner')[:120]}")

        # HTTP checks
        http_ports = [r["port"] for r in report["ports"] if r["open"] and r["port"] in (80, 443, 8080, 8443, 8000)]
        schemes = []
        for port in http_ports:
            if port in (443, 8443):
                schemes.append(("https", port))
            else:
                schemes.append(("http", port))
        schemes = list(dict.fromkeys(schemes))

        for scheme, port in schemes:
            url = f"{scheme}://{target}" if port in (80, 443) else f"{scheme}://{target}:{port}"
            http_res = http_header_check(url)
            http_res["url"] = url
            report["http_checks"].append(http_res)
            missing = http_res.get("missing_security_headers")
            self.append_text(f"    HTTP {url} status={http_res.get('status_code')} missing_headers={missing}")

            if do_dir:
                found = dir_probe(url, wordlist, rate_delay=rate_delay)
                report["dir_probe"].extend(found)
                for fnd in found:
                    self.append_text(f"    Found {fnd['path']} status={fnd['status']}")

        # Try plain scheme if nothing found and HTTP probe enabled
        if not report["http_checks"]:
            for scheme in ("http", "https"):
                url = f"{scheme}://{target}"
                http_res = http_header_check(url)
                if "error" not in http_res:
                    http_res["url"] = url
                    report["http_checks"].append(http_res)
                    self.append_text(f"    HTTP fallback {url} status={http_res.get('status_code')}")
                    if do_dir:
                        found = dir_probe(url, wordlist, rate_delay=rate_delay)
                        report["dir_probe"].extend(found)
                        for fnd in found:
                            self.append_text(f"    Found {fnd['path']} status={fnd['status']}")
                    break

        # Optional nmap
        if do_nmap:
            self.append_text("[+] Running nmap service/version detection (this requires nmap binary installed)")
            ports_str = ",".join(str(p) for p in scan_ports)
            nm_out = run_nmap_scan(target, ports_str=ports_str)
            report["nmap"] = nm_out
            if isinstance(nm_out, dict) and nm_out.get("error"):
                self.append_text(f"    nmap error: {nm_out.get('error')}")
            else:
                self.append_text(f"    nmap returned scan information")

        self.last_report = report
        # Pretty-print final summary
        open_ports = [p["port"] for p in report["ports"] if p.get("open")]
        self.append_text(f"[+] Scan complete. Open ports: {open_ports}")
        if report.get("dir_probe"):
            self.append_text(f"[+] Directories found: {[d['path'] for d in report['dir_probe']]}")

        self.lbl_status.configure(text="Idle")


if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    app = VulnScannerApp()
    app.mainloop()
