#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import datetime

class Reporter:
    def __init__(self, stats, args):
        self.stats = stats
        self.args = args
        
    def save_report(self, filename="stress_test_report.json"):
        """حفظ التقرير كملف JSON"""
        report = {
            'timestamp': datetime.datetime.now().isoformat(),
            'target': self.args.target,
            'port': self.args.port,
            'attack_type': self.args.method,
            'threads': self.args.threads,
            'duration': self.args.duration,
            'results': {
                'total_requests': self.stats['total_requests'],
                'successful': self.stats['successful'],
                'failed': self.stats['failed'],
                'start_time': self.stats['start_time'].isoformat() if self.stats['start_time'] else None,
                'end_time': self.stats['end_time'].isoformat() if self.stats['end_time'] else None
            }
        }
        
        # حساب نسبة النجاح
        if self.stats['total_requests'] > 0:
            report['results']['success_rate'] = (self.stats['successful'] / self.stats['total_requests']) * 100
            
        # حساب الطلبات في الثانية
        if self.stats['start_time'] and self.stats['end_time']:
            duration = (self.stats['end_time'] - self.stats['start_time']).total_seconds()
            if duration > 0:
                report['results']['requests_per_second'] = self.stats['total_requests'] / duration
                
        with open(filename, 'w') as f:
            json.dump(report, f, indent=4)
            
        return filename
