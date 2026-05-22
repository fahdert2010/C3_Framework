#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ultimate C3 Framework - Visual Hardened Access Point Registration UI
File: /home/kali/C3_Framework/modules/ap_ui.py
"""

import sys
from core.database import DatabaseManager

class ProtectedDevicesConsoleUI:
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager

    def display_ui_frame(self):
        while True:
            print("\n" + "─"*60)
            print("   \033[96mمدير العتاد التكتيكي - تسجيل وإضافة منصات الأكسس بوينت\033[0m   ")
            print("─"*60)
            print(" [\033[92m1\033[0m] استعلام وعرض كافة منصات البث المهاجمة والمسجلة")
            print(" [\033[92m2\033[0m] تسجيل جهاز أكسس بوينت جديد وتأمين كلمة سره بالـ AES")
            print(" [\033[91m0\033[0m] العودة إلى لوحة التحكم الرئيسية (أو اضغط Enter مباشرة)")
            print("─"*60)
            
            opt = input("[>] اختيارك العملياتي: ").strip()
            if opt == "0" or opt == "":
                break
            elif opt == "1":
                aps = self.db.fetch_all_registered_aps()
                print(f"\n\033[94m[*] قواذف الأثير المسجلة بالنظام حالياً ({len(aps)} جهاز):\033[0m")
                for item in aps:
                    print(f"  -> المعرف: \033[92m{item[0]}\033[0m | الاسم: \033[93m{item[1]:<14}\033[0m | الآي بي: \033[96m{item[2]:<15}\033[0m | المجموعة: \033[95m{item[5]}\033[0m")
            elif opt == "2":
                name = input("[+] اسم الأكسس بوينت (فريد حصرًا): ").strip()
                ip = input("[+] عنوان الآي بي الصريح (IP فريد): ").strip()
                username = input("[+] اسم مستخدم SSH (اضغط Enter للـ root افتراضياً): ").strip()
                password = input("[+] كلمة المرور الحركية للراوتر: ").strip()
                group = input("[+] اسم المجموعة القتالية التابع لها العتاد: ").strip()
                
                if not name or not ip or not password or not group:
                    print("\033[91m[!] خطأ: لا يمكن ترك الحقول الأساسية فارغة.\033[0m")
                    continue
                if self.db.register_access_point(name, ip, username, password, group):
                    print("\033[92m[+] تم تسجيل وقفل بيانات جهاز الإرسال وتأمين التشفير بالـ AES بنجاح صامد.\033[0m")
            else:
                print("[!] اختيار خارج الحدود البرمجية.")
