#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ultimate C3 Framework - Hardened Central Database Engine (AP Sourced)
File: /home/kali/C3_Framework/core/database.py
"""

import os
import sqlite3
import datetime
import traceback
import re
import base64

class DatabaseManager:
    def __init__(self):
        self.db_path = "/home/kali/C3_Framework/storage/c3_arsenal.db"
        self.log_path = "/home/kali/C3_Framework/storage/logs/attack_errors.log"
        self.aes_key = b"C3_Framework_Hardened_Secret_Key"
        
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        os.makedirs(os.path.dirname(self.log_path), exist_ok=True)
        self.initialize_database()

    def _trigger_double_guard(self, line_num, reason):
        print(f"\033[91m[!] خطأ قاعدة البيانات | السطر: {line_num} | السبب: {reason}\033[0m")
        try:
            with open(self.log_path, "a", encoding="utf-8") as log_file:
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                log_file.write(f"[{timestamp}] CRITICAL - DatabaseManager | Line: {line_num} | Reason: {reason}\n")
        except IOError:
            pass

    def _encrypt_password(self, raw_password):
        try:
            encoded_bytes = raw_password.encode('utf-8')
            cipher_bytes = bytes([b ^ self.aes_key[i % len(self.aes_key)] for i, b in enumerate(encoded_bytes)])
            return base64.b64encode(cipher_bytes).decode('utf-8')
        except Exception:
            return ""

    def _decrypt_password(self, cipher_text):
        try:
            cipher_bytes = base64.b64decode(cipher_text.encode('utf-8'))
            plain_bytes = bytes([b ^ self.aes_key[i % len(self.aes_key)] for i, b in enumerate(cipher_bytes)])
            return plain_bytes.decode('utf-8')
        except Exception:
            return ""

    def initialize_database(self):
        connection = None
        try:
            connection = sqlite3.connect(self.db_path)
            cursor = connection.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS access_points (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ap_name TEXT UNIQUE NOT NULL,
                    ap_ip TEXT UNIQUE NOT NULL,
                    username TEXT NOT NULL,
                    password_encrypted TEXT NOT NULL,
                    group_name TEXT NOT NULL,
                    date_added TEXT NOT NULL
                )
            """)
            connection.commit()
        except sqlite3.Error as e:
            self._trigger_double_guard(58, str(e))
        finally:
            if connection: connection.close()

    def register_access_point(self, name, ip, username, password, group):
        connection = None
        clean_name = re.sub(r'[^\w\s\-\_]', '', name).strip()
        clean_ip = ip.strip()
        clean_user = username.strip() if username.strip() else "root"
        clean_group = re.sub(r'[^\w\s]', '', group).strip()
        enc_pass = self._encrypt_password(password)
        success = False
        
        try:
            connection = sqlite3.connect(self.db_path)
            cursor = connection.cursor()
            date_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute("""
                INSERT INTO access_points (ap_name, ap_ip, username, password_encrypted, group_name, date_added)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (clean_name, clean_ip, clean_user, enc_pass, clean_group, date_now))
            connection.commit()
            success = True
        except sqlite3.IntegrityError:
            print("\033[91m[!] خطأ: الاسم أو عنوان الآي بي مسجل مسبقاً في المنظومة.\033[0m")
        except sqlite3.Error as e:
            self._trigger_double_guard(88, str(e))
        finally:
            if connection: connection.close()
        return success

    def fetch_all_registered_aps(self):
        connection = None
        results = []
        try:
            connection = sqlite3.connect(self.db_path)
            cursor = connection.cursor()
            cursor.execute("SELECT id, ap_name, ap_ip, username, password_encrypted, group_name FROM access_points")
            results = cursor.fetchall()
        except sqlite3.Error as e:
            self._trigger_double_guard(102, str(e))
        finally:
            if connection: connection.close()
        return results

    def fetch_all_groups(self):
        connection = None
        results = []
        try:
            connection = sqlite3.connect(self.db_path)
            cursor = connection.cursor()
            cursor.execute("SELECT DISTINCT group_name FROM access_points")
            results = cursor.fetchall()
        except sqlite3.Error:
            pass
        finally:
            if connection: connection.close()
        return results
