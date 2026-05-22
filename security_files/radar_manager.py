#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ultimate C3 Framework - Hardened Persistent Radar & File Size Guard
File: /home/kali/C3_Framework/security_files/radar_manager.py
"""

import os
import time
import subprocess
import signal
import datetime
import traceback
import glob

class RadarSizeGuardManager:
    def __init__(self):
        self.log_path = "/home/kali/C3_Framework/storage/logs/attack_errors.log"
        self.csv_directory = "/home/kali/C3_Framework/storage/logs/"
        self.output_prefix = "radar_output"

    def _trigger_double_guard(self, line_num, reason, stack_trace):
        print(f"\033[91m[!] CRITICAL - Class: RadarSizeGuardManager | Line: {line_num} | Reason: {reason}\033[0m")
        try:
            with open(self.log_path, "a", encoding="utf-8") as log_file:
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                log_file.write(f"[{timestamp}] CRITICAL - Class: RadarSizeGuardManager | Line: {line_num} | Reason: {reason}\n")
                log_file.write(f"Stack Trace:\n{stack_trace}\n{'-'*50}\n")
        except IOError as e:
            print(f"\033[91m[!] FATAL - Log write failed: {str(e)}\033[0m")

    def purge_legacy_session_files(self):
        """
        تطهير ساحة اللوجات تماماً قبل الإقلاع لمنع التداخل الجلساتي وحلقة إعادة التشغيل اللانهائية
        """
        try:
            pattern = os.path.join(self.csv_directory, f"{self.output_prefix}*")
            for filepath in glob.glob(pattern):
                if os.path.isfile(filepath):
                    os.remove(filepath)
        except Exception as e:
            pass

    def get_latest_csv_path_and_size(self):
        """
        التصحيح الهندسي: العثور على ملف الجلسة الفعلي والحي المولد بواسطة الأداة ديناميكياً
        """
        try:
            pattern = os.path.join(self.csv_directory, f"{self.output_prefix}*.csv")
            files = glob.glob(pattern)
            if not files:
                return None, 0
            # قنص الملف الأحدث والحي بناءً على تاريخ التعديل الفعلي للـ Kernel
            latest_file = max(files, key=os.path.getmtime)
            return latest_file, os.path.getsize(latest_file)
        except Exception as e:
            return None, 0

    def launch_local_radar(self, router_ip, airserv_port):
        """
        إطلاق الرادار المحلي بعد تطهير وبتر الملفات الميتة لامتصاص الحزم الصافي
        """
        self.terminate_local_radar()
        self.purge_legacy_session_files() # البتر التطهيري الفوري
        
        full_prefix_path = os.path.join(self.csv_directory, self.output_prefix)
        radar_cmd = [
            "airodump-ng",
            f"{router_ip}:{airserv_port}",
            "--write", full_prefix_path,
            "--output-format", "csv"
        ]
        
        try:
            self.radar_process = subprocess.Popen(
                radar_cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                preexec_fn=os.setsid
            )
            return True
        except Exception as e:
            tb = traceback.extract_tb(e.__traceback__)
            line_num = tb[-1].lineno if tb else "LaunchRadar"
            self._trigger_double_guard(line_num, f"Radar crash: {str(e)}", traceback.format_exc())
            return False

    def execute_file_size_guard_check(self, router_ip, airserv_port):
        """
        ميكانيزم حارس حجم الملف المحدث المقاوم للجمود والملفات الميتة
        """
        try:
            _, size_1 = self.get_latest_csv_path_and_size()
            time.sleep(8)
            _, size_2 = self.get_latest_csv_path_and_size()
            
            if size_1 == size_2 and size_1 >= 0:
                check_cmd = ["nc", "-z", "-w", "2", router_ip, str(airserv_port)]
                status = subprocess.run(check_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                
                if status.returncode == 0:
                    print("\033[93m[*] WARNING - Local Radar Hung. Purging and restarting fresh...\033[0m")
                    self.launch_local_radar(router_ip, airserv_port)
                    return "restarted"
                else:
                    return "router_dead"
            return "stable"
        except Exception as e:
            return "error"

    def terminate_local_radar(self):
        if hasattr(self, 'radar_process') and self.radar_process and self.radar_process.poll() is None:
            try:
                os.killpg(os.path.getpgid(self.radar_process.pid), signal.SIGKILL)
                self.radar_process = None
                return True
            except Exception:
                return False
        return False
