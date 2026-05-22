#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ultimate C3 Framework - Hardened Intelligent State-Driven Menu Router
File: /home/kali/C3_Framework/modules/menu_router.py
"""

class TacticalMenuRouter:
    def __init__(self, context_bridge):
        self.ctx = context_bridge

    def display_clear_dashboard(self):
        """توليد اللوحة الرئيسية بعدادات ذكية ومؤشرات الأثير حياً بالرام"""
        aps_count = len(self.ctx.db.fetch_all_registered_aps())
        group_count = len(self.ctx.db.fetch_all_groups())
        status_flag = "\033[92m[ نشط وآمن ]\033[0m" if not self.ctx.is_attack_active else "\033[91m[ قذف مستمر بالخلفية ]\033[0m"

        print("\n" + "═"*65)
        print(f"   \033[96mمركز التحكم والسيطرة للترسانة اللاسلكية\033[0m -> وضع المنصة: {status_flag}")
        print("═"*65)
        print(f" [\033[92m1\033[0m] تسجيل وإدارة قواذف الأكسس بوينت -> (المسجل حالياً: {aps_count} جهاز مهاجم)")
        print(f" [\033[92m2\033[0m] مصفوفة المجموعات وقنوات الفرز     -> (المجموعات النشطة: {group_count} مجموعة)")
        print(" [\033[92m3\033[0m] مركز الفحص والتعطيل الحار السريع  -> (نبض العتاد وتفريغ الكاش)")
        print(" [\033[92m4\033[0m] تقصي الأثير والاستطلاع المباشر      -> (قراءة قنوات ubus حياً بالخلفية)")
        
        if not self.ctx.is_attack_active:
            print(" [\033[92m5\033[0m] إطلاق الترسانة والهجوم الآلي الموجه -> (بدء توجيه حزم الفصل بالأثير)")
        else:
            print(" [\033[91m5\033[0m] إوقاف الهجوم النشط فوراً طوعياً     -> (تفكيك قنوات الحقن والانسحاب)")
            print(" [\033[93mW\033[0m] استعلام حمل معالج الراوتر البعيد  -> (نبض حساس حارس الكيرنل اللحظي)")
            
        print(" [\033[91m0\033[0m] التطهير التكتيكي وإغلاق المنصة     -> (إبادة العمليات والانسحاب النظيف)")
        print("═"*65)
        return input("[>] اختيارك العملياتي: ").strip()
