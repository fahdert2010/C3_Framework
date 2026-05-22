#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ultimate C3 Framework - Hardened Hardware SSH Executor
File: /home/kali/C3_Framework/core/ssh_executor.py
"""

import subprocess
import os
import datetime
import traceback
import shlex

class SSHHardwareExecutor:
    def __init__(self, ip=None, password=None):
        self.ip = ip or os.environ.get("C3_ROUTER_IP", "10.0.4.93")
        self.password = password or os.environ.get("C3_ROUTER_PASS", "root")
        self.log_path = "/home/kali/C3_Framework/storage/logs/attack_errors.log"

    def _trigger_double_guard(self, line_num, reason, stack_trace):
        print(f"\033[91m[!] CRITICAL - Class: SSHHardwareExecutor | Line: {line_num} | Reason: {reason}\033[0m")
        try:
            with open(self.log_path, "a", encoding="utf-8") as log_file:
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                log_file.write(f"[{timestamp}] CRITICAL - Class: SSHHardwareExecutor | Line: {line_num} | Reason: {reason}\n")
                log_file.write(f"Stack Trace:\n{stack_trace}\n{'-'*50}\n")
        except IOError as e:
            print(f"\033[91m[!] FATAL - Log write failed: {str(e)}\033[0m")

    def execute_raw_command(self, command_list, timeout=10):
        if isinstance(command_list, str):
            command_list = shlex.split(command_list)

        full_ssh_cmd = [
            "sshpass", "-p", self.password,
            "ssh", "-o", "StrictHostKeyChecking=no",
            "-o", "ConnectTimeout=5",
            f"root@{self.ip}"
        ] + command_list
        
        try:
            process = subprocess.run(
                full_ssh_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=timeout
            )
            
            if process.returncode != 0 and process.stderr:
                return {"status": "hardware_error", "output": process.stderr.strip()}
                
            return {"status": "success", "output": process.stdout.strip()}
            
        except subprocess.TimeoutExpired as e:
            tb = traceback.extract_tb(e.__traceback__)
            line_num = tb[-1].lineno if tb else "Timeout"
            self._trigger_double_guard(line_num, "Command timeout expired", traceback.format_exc())
            return {"status": "timeout", "output": ""}
        except Exception as e:
            tb = traceback.extract_tb(e.__traceback__)
            line_num = tb[-1].lineno if tb else "Unknown"
            self._trigger_double_guard(line_num, f"Execution crash: {str(e)}", traceback.format_exc())
            return {"status": "failed", "output": ""}
