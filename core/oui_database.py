#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ultimate C3 Framework - Micro OUI Database Analyzer
File: /home/kali/C3_Framework/core/oui_database.py
"""

import datetime

class OUIHardwareDatabase:
    def __init__(self):
        self.log_path = "/home/kali/C3_Framework/storage/logs/attack_errors.log"
        # مسبح البصمات الصلب المرفوع في الرام حصرًا لحماية طاقة المعالجة
        self.oui_registry = {
            "00:0f:c4": "Hikvision_Camera",
            "bc:ad:28": "Hikvision_Camera",
            "00:1a:8c": "Dahua_Camera",
            "bc:5f:f4": "Huawei_Device",
            "ac:3b:7a": "Apple_Device",
            "4c:cc:6a": "Apple_Device",
            "7c:c7:09": "Samsung_Device",
            "e0:b9:e5": "Xiaomi_Device"
        }

    def _trigger_double_guard(self, line_num, reason):
        print(f"\033[91m[!] CRITICAL - Class: OUIHardwareDatabase | Line: {line_num} | Reason: {reason}\033[0m")
        try:
            with open(self.log_path, "a", encoding="utf-8") as log_file:
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                log_file.write(f"[{timestamp}] CRITICAL - Class: OUIHardwareDatabase | Line: {line_num} | Reason: {reason}\n")
        except IOError:
            pass

    def extract_oui_prefix(self, mac_address):
        """استخراج أول 3 خانات من الماك أدرس بشكل مطهر وموحد صريح"""
        try:
            clean_mac = mac_address.strip().lower().replace("-", ":")
            segments = clean_mac.split(":")
            if len(segments) >= 3:
                return ":".join(segments[:3])
            return None
        except Exception as e:
            self._trigger_double_guard(42, f"Prefix extraction crash: {str(e)}")
            return None

    def resolve_vendor_by_mac(self, mac_address):
        """مطابقة الماك مع مسبح الـ OUI لإرجاع اسم الشركة المصنعة جراحياً"""
        prefix = self.extract_oui_prefix(mac_address)
        if not prefix:
            return "Unknown_Vendor"
        return self.oui_registry.get(prefix, "Unknown_Vendor")
