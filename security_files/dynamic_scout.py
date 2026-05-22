import re
import json

class DynamicScout:
    def __init__(self, ssh_context):
        self.ssh = ssh_context

    def scan_frequency_clients(self, target_band):
        print(f"[*] Analyzing wireless infrastructure for band: {target_band}...")
        cmd = "ubus call network.wireless status"
        stdout, stderr = self.ssh.execute(cmd)
        
        if not stdout:
            print("[!] CRITICAL - Class: DynamicScout | Reason: Ubus response empty")
            return {"status": "error", "reason": "ubus_down"}

        wireless_data = json.loads(stdout)
        target_interfaces = []
        total_clients = 0

        for radio, radio_data in wireless_data.items():
            interfaces = radio_data.get("interfaces", [])
            for iface in interfaces:
                iface_band = iface.get("band", "2g") 
                if target_band.lower() in iface_band.lower() or target_band.lower() in radio.lower():
                    ifname = iface.get("ifname")
                    if ifname:
                        target_interfaces.append(ifname)
                        stations_cmd = f"iw dev {ifname} station dump | grep Station"
                        st_out, _ = self.ssh.execute(stations_cmd)
                        if st_out:
                            total_clients += len(re.findall(r"Station", st_out))

        print(f"[+] Dynamic Scout found actual active interfaces: {target_interfaces}")
        
        if total_clients > 0:
            print(f"[!] WARNING: {total_clients} ACTIVE CLIENTS DETECTED ON TARGET FREQUENCY!")
            choice = input("[?] Force execution and isolate clients? [y/n]: ").strip().lower()
            if choice != 'y':
                print("[-] Attack aborted by user. Safe retreat triggered.")
                return {"status": "aborted"}
        else:
            print("[+] Zero active clients found on native interface. Moving forward.")

        iw_dev_out, _ = self.ssh.execute("iw dev")
        monitor_interfaces = re.findall(r"Interface\s+([a-zA-Z0-9.\-_]+).*?type\s+monitor", iw_dev_out, re.DOTALL)
        
        if monitor_interfaces:
            print(f"[!] DETECTED ACTIVE MONITOR INTERFACES: {monitor_interfaces}")
            print("[!] CRITICAL: Native scouting is blocked. Suspicion of Airserv-ng server or Aireplay-ng strike!")
            return {"status": "monitor_lock", "interfaces": monitor_interfaces}

        return {"status": "clear", "interfaces": target_interfaces}
