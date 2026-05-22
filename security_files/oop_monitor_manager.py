#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ultimate C3 Framework - Hardened Monitor Interface Manager
File: /home/kali/C3_Framework/security_files/oop_monitor_manager.py
"""

import time
import re
import datetime
import traceback
from core.ssh_executor import SSHHardwareExecutor

class MonitorInterfaceManager:
    def __init__(self, ssh_executor=None):
        self.executor = ssh_executor if ssh_executor else SSHHardwareExecutor()
        self.log_path = "/home/kali/C3_Framework/storage/logs/attack_errors.log"
        self.interface_regex = re.compile(r'Interface\s+([a-zA-Z0-9_\-\.]+)')

    def _trigger_double_guard(self, line_num, reason, stack_trace):
        print(f"\033[91m[!] CRITICAL - Class: MonitorInterfaceManager | Line: {line_num} | Reason: {reason}\033[0m")
        try:
            with open(self.log_path, "a", encoding="utf-8") as log_file:
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                log_file.write(f"[{timestamp}] CRITICAL - Class: MonitorInterfaceManager | Line: {line_num} | Reason: {reason}\n")
                log_file.write(f"Stack Trace:\n{stack_trace}\n{'-'*50}\n")
        except IOError as e:
            print(f"\033[91m[!] FATAL - Log write failed: {str(e)}\033[0m")

    def establish_hardware_monitors(self, radio_id="radio0", monitor_idx=0):
        """
        تثبيت المعرفات عتادياً وسحق ثغرة الاسم المشوه عبر استخراج الأرقام ديناميكياً بالـ Regex
        """
        mon_vif = f"mon{monitor_idx}"
        
        # قنص رقم الكرت بشكل آمن رغماً عن التسميات المصنعية المتغيرة للـ Kernel
        match = re.search(r'\d+', radio_id)
        phy_idx = match.group(0) if match else "0"
        phy_ifname = f"phy{phy_idx}-mon{monitor_idx}"
        
        commands = [
            f"uci set wireless.{mon_vif}=wifi-iface",
            f"uci set wireless.{mon_vif}.device='{radio_id}'",
            f"uci set wireless.{mon_vif}.ifname='{phy_ifname}'",
            f"uci set wireless.{mon_vif}.mode='monitor'",
            "uci commit wireless",
            "wifi reload"
        ]
        
        execution_cmd = ["/bin/sh", "-c", " && ".join(commands)]
        response = self.executor.execute_raw_command(execution_cmd)
        return response["status"] == "success"

    def snatch_actual_kernel_name(self):
        """
        تجاوز ثغرة عمى الكيرنل عبر حلقة الـ Exponential Backoff وقنص الاسم الحركي الفعلي
        """
        delay = 0.5
        for attempt in range(1, 6):
            time.sleep(delay)
            response = self.executor.execute_raw_command(["iw", "dev"])
            
            if response["status"] == "success" and response["output"]:
                matches = self.interface_regex.findall(response["output"])
                for name in matches:
                    if "mon" in name or "wlan" in name:
                        return {"status": "success", "actual_name": name}
            delay *= 1.5
            
        return {"status": "kernel_blindness", "actual_name": None}

    def force_kickstart_interface(self, actual_name):
        """
        الرفع القسري عتادياً عبر غلاف شل صريح وموحد لمنع فخ المعاملات المعزولة في SSH
        """
        if not actual_name:
            return False
            
        # التصحيح الهندسي: تمرير الأمر داخل شل صريح لضمان الرفع الفيزيائي للكرت
        shell_cmd = ["/bin/sh", "-c", f"ifconfig {actual_name} up"]
        response = self.executor.execute_raw_command(shell_cmd)
        return response["status"] == "success"

    def clear_monitor_structures(self, monitor_idx=0):
        mon_vif = f"mon{monitor_idx}"
        commands = [
            f"uci del wireless.{mon_vif}",
            "uci commit wireless",
            "wifi reload"
        ]
        execution_cmd = ["/bin/sh", "-c", " && ".join(commands)]
        response = self.executor.execute_raw_command(execution_cmd)
        return response["status"] == "success"
