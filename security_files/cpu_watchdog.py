#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ultimate C3 Framework - Hardened Micro Remote CPU Watchdog Core
File: /home/kali/C3_Framework/security_files/cpu_watchdog.py
"""

import datetime
from core.ssh_executor import SSHHardwareExecutor

class RemoteCPUWatchdog:
    def __init__(self, ssh_executor: SSHHardwareExecutor):
        self.executor = ssh_executor
        self.log_path = "/home/kali/C3_Framework/storage/logs/attack_errors.log"

    def _trigger_double_guard(self, line_num, reason):
        print(f"\033[91m[!] CRITICAL - Class: RemoteCPUWatchdog | Line: {line_num} | Reason: {reason}\033[0m")
        try:
            with open(self.log_path, "a", encoding="utf-8") as log_file:
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                log_file.write(f"[{timestamp}] CRITICAL - Class: RemoteCPUWatchdog | Line: {line_num} | Reason: {reason}\n")
        except IOError:
            pass

    def fetch_hardware_cpu_load(self):
        """
        التصحيح الهندسي الصخر: استدعاء المصفوفة معراة دون شل تكراري لمنع المخرج الفارغ
        """
        cmd = ["cat", "/proc/loadavg"]
        response = self.executor.execute_raw_command(cmd)
        
        if response["status"] == "success" and response["output"]:
            try:
                # استخراج معدل حمل المعالج الفعلي للدقيقة الأولى حياً من النواة
                load_1min = float(response["output"].split()[0])
                return load_1min
            except (ValueError, IndexError, AttributeError) as e:
                self._trigger_double_guard(34, f"Failed to parse loadavg string: {str(e)}")
                return 0.0
        return 0.0

    def is_processor_exhausted(self, critical_threshold=4.5):
        current_load = self.fetch_hardware_cpu_load()
        if current_load >= critical_threshold:
            print(f"\033[93m[!] WARNING - Hardware Core Strain Detected! Current Load: {current_load}\033[0m")
            return True
        return False
