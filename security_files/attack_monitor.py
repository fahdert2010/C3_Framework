#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ultimate C3 Framework - Micro Port Stability Watchdog
File: /home/kali/C3_Framework/security_files/attack_monitor.py
"""

import subprocess
import datetime

class AttackPortMonitor:
    def __init__(self):
        self.log_path = "/home/kali/C3_Framework/storage/logs/attack_errors.log"

    def verify_remote_port_binding(self, router_ip, airserv_port):
        """إجراء فحص اتصال صامت وسريع جداً عبر Netcat للكشف عن انهيار المنفذ البعيد"""
        try:
            check_cmd = ["nc", "-z", "-w", "1", router_ip, str(airserv_port)]
            status = subprocess.run(check_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            if status.returncode == 0:
                return "active"
            return "collapsed"
        except Exception as e:
            try:
                with open(self.log_path, "a", encoding="utf-8") as log_file:
                    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    log_file.write(f"[{timestamp}] CRITICAL - AttackPortMonitor: Check broke -> {str(e)}\n")
            except IOError:
                pass
            return "error"
