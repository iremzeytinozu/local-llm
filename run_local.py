#!/usr/bin/env python3
"""
Yerel test için basit başlatma scripti
"""
import subprocess
import sys

if __name__ == "__main__":
    print("🚀 Flask chatbot başlatılıyor...")
    try:
        subprocess.run([sys.executable, "app_flask.py"])
    except KeyboardInterrupt:
        print("\n👋 Chatbot durduruldu!")
