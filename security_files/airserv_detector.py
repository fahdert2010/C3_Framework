class AirservDetector:
    def __init__(self, ssh_context):
        self.ssh = ssh_context

    def audit_airserv_servers(self, band):
        default_port = 666 if band == "2G" else 777
        print(f"[*] Deploying Airserv Forensic Scan on port: {default_port}...")

        netstat_out, _ = self.ssh.execute(f"netstat -tlpn | grep :{default_port}")
        pid_out, _ = self.ssh.execute("pidof airserv-ng")
        pids = pid_out.strip().split() if pid_out else []

        if not pids and not netstat_out:
            print("[-] Pure Space: No active Airserv-ng servers found on this platform.")
            return {"status": "not_found"}

        print(f"[+] CRITICAL: Detected active Airserv infrastructure! PIDs: {pids}")

        if len(pids) == 1:
            opt = input("[?] Single server detected. Close it? [y/n/cancel]: ").strip().lower()
            if opt == 'y':
                self.ssh.execute(f"kill -9 {pids[0]}")
                print(f"[+] Killed Airserv server PID: {pids[0]}")
                return {"status": "cleaned", "killed": pids}
            elif opt == 'cancel':
                return {"status": "cancel_scan"}
        else:
            print("\n--- ACTIVE AIRSERV REGISTRY ---")
            for idx, pid in enumerate(pids, start=1):
                print(f" [{idx}] Server Process PID: {pid}")
            print(" [A] Terminate ALL active servers")
            print(" [C] Cancel scan and return to main console")
            
            action = input("[?] Choose target index to isolate: ").strip().upper()
            if action == 'A':
                for pid in pids:
                    self.ssh.execute(f"kill -9 {pid}")
                return {"status": "cleaned", "killed": pids}
            elif action == 'C':
                return {"status": "cancel_scan"}
            elif action.isdigit() and 1 <= int(action) <= len(pids):
                target_pid = pids[int(action) - 1]
                self.ssh.execute(f"kill -9 {target_pid}")
                return {"status": "cleaned", "killed": [target_pid]}
        return {"status": "ignored"}
