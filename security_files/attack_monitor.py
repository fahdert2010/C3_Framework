import re

class AttackMonitor:
    def __init__(self, ssh_context):
        self.ssh = ssh_context

    def audit_and_purge_strikes(self):
        print("[*] Deploying Aireplay Strike Forensic Scan on Router...")
        pid_out, _ = self.ssh.execute("pidof aireplay-ng")
        pids = pid_out.strip().split() if pid_out else []

        if not pids:
            print("[-] Pure Space: No active Aireplay-ng strikes detected.")
            return {"status": "clear"}

        print(f"[!] ALERT: Detected {len(pids)} active Aireplay-ng attack processes!")
        print("\n--- ACTIVE STRIKE REGISTRY ---")
        for idx, pid in enumerate(pids, start=1):
            print(f" [{idx}] Attack Process PID: {pid}")
        print(" [A] Terminate ALL active strikes")
        print(" [C] Cancel scan and retreat to main console")
        
        action = input("[?] Choose action index to enforce: ").strip().upper()
        if action == 'A':
            for pid in pids:
                self.ssh.execute(f"kill -9 {pid}")
            self.cleanup_monitor_interfaces()
            return {"status": "purged", "killed": pids}
        elif action == 'C':
            return {"status": "canceled"}
        return {"status": "ignored"}

    def cleanup_monitor_interfaces(self):
        print("[*] Launching Monitor Interface Hard Sterilization...")
        iw_out, _ = self.ssh.execute("iw dev")
        mon_interfaces = re.findall(r"Interface\s+([a-zA-Z0-9.\-_]+).*?type\s+monitor", iw_out, re.DOTALL)
        
        for mon_iface in mon_interfaces:
            self.ssh.execute(f"ifconfig {mon_iface} down")
            if "mon" in mon_iface:
                self.ssh.execute(f"uci del wireless.{mon_iface}")
        
        self.ssh.execute("uci commit wireless")
        activate_bcast = input("[?] Activate native broadcasting for clients now? [y/n]: ").strip().lower()
        if activate_bcast == 'y':
            self.ssh.execute("uci set wireless.default_radio0.disabled='0'")
            self.ssh.execute("uci commit wireless && wifi reload")
            print("[+] Native radio signal revived. Clients reconnected.")
