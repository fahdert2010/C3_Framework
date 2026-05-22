#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ultimate C3 Framework - Visual Hardened Fast Control Center UI
File: /home/kali/C3_Framework/modules/control_center_ui.py
"""

import sys
import subprocess
from core.ssh_executor import SSHHardwareExecutor
from core.dynamic_scout import DynamicScout

class FastControlCenterUI:
    def __init__(self, current_executor: SSHHardwareExecutor, shared_scout: DynamicScout):
        self.executor = current_executor
        self.scout = shared_scout

    def display_hot_center(self):
        while True:
            print("\n" + "═"*50)
            print("   \033[91mجدار ناري C3 - مركز الفحص العتادي والتعطيل الحار السريع\033[0m   ")
            print("═"*50)
            print(" [\033[92m1\033[0m] فحص النبض الفيزيائي الحي للراوتر وجاهزية منفذ الـ SSH")
            print(" [\033[92m2\033[0m] استعلام فوري عن الزبائن المتصلين في الوقت الفعلي")
            print(" [\033[92m3\033[0m] التطهير القسري لكاش ذاكرة الراوتر (تحرير النواة البعيدة)")
            print(" [\033[91m0\033[0m] العودة إلى لوحة التحكم الرئيسية (أو اضغط Enter مباشرة)")
            print("═"*50)

            opt = input("[>] اختيارك العملياتي: ").strip()

            if opt == "0" or opt == "":
                # تنظيف صريح لـ Buffer الإدخال لمنع تداخل القوائم الذكية
                sys.stdin.flush()
                break
            elif opt == "1":
                print("[*] جارٍ قذف حزمة الفحص التشخيصي نحو منفذ العتاد...")
                check_cmd = ["nc", "-z", "-w", "2", self.executor.ip, "22"]
                status = subprocess.run(check_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                if status.returncode == 0:
                    print("\033[92m[+] العتاد متصل حياً (HARDWARE ONLINE): منفذ SSH يستجيب بكفاءة.\033[0m")
                else:
                    print("\033[91m[!] العتاد منفصل (HARDWARE OFFLINE): انقطع الاتصال عتادياً.\033[0m")
            elif opt == "2":
                print("[*] جارٍ سحب مصفوفة المصافحات النشطة مباشرة من الـ ubus بالخلفية...")
                raw_json = self.scout.fetch_wireless_status_json()
                if raw_json:
                    print("\033[94m[*] الأجهزة والزبائن المرصودين متصلين فيزيائياً حالياً:\033[0m")
                    for radio, data in raw_json.items():
                        for iface in data.get("interfaces", []):
                            assoclist = iface.get("assoclist", {})
                            for mac, details in assoclist.items():
                                print(f" -> جهاز زبون: {mac} | قوة الإشارة: {details.get('signal', 'N/A')} dBm")
                else:
                    print("[!] فشل تفكيك شجرة الشبكة اللاسلكية بالراوتر.")
            elif opt == "3":
                print("[*] جارٍ ترحيل التطهير العتادي الصارم ليعمل كأوامر معزولة متتالية...")
                # التصحيح المعماري الحصين: إبادة غلاف الشل والتوجيه المباشر للمفسر
                purge_cmd = ["sysctl", "-w", "vm.drop_caches=3"]
                res = self.executor.execute_raw_command(purge_cmd)
                if res["status"] == "success":
                    print("\033[92m[+] تم تحرير كاش النواة البعيدة بالكامل بنجاح واستقرت الذاكرة.\033[0m")
                else:
                    print("\033[91m[!] فشل الأمر أو رفض العتاد معالجة الطلب.\033[0m")
            else:
                print("[!] اختيار غير مدعوم برمجياً.")
