#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ultimate C3 Framework - Micro OUI Target Filter Module
File: /home/kali/C3_Framework/modules/oui_filter_module.py
"""

from core.oui_database import OUIHardwareDatabase

class OUITargetFilterModule:
    def __init__(self):
        self.oui_db = OUIHardwareDatabase()
        self.target_vendors_pool = set() # مسبح الشركات المراد ضربها جراحياً

    def set_target_vendors(self, vendors_list):
        """تحديد الشركات المستهدفة بالهجوم (مثال: ['Hikvision_Camera', 'Dahua_Camera'])"""
        self.target_vendors_pool = set([v.strip() for v in vendors_list])

    def is_device_targeted(self, mac_address):
        """التحقق الجراحي: هل يطابق الماك الحالي بصمة الشركات المستهدفة؟"""
        if not self.target_vendors_pool:
            return True # إذا لم يحدد المشغل شركة، يتم تمرير الهدف كالمعتاد
            
        vendor = self.oui_db.resolve_vendor_by_mac(mac_address)
        return vendor in self.target_vendors_pool

    def render_scanned_target_details(self, mac_address):
        """إرجاع تحليل البصمة الكامل للهدف لطباعته في التيرمنال التراكمي"""
        vendor = self.oui_db.resolve_vendor_by_mac(mac_address)
        return f"Device: {mac_address} [Vendor: {vendor}]"
