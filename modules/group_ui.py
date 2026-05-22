#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ultimate C3 Framework - Visual Hardened Target Grouping UI
File: /home/kali/C3_Framework/modules/group_ui.py
"""

import sys
import re
from core.database import DatabaseManager

class TargetGroupConsoleUI:
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager

    def display_group_menu(self):
        while True:
            print("\n" + "═"*50)
            print("   \033[95mترسانة C3 - مدير تقسيم المجموعات وقنوات الفرز بالأثير\033[0m   ")
            print("═"*50)
            print(" \033[92m[\033[1m1\033[0m\033[92m]\033[0m استعلام وعرض كافة المجموعات القتالية المسجلة")
            print(" \033[92m[\033[1m2\033[0m\033[92m]\033[0m إسناد وتعيين ماك أدرس مستهدف إلى مجموعة مخصصة")
            print(" \033[92m[\033[1m3\033[0m\033[92m]\033[0m تفكيك ومحو كافة سجلات المجموعات بالكامل (Purge)")
            print(" \033[91m[\033[1m0\033[0m\033[91m]\033[0m العودة إلى لوحة التحكم الرئيسية (أو اضغط Enter مباشرة)")
            print("═"*50)

            choice = input("[>] خيارك العملياتي: ").strip()

            if choice == "0" or choice == "":
                break
            elif choice == "1":
                rows = self.db.fetch_all_groups()
                print(f"\n\033[94m[*] المجموعات القتالية النشطة حالياً ({len(rows)} جهاز):\033[0m")
                if not rows:
                    print("  [!] لا توجد أي مجموعات تكتيكية تم إنشاؤها حتى الآن.")
                for row in rows:
                    print(f"  -> هدف فيزيائي: \033[91m{row}\033[0m | القناة التابع لها: \033[93m{row}\033[0m")
            elif choice == "2":
                mac = input("[+] أدخل ماك أدرس الهدف: ").strip().lower()
                gname = input("[+] اسم المجموعة المستهدفة (مثال: كاميرات / هواتف): ").strip()

                if not re.match(r'^([0-9a-f]{2}[:-]){5}([0-9a-f]{2})$', mac) or not gname:
                    print("\033[91m[!] تم الرفض: ماك أدرس مشوه أو اسم مجموعة فارغ.\033[0m")
                    return

                clean_gname = re.sub(r'[^\w\s]', '', gname).strip()
                if self.db.add_mac_to_group_record(mac, clean_gname):
                    print("\033[92m[+] تم إنشاء وتثبيت شريحة المجموعة التكتيكية بنجاح صامد.\033[0m")
                else:
                    print("\033[91m[!] فشلت العملية بسبب حظر في طبقة المعالجة.\033[0m")
            elif choice == "3":
                confirm = input("[?] هل أنت متأكد من مسح وتطهير كافة المجموعات؟ [y/n]: ").strip().lower()
                if confirm == 'y' and self.db.purge_all_group_records():
                    print("\033[92m[+] تم تدمير ومحو مصفوفة المجموعات القتالية بالكامل من القرص.\033[0m")
            else:
                print("[!] اختيار خارج الحدود البرمجية المسموح بها.")
