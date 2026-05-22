#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ultimate C3 Framework - Hardened Airserv Server Detector (Concurreny Proof)
File: /home/kali/C3_Framework/security_files/airserv_detector.py
"""

import random
import datetime
import traceback
from core.ssh_executor import SSHHardwareExecutor

class AirservDetector:
    def __init__(self, ssh_executor=None):
        self.executor = ssh_executor if ssh_executor else SSHHardwareExecutor()
        self.log_path = "/home/kali/C3_Framework/storage/logs/attack_errors.log"

    def _trigger_double_guard(self, line_num, reason, stack_trace):
        print(f"\033[91m[!] CRITICAL - Class: AirservDetector | Line: {line_num} | Reason: {reason}\033[0m")
        try:
            with open(self.log_path, "a", encoding="utf-8") as log_file:
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                log_file.write(f"[{timestamp}] CRITICAL - Class: AirservDetector | Line: {line_num} | Reason: {reason}\n")
                log_file.write(f"Stack Trace:\n{stack_trace}\n{'-'*50}\n")
        except IOError as e:
            print(f"\033[91m[!] FATAL - Log write failed: {str(e)}\033[0m")

    def fetch_all_active_ports(self):
        """
        تجميع الفحص الحي: جلب جدول المنافذ بالكامل لمرة واحدة حصرًا لحماية معالج الراوتر من الإغراق
        """
        cmd = ["/bin/sh", "-c", "netstat -an | grep 'LISTEN '"]
        response = self.executor.execute_raw_command(cmd)
        if response["status"] == "success" and response["output"]:
            return response["output"].strip()
        return ""

    def generate_unique_hardware_port(self, frequency_target="2G", channel=6):
        """
        حل مشكلة الخلل في البورت: إنشاء منفذ فريد ومعزول مبني هندسياً على هوية التردد والقناة المستهدفة
        """
        # توليد البورت الأساسي بناءً على مدخلات الأثير لمنع التكرار والتصادم
        base_port = 5000 + int(channel) if frequency_target == "5G" else 2000 + int(channel)
        
        # قراءة المنافذ حياً محلياً في بايثون لمرة واحدة
        active_ports_dump = self.fetch_all_active_ports()
        
        # البحث عن منفذ متاح بإزاحة تصاعدية آمنة دون إرهاق الراوتر بالـ SSH
        chosen_port = base_port
        while f":{chosen_port} " in active_ports_dump:
            chosen_port += 100 # إزاحة البورت في حال التصادم مع هجوم نشط آخر
            if chosen_port > 65535:
                chosen_port = random.randint(1025, 9999)
                break
                
        return chosen_port

    def launch_airserv_daemon(self, actual_mon_name, unique_port):
        """
        إطلاق خادم الـ airserv-ng بشكل صامت ومستقل ومقفل عتادياً على البورت الفرعي المستحدث
        """
        launch_cmd = ["/bin/sh", "-c", f"airserv-ng -p {unique_port} {actual_mon_name} > /dev/null 2>&1 &"]
        response = self.executor.execute_raw_command(launch_cmd)
        return response["status"] == "success"

    def snatch_active_pids_list(self):
        """
        عزل المعالجات: تحويل مخرج pidof إلى مصفوفة صريحة لحل قصور الجلسات المتعددة وبقايا الخوادم المعلقة
        """
        response = self.executor.execute_raw_command(["pidof", "airserv-ng"])
        if response["status"] == "success" and response["output"]:
            # تفكيك السلسلة النصية إلى مصفوفة معالجات معزولة صالحة للاستهداف الفردي اللاحق
            return response["output"].strip().split()
        return []

    def terminate_all_airserv_processes(self):
        """
        التطهير الشامل للذاكرة وإبادة كافة المعرفات دون ترك عمليات زومبي
        """
        kill_cmd = ["/bin/sh", "-c", "killall -9 airserv-ng > /dev/null 2>&1"]
        response = self.executor.execute_raw_command(kill_cmd)
        return response["status"] == "success"
