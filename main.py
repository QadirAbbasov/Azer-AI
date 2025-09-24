import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="pygame.pkgdata")


import sys
import os
import numpy as np
import datetime
import pyttsx3
import speech_recognition as sr
import psutil
import pygame
import tempfile
import asyncio
import threading
import math
import time
import requests
from pydub import AudioSegment
from pydub.playback import play
from gtts import gTTS
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import pyaudio
import edge_tts
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QLabel, QFrame, QLineEdit, QPushButton,
                            QMessageBox, QComboBox, QDialog)
from PyQt6.QtCore import Qt, QTimer, QSize, QPoint, QRect
from PyQt6.QtGui import QFont, QColor, QPainter, QPen, QPixmap, QRadialGradient, QIcon
import random
from db_manager import db_manager
version_data = db_manager.get_version()

# Bu sətir, qt.qpa.window kimi logların göstərilməsini maneə törədir.
os.environ["QT_LOGGING_RULES"] = "*.debug=false;qt.qpa.*=false"

# Modulları daxil et
from login_screen import LoginScreen
from loading_screen import LoadingScreen
from program_exit import ProgramExit
from user_settings import UserSettings
from subscription_manager import SubscriptionManager
from admin_panel import AdminPanel
from commands import Azer_AICommands
from update_checker import check_version
from plugins.plugin_manager import PluginManager

class ModernAzer_AI(QMainWindow):
    def __init__(self):
        # Versiya yoxlaması
        if not check_version():
            return
            
        # TTS və dil parametrləri üçün standart dəyərlər
        self.voice_settings = {
            'tts_engine': 'edge',  # 'edge' və ya 'gtts'
            'language': 'az-AZ',   # 'az-AZ' və ya 'tr-TR'
            'voice_gender': 'male' # 'male' və ya 'female'
        }
        
        # Cavab gözləmə vəziyyəti üçün dəyişən
        self.waiting_for_response = False
        self.text_response = None

        # Wake word parametrləri üçün standart dəyərlər
        self.wake_word_settings = {
            'az_word': 'azər',
            'tr_word': 'azer'
        }
        
        # Voice mapping
        self.voice_options = {
            'az-AZ': {
                'male': 'az-AZ-BabekNeural',
                'female': 'az-AZ-BanuNeural'
            },
            'tr-TR': {
                'male': 'tr-TR-AhmetNeural',
                'female': 'tr-TR-EmelNeural'
            }
        }
        
        # Recognition language mapping
        self.recognition_languages = {
            'az-AZ': 'az-AZ',
            'tr-TR': 'tr-TR'
        }
        
        # Başlangıç dil ayarını yap
        self.recognition_language = self.recognition_languages[self.voice_settings['language']]
        
        # Səs tanıma üçün recognizer'ı başlat
        self.recognizer = sr.Recognizer()
        
        # Əvvəlcə giriş ekranını göstər
        app = QApplication(sys.argv)
        app.setStyle('Fusion')  # Daha müasir görünüş
        login_screen = LoginScreen()
        login_success, user_info = login_screen.run()
        
        # Əgər giriş uğursuzdursa tətbiqi bağla
        if not login_success:
            sys.exit()
            
        # İstifadəçi məlumatlarını saxla
        self.current_user = user_info
        
        # İstifadəçinin səs parametrlərini yüklə
        self.load_voice_settings()
        
        # İstifadəçinin wake word parametrlərini yüklə
        self.load_wake_word_settings()
        
        # Giriş uğurlu olduqda yükləmə ekranını göstər
        loading_screen = LoadingScreen()
        loading_screen.start()
        
        # Əsas tətbiqi başlat
        super().__init__()
        
        # Pəncərə quraşdırmasını et (rənglər lüğəti burada yaradılır)
        self.setup_window()
        
        # Abunəlik idarəçisini başlat (rənglər lüğətinə ehtiyac duyur)
        self.subscription_manager = SubscriptionManager(self)
        
        # İstifadəçi parametrləri idarəçisini başlat
        self.user_settings = UserSettings(self)

        # Proqram çıxış idarəçisini başlat
        self.program_exit = ProgramExit(self, self.colors)
        
        # Qalan mövcud kodlar...
        self.current_speech = ""
        self.speech_fade_time = 0
        self.speech_active = False
        self.speech_animation_index = 0
        self.speech_animation_speed = 2
        self.last_animation_time = 0
        
        self.internet_status = "Yoxlanılır..."
        self.internet_color = self.colors['accent']
        
        self.audio_data = np.zeros(128)
        
        self.initialize_voice()
        self.setup_audio()
        self.setup_audio_visualization()
        
        # İnterfeysi yarad
        self.create_interface()
        
        self.listening = False
        self.wake_word_listening = False
        self.continuous_listening = False
        
        self.start_wake_word_detection()
        
        self.commands = Azer_AICommands(self)
        
        # Xüsusi əmrləri yenilə (başlanğıcda)
        self.refresh_custom_commands()
        
        # Plugin idarəçisini başlat
        self.plugin_manager = PluginManager(self)
        
        # Pro müddətini yoxla
        self.subscription_manager.check_pro_status()
        
        # Admin panel nümunəsini yarad
        if self.current_user['role'] == 'admin':
            self.admin_panel = AdminPanel(self, self.colors)
        
        self.show()
        sys.exit(app.exec())

    def load_custom_commands(self):
        """Xüsusi əmrləri verilənlər bazasından yüklə"""
        try:
            from db_manager import db_manager
            
            # İstifadəçinin xüsusi əmrlərini verilənlər bazasından al
            db_commands = db_manager.get_custom_commands(self.current_user['id'])
            
            if not db_commands:
                return []
                
            # Verilənlər bazası formatını tətbiqə uyğun formata çevir
            commands = []
            for cmd in db_commands:
                # Tətikləyiciləri ayırıb siyahı halına gətir
                triggers_az = cmd['triggers_az'].split(',') if cmd['triggers_az'] else []
                triggers_tr = cmd['triggers_tr'].split(',') if cmd['triggers_tr'] else []
                
                commands.append({
                    'id': cmd['id'],
                    'name': cmd['name'],
                    'action': cmd['action'],
                    'target': cmd['target'],
                    'triggers': {
                        'az-AZ': triggers_az,
                        'tr-TR': triggers_tr
                    }
                })
                
            return commands
        except Exception as e:
            # Dilə görə xəta mesajı
            if hasattr(self, 'voice_settings') and self.voice_settings.get('language') == 'tr-TR':
                self.speak(f"Özel komutlar yüklenirken hata: {e}")
            else:
                self.speak(f"Xüsusi əmrlər yüklənərkən xəta: {e}")
            return []

    def save_custom_commands(self, commands):
        """Xüsusi əmrləri verilənlər bazasına yadda saxla"""
        try:
            from db_manager import db_manager
            
            # Əvvəlcə mövcud əmrləri sil (təmiz başlanğıc üçün)
            existing_commands = db_manager.get_custom_commands(self.current_user['id'])
            for cmd in existing_commands:
                db_manager.delete_custom_command(cmd['id'])
            
            # Yeni əmrləri yadda saxla
            for cmd in commands:
                triggers_az = cmd['triggers'].get('az-AZ', [])
                triggers_tr = cmd['triggers'].get('tr-TR', [])
                
                db_manager.add_custom_command(
                    self.current_user['id'],
                    cmd['name'],
                    cmd['action'],
                    cmd['target'],
                    triggers_az,
                    triggers_tr
                )
            
            # Əmrlər sistemini yenilə
            self.refresh_custom_commands()
            
        except Exception as e:
            # Dilə görə xəta mesajı
            if hasattr(self, 'voice_settings') and self.voice_settings.get('language') == 'tr-TR':
                self.speak("Özel Komutları kaydederken hata oluştu.")
            else:
                self.speak("Xüsusi Əmrləri yadda saxlayarkən xəta baş verdi.")

    def refresh_custom_commands(self):
        """Xüsusi əmrləri yenilə və əmrlər sistemini yenidən yüklə"""
        try:
            # Əmrlər sistemindəki xüsusi əmrləri yenilə
            if hasattr(self, 'commands'):
                old_count = len(self.commands.custom_commands) if self.commands.custom_commands else 0
                self.commands.custom_commands = self.load_custom_commands()
                new_count = len(self.commands.custom_commands) if self.commands.custom_commands else 0
        except Exception as e:
            # Dilə görə xəta mesajı
            if hasattr(self, 'voice_settings') and self.voice_settings.get('language') == 'tr-TR':
                self.speak(f"Özel komutlar yenilenirken hata: {e}")
            else:
                self.speak(f"Xüsusi əmrlər yenilənərkən xəta: {e}")

    def load_voice_settings(self):
        """İstifadəçinin səs parametrlərini yüklə"""
        try:
            # Verilənlər bazasından istifadəçinin səs parametrlərini al
            if 'voice_settings' in self.current_user:
                # İstifadəçi obyekti içindəki parametrləri istifadə et
                self.voice_settings = self.current_user['voice_settings']
            else:
                # Standart parametrləri istifadə et
                # Dilə görə xəta mesajı
                if hasattr(self, 'voice_settings') and self.voice_settings.get('language') == 'tr-TR':
                    self.speak("Standart ses ayarları kullanılıyor.")
                else:
                    self.speak("Standart səs parametrləri istifadə olunur.")
                
            # Səs tanıma dilini yenilə
            self.update_listening_language()
        except Exception as e:
            # Dilə görə xəta mesajı
            if hasattr(self, 'voice_settings') and self.voice_settings.get('language') == 'tr-TR':
                self.speak(f"Ses ayarları yüklenirken hata: {e}")
            else:
                self.speak(f"Səs parametrləri yüklənərkən xəta: {e}")


    def setup_window(self):
        # Əsas pəncərə parametrləri
        self.setWindowTitle("Azer AI Səsli Asistan " + version_data['version'])
        self.setMinimumSize(900, 700)
        self.setWindowIcon(QIcon('images/logo.ico'))
        
        # Müasir qaranlıq tema rəng sxemi - Material Design Dark Theme uyğun
        self.colors = {
            'bg': '#0D1117',  # GitHub Dark tema arxa fon
            'bg_secondary': '#161B22',  # GitHub Dark tema ikinci dərəcəli arxa fon
            'bg_tertiary': '#21262D',  # Üçüncü dərəcəli arxa fon
            'primary': '#58A6FF',  # GitHub Dark tema əsas
            'secondary': '#79C0FF',  # Daha açıq əsas
            'accent': '#1F6FEB',  # GitHub Dark tema vurğu
            'warning': '#D29922',  # GitHub Dark tema xəbərdarlıq
            'error': '#F85149',  # GitHub Dark tema xəta
            'success': '#238636',  # GitHub Dark tema uğur
            'text': '#F0F6FC',  # GitHub Dark tema mətn
            'text_secondary': '#8B949E',  # GitHub Dark tema ikinci dərəcəli mətn
            'text_muted': '#6E7681',  # GitHub Dark tema səssiz mətn
            'border': '#30363D',  # GitHub Dark tema sərhəd
            'border_secondary': '#21262D',  # İkinci dərəcəli sərhəd
            'overlay': '#161B22',  # Overlay rəngi
            'shadow': '#000000'  # Kölgə rəngi
        }
        
        # Pəncərə ölçüləri
        self.width = 900
        self.height = 700

    def initialize_voice(self):
        """Səs tanıma və sintez sistemlərini başlat"""
        # Ehtiyat TTS mühərriki kimi pyttsx3'ü başlat
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)
        voices = self.engine.getProperty('voices')
        
        # Dilə görə pyttsx3 səsini tənzimlə
        if self.voice_settings['language'] == 'tr-TR':
            # Türk dili səsi üçün
            for voice in voices:
                if 'turkish' in voice.name.lower():
                    self.engine.setProperty('voice', voice.id)
                    break
        else:
            # Standart səs
            self.engine.setProperty('voice', voices[0].id)

    def create_interface(self):
        # Əsas widget və layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Arxa fon rəngini tənzimlə
        central_widget.setStyleSheet(f"background-color: {self.colors['bg']};")
        
        # Status bar yuxarıda
        self.create_status_bar(main_layout)
        
        # Holografik dairə üçün əsas canvas
        self.canvas_frame = QFrame()
        self.canvas_frame.setStyleSheet(f"background-color: {self.colors['bg']};")
        main_layout.addWidget(self.canvas_frame, 1)  # 1 stretch factor ilə genişləyə bilər
        
        # Çəkmə üçün canvas label yarad
        self.canvas_label = QLabel(self.canvas_frame)
        self.canvas_label.setGeometry(0, 0, self.width, self.height)
        self.canvas_label.setStyleSheet("background-color: transparent;")
        
        # Daxiletmə çərçivəsini yarad
        self.create_input_frame(main_layout)
        
        # Sistem məlumatı göstəricisini yarad
        self.create_system_info()
        
        # Animasiyaları başlat
        self.animation_timer = QTimer(self)
        self.animation_timer.timeout.connect(self.animate)
        self.animation_timer.start(50)  # 50ms'də bir yenilə
        
        # Əmr siyahısı düyməsini əlavə et
        self.add_command_list_button()
        
        # İstifadəçi parametrləri düyməsi (bütün istifadəçilər üçün)
        settings_btn = QPushButton("⚙️ Parametrlər", self.canvas_frame)
        settings_btn.setGeometry(self.width - 200, 120, 180, 40)  # Admin düyməsinin altına
        settings_btn.setStyleSheet(
            f"""
            QPushButton {{
                background-color: {self.colors['secondary']}; 
                color: white; 
                border: none; 
                border-radius: 20px; 
                font-family: 'Segoe UI', Arial; 
                font-size: 13px; 
                padding: 5px 15px;
            }}
            QPushButton:hover {{
                background-color: {self.colors['primary']}; 
                color: white;
            }}
            """
        )
        settings_btn.clicked.connect(lambda: self.user_settings.show_settings())

    def create_status_bar(self, main_layout):
        # Status bar konteyner - daha müasir görünüş
        status_bar = QFrame()
        status_bar.setFixedHeight(50)  # Bir az daha yüksək
        status_bar.setStyleSheet(
            f"background-color: {self.colors['bg_secondary']}; "
            f"border-bottom: 1px solid {self.colors['border']};"
        )
        
        status_layout = QHBoxLayout(status_bar)
        status_layout.setContentsMargins(15, 0, 15, 0)
        status_layout.setSpacing(15)  # Daha çox boşluq
        
        # Logo/Ad etiketi
        logo_label = QLabel("Azer AI")
        logo_label.setStyleSheet(
            f"color: {self.colors['text']}; font-weight: bold; font-size: 16px; "
            f"font-family: 'Segoe UI', Arial;"
        )
        status_layout.addWidget(logo_label)
        
        # Dinləmə vəziyyəti - daha müasir görünüş
        self.listening_label = QLabel("🎤 Sizi Dinləyirəm...")
        self.listening_label.setStyleSheet(
            f"color: {self.colors['text']}; font-weight: bold; "
            f"background-color: {self.colors['bg_tertiary']}; padding: 5px 15px; border-radius: 15px;"
            f"font-family: 'Segoe UI', Arial;"
        )
        status_layout.addWidget(self.listening_label)
        
        # Wake word toggle düyməsini əlavə et
        self.wake_word_toggle = QPushButton("🎧 Wake Word Aktiv")
        self.wake_word_toggle.setStyleSheet(
            f"""
            QPushButton {{
                background-color: {self.colors['accent']}; 
                color: white; 
                border: none; 
                padding: 5px 15px; 
                border-radius: 15px; 
                font-family: 'Segoe UI', Arial;
            }}
            QPushButton:hover {{
                background-color: {self.colors['primary']};
            }}
            """
        )
        self.wake_word_toggle.clicked.connect(self.toggle_wake_word)
        status_layout.addWidget(self.wake_word_toggle)
        
        # Boşluq əlavə et
        status_layout.addStretch(1)
        
        # İstifadəçi məlumatı (sağda) - daha müasir görünüş
        self.user_label = QLabel(f"👤 {self.current_user['name']}")
        self.user_label.setStyleSheet(
            f"color: {self.colors['text']}; font-weight: bold; "
            f"background-color: {self.colors['bg_tertiary']}; padding: 5px 15px; border-radius: 15px;"
            f"font-family: 'Segoe UI', Arial;"
        )
        status_layout.addWidget(self.user_label)
        
        # Çıxış düyməsi
        logout_btn = QPushButton("🚪 Çıxış")
        logout_btn.setStyleSheet(
            f"""
            QPushButton {{
                background-color: {self.colors['error']}; 
                color: white; 
                border: none; 
                padding: 5px 15px; 
                border-radius: 15px; 
                font-family: 'Segoe UI', Arial;
                font-size: 12px;
            }}
            QPushButton:hover {{
                background-color: #D32F2F;
            }}
            """
        )
        logout_btn.clicked.connect(self.logout)
        status_layout.addWidget(logout_btn)
        
        # Saat məlumatı (ən sağda) - daha müasir görünüş
        self.time_label = QLabel("00:00:00")
        self.time_label.setStyleSheet(
            f"color: {self.colors['text']}; "
            f"background-color: {self.colors['bg_tertiary']}; padding: 5px 15px; border-radius: 15px;"
            f"font-family: 'Segoe UI', Arial;"
        )
        status_layout.addWidget(self.time_label)
        
        # Saat yeniləyicisi
        self.time_timer = QTimer(self)
        self.time_timer.timeout.connect(self.update_time)
        self.time_timer.start(1000)  # Hər saniyə yenilə
        
        main_layout.addWidget(status_bar)

    def create_input_frame(self, main_layout):
        # Daxiletmə çərçivəsi konteyner
        input_frame = QFrame()
        input_frame.setFixedHeight(70)  # Bir az daha yüksək
        input_frame.setStyleSheet(f"background-color: {self.colors['bg_secondary']}; border-top: 1px solid {self.colors['border']};")
        
        input_layout = QHBoxLayout(input_frame)
        input_layout.setContentsMargins(20, 15, 20, 15)
        input_layout.setSpacing(15)  # Daha çox boşluq
        
        # Mətn daxiletməsi - daha müasir görünüş və hover/focus effektləri
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Mənə bir şey de...")
        self.input_field.setStyleSheet(
            f"""
            QLineEdit {{
                background-color: {self.colors['bg_tertiary']}; 
                color: {self.colors['text']}; 
                border: 1px solid {self.colors['border']}; 
                border-radius: 10px; 
                padding: 8px 20px; 
                font-size: 14px; 
                font-family: 'Segoe UI', Arial;
            }}
            QLineEdit:hover {{
                border: 1px solid {self.colors['primary']};
                background-color: {self.colors['bg_secondary']};
            }}
            QLineEdit:focus {{
                border: 2px solid {self.colors['accent']};
                background-color: {self.colors['bg_secondary']};
            }}
            """
        )
        self.input_field.returnPressed.connect(self.process_text_input)
        input_layout.addWidget(self.input_field)
        
        # Davamlı dinləmə düyməsi - daha müasir görünüş və hover effekti
        self.continuous_listen_button = QPushButton("🎧")
        self.continuous_listen_button.setFixedSize(46, 46)
        self.continuous_listen_button.setStyleSheet(
            f"""
            QPushButton {{
                background-color: {self.colors['secondary']}; 
                color: white; 
                border: none; 
                border-radius: 23px; 
                font-size: 18px;
            }}
            QPushButton:hover {{
                background-color: {self.colors['primary']};
                font-size: 20px;
            }}
            QPushButton:pressed {{
                background-color: {self.colors['accent']};
            }}
            """
        )
        self.continuous_listen_button.clicked.connect(self.toggle_continuous_listening)
        input_layout.addWidget(self.continuous_listen_button)
        
        # Mikrofon düyməsi - daha müasir görünüş və hover effekti
        self.mic_button = QPushButton("🎤")
        self.mic_button.setFixedSize(46, 46)
        self.mic_button.setStyleSheet(
            f"""
            QPushButton {{
                background-color: {self.colors['primary']}; 
                color: white; 
                border: none; 
                border-radius: 23px; 
                font-size: 18px;
            }}
            QPushButton:hover {{
                background-color: {self.colors['accent']};
                font-size: 20px;
            }}
            QPushButton:pressed {{
                background-color: {self.colors['error']};
            }}
            """
        )
        self.mic_button.clicked.connect(self.toggle_listening)
        input_layout.addWidget(self.mic_button)
        
        # Göndər düyməsi - daha müasir görünüş və hover effekti
        self.send_button = QPushButton("📤")
        self.send_button.setFixedSize(46, 46)
        self.send_button.setStyleSheet(
            f"""
            QPushButton {{
                background-color: {self.colors['primary']}; 
                color: white; 
                border: none; 
                border-radius: 23px; 
                font-size: 18px;
            }}
            QPushButton:hover {{
                background-color: {self.colors['accent']};
                font-size: 20px;
            }}
            QPushButton:pressed {{
                background-color: {self.colors['success']};
            }}
            """
        )
        self.send_button.clicked.connect(self.process_text_input)
        input_layout.addWidget(self.send_button)
        
        main_layout.addWidget(input_frame)

    def create_system_info(self):
        # Sistem məlumatı konteyner - Qaranlıq tema uyğun müasir görünüş
        system_frame = QFrame(self.canvas_frame)
        system_frame.setGeometry(20, 20, 250, 180)  # Bir az daha böyük
        system_frame.setStyleSheet(
            f"background-color: {self.colors['bg_secondary']}; border-radius: 10px; "
            f"border: 1px solid {self.colors['border']};"
        )
        
        system_layout = QVBoxLayout(system_frame)
        system_layout.setContentsMargins(15, 15, 15, 15)
        system_layout.setSpacing(7)
        
        # Başlıq
        title_label = QLabel("Sistem Vəziyyəti")
        title_label.setStyleSheet(
            f"color: {self.colors['text']}; font-weight: bold; font-size: 14px; "
            f"border-bottom: 1px solid rgba(255, 255, 255, 0.1); padding-bottom: 5px;"
            f"font-family: 'Segoe UI', Arial;"
        )
        system_layout.addWidget(title_label)
        
        # CPU istifadəsi - daha müasir görünüş
        cpu_layout = QHBoxLayout()
        cpu_label = QLabel("CPU:")
        cpu_label.setStyleSheet(f"color: {self.colors['text']}; font-family: 'Segoe UI', Arial;")
        cpu_layout.addWidget(cpu_label)
        
        # CPU progress bar konteyner
        self.cpu_bar_container = QFrame()
        self.cpu_bar_container.setFixedHeight(6)
        self.cpu_bar_container.setStyleSheet(f"background-color: {self.colors['bg_tertiary']}; border-radius: 3px;")
        
        # CPU progress bar
        self.cpu_progress = QFrame(self.cpu_bar_container)
        self.cpu_progress.setFixedHeight(6)
        self.cpu_progress.setStyleSheet(f"background-color: {self.colors['primary']}; border-radius: 3px;")
        
        cpu_layout.addWidget(self.cpu_bar_container, 1)
        
        self.cpu_value = QLabel("0%")
        self.cpu_value.setStyleSheet(f"color: {self.colors['text']}; font-family: 'Segoe UI', Arial;")
        cpu_layout.addWidget(self.cpu_value)
        
        system_layout.addLayout(cpu_layout)
        
        # RAM istifadəsi - daha müasir görünüş
        ram_layout = QHBoxLayout()
        ram_label = QLabel("RAM:")
        ram_label.setStyleSheet(f"color: {self.colors['text']}; font-family: 'Segoe UI', Arial;")
        ram_layout.addWidget(ram_label)
        
        # RAM progress bar konteyner
        self.ram_bar_container = QFrame()
        self.ram_bar_container.setFixedHeight(6)
        self.ram_bar_container.setStyleSheet(f"background-color: {self.colors['bg_tertiary']}; border-radius: 3px;")
        
        # RAM progress bar
        self.ram_progress = QFrame(self.ram_bar_container)
        self.ram_progress.setGeometry(0, 0, 0, 6)  # Başlanğıcda 0 genişlik
        self.ram_progress.setStyleSheet(f"background-color: {self.colors['secondary']}; border-radius: 3px;")
        
        ram_layout.addWidget(self.ram_bar_container, 1)
        
        self.ram_value = QLabel("0%")
        self.ram_value.setStyleSheet(f"color: {self.colors['text']}; font-family: 'Segoe UI', Arial;")
        ram_layout.addWidget(self.ram_value)
        
        system_layout.addLayout(ram_layout)
        
        # Batareya vəziyyəti - daha müasir görünüş
        battery_layout = QHBoxLayout()
        battery_label = QLabel("BATAREYA:")
        battery_label.setStyleSheet(f"color: {self.colors['text']}; font-family: 'Segoe UI', Arial;")
        battery_layout.addWidget(battery_label)
        
        # Battery progress bar konteyner
        self.battery_bar_container = QFrame()
        self.battery_bar_container.setFixedHeight(6)
        self.battery_bar_container.setStyleSheet(f"background-color: {self.colors['bg_tertiary']}; border-radius: 3px;")
        
        # Battery progress bar
        self.battery_progress = QFrame(self.battery_bar_container)
        self.battery_progress.setGeometry(0, 0, 0, 6)  # Başlanğıcda 0 genişlik
        self.battery_progress.setStyleSheet(f"background-color: {self.colors['accent']}; border-radius: 3px;")
        
        battery_layout.addWidget(self.battery_bar_container, 1)
        
        self.battery_value = QLabel("0%")
        self.battery_value.setStyleSheet(f"color: {self.colors['text']}; font-family: 'Segoe UI', Arial;")
        battery_layout.addWidget(self.battery_value)
        
        system_layout.addLayout(battery_layout)
        
        # İnternet vəziyyəti - daha müasir görünüş
        internet_layout = QHBoxLayout()
        internet_label = QLabel("İNTERNET:")
        internet_label.setStyleSheet(f"color: {self.colors['text']}; font-family: 'Segoe UI', Arial;")
        internet_layout.addWidget(internet_label)
        
        self.internet_status_label = QLabel("Bağlı")
        self.internet_status_label.setStyleSheet(
            f"color: {self.colors['accent']}; font-family: 'Segoe UI', Arial;"
        )
        internet_layout.addWidget(self.internet_status_label, 1, Qt.AlignmentFlag.AlignRight)
        
        system_layout.addLayout(internet_layout)
        
        # IP ünvanı - daha müasir görünüş
        ip_layout = QHBoxLayout()
        ip_label = QLabel("IP:")
        ip_label.setStyleSheet(f"color: {self.colors['text']}; font-family: 'Segoe UI', Arial;")
        ip_layout.addWidget(ip_label)
        
        self.ip_value = QLabel("0.0.0.0")
        self.ip_value.setStyleSheet(f"color: {self.colors['text']}; font-family: 'Segoe UI', Arial;")
        ip_layout.addWidget(self.ip_value, 1, Qt.AlignmentFlag.AlignRight)
        
        system_layout.addLayout(ip_layout)
        
        # Sistem məlumatlarını yeniləmə zamanlayıcısı
        self.system_timer = QTimer(self)
        self.system_timer.timeout.connect(self.update_system_info)
        self.system_timer.start(2000)  # 2 saniyədə bir yenilə

    def add_command_list_button(self):
        # Əmr siyahısı düyməsi (sağ yuxarı künc) - daha müasir görünüş və hover effekti
        command_list_btn = QPushButton("📋 Əmrlər Siyahısı", self.canvas_frame)
        command_list_btn.setGeometry(self.width - 200, 20, 180, 40)
        command_list_btn.setStyleSheet(
            f"""
            QPushButton {{
                background-color: {self.colors['primary']}; 
                color: white; 
                border: none; 
                border-radius: 20px; 
                font-family: 'Segoe UI', Arial; 
                font-size: 13px; 
                padding: 5px 15px;
            }}
            QPushButton:hover {{
                background-color: {self.colors['accent']};
                font-size: 14px;
            }}
            QPushButton:pressed {{
                background-color: {self.colors['secondary']};
            }}
            """
        )
        command_list_btn.clicked.connect(self.subscription_manager.show_command_list)
        
        # Admin panel düyməsi (yalnız admin istifadəçilər üçün) - daha müasir görünüş və hover effekti
        if self.current_user['role'] == 'admin':
            admin_btn = QPushButton("👑 Admin Panel", self.canvas_frame)
            admin_btn.setGeometry(self.width - 200, 70, 180, 40)  # Əmr siyahısı düyməsinin altına
            admin_btn.setStyleSheet(
                f"""
                QPushButton {{
                    background-color: {self.colors['warning']}; 
                    color: white; 
                    border: none; 
                    border-radius: 20px; 
                    font-family: 'Segoe UI', Arial; 
                    font-size: 13px; 
                    padding: 5px 15px;
                }}
                QPushButton:hover {{
                    background-color: #FFA000;
                    font-size: 14px;
                }}
                QPushButton:pressed {{
                    background-color: #FF8F00;
                }}
                """
            )
            
            def show_admin_panel():
                # Admin panel'i birbaşa yarad, əlavə dialog yaratma
                self.admin_panel.create_admin_panel()
            
            admin_btn.clicked.connect(show_admin_panel)
        
        # İstifadəçi parametrləri düyməsi (bütün istifadəçilər üçün) - daha müasir görünüş və hover effekti
        settings_btn = QPushButton("⚙️ Parametrlər", self.canvas_frame)
        settings_btn.setGeometry(self.width - 200, 120, 180, 40)  # Admin düyməsinin altına
        settings_btn.setStyleSheet(
            f"""
            QPushButton {{
                background-color: {self.colors['secondary']}; 
                color: white; 
                border: none; 
                border-radius: 20px; 
                font-family: 'Segoe UI', Arial; 
                font-size: 13px; 
                padding: 5px 15px;
            }}
            QPushButton:hover {{
                background-color: {self.colors['primary']};
                font-size: 14px;
            }}
            QPushButton:pressed {{
                background-color: {self.colors['accent']};
            }}
            """
        )
        settings_btn.clicked.connect(lambda: self.user_settings.show_settings())

    def update_time(self):
        current_time = datetime.datetime.now()
        
        # Yalnız rəqəmlərlə tarix formatı
        time_str = current_time.strftime("%H:%M:%S")
        date_str = current_time.strftime("%d.%m.%Y")
        
        # Etiketi yenilə
        self.time_label.setText(f"🕒 {time_str} | 📅 {date_str}")

    def update_system_info(self):
        try:
            cpu_percent = psutil.cpu_percent()
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            
            # CPU vəziyyətini müəyyən et
            cpu_status = "Normal" if cpu_percent <= 60 else "Yüksək" if cpu_percent <= 80 else "Kritik"
            cpu_status_color = (
                self.colors['accent'] if cpu_percent <= 60 
                else self.colors['warning'] if cpu_percent <= 80 
                else self.colors['error']
            )
            
            # RAM vəziyyətini müəyyən et
            ram_status = "Normal" if memory_percent <= 60 else "Yüksək" if memory_percent <= 80 else "Kritik"
            ram_status_color = (
                self.colors['accent'] if memory_percent <= 60 
                else self.colors['warning'] if memory_percent <= 80 
                else self.colors['error']
            )
            
            # Konteyner genişliyini al
            container_width = self.cpu_bar_container.width()
            
            # CPU yeniləməsi
            self.cpu_value.setText(f"{cpu_percent:.1f}% ({cpu_status})")
            self.cpu_value.setStyleSheet(f"color: {cpu_status_color};")
            
            # CPU progress bar yeniləməsi
            progress_width = int(container_width * cpu_percent / 100)
            self.cpu_progress.setGeometry(0, 0, progress_width, self.cpu_progress.height())
            
            # RAM yeniləməsi
            used_ram = memory.used / (1024 * 1024 * 1024)  # GB ilə
            total_ram = memory.total / (1024 * 1024 * 1024)  # GB ilə
            self.ram_value.setText(f"{memory_percent:.1f}% ({ram_status})")
            self.ram_value.setStyleSheet(f"color: {ram_status_color};")
            
            # RAM progress bar yeniləməsi
            ram_width = int(container_width * memory_percent / 100)
            self.ram_progress.setGeometry(0, 0, ram_width, self.ram_progress.height())
            
            # CPU and RAM colors
            if cpu_percent > 80:
                self.cpu_progress.setStyleSheet(f"background-color: {self.colors['error']}; border-radius: 3px;")
            elif cpu_percent > 60:
                self.cpu_progress.setStyleSheet(f"background-color: {self.colors['warning']}; border-radius: 3px;")
            else:
                self.cpu_progress.setStyleSheet(f"background-color: {self.colors['primary']}; border-radius: 3px;")
            
            if memory_percent > 80:
                self.ram_progress.setStyleSheet(f"background-color: {self.colors['error']}; border-radius: 3px;")
            elif memory_percent > 60:
                self.ram_progress.setStyleSheet(f"background-color: {self.colors['warning']}; border-radius: 3px;")
            else:
                self.ram_progress.setStyleSheet(f"background-color: {self.colors['secondary']}; border-radius: 3px;")
            
            # Batareya vəziyyəti yeniləməsi
            try:
                battery = psutil.sensors_battery()
                if battery:
                    percent = battery.percent
                    power_plugged = battery.power_plugged
                    
                    # Batareya progress bar yeniləməsi
                    container_width = self.battery_bar_container.width()
                    battery_width = int(container_width * percent / 100)
                    self.battery_progress.setGeometry(0, 0, battery_width, self.battery_progress.height())
                    
                    # Batareya vəziyyəti simgesi
                    if power_plugged:
                        status_icon = "⚡"  # Yüklənir
                    elif percent <= 20:
                        status_icon = "🔋"  # Aşağı batareya
                    else:
                        status_icon = "🔌"  # Normal
                    
                    self.battery_value.setText(f"{percent}% {status_icon}")
                    
                    # Batareya rəngi yeniləməsi
                    if percent <= 20:
                        self.battery_progress.setStyleSheet(f"background-color: {self.colors['error']}; border-radius: 3px;")
                    elif percent <= 50:
                        self.battery_progress.setStyleSheet(f"background-color: {self.colors['warning']}; border-radius: 3px;")
                    else:
                        self.battery_progress.setStyleSheet(f"background-color: {self.colors['accent']}; border-radius: 3px;")
                else:
                    # Batareya məlumatı alına bilmədikdə
                    self.battery_value.setText("N/A")
                    self.battery_progress.setGeometry(0, 0, 0, self.battery_progress.height())
            except Exception as e:
                # Dilə görə xəta mesajı
                if hasattr(self, 'voice_settings') and self.voice_settings.get('language') == 'tr-TR':
                    self.speak(f"Pil bilgisi alınamadı: {e}")
                else:
                    self.speak(f"Batareya məlumatı alına bilmədi: {e}")
                self.battery_value.setText("N/A")
                self.battery_progress.setGeometry(0, 0, 0, self.battery_progress.height())
            
            # İnternet yoxlamasını daha az tez-tez edək (hər 10 saniyədə bir)
            current_time = time.time()
            if not hasattr(self, 'last_internet_check') or current_time - self.last_internet_check >= 10:
                threading.Thread(target=self.check_internet, daemon=True).start()
                self.last_internet_check = current_time
            
            # İnternet vəziyyətini yenilə
            self.internet_status_label.setText(self.internet_status)
            self.internet_status_label.setStyleSheet(f"color: {self.internet_color};")
            
        except Exception as e:
            # Dilə görə xəta mesajı
            if hasattr(self, 'voice_settings') and self.voice_settings.get('language') == 'tr-TR':
                self.speak(f"Sistem bilgisi güncellenirken hata oluştu: {e}")
            else:
                self.speak(f"Sistem məlumatı yenilənərkən xəta baş verdi: {e}")
        finally:
            # Hər halda yeniləməyə davam et
            self.system_timer.start(2000)  # 2 saniyədə bir yenilə

    def animate(self):
        # Mərkəzi hesabla
        canvas_width = self.canvas_frame.width()
        canvas_height = self.canvas_frame.height()
        cx = canvas_width / 2
        cy = canvas_height / 2
        
        # Vizualizasiya üçün radius
        radius = min(cx, cy) * 0.4  # Canvas'ın 40%-i radius üçün
        
        # Çəkmə üçün pixmap yarad
        pixmap = QPixmap(canvas_width, canvas_height)
        pixmap.fill(Qt.GlobalColor.transparent)  # Şəffaf arxa fon istifadə et
        
        # Pixmap üçün rəssam yarad
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Arxa fon effekti (seçimli)
        self.draw_background_effect(painter, canvas_width, canvas_height)
        
        # Vizualizasiya elementlərini çək
        self.draw_circle(painter, cx, cy, radius)
        self.draw_audio_waves(painter, cx, cy, radius)
        self.draw_particles(painter, cx, cy, radius)
        self.draw_wave(painter, cx, cy, radius)
        self.draw_speech(painter, cx, cy, radius)
        
        painter.end()
        
        # Pixmap'i canvas_frame'dəki label'ın arxa fonu kimi təyin et
        self.canvas_label.setGeometry(0, 0, canvas_width, canvas_height)
        self.canvas_label.setPixmap(pixmap)

    def draw_background_effect(self, painter, width, height):
        """Arxa fon üçün yüngül effekt çək - Qaranlıq tema uyğun"""
        # Gradient arxa fon - GitHub Dark tema rəngləri
        gradient = QRadialGradient(width/2, height/2, height)
        gradient.setColorAt(0, QColor(13, 17, 23))  # GitHub Dark tema mərkəz
        gradient.setColorAt(1, QColor(10, 13, 18))  # GitHub Dark tema kənar
        
        painter.setBrush(gradient)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRect(0, 0, width, height)
        
        # Arxa fonda yüngül şəbəkə xətləri - Qaranlıq tema uyğun
        painter.setPen(QPen(QColor(48, 54, 61, 20), 1))  # GitHub Dark tema border rəngi, çox yüngül
        
        # Üfüqi xətlər
        step = 40
        for y in range(0, height, step):
            painter.drawLine(0, y, width, y)
            
        # Şaquli xətlər
        for x in range(0, width, step):
            painter.drawLine(x, 0, x, height)

    def draw_audio_waves(self, painter, cx, cy, radius):
        """Səs vizualizasiya dalğalarını çək"""
        num_points = len(self.audio_data)
        angle_step = 360 / num_points
        
        # Daxili və xarici radius
        inner_radius = radius * 0.6
        outer_radius = radius * 0.9
        
        # Səs dalğalarını daha estetik göstər
        for i in range(num_points):
            # Bucağı hesabla
            angle = math.radians(i * angle_step)
            
            # Səs məlumatını normallaşdır (0-1 diapazonuna)
            amplitude = self.audio_data[i] * 5  # Vizual effekt üçün vur
            
            # Daha yumşaq dalğalar üçün sinus funksiyası əlavə et
            smooth_factor = math.sin(i * 0.2 + time.time() * 2) * 0.2
            amplitude = max(0, amplitude + smooth_factor)
            
            # Daxili və xarici nöqtələri hesabla
            r1 = inner_radius + (amplitude * 20)  # Daxili radius + səs amplitudu
            r2 = outer_radius + (amplitude * 20)  # Xarici radius + səs amplitudu
            
            # Nöqtə koordinatlarını hesabla
            x1 = cx + math.cos(angle) * r1
            y1 = cy + math.sin(angle) * r1
            x2 = cx + math.cos(angle) * r2
            y2 = cy + math.sin(angle) * r2
            
            # Xətt rəngini amplituda əsasında gradient ilə təyin et
            intensity = min(255, int(amplitude * 255))
            
            # Gradient rəng (daha canlı)
            if amplitude > 0.5:  # Yüksək amplitud
                color = QColor(self.colors['accent'])
            elif amplitude > 0.2:  # Orta amplitud
                color = QColor(self.colors['primary'])
            else:  # Aşağı amplitud
                color = QColor(self.colors['secondary'])
                
            # Xətt qalınlığını amplituda görə tənzimlə
            line_width = 1 + amplitude * 3
                
            # Xətti çək
            pen = QPen(color, line_width)
            painter.setPen(pen)
            painter.drawLine(int(x1), int(y1), int(x2), int(y2))

    def draw_circle(self, painter, cx, cy, radius):
        """Parıltı effekti ilə əsas dairəni çəkin"""
        # Fon halqası (daha aydın parıltı effekti)
        for i in range(5):
            glow_radius = radius + i * 3
            alpha = 150 - i * 30  # Xaricə doğru qeyri-şəffaflıq azalır
            glow_color = QColor(self.colors['primary'])
            glow_color.setAlpha(alpha)
            pen = QPen(glow_color, 2 - i * 0.3)
            painter.setPen(pen)
            painter.drawEllipse(
                int(cx - glow_radius), 
                int(cy - glow_radius),
                int(glow_radius * 2), 
                int(glow_radius * 2)
            )
        
        # Daxili halqa (daha parlaq və dinamik)
        base_inner_radius = radius * 0.8
        amplitude_sum = np.mean(self.audio_data) * 50
        inner_radius = base_inner_radius + amplitude_sum
        
        # Qradiyent doldurma əlavə edin
        gradient = QRadialGradient(cx, cy, inner_radius)
        primary_color = QColor(self.colors['primary'])
        secondary_color = QColor(self.colors['secondary'])
        
        gradient.setColorAt(0, QColor(255, 255, 255, 30))  # Mərkəz daha parlaqdır
        gradient.setColorAt(0.5, primary_color)
        gradient.setColorAt(1, secondary_color)
        
        painter.setBrush(gradient)
        painter.setPen(QPen(QColor(self.colors['secondary']), 1))
        painter.drawEllipse(
            int(cx - inner_radius),
            int(cy - inner_radius),
            int(inner_radius * 2),
            int(inner_radius * 2)
        )
        
        # Lisenziya vəziyyəti (daha müasir görünüş)
        license_text = "PRO" if self.current_user['license_status'] == 'pro' else "FREE"
        
        if license_text == "PRO":
            # PRO üçün xüsusi effekt
            text_color = QColor(self.colors['accent'])
            bg_color = QColor(0, 0, 0, 100)
            
            # Arxa fon düzbucaqlısı
            bg_rect = QRect(int(cx - 50), int(cy - 20), 100, 40)
            painter.setBrush(bg_color)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRoundedRect(bg_rect, 20, 20)
            
            # Parlaq kənar
            glow_pen = QPen(text_color, 2)
            painter.setPen(glow_pen)
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawRoundedRect(bg_rect, 20, 20)
        else:
            # FREE üçün daha sadə görünüş
            text_color = QColor(self.colors['text_secondary'])
        
        font = QFont('Segoe UI', 24, QFont.Weight.Bold)
        painter.setFont(font)
        painter.setPen(text_color)
        painter.drawText(
            int(cx - 50), int(cy - 15),
            100, 30,
            Qt.AlignmentFlag.AlignCenter,
            license_text
        )
        
    def draw_particles(self, painter, cx, cy, radius):
        """Dairə ətrafında cizgi hissəcikləri çəkin"""
        t = time.time()
        audio_boost = np.mean(self.audio_data) * 30  # Səs səviyyəsinə əsaslanan hissəcik ölçüsü
        
        # Daha çox hissəciklər və daha təkmil effektlər
        for i in range(80):  # Hissəciklərin sayını artırın
            # Fərqli sürətlə fırlanan hissəciklər
            speed_factor = 0.5 + (i % 3) * 0.2
            angle = (t * speed_factor + i * (360/80)) * math.pi / 180
            
            # Fərqli orbitlərdə hərəkət edən hissəciklər
            orbit_variation = math.sin(i * 0.1 + t) * 0.1
            r = radius * (0.8 + orbit_variation + math.sin(t * 2 + i) * 0.1)
            
            x = cx + math.cos(angle) * r
            y = cy + math.sin(angle) * r
            
            # Parçacık ölçüsü səs səviyyəsinə və zamana görə dəyişsin
            size = 1.5 + math.sin(t * 3 + i) * 1 + audio_boost * 0.05
            
            # Parçacık rəngi və parlaqlığı
            hue = (i * 3 + t * 20) % 360  # Rəng döngüsü
            
            # Səs səviyyəsinə görə parlaqlıq
            if audio_boost > 10:
                # Yüksək səs səviyyəsində parlaq rənglər
                color = QColor(self.colors['accent'])
            elif audio_boost > 5:
                # Orta səs səviyyəsində normal rənglər
                color = QColor(self.colors['primary'])
            else:
                # Aşağı səs səviyyəsində solğun rənglər
                color = QColor(self.colors['secondary'])
            
            # Parçacık çizimi
            painter.setPen(QPen(color, 1))
            painter.setBrush(color)
            
            # Farklı parçacık şekilleri
            if i % 3 == 0:  # Yuvarlak parçacıklar
                painter.drawEllipse(
                    int(x - size), 
                    int(y - size),
                    int(size * 2), 
                    int(size * 2)
                )
            elif i % 3 == 1:  # Kare parçacıklar
                painter.drawRect(
                    int(x - size), 
                    int(y - size),
                    int(size * 2), 
                    int(size * 2)
                )
            else:  # Ulduz hissəcikləri (sadələşdirilmiş)
                points = []
                for j in range(4):
                    star_angle = j * math.pi / 2 + t
                    points.append(QPoint(int(x + math.cos(star_angle) * size * 1.5), 
                                         int(y + math.sin(star_angle) * size * 1.5)))
                painter.drawPolygon(points)

    def draw_wave(self, painter, cx, cy, radius):
        """Dairə ətrafında cizgi dalğası çəkin"""
        t = time.time()
        segments = 150  # Daha çox seqmentli daha hamar dalğalar
        wave_radius = radius * 1.2
        audio_amplitude = np.mean(self.audio_data) * 50  # Səs səviyyəsinə əsaslanan dalğa ölçüsü
        
        # Dalğa rəngi üçün gradient yaradın
        gradient = QRadialGradient(cx, cy, wave_radius * 1.5)
        gradient.setColorAt(0, QColor(self.colors['primary']))
        gradient.setColorAt(0.5, QColor(self.colors['accent']))
        gradient.setColorAt(1, QColor(self.colors['secondary']))
        
        # Dalğa qalınlığı səs səviyyəsinə görə dəyişsin
        wave_thickness = 2 + audio_amplitude * 0.05
        
        # Poliline nöqtələri yaradın
        points = []
        
        for i in range(segments + 1):
            angle = (i * (360/segments)) * math.pi / 180
            
            # Daha mürəkkəb dalğa forması
            wave_factor = math.sin(angle * 8 + t * 5) * (10 + audio_amplitude)
            wave_factor += math.sin(angle * 12 + t * 3) * (5 + audio_amplitude * 0.5)
            wave_factor += math.cos(angle * 6 - t * 4) * (8 + audio_amplitude * 0.3)
            
            r = wave_radius + wave_factor
            x = cx + math.cos(angle) * r
            y = cy + math.sin(angle) * r
            points.append(QPoint(int(x), int(y)))
            
        # Dalğa xəttini çəkin
        pen = QPen(gradient, wave_thickness)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(pen)
        painter.drawPolyline(points)
        
        # İkinci dalğa (daha kiçik və fərqli sürət)
        points2 = []
        wave_radius2 = wave_radius * 0.9
        
        for i in range(segments + 1):
            angle = (i * (360/segments)) * math.pi / 180
            
            # Fərqli dalğa forması
            wave_factor = math.sin(angle * 6 - t * 3) * (5 + audio_amplitude * 0.7)
            wave_factor += math.cos(angle * 10 + t * 2) * (3 + audio_amplitude * 0.4)
            
            r = wave_radius2 + wave_factor
            x = cx + math.cos(angle) * r
            y = cy + math.sin(angle) * r
            points2.append(QPoint(int(x), int(y)))
            
        # İkinci dalğa xəttini çəkin
        pen2 = QPen(QColor(self.colors['accent']), wave_thickness * 0.7)
        pen2.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(pen2)
        painter.drawPolyline(points2)

    def draw_speech(self, painter, cx, cy, radius):
        """Animasiya ilə köməkçi nitqini çəkin"""
        if not hasattr(self, 'current_speech') or not self.current_speech:
            return
            
        if self.speech_active or time.time() < self.speech_fade_time:
            # Nitq aktivdirsə və ya sönmə vaxtı keçməyibsə
            opacity = 255
            if not self.speech_active:  # Nitq bitibsə, solğun effekti tətbiq edin
                remaining_time = self.speech_fade_time - time.time()
                opacity = int(min(255, remaining_time * 255))
            
            text_color = QColor(opacity, opacity, opacity)
            
            # Mətni dairənin altına yerləşdirin
            x_pos = cx  # Kətan mərkəzi
            y_pos = cy + radius * 1.2  # Dairənin altında
            
            # Animasiya üçün mətn uzunluğunu yoxlayın
            current_time = time.time()
            if self.speech_active:
                # Hər çərçivədə simvolları artırın
                if current_time - self.last_animation_time > 0.02:  # 20 ms gecikmə
                    self.speech_animation_index = min(
                        self.speech_animation_index + self.speech_animation_speed,
                        len(self.current_speech)
                    )
                    self.last_animation_time = current_time
            else:
                # Nitq bitdikdə bütün mətni göstərin
                self.speech_animation_index = len(self.current_speech)
            
            # Animasiya mətni çəkin
            animated_text = self.current_speech[:self.speech_animation_index]
            
            # Mətn rəsmini qurun
            font = QFont('Segoe UI', 14)
            painter.setFont(font)
            painter.setPen(QPen(text_color))
            
            # Bükmək üçün mətn rect yaradın
            text_rect = QRect(
                int(cx - 300), int(y_pos - 15),  # Daha böyük mətn sahəsi
                600, 200
            )
            
            # Daha yaxşı görünmə üçün mətn fonunu çəkin
            bg_rect = QRect(text_rect)
            path = painter.fontMetrics().boundingRect(
                text_rect, 
                Qt.AlignmentFlag.AlignCenter | Qt.TextFlag.TextWordWrap,
                animated_text
            )
            
            # Mətnə uyğunlaşmaq üçün fon düzbucağını tənzimləyin
            bg_rect.setX(path.x() - 20)
            bg_rect.setY(path.y() - 15)
            bg_rect.setWidth(path.width() + 40)
            bg_rect.setHeight(path.height() + 30)
            
            # Yarı şəffaflıq və gradient ilə dairəvi fon çəkin - Qaranlıq tema uyğun
            gradient = QRadialGradient(
                bg_rect.center().x(), 
                bg_rect.center().y(), 
                bg_rect.width() / 2
            )
            gradient.setColorAt(0, QColor(22, 27, 34, 240))  # GitHub Qaranlıq mövzu bg_secondary
            gradient.setColorAt(1, QColor(13, 17, 23, 220))  # GitHub Qaranlıq mövzu bg
            
            painter.setBrush(gradient)
            painter.setPen(QPen(QColor(self.colors['primary']), 1))
            painter.drawRoundedRect(bg_rect, 15, 15)
            
            # Mətn çəkin
            painter.setPen(QPen(text_color))
            painter.drawText(
                text_rect,
                Qt.AlignmentFlag.AlignCenter | Qt.TextFlag.TextWordWrap,
                animated_text
            )
            
            # Nitq göstərici animasiyası (nitq aktiv olduqda)
            if self.speech_active:
                indicator_width = 60
                indicator_height = 6
                indicator_x = bg_rect.x() + (bg_rect.width() - indicator_width) / 2
                indicator_y = bg_rect.y() + bg_rect.height() + 10
                
                # Səs dalğası animasiyası
                for i in range(5):
                    bar_height = random.randint(3, indicator_height) if self.speech_active else 2
                    bar_x = indicator_x + i * (indicator_width / 5)
                    bar_y = indicator_y + (indicator_height - bar_height) / 2
                    
                    bar_color = QColor(self.colors['accent'])
                    painter.setBrush(bar_color)
                    painter.setPen(Qt.PenStyle.NoPen)
                    painter.drawRoundedRect(
                        int(bar_x), int(bar_y),
                        int(indicator_width / 6), int(bar_height),
                        2, 2
                    )

    def toggle_listening(self):
        """Manuel olaraq dinləməni başladır"""
        if not self.listening:
            # Digər dinləmə rejimlərini bağla
            self.wake_word_listening = False
            self.continuous_listening = False
            
            # Continuous listen düyməsini normal rəngə qaytar
            self.continuous_listen_button.setStyleSheet(
                f"""
                QPushButton {{
                    background-color: {self.colors['secondary']}; 
                    color: white; 
                    border: none; 
                    border-radius: 23px; 
                    font-size: 18px;
                }}
                QPushButton:hover {{
                    background-color: {self.colors['primary']};
                    font-size: 20px;
                }}
                QPushButton:pressed {{
                    background-color: {self.colors['accent']};
                }}
                """
            )
            
            self.wake_word_toggle.setText("🔇 Wake Word Deaktiv")
            self.wake_word_toggle.setStyleSheet(
                f"""
                QPushButton {{
                    background-color: {self.colors['error']}; 
                    color: white; 
                    border: none; 
                    padding: 5px 15px; 
                    border-radius: 15px; 
                    font-family: 'Segoe UI', Arial;
                }}
                QPushButton:hover {{
                    background-color: #D32F2F;
                }}
                """
            )
            
            # Manuel dinləməni başlat
            self.listening = True
            self.listening_label.setText("🎤 Əmr Gözlənilir...")
            self.listening_label.setStyleSheet(
                f"""
                color: {self.colors['error']}; 
                font-weight: bold; 
                background-color: rgba(244, 67, 54, 0.2); 
                padding: 5px 15px; 
                border-radius: 15px;
                font-family: 'Segoe UI', Arial;
                """
            )
            self.mic_button.setStyleSheet(
                f"""
                QPushButton {{
                    background-color: {self.colors['error']}; 
                    color: white; 
                    border: none; 
                    border-radius: 23px;
                    font-size: 18px;
                }}
                QPushButton:hover {{
                    background-color: #D32F2F;
                    font-size: 20px;
                }}
                """
            )
            threading.Thread(target=self.listen_once_for_command, daemon=True).start()
        else:
            # Manuel dinləməni bağla
            self.listening = False
            
            # Heç bir dinləmə rejimi aktiv deyil vəziyyətinə keç
            self.update_not_listening_state()

    def toggle_continuous_listening(self):
        """Davamlı dinləməni başlat/dayandır"""
        if not self.continuous_listening:
            # Digər dinləmə rejimlərini bağla
            self.wake_word_listening = False
            self.listening = False
            self.wake_word_toggle.setText("🔇 Wake Word Deaktiv")
            self.wake_word_toggle.setStyleSheet(
                f"""
                QPushButton {{
                    background-color: {self.colors['error']}; 
                    color: white; 
                    border: none; 
                    padding: 5px 15px; 
                    border-radius: 15px; 
                    font-family: 'Segoe UI', Arial;
                }}
                QPushButton:hover {{
                    background-color: #D32F2F;
                }}
                """
            )
            
            # Davamlı dinləməni başlat və düyməni qırmızı et
            self.continuous_listening = True
            self.continuous_listen_button.setStyleSheet(
                f"""
                QPushButton {{
                    background-color: {self.colors['error']}; 
                    color: white; 
                    border: none; 
                    border-radius: 23px; 
                    font-size: 18px;
                }}
                QPushButton:hover {{
                    background-color: #D32F2F;
                    font-size: 20px;
                }}
                QPushButton:pressed {{
                    background-color: {self.colors['accent']};
                }}
                """
            )
            self.listening_label.setText("🎤 Davamlı Dinləmə Aktivdir...")
            self.listening_label.setStyleSheet(
                f"""
                color: {self.colors['error']}; 
                font-weight: bold;
                background-color: rgba(244, 67, 54, 0.2); 
                padding: 5px 15px; 
                border-radius: 15px;
                font-family: 'Segoe UI', Arial;
                """
            )
            threading.Thread(target=self.continuous_listen, daemon=True).start()
        else:
            # Davamlı dinləməni bağla və düyməni normal rəngə qaytar
            self.continuous_listening = False
            self.continuous_listen_button.setStyleSheet(
                f"""
                QPushButton {{
                    background-color: {self.colors['secondary']}; 
                    color: white; 
                    border: none; 
                    border-radius: 23px; 
                    font-size: 18px;
                }}
                QPushButton:hover {{
                    background-color: {self.colors['primary']};
                    font-size: 20px;
                }}
                QPushButton:pressed {{
                    background-color: {self.colors['accent']};
                }}
                """
            )
            # Heç bir dinləmə rejimi aktiv deyil vəziyyətinə keç
            self.update_not_listening_state()

    def continuous_listen(self):
        """Davamlı dinləmə funksiyası"""
        with sr.Microphone() as source:
            # Ətraf mühit səsini tənzimləmə
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            
            while self.continuous_listening:
                try:
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=None)
                    
                    try:
                        # Cari dil parametrini istifadə et
                        text = self.recognizer.recognize_google(audio, language=self.recognition_language)

                        if text.strip():
                            try:
                                song = AudioSegment.from_wav("wav/start.wav")
                                play(song)
                            except Exception as e:
                                # Dilə görə xəta mesajı
                                if hasattr(self, 'voice_settings') and self.voice_settings.get('language') == 'tr-TR':
                                    self.speak(f"Ses dosyası çalınamadı: {e}")
                                else:
                                    self.speak(f"Səs faylı oxuna bilmədi: {e}")
                                
                            self.commands.process_command(text)
                            
                    except sr.UnknownValueError:
                        continue
                    except sr.RequestError:
                        # Dilə görə xəta mesajı
                        if hasattr(self, 'voice_settings') and self.voice_settings.get('language') == 'tr-TR':
                            self.speak("İnternet bağlantısı sorunu. Lütfen bağlantınızı kontrol edin.")
                        else:
                            self.speak("İnternet bağlantısı problemi. Zəhmət olmasa bağlantınızı yoxlayın.")
                        break
                except sr.WaitTimeoutError:
                    continue
                except Exception as e:
                    # Dilə görə xəta mesajı
                    if hasattr(self, 'voice_settings') and self.voice_settings.get('language') == 'tr-TR':
                        self.speak(f"Dinleme sırasında hata oluştu: {e}")
                    else:
                        self.speak(f"Dinləmə zamanı xəta baş verdi: {e}")
                    break

    def process_text_input(self):
        # Mətn daxiletməsini emal et
        text = self.input_field.text().strip()
        if text:
            self.input_field.clear()
            
            # Əgər bir cavab gözlənilirsə
            if self.waiting_for_response:
                self.text_response = text.lower()
                self.waiting_for_response = False
            else:
                # Normal əmr emalı
                threading.Thread(target=self.commands.process_command, args=(text,), daemon=True).start()

    def speak(self, text):
        """Əsas söhbət üsulu"""
        self.current_speech = text
        self.speech_active = True
        self.speech_animation_index = 0
        
        # Seçilmiş TTS mühərrikinə görə danış
        if self.voice_settings['tts_engine'] == 'edge':
            asyncio.run(self.edge_speak(text))
        else:
            self.gtts_speak(text)
        
        self.speech_active = False
        self.speech_fade_time = time.time() + 1

        
    async def edge_speak(self, text):
        """Edge TTS istifadə edərək mətni səsə çevir"""
        try:
            # Seçilmiş dil və cinsiyətə görə səsi müəyyən et
            voice = self.voice_options[self.voice_settings['language']][self.voice_settings['voice_gender']]
            
            communicate = edge_tts.Communicate(text, voice)
            
            # Müvəqqəti fayl yarat
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as fp:
                temp_filename = fp.name
                
            # Səsi yadda saxla    
            await communicate.save(temp_filename)
            
            # Səsi çal
            pygame.mixer.init()
            pygame.mixer.music.load(temp_filename)
            pygame.mixer.music.play()
            
            # Səsin çalınmasını gözlə
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
                
            # Təmizlik
            pygame.mixer.quit()
            os.unlink(temp_filename)
            
        except Exception as e:
            # Dilə görə xəta mesajı
            if hasattr(self, 'voice_settings') and self.voice_settings.get('language') == 'tr-TR':
                self.speak(f"Edge TTS hatası: {e}")
            else:
                self.speak(f"Edge TTS xətası: {e}")
            # Xəta vəziyyətində gTTS'ə qayıt
            self.gtts_speak(text)

    def gtts_speak(self, text):
        """Google TTS istifadə edərək mətni səsə çevir"""
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as fp:
                temp_filename = fp.name
                
            # Dil kodunu gTTS formatına çevir
            lang_code = self.voice_settings['language'].split('-')[0].lower()
            tts = gTTS(text=text, lang=lang_code)
            tts.save(temp_filename)
            
            pygame.mixer.init()
            pygame.mixer.music.load(temp_filename)
            pygame.mixer.music.play()
            
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
                
            pygame.mixer.quit()
            os.unlink(temp_filename)
            
        except Exception as e:
            # Dilə görə xəta mesajı
            if hasattr(self, 'voice_settings') and self.voice_settings.get('language') == 'tr-TR':
                self.speak(f"Google TTS hatası: {e}")
            else:
                self.speak(f"Google TTS xətası: {e}")
            # Son çarə olaraq pyttsx3'ə qayıt
            self.engine.say(text)
            self.engine.runAndWait()

    def listen_for_response(self, timeout=10):
        """İstifadəçidən səsli və ya yazılı cavab gözləyir"""
        # Cavab gözləmə vəziyyətini başlat
        self.waiting_for_response = True
        self.text_response = None
        
        # Mövcud status'u və düymə vəziyyətlərini saxla
        previous_status = self.listening_label.text()
        
        try:
            # Status'u yenilə və mikrofon düyməsini qırmızı et
            self.listening_label.setText("🎤 Cavabınızı gözləyirəm...")
            self.listening_label.setStyleSheet(f"color: {self.colors['error']}; font-weight: bold;")
            self.mic_button.setStyleSheet(
                f"background-color: {self.colors['error']}; color: white; "
                f"border: none; border-radius: 20px;"
            )
            
            # Input field'ı aktiv et və placeholder'ı yenilə
            self.input_field.setPlaceholderText("Cavabınızı yazın və Enter'a basın...")
            self.input_field.setEnabled(True)
            
            # Səs effekti
            try:
                song = AudioSegment.from_wav("wav/listen.wav")
                play(song)
            except Exception as e:
                # Dilə görə xəta mesajı
                if hasattr(self, 'voice_settings') and self.voice_settings.get('language') == 'tr-TR':
                    self.speak(f"Ses dosyası çalınamadı: {e}")
                else:
                    self.speak(f"Səs faylı oxuna bilmədi: {e}")
            
            # Mikrofon dinləmə thread'ini başlat
            mic_thread = threading.Thread(target=self.listen_mic_for_response, daemon=True)
            mic_thread.start()
            
            # Yazılı və ya səsli cavab gələnə qədər və ya timeout olana qədər gözlə
            start_time = time.time()
            while self.waiting_for_response and (time.time() - start_time < timeout):
                # GUI yeniləməsi
                QApplication.processEvents()
                
                # Yazılı və ya səsli cavab alındısa
                if self.text_response:
                    return self.text_response
                
                # Qısa bir gözləmə
                time.sleep(0.1)
            
            # Timeout oldu və ya cavab alındı
            if not self.text_response and self.waiting_for_response:
                # Dilə görə xəta mesajı
                if hasattr(self, 'voice_settings') and self.voice_settings.get('language') == 'tr-TR':
                    self.speak("Cevap bekleme süresi doldu.")
                else:
                    self.speak("Cavab gözləmə müddəti bitdi.")
            
            return self.text_response
            
        finally:
            # Input field'ı normal vəziyyətə gətir
            self.input_field.setPlaceholderText("Mənə bir şey de...")
            self.input_field.setEnabled(True)
            
            # Heç bir dinləmə rejimi aktiv deyilsə "Dinləmə Deaktivdir" vəziyyətinə keç
            if not any([self.wake_word_listening, self.continuous_listening, self.listening]):
                self.update_not_listening_state()
            else:
                # Əvvəlki status'a qayıt
                self.listening_label.setText(previous_status)
                self.mic_button.setStyleSheet(
                    f"""
                    QPushButton {{
                        background-color: {self.colors['primary']}; 
                        color: white; 
                        border: none; 
                        border-radius: 20px;
                    }}
                    QPushButton:hover {{
                        background-color: {self.colors['accent']};
                        font-size: 20px;
                    }}
                    """
                )

    def listen_mic_for_response(self):
        """Mikrofon ilə cavab dinləmə (ayrı thread'də işləyir)"""
        if not self.waiting_for_response:
            return
        
        try:
            with sr.Microphone() as source:
                # Ətraf mühit səsini tənzimləmə
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                
                # Səsi dinlə
                try:
                    audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)
                    
                    # Əgər hələ cavab gözləyiriksə
                    if self.waiting_for_response:
                        try:
                            # Cari dil parametrini istifadə et
                            response = self.recognizer.recognize_google(audio, language=self.recognition_language)
                            
                            try:
                                # Başlama səsi
                                song = AudioSegment.from_wav("wav/start.wav")
                                play(song)
                            except Exception as e:
                                # Dilə görə xəta mesajı
                                if hasattr(self, 'voice_settings') and self.voice_settings.get('language') == 'tr-TR':
                                    self.speak(f"Ses dosyası çalınamadı: {e}")
                                else:
                                    self.speak(f"Səs faylı oxuna bilmədi: {e}")
                            
                            # Cavabı saxla
                            self.text_response = response.lower()
                            self.waiting_for_response = False
                            
                        except sr.UnknownValueError:
                            # Dilə görə xəta mesajı
                            if hasattr(self, 'voice_settings') and self.voice_settings.get('language') == 'tr-TR':
                                self.speak("Üzgünüm, söylediğinizi anlayamadım.")
                            else:
                                self.speak("Üzr istəyirəm, dediyinizi başa düşə bilmədim.")
                        except sr.RequestError:
                            # Dilə görə xəta mesajı
                            if hasattr(self, 'voice_settings') and self.voice_settings.get('language') == 'tr-TR':
                                self.speak("İnternet bağlantısı sorunu. Lütfen bağlantınızı kontrol edin.")
                            else:
                                self.speak("İnternet bağlantısı problemi. Zəhmət olmasa bağlantınızı yoxlayın.")
                except sr.WaitTimeoutError:
                    pass
        except Exception as e:
            # Dilə görə xəta mesajı
            if hasattr(self, 'voice_settings') and self.voice_settings.get('language') == 'tr-TR':
                self.speak(f"Mikrofon dinleme hatası: {e}")
            else:
                self.speak(f"Mikrofon dinləmə xətası: {e}")

    def setup_audio(self):
        # Səs səviyyəsi idarəsini başlat
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        self.volume = cast(interface, POINTER(IAudioEndpointVolume))

    def setup_audio_visualization(self):
        """Səs vizualizasiyası üçün PyAudio quraşdırması"""
        self.CHUNK = 1024
        self.FORMAT = pyaudio.paFloat32
        self.CHANNELS = 1
        self.RATE = 44100
        self.audio = pyaudio.PyAudio()
        
        # Mikrofon stream'ini başlat
        self.stream = self.audio.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,
            frames_per_buffer=self.CHUNK,
            stream_callback=self.audio_callback
        )
        self.stream.start_stream()
        
    def audio_callback(self, in_data, frame_count, time_info, status):
        """Səs məlumatlarını emal et və vizualizasiya üçün saxla"""
        data = np.frombuffer(in_data, dtype=np.float32)
        self.audio_data = np.abs(data[:128])  # Yalnız ilk 128 sample'ı al
        return (in_data, pyaudio.paContinue)

    def start_wake_word_detection(self):
        """Davamlı olaraq wake word'ü dinləyən thread'i başladır"""
        self.wake_word_listening = True
        threading.Thread(target=self.listen_for_wake_word, daemon=True).start()
        self.listening_label.setText("🎧 Sizi Dinləyirəm...")
        
    def listen_for_wake_word(self):
        """Wake word'ü dinləyir"""
        # Cari dil parametrinə görə wake word'ü seç
        current_language = self.voice_settings['language']
        
        # Mövcud dilə görə əsas wake words (vergüllə ayrılmış)
        base_words_text = self.wake_word_settings['tr_word'] if current_language == 'tr-TR' else self.wake_word_settings['az_word']
        
        # Vergüllə ayrılmış sözləri siyahıya çevir
        base_words = [word.strip() for word in base_words_text.split(',') if word.strip()]
        
        if not base_words:
            # Boşdursa standart dəyəri istifadə et
            if current_language == 'tr-TR':
                base_words = ["azer"]
            else:
                base_words = ["azər"]
        
        # Hər bir söz üçün variantları yarad
        wake_word_variants = []
        for word in base_words:
            wake_word_variants.append(word)
            wake_word_variants.append(f"hey {word}")
            wake_word_variants.append(f"hey {word} ai")
            wake_word_variants.append(f"{word} ai")
        
        # Dilə xas wake word variantlarını yarad
        wake_words = {
            'tr-TR': wake_word_variants,
            'az-AZ': wake_word_variants
        }
        
        with sr.Microphone() as source:
            # Ətraf mühit səsini tənzimləmə
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            
            while self.wake_word_listening:  # Wake word dinləmə aktiv olduğu müddətcə dinlə
                try:
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=None)
                    try:
                        # Cari dil parametrini istifadə et
                        text = self.recognizer.recognize_google(audio, language=self.recognition_language).lower()
                        
                        # Seçilmiş dilə görə wake words'ü istifadə et
                        current_wake_words = wake_words[self.voice_settings['language']]
                        
                        # Wake word aşkarlanıb aşkarlanmadığını yoxla
                        if any(word in text for word in current_wake_words):
                            self.activate_assistant()
                            
                    except sr.UnknownValueError:
                        continue
                    except sr.RequestError:
                        continue
                        
                except sr.WaitTimeoutError:
                    continue
                
                if not self.wake_word_listening:  # Wake word dinləmə bağlandıqda döngüdən çıx
                    break

    def activate_assistant(self):
        """Asistanı aktivləşdirir və əmr gözləməyə başlayır"""
        try:
            song = AudioSegment.from_wav("wav/listen.wav")
            play(song)
        except Exception as e:
            # Dilə görə xəta mesajı
            if hasattr(self, 'voice_settings') and self.voice_settings.get('language') == 'tr-TR':
                self.speak(f"Ses dosyası çalınamadı: {e}")
            else:
                self.speak(f"Səs faylı oxuna bilmədi: {e}")
        
        # Dilə görə cavab seç
        current_language = self.voice_settings['language']
        
        if current_language == 'az-AZ':
            # Azərbaycan dili cavabları
            responses = [
                "Hə, sizi dinləyirəm.",
                "Buyurun, sizə necə kömək edə bilərəm?",
                "Əmrinizdəyəm.",
                "Sizi Eşidirəm.",
                "Bəli, sizi dinləyirəm.",
                "Nə buyurursunuz?",
                "Sizə kömək etməyə hazıram."
            ]
        else:
            # Türk dili cavabları
            responses = [
                "Evet, sizi dinliyorum.",
                "Buyurun, size nasıl yardım edebilirim?",
                "Emrinizdeyim.",
                "Sizi Duyuyorum.",
                "Evet, sizi dinliyorum.",
                "Ne buyuruyorsunuz?",
                "Size yardım etmeye hazırım."
            ]
            
        self.speak(random.choice(responses))
        
        # İnterfeysi yenilə
        self.listening_label.setText("🎤 Əmr Gözlənilir...")
        self.listening_label.setStyleSheet(f"color: {self.colors['error']}; font-weight: bold;")
        self.mic_button.setStyleSheet(
            f"background-color: {self.colors['error']}; color: white; "
            f"border: none; border-radius: 20px;"
        )
        
        # Tək dəfəlik əmr dinləməsi
        self.listen_once_for_command()
        
    def listen_once_for_command(self):
        """Tək bir əmr üçün dinləyir"""
        with sr.Microphone() as source:
            try:
                # Ətraf mühit səsini tənzimləmə
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                
                self.listening_label.setText("🎤 Sizi Dinləyirəm...")
                self.listening_label.setStyleSheet(f"color: {self.colors['error']}; font-weight: bold;")
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=None)
                
                try:
                    song = AudioSegment.from_wav("wav/start.wav")
                    play(song)
                except Exception as e:
                    # Dilə görə xəta mesajı
                    if hasattr(self, 'voice_settings') and self.voice_settings.get('language') == 'tr-TR':
                        self.speak(f"Ses dosyası çalınamadı: {e}")
                    else:
                        self.speak(f"Səs faylı oxuna bilmədi: {e}")

                # Cari dil parametrini istifadə et
                text = self.recognizer.recognize_google(audio, language=self.recognition_language)
                self.commands.process_command(text)
                
            except sr.WaitTimeoutError:
                # Dilə görə xəta mesajı
                if hasattr(self, 'voice_settings') and self.voice_settings.get('language') == 'tr-TR':
                    self.speak("Bir komut duymadım.")
                else:
                    self.speak("Bir əmr eşitmədim.")
            except sr.UnknownValueError:
                # Dilə görə xəta mesajı
                if hasattr(self, 'voice_settings') and self.voice_settings.get('language') == 'tr-TR':
                    self.speak("Söylediğinizi anlayamadım.")
                else:
                    self.speak("Dediyinizi başa düşə bilmədim.")
            except sr.RequestError:
                # Dilə görə xəta mesajı
                if hasattr(self, 'voice_settings') and self.voice_settings.get('language') == 'tr-TR':
                    self.speak("Üzgünüm, bir hata oluştu.")
                else:
                    self.speak("Üzr istəyirəm, bir xəta baş verdi.")
            finally:
                self.listening = False
                # Heç bir dinləmə rejimi aktiv deyilsə "Dinləmə Deaktivdir" vəziyyətinə keç
                if not any([self.wake_word_listening, self.continuous_listening, self.listening]):
                    self.update_not_listening_state()
                else:
                    self.listening_label.setText("🎧 Sizi Dinləyirəm...")
                    self.listening_label.setStyleSheet(f"color: {self.colors['accent']}; font-weight: bold;")
                    self.mic_button.setStyleSheet(
                        f"""
                        QPushButton {{
                            background-color: {self.colors['primary']}; 
                            color: white; 
                            border: none; 
                            border-radius: 20px;
                        }}
                        QPushButton:hover {{
                            background-color: {self.colors['accent']};
                            font-size: 20px;
                        }}
                        """
                    )

    def update_listening_language(self):
        """Dinləmə dilini yenilə"""
        self.recognition_language = self.recognition_languages[self.voice_settings['language']]

    def save_voice_settings(self):
        """İstifadəçinin səs parametrlərini verilənlər bazasına yadda saxla"""
        try:
            from db_manager import db_manager
            
            # Verilənlər bazasına səs parametrlərini yadda saxla
            db_manager.update_voice_settings(
                self.current_user['id'],
                self.voice_settings['tts_engine'],
                self.voice_settings['language'],
                self.voice_settings['voice_gender']
            )
            
            # İstifadəçi məlumatlarını yenilə
            if 'voice_settings' not in self.current_user:
                self.current_user['voice_settings'] = {}
                
            self.current_user['voice_settings'] = self.voice_settings
            
        except Exception as e:
            # Dilə görə xəta mesajı
            if hasattr(self, 'voice_settings') and self.voice_settings.get('language') == 'tr-TR':
                self.speak(f"Ses ayarları kaydetme hatası: {e}")
            else:
                self.speak(f"Səs parametrləri yadda saxlama xətası: {e}")

    def update_voice_settings(self, settings):
        """Səs parametrlərini yenilə və yadda saxla"""
        
        self.voice_settings.update(settings)
        
        # Səs tanıma dilini yenilə
        if hasattr(self, 'recognizer'):
            self.recognizer = sr.Recognizer()
            
        # Wake word və davamlı dinləmə üçün dil parametrini yenilə
        self.update_listening_language()
        
        # pyttsx3 səsini yenilə
        self.initialize_voice()
        
        # Parametrləri yadda saxla
        self.save_voice_settings()

    def closeEvent(self, event):
        """Proqramı bağlamadan əvvəl təsdiq istə"""
        self.program_exit.show_exit_dialog()
        event.ignore()  # Hadisəni yox say, çıxış dialog'u özü bağlayacaq

    def logout(self):
        """İstifadəçini çıxış edir və giriş ekranına qaytarır"""
        try:
            # Giriş məlumatlarını təmizlə
            from login_screen import LoginScreen
            login_screen = LoginScreen()
            login_screen.clear_login_credentials()
            
            # Tətbiqi yenidən başlat
            import sys
            import subprocess
            
            # Mövcud tətbiqi bağla
            self.close()
            
            # Tətbiqi yenidən başlat
            subprocess.Popen([sys.executable] + sys.argv)
            sys.exit()
            
        except Exception as e:
            # Dilə görə xəta mesajı
            if hasattr(self, 'voice_settings') and self.voice_settings.get('language') == 'tr-TR':
                self.speak(f"Çıkış yapılırken hata: {e}")
            else:
                self.speak(f"Çıxış edilərkən xəta: {e}")
            # Xəta vəziyyətində normal çıxış et
            import sys
            sys.exit()

    def check_internet(self):
        """İnternet bağlantısını və IP ünvanını yoxla"""
        try:
            # IP ünvanını al
            ip_response = requests.get('https://api.ipify.org?format=json', timeout=2)
            if ip_response.status_code == 200:
                ip = ip_response.json()['ip']
                self.ip_value.setText(ip)
            
            # Bir neçə etibarlı sayt sınayaq
            sites = [
                "http://www.google.com",
                "http://www.cloudflare.com",
                "http://www.amazon.com"
            ]
            
            for site in sites:
                try:
                    response = requests.get(site, timeout=2)
                    if response.status_code == 200:
                        self.internet_status = "🌐 Bağlı"
                        self.internet_color = self.colors['accent']
                        self.internet_status_label.setText(self.internet_status)
                        self.internet_status_label.setStyleSheet(f"color: {self.internet_color};")
                        return
                except:
                    continue
                
            # Heç bir sayta bağlanıla bilmədisə
            raise Exception("Bağlantı yoxdur")
            
        except:
            self.internet_status = "❌ Bağlantı yoxdur"
            self.internet_color = self.colors['error']
            self.internet_status_label.setText(self.internet_status)
            self.internet_status_label.setStyleSheet(f"color: {self.internet_color};")
            self.ip_value.setText("Bağlantı yoxdur")

    def __del__(self):
        """Səs resurslarını təmizlə"""
        if hasattr(self, 'stream'):
            self.stream.stop_stream()
            self.stream.close()
        if hasattr(self, 'audio'):
            self.audio.terminate()

    def toggle_wake_word(self):
        """Wake word dinləməsini aç/bağla"""
        if self.wake_word_listening:
            # Wake word dinləməsini bağla
            self.wake_word_listening = False
            
            self.wake_word_toggle.setText("🔇 Wake Word Deaktiv")
            self.wake_word_toggle.setStyleSheet(
                f"""
                QPushButton {{
                    background-color: {self.colors['error']}; 
                    color: white; 
                    border: none; 
                    padding: 5px 15px; 
                    border-radius: 15px; 
                    font-family: 'Segoe UI', Arial;
                }}
                QPushButton:hover {{
                    background-color: #D32F2F;
                }}
                """
            )
            self.listening_label.setText("⏸️ Wake Word Dinləməsi Dayandırıldı")
            # Heç bir dinləmə rejimi aktiv deyil vəziyyətinə keç
            self.update_not_listening_state()
        else:
            # Digər dinləmə rejimlərini bağla
            self.listening = False
            self.continuous_listening = False
            
            # Continuous listen düyməsini normal rəngə qaytar
            self.continuous_listen_button.setStyleSheet(
                f"""
                QPushButton {{
                    background-color: {self.colors['secondary']}; 
                    color: white; 
                    border: none; 
                    border-radius: 23px; 
                    font-size: 18px;
                }}
                QPushButton:hover {{
                    background-color: {self.colors['primary']};
                    font-size: 20px;
                }}
                QPushButton:pressed {{
                    background-color: {self.colors['accent']};
                }}
                """
            )
            
            # Wake word dinləməsini aç
            self.wake_word_listening = True
            self.wake_word_toggle.setText("🎧 Wake Word Aktiv")
            self.wake_word_toggle.setStyleSheet(
                f"""
                QPushButton {{
                    background-color: {self.colors['accent']}; 
                    color: white; 
                    border: none; 
                    padding: 5px 15px; 
                    border-radius: 15px; 
                    font-family: 'Segoe UI', Arial;
                }}
                QPushButton:hover {{
                    background-color: {self.colors['primary']};
                }}
                """
            )
            self.listening_label.setText("🎧 Sizi Dinləyirəm...")
            threading.Thread(target=self.listen_for_wake_word, daemon=True).start()
            
            # Wake word parametrlərini yadda saxla
            self.save_wake_word_settings()

    # Bu yeni metodu əlavə et
    def update_not_listening_state(self):
        """Heç bir dinləmə rejimi aktiv deyilən zaman vəziyyəti yenilə"""
        if not any([self.wake_word_listening, self.continuous_listening, self.listening]):
            self.listening_label.setText("⏸️ Dinləmə Deaktivdir")
            self.listening_label.setStyleSheet(
                f"""
                color: {self.colors['text_secondary']}; 
                font-weight: bold;
                background-color: {self.colors['bg_tertiary']}; 
                padding: 5px 15px; 
                border-radius: 15px;
                font-family: 'Segoe UI', Arial;
                """
            )
            
            # Bütün dinləmə düymələrini normal rəngə qaytar
            self.mic_button.setStyleSheet(
                f"""
                QPushButton {{
                    background-color: {self.colors['secondary']}; 
                    color: white; 
                    border: none; 
                    border-radius: 23px;
                    font-size: 18px;
                }}
                QPushButton:hover {{
                    background-color: {self.colors['primary']};
                    font-size: 20px;
                }}
                """
            )
            
            self.continuous_listen_button.setStyleSheet(
                f"""
                QPushButton {{
                    background-color: {self.colors['secondary']}; 
                    color: white; 
                    border: none; 
                    border-radius: 23px; 
                    font-size: 18px;
                }}
                QPushButton:hover {{
                    background-color: {self.colors['primary']};
                    font-size: 20px;
                }}
                QPushButton:pressed {{
                    background-color: {self.colors['accent']};
                }}
                """
            )

    def load_wake_word_settings(self):
        """İstifadəçinin wake word parametrlərini verilənlər bazasından yüklə"""
        try:
            from db_manager import db_manager
            
            # Verilənlər bazasından istifadəçinin wake word parametrlərini al
            settings = db_manager.get_wake_word_settings(self.current_user['id'])
            
            if settings:
                self.wake_word_settings = {
                    'az_word': settings['az_word'],
                    'tr_word': settings['tr_word']
                }
                # İstifadəçinin wake word parametrlərini mövcud user məlumatına əlavə et
                if 'wake_word_settings' not in self.current_user:
                    self.current_user['wake_word_settings'] = {}
                
                self.current_user['wake_word_settings'] = self.wake_word_settings
                
            else:
                # Standart parametrləri istifadə et və yadda saxla
                db_manager.update_wake_word_settings(
                    self.current_user['id'],
                    self.wake_word_settings['az_word'],
                    self.wake_word_settings['tr_word']
                )
                # Dilə görə xəta mesajı
                if hasattr(self, 'voice_settings') and self.voice_settings.get('language') == 'tr-TR':
                    self.speak("Standart wake word ayarları kullanılıyor ve kaydedildi.")
                else:
                    self.speak("Standart wake word parametrləri istifadə olunur və yadda saxlanıldı.")
        except Exception as e:
            # Dilə görə xəta mesajı
            if hasattr(self, 'voice_settings') and self.voice_settings.get('language') == 'tr-TR':
                self.speak(f"Wake word ayarları yüklenirken hata: {e}")
            else:
                self.speak(f"Wake word parametrləri yüklənərkən xəta: {e}")

    def save_wake_word_settings(self):
        """İstifadəçinin wake word parametrlərini verilənlər bazasına yadda saxla"""
        try:
            from db_manager import db_manager
            
            # Verilənlər bazasına wake word parametrlərini yadda saxla
            db_manager.update_wake_word_settings(
                self.current_user['id'],
                
                self.wake_word_settings['az_word'],
                self.wake_word_settings['tr_word']
            )
            
            # İstifadəçi məlumatlarını yenilə
            if 'wake_word_settings' not in self.current_user:
                self.current_user['wake_word_settings'] = {}
                
            self.current_user['wake_word_settings'] = self.wake_word_settings
                
            
        except Exception as e:
            # Dilə görə xəta mesajı
            if hasattr(self, 'voice_settings') and self.voice_settings.get('language') == 'tr-TR':
                self.speak(f"Wake word ayarları kaydetme hatası: {e}")
            else:
                self.speak(f"Wake word parametrləri yadda saxlama xətası: {e}")

if __name__ == "__main__":
    app = ModernAzer_AI()
