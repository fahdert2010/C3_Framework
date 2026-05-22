#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ultimate C3 Framework - Visual Hardened OOP Main Bootstrap (v2 - Refactored Edition)
File: /home/kali/C3_Framework/main_v2.py
"""

import os
import sys

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
from modules.ap_selector import AccessPointSelectorMatrix

class C3MicroFrameworkBootstrap:
    def __init__(self):
        self.attack_shutdown_lock = threading.Event()
        self.is_attack_active = False
        self.strain_counter = 0
        self.target_vifs_cache = []

        self.active_ap_name = "N/A"
        self.active_frequency = "N/A"
        self.active_channel = "N/A"
        self.active_port = "N/A"

        self.db = DatabaseManager()
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
        self.verifier = AccessPointHardwareVerifier(self.scout_executor)
        
        self.ap_interface = ProtectedDevicesConsoleUI(self.db)
        self.group_interface = TargetGroupConsoleUI(self.db)
        self.fast_control_center = FastControlCenterUI(self.scout_executor, self.scout)
        
        # لودر ربط الموديلات الفرعية المستحدثة
        self.router = TacticalMenuRouter(self)
        self.pipeline = TacticalAttackEngine(self)
        self.ap_selector = AccessPointSelectorMatrix(self)
        
        signal.signal(signal.SIGINT, self.pure_safe_retreat_handler)

    def pure_safe_retreat_handler(self, signum, frame):
        """التطهير الترددي الشامل وتصحيح إعادة إحياء البث بقفل العتاد الحقيقي"""
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
        
        # التصحيح الميداني الصخر: استخدام مفتاح العزل الحقيقي vif_uci_id لضمان استيقاظ شبكة الزبائن
        if self.target_vifs_cache:
            commands_pool = [f"uci set wireless.{item.get('vif_uci_id')}.disabled='0'" for item in self.target_vifs_cache if item.get('vif_uci_id')]
            if commands_pool:
                commands_pool.extend(["uci commit wireless", "wifi reload"])
                emergency_executor.execute_raw_command(["/bin/sh", "-c", " && ".join(commands_pool)])
                
        print("\033[92m[+] اكتمل التطهير التكتيكي الشامل. الأثير آمن والمنصة مغلقة ونظيفة.\033[0m")
        if signum is not None:
            sys.exit(0)

    def _inject_ap_session_credentials(self, ap_record):
        ap_ip = ap_record[2]
        ap_plain_pass = self.db._decrypt_password(ap_record[4])
        for executor in [self.scout_executor, self.orch_executor, self.airserv_executor, self.filter_executor, self.watchdog_executor]:
            executor.ip = ap_ip
            executor.password = ap_plain_pass

    def bootstrap_orchestration_loop(self):
        while True:
            sys.stdin.flush()
            choice = self.router.display_clear_dashboard()
            
            if choice == "1":
                self.ap_interface.display_ui_frame()
            elif choice == "2":
                # التصحيح المعماري: استدعاء الدالة الصريحة الموحدة للواجهة الفرعية لمنع AttributeError
                self.group_interface.display_ui_frame()
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
                    # ترحيل السيطرة الحركية لكائن عزل وقراءة قواذف العتاد المستحدث
                    self.ap_selector.execute_ap_selection_pipeline(choice)
                else:
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
        print("[!] خطأ في الصلاحيات: يرجى التشغيل بصلاحيات الجذر (sudo).")
        sys.exit(1)
    launcher = C3MicroFrameworkBootstrap()
    launcher.bootstrap_orchestration_loop()
