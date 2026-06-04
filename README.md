             # الإعدادات
<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8%2B-blue">
  <img src="https://img.shields.io/badge/License-MIT-green">
  <img src="https://img.shields.io/badge/Version-1.0.0-red">
</p>

# ⚡ PyStresser

**أداة اختبار تحمل الخوادم (Stress Testing) بلغة Python**

---

## 📋 المتطلبات

```bash
pip install -r requirements.txt
# اختبار HTTP بسيط
python pystresser.py --target http://yourserver.com --threads 100 --duration 30

# اختبار TCP
python pystresser.py --target 192.168.1.100 --port 80 --method tcp --threads 200

# اختبار UDP
python pystresser.py --target 192.168.1.100 --port 53 --method udp --threads 50

# اختبار Slowloris
python pystresser.py --target 192.168.1.100 --port 80 --method slowloris --threads 500

# استخدام بروكسيات
python pystresser.py --target http://yourserver.com --proxies proxies.txt
