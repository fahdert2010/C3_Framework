import os
import glob

class LiveAttackParser:
    def __init__(self, access_point_name):
        self.target_dir = f"/home/kali/C3_Framework/storage/{access_point_name}/"

    def get_latest_capture_file(self):
        search_path = os.path.join(self.target_dir, "*.csv")
        files = glob.glob(search_path)
        if not files:
            return None
        return max(files, key=os.path.getmtime)

    def extract_live_targets(self):
        latest_csv = self.get_latest_capture_file()
        if not latest_csv:
            print("[-] No live capture files found in target storage directory.")
            return []

        try:
            with open(latest_csv, 'r', errors='ignore') as f:
                lines = f.readlines()

            targets = []
            for line in lines:
                if "," in line and "BSSID" not in line:
                    parts = line.split(",")
                    if len(parts) > 6 and len(parts[0].strip()) == 17:
                        targets.append({
                            "bssid": parts[0].strip().upper(),
                            "channel": parts[3].strip(),
                            "signal": parts[8].strip(),
                            "essid": parts[13].strip() if len(parts) > 13 else "Hidden"
                        })
            return targets
        except Exception as e:
            print(f"[!] Critical Error parsing live matrix: {str(e)}")
            return []
