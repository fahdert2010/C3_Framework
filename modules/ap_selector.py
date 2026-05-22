#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ultimate C3 Framework - Micro Access Point Context Selector
File: /home/kali/C3_Framework/modules/ap_selector.py
"""

import sys
from modules.ap_selector_core import UnifiedBandSelectorCore

class AccessPointSelectorMatrix:
    def __init__(self, bootstrap_context):
        """
        ربط السياق لمنع الـ Multi-Instantiation والاعتماد الدائري
        """
        self.ctx = bootstrap_context
        self.band_core = UnifiedBandSelectorCore(self.ctx)

    def execute_ap_selection_pipeline(self, selected_ap):
        """
        واجهة توجيه تكتيكية تسأل عن التردد وتضخه نحو معالج النطاقات الموحد
        """
        while True:
            print("\n" + "─"*50)
            print("   \033[95mترسانة C3 - سويتش عزل وترشيح النطاقات اللاسلكية\033[0m   ")
            print("─"*50)
            print(" [\033[92m1\033[0m] استهداف ونشر العمليات على نطاق وتردد الـ 2G (2.4 GHz)")
            print(" [\033[92m2\033[0m] استهداف ونشر العمليات على نطاق وتردد الـ 5G (5 GHz)")
            print(" [\033[91m0\033[0m] العودة إلى قائمة القواذف (أو اضغط Enter مباشرة)")
            print("─"*50)
            
            choice = input("[>] نطاق العمليات المستهدف: ").strip()
            
            if choice == "0" or choice == "":
                sys.stdin.flush()
                break
            elif choice == "1":
                if self.band_core.process_isolated_band_flow(selected_ap, "2G"):
                    break
            elif choice == "2":
                if self.band_core.process_isolated_band_flow(selected_ap, "5G"):
                    break
            else:
                print("[!] اختيار خارج الحدود البرمجية.")
