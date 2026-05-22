#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ultimate C3 Framework - Hardened Dynamic Scout Module
File: /home/kali/C3_Framework/core/dynamic_scout.py
"""

import json
import datetime
import traceback
from core.ssh_executor import SSHHardwareExecutor

class DynamicScout:
    def __init__(self, ssh_executor=None):
        self.executor = ssh_executor if ssh_executor else SSHHardwareExecutor()
        self.log_path = "/home/kali/C3_Framework/storage/logs/attack_errors.log"

    def _trigger_double_guard(self, line_num, reason, stack_trace):
        print(f"\033[91m[!] CRITICAL - Class: DynamicScout | Line: {line_num} | Reason: {reason}\033[0m")
        try:
            with open(self.log_path, "a", encoding="utf-8") as log_file:
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                log_file.write(f"[{timestamp}] CRITICAL - Class: DynamicScout | Line: {line_num} | Reason: {reason}\n")
                log_file.write(f"Stack Trace:\n{stack_trace}\n{'-'*50}\n")
        except IOError as e:
            print(f"\033[91m[!] FATAL - Log write failed: {str(e)}\033[0m")

    def fetch_wireless_status_json(self):
        response = self.executor.execute_raw_command(["ubus", "call", "network.wireless", "status"])
        if response["status"] == "success" and response["output"]:
            try:
                return json.loads(response["output"])
            except json.JSONDecodeError as e:
                tb = traceback.extract_tb(e.__traceback__)
                line_num = tb[-1].lineno if tb else "JSONParse"
                self._trigger_double_guard(line_num, "JSON breakdown failure", traceback.format_exc())
                return None
        return None

    def parse_interfaces_by_frequency(self, frequency_target="2G"):
        """
        إزاحة أمر الـ return بالكامل إلى الخارج لضمان المرور على كافة الكروت اللاسلكية دون تعمية
        """
        scouted_data = []
        raw_json = self.fetch_wireless_status_json()
        
        if not raw_json:
            return scouted_data

        try:
            for radio_id, radio_content in raw_json.items():
                interfaces = radio_content.get("interfaces", [])
                hardware_band = radio_content.get("config", {}).get("band", "").lower()
                
                for iface in interfaces:
                    config = iface.get("config", {})
                    iwdata = iface.get("iwinfo", {})
                    
                    try:
                        channel = int(iwdata.get("channel", 0))
                    except (ValueError, TypeError):
                        channel = 0
                    
                    if hardware_band:
                        is_5g = "5g" in hardware_band or "a" in hardware_band
                    else:
                        is_5g = channel > 14

                    current_freq = "5G" if is_5g else "2G"
                    
                    if current_freq == frequency_target:
                        scouted_data.append({
                            "radio_id": radio_id,
                            "vif_id": config.get("name", "unknown"),
                            "ifname": iface.get("ifname", "unknown"),
                            "channel": channel,
                            "clients": len(iface.get("assoclist", {}))
                        })
            # تم إزاحة السطر بنجاح خارج حلقات التكرار لقراءة كافة معرفات الراديو
            return scouted_data
            
        except Exception as e:
            tb = traceback.extract_tb(e.__traceback__)
            line_num = tb[-1].lineno if tb else "ParsingError"
            self._trigger_double_guard(line_num, f"Hardware frequency filtering broken: {str(e)}", traceback.format_exc())
            return scouted_data

    def evaluate_client_danger_zone(self, frequency_target="2G"):
        total_clients = 0
        target_vifs = []
        scouted_interfaces = self.parse_interfaces_by_frequency(frequency_target)
        
        for iface in scouted_interfaces:
            total_clients += iface["clients"]
            if iface["vif_id"] != "unknown":
                target_vifs.append({
                    "radio": iface["radio_id"],
                    "vif": iface["vif_id"],
                    "channel": iface["channel"]
                })
        return total_clients, target_vifs
