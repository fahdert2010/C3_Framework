#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ultimate C3 Framework - Hardened Access Point Hardware & Interface Verifier
File: /home/kali/C3_Framework/core/ap_verifier.py
"""

import json
import datetime
import traceback
from core.ssh_executor import SSHHardwareExecutor

class AccessPointHardwareVerifier:
    def __init__(self, ssh_executor: SSHHardwareExecutor):
        self.executor = ssh_executor
        self.log_path = "/home/kali/C3_Framework/storage/logs/attack_errors.log"

    def _trigger_double_guard(self, line_num, reason, stack_trace):
        # التصحيح البصري الصارم: إزالة المسافات البيضاء المشوهة من رموز ANSI للألوان
        print(f"\033[91m[!] خطأ حرج - الفئة: APVerifier | السطر: {line_num} | السبب: {reason}\033[0m")
        try:
            with open(self.log_path, "a", encoding="utf-8") as log_file:
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                log_file.write(f"[{timestamp}] CRITICAL - APVerifier | Line: {line_num} | Reason: {reason}\n")
        except IOError:
            pass

    def verify_hardware_connection_pulse(self):
        """فحص النبض الفيزيائي الأولي واستجابة موجه الأوامر بالراوتر البعيد"""
        response = self.executor.execute_raw_command(["echo", "C3_PULSE"])
        if response["status"] == "success" and "C3_PULSE" in response["output"]:
            return True
        return False

    def fetch_openwrt_firmware_release(self):
        """قراءة صريحة لملف النظام الداخلي لاستخراج إصدار OpenWrt ونوع النواة"""
        firmware_details = {"dist": "Unknown", "version": "Unknown", "kernel": "Unknown"}
        
        res_release = self.executor.execute_raw_command(["cat", "/etc/openwrt_release"])
        res_kernel = self.executor.execute_raw_command(["uname", "-r"])
        
        if res_kernel["status"] == "success":
            firmware_details["kernel"] = res_kernel["output"].strip()
            
        if res_release["status"] == "success" and res_release["output"]:
            lines = res_release["output"].split("\n")
            for line in lines:
                if "DISTRIB_DESCRIPTION" in line:
                    firmware_details["dist"] = line.split("=")[-1].replace("'", "").replace('"', '').strip()
                elif "DISTRIB_RELEASE" in line:
                    firmware_details["version"] = line.split("=")[-1].replace("'", "").replace('"', '').strip()
                    
        return firmware_details

    def fetch_isolated_interfaces_map(self):
        """
        استعلام بنيوي شامل عبر ubus لتفكيك وعرض معلومات الترددات (2G/5G) منفصلة
        مع تحصين الفك الجراحي لمنع انهيار مفسر البيانات اللحظي
        """
        hardware_map = {"2G": [], "5G": []}
        response = self.executor.execute_raw_command(["ubus", "call", "network.wireless", "status"])
        
        if response["status"] != "success" or not response["output"]:
            return hardware_map

        # التحقق الصارم من استهلال النص بصيغة الـ JSON الصريحة قبل الفك لمنع الصدمات
        clean_output = response["output"].strip()
        if not (clean_output.startswith("{") or clean_output.startswith("[")):
            self._trigger_double_guard(58, "جهاز الراوتر أعاد مخرجاً نصياً مشوهاً عمارياً وليس شجرة JSON صالحة", clean_output)
            return hardware_map

        try:
            raw_json = json.loads(clean_output)
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
                        
                    is_5g = "5g" in hardware_band or "a" in hardware_band if hardware_band else channel > 14
                    current_freq = "5G" if is_5g else "2G"
                    
                    iface_details = {
                        "radio": radio_id,
                        "interface_name": iface.get("ifname", "unknown"),
                        "ssid": config.get("ssid", "<Hidden_or_Broadcast_Disabled>"),
                        "channel": channel,
                        "vif_uci_id": config.get("name", "unknown"),
                        "status": "UP" if iface.get("up", False) else "DOWN"
                    }
                    
                    hardware_map[current_freq].append(iface_details)
                    
            return hardware_map
            
        except Exception as e:
            self._trigger_double_guard(92, f"Failed to map internal wireless structures: {str(e)}", traceback.format_exc())
            return hardware_map
