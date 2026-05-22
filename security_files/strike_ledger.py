#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ultimate C3 Framework - Hardened Asynchronous Forensic Strike Ledger Manager
File: /home/kali/C3_Framework/security_files/strike_ledger.py
"""

import os
import glob
import time
import queue
import threading
import datetime

class StrikeLedgerManager:
    def __init__(self, ap_name):
        self.ap_name = ap_name
        self.base_dir = "/home/kali/C3_Framework/storage/loot"
        self.archive_dir = "/home/kali/C3_Framework/storage/archive"
        self.log_path = "/home/kali/C3_Framework/storage/logs/attack_errors.log"
        
        os.makedirs(self.base_dir, exist_ok=True)
        os.makedirs(self.archive_dir, exist_ok=True)
        
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        self.current_ledger_file = os.path.join(self.base_dir, f"strike_ledger_{self.ap_name}_{timestamp}.sh")
        
        self.write_queue = queue.Queue()
        self.shutdown_event = threading.Event()
        self.behavioral_ageing_cache = {}
        
        self._initialize_ledger_header()
        self._start_asynchronous_writer_worker()

    def _initialize_ledger_header(self):
        header = (
            "#!/bin/bash\n"
            f"# ======================================================================\n"
            f"# [✔] C3 Framework - Self-Executable Forensic Ledger\n"
            f"# Launch Session Destination: AP_{self.ap_name}\n"
            f"# Session Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"# ======================================================================\n\n"
        )
        self.write_queue.put(header)

    def _start_asynchronous_writer_worker(self):
        def writer_loop():
            with open(self.current_ledger_file, "w", encoding="utf-8", buffering=1) as f:
                while not self.shutdown_event.is_set() or not self.write_queue.empty():
                    try:
                        data = self.write_queue.get(timeout=1.0)
                        f.write(data)
                        self.write_queue.task_done()
                    except queue.Empty:
                        continue
        threading.Thread(target=writer_loop, daemon=True).start()

    def commit_forensic_strike(self, bssid, target_mac, essid_clean, attack_command):
        """
        التصحيح المبرهن: تطهير الماك تماماً من الفواصل وقص 6 محارف لتمثيل الـ OUI بدقة
        """
        current_time = time.time()
        
        # التطهير الوقائي المطلق ضد تشوه الماكات القادمة من الأثير
        raw_clean = target_mac.strip().lower().replace(":", "").replace("-", "")
        oui_prefix = raw_clean[:6]
        
        if not oui_prefix or len(oui_prefix) < 6:
            return False
            
        behavior_key = f"{bssid}_{oui_prefix}"
        
        if behavior_key in self.behavioral_ageing_cache:
            if current_time - self.behavioral_ageing_cache[behavior_key] < 60:
                return False 
                
        self.behavioral_ageing_cache[behavior_key] = current_time
        
        timestamp_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        forensic_row = (
            f"# [{timestamp_str}] Target_SSID: [{essid_clean}] | Client_MAC: [{target_mac}]\n"
            f"{attack_command}\n\n"
        )
        
        self.write_queue.put(forensic_row)
        return True

    def execute_safe_archive_and_rotation(self):
        """
        التصحيح الهندسي الصخر: تفريغ طابور الرام أولاً لمنع الـ Thread-Dead Lock
        """
        try:
            self.write_queue.join() # تفريغ آمن تحت الحماية الصامتة لقنوات الطوارئ
        except Exception:
            pass
            
        self.shutdown_event.set() # قفل الخيط بأمان بعد حسم سياق السطور
        
        try:
            filename = os.path.basename(self.current_ledger_file)
            archive_target = os.path.join(self.archive_dir, filename)
            if os.path.exists(self.current_ledger_file):
                os.rename(self.current_ledger_file, archive_target)
                os.chmod(archive_target, 0o755) 
            
            pattern = os.path.join(self.archive_dir, "strike_ledger_*.sh")
            archive_files = sorted(glob.glob(pattern), key=os.path.getmtime)
            
            while archive_files:
                total_size = sum(os.path.getsize(f) for f in archive_files)
                if total_size > 50 * 1024 * 1024:
                    oldest_file = archive_files.pop(0)
                    os.remove(oldest_file)
                else:
                    break
        except Exception:
            pass
