#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ultimate C3 Framework - Hardened Tactical Hardware Orchestrator
File: /home/kali/C3_Framework/security_files/oop_orchestrator.py
"""

import os
import datetime
import traceback
from core.ssh_executor import SSHHardwareExecutor

class AttackOrchestrator:
    def __init__(self, ssh_executor=None):
        self.executor = ssh_executor if ssh_executor else SSHHardwareExecutor()
        self.log_path = "/home/kali/C3_Framework/storage/logs/attack_errors.log"

    def _trigger_double_guard(self, line_num, reason, stack_trace):
        print(f"\033[91m[!] CRITICAL - Class: AttackOrchestrator | Line: {line_num} | Reason: {reason}\033[0m")
        try:
            with open(self.log_path, "a", encoding="utf-8") as log_file:
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                log_file.write(f"[{timestamp}] CRITICAL - Class: AttackOrchestrator | Line: {line_num} | Reason: {reason}\n")
                log_file.write(f"Stack Trace:\n{stack_trace}\n{'-'*50}\n")
        except IOError as e:
            print(f"\033[91m[!] FATAL - Log write failed: {str(e)}\033[0m")

    def hard_isolate_frequency(self, target_vifs):
        """
        تعطيل واجهات البث حركياً مع سحق ثغرة التكرار وتفادي تعليق الباش
        """
        if not target_vifs:
            return False

        commands_pool = []
        processed_radios = set()
        
        try:
            for item in target_vifs:
                radio = item.get("radio")
                vif = item.get("vif")
                channel = item.get("channel")
                
                if radio and vif:
                    commands_pool.append(f"uci set wireless.{vif}.disabled='1'")
                    
                    # سحق ثغرة تكرار تعديل القناة لنفس كرت الراديو
                    if channel and (radio not in processed_radios):
                        commands_pool.append(f"uci set wireless.{radio}.channel='{channel}'")
                        processed_radios.add(radio)

            if not commands_pool:
                return False

            commands_pool.append("uci commit wireless")
            commands_pool.append("wifi reload")
            
            # الحل البنيوي: إجبار الباش بالراوتر على التنفيذ المتسلسل الآمن كمصفوفة دخل
            execution_cmd = ["/bin/sh", "-c", " && ".join(commands_pool)]
            response = self.executor.execute_raw_command(execution_cmd)
            
            return response["status"] == "success"

        except Exception as e:
            tb = traceback.extract_tb(e.__traceback__)
            line_num = tb[-1].lineno if tb else "IsolateFreq"
            self._trigger_double_guard(line_num, f"UCI isolation pipeline collapsed: {str(e)}", traceback.format_exc())
            return False

    def pure_safe_revival(self, target_vifs):
        """
        إحياء بث الزبائن بقوة الـ UCI وعبر مصفوفة دخل الشل المحمية
        """
        if not target_vifs:
            return False

        commands_pool = []
        try:
            for item in target_vifs:
                vif = item.get("vif")
                if vif:
                    commands_pool.append(f"uci set wireless.{vif}.disabled='0'")

            if not commands_pool:
                return False

            commands_pool.append("uci commit wireless")
            commands_pool.append("wifi reload")
            
            execution_cmd = ["/bin/sh", "-c", " && ".join(commands_pool)]
            response = self.executor.execute_raw_command(execution_cmd)
            
            return response["status"] == "success"

        except Exception as e:
            tb = traceback.extract_tb(e.__traceback__)
            line_num = tb[-1].lineno if tb else "RevivalFreq"
            self._trigger_double_guard(line_num, f"UCI revival pipeline collapsed: {str(e)}", traceback.format_exc())
            return False
