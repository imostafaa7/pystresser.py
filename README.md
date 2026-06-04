<div align="center">

# ⚡ PyStresser

### Professional Server Load Testing Tool

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20Windows%20%7C%20macOS-lightgrey?style=for-the-badge)]()

</div>

---

## 🎯 What is PyStresser?

**PyStresser** is a professional server load testing tool written in Python. It allows you to test your server's ability to handle high concurrent traffic, helping you with:

- ✅ Discovering vulnerabilities before attackers do
- ✅ Improving server performance under pressure
- ✅ Testing firewall capabilities
- ✅ Evaluating horizontal scaling strategies

> ⚠️ **Important Notice:** This tool is designed **only for testing your own servers**. Using it on others' servers without permission is a cybercrime.

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🚀 **4 Attack Types** | HTTP, TCP, UDP, Slowloris |
| 💪 **Multi-threaded** | Thousands of concurrent threads for maximum pressure |
| 🎭 **Fake User-Agent** | Automatic User-Agent rotation to avoid detection |
| 🌐 **Proxy Support** | Use multiple proxies to hide source |
| 📊 **Live Statistics** | Real-time progress and results |
| 📄 **JSON Reports** | Save test results for later analysis |
| 🎨 **Colored Output** | Beautiful colors for easy reading |

---

## 📋 Requirements

| Requirement | Version |
|-------------|---------|
| Python | 3.8 or newer |
| pip | Latest version |
| OS | Linux / Windows / macOS |

---

## 🔧 Installation

### Method 1: Direct Installation

```bash
# 1. Clone the repository
git clone https://github.com/imostafaa7/pystresser.py
cd pystresser.py

# 2. Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Linux/macOS
# OR
venv\Scripts\activate     # On Windows

# 3. Install requirements
pip install -r requirements.txt

# 4. Run the tool
python pystresser.py --help
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
