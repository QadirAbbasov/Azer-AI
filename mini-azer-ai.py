import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="pygame.pkgdata")


import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QPushButton, 
                           QLabel, QVBoxLayout, QFrame, QMenu)
from PyQt6.QtCore import Qt, QTimer, QPoint, QRect
from PyQt6.QtGui import QPainter, QPen, QColor, QPainterPath, QAction, QIcon
import speech_recognition as sr
import threading
import numpy as np
import pyaudio
import math
import time
from commands import Azer_AICommands
import pygame
from gtts import gTTS
import tempfile
import os
import edge_tts
import asyncio
from pydub import AudioSegment
from pydub.playback import play
import random
from plugins.plugin_manager import PluginManager
from login_screen import LoginScreen
from db_manager import db_manager
version_data = db_manager.get_version()
from update_checker import check_version

# Bu sətir, qt.qpa.window kimi logların göstərilməsini əngəlləyir.
os.environ["QT_LOGGING_RULES"] = "*.debug=false;qt.qpa.*=false"

class LoadingScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # Pəncərə ölçüsü
        self.width = 200
        self.height = 100
        
        # Sağ alt küncdə yerləşdir
        screen = QApplication.primaryScreen().geometry()
        x = screen.width() - self.width - 20
        y = screen.height() - self.height - 60
        
        self.setGeometry(x, y, self.width, self.height)
        
        # Rənglər
        self.colors = {
            'bg': '#000001',
            'fg': '#00A3FF',
            'text': '#FFFFFF'
        }
        
        self.progress = 0
        self.setup_ui()
        self.start_animation()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Yükləmə mesajı
        self.loading_label = QLabel(version_data['version'] + " Mini Azer AI Başladılır...")
        self.loading_label.setStyleSheet(f"color: {self.colors['text']}; font-size: 12px;")
        layout.addWidget(self.loading_label, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Tərəqqi etiketi
        self.percentage_label = QLabel("0%")
        self.percentage_label.setStyleSheet(f"color: {self.colors['fg']}; font-size: 12px; font-weight: bold;")
        layout.addWidget(self.percentage_label, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.setLayout(layout)
        
    def start_animation(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_progress)
        self.timer.start(50)
        
    def update_progress(self):
        if self.progress < 100:
            self.progress += 2
            self.percentage_label.setText(f"{self.progress}%")
            self.update()
        else:
            self.timer.stop()
            self.close()
            if hasattr(self, 'on_finished'):
                self.on_finished()
            
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Arxa fonu çək
        path = QPainterPath()
        path.addRoundedRect(0, 0, self.width, self.height, 10, 10)
        painter.fillPath(path, QColor(self.colors['bg']))
        
        # Tərəqqi xəttini çək
        line_width = 160
        line_y = self.height // 2
        
        # Arxa fon xətti
        pen = QPen(QColor('#1A1A1A'))
        pen.setWidth(4)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(pen)
        painter.drawLine(20, line_y, 20 + line_width, line_y)
        
        # Tərəqqi xətti
        progress_width = int((self.progress / 100) * line_width)
        pen.setColor(QColor(self.colors['fg']))
        painter.setPen(pen)
        painter.drawLine(20, line_y, 20 + progress_width, line_y)
        
        # Parlaq nöqtə
        painter.setBrush(QColor(self.colors['fg']))
        painter.drawEllipse(QPoint(20 + progress_width, line_y), 3, 3)

class MiniAzer_AI(QMainWindow):
    def __init__(self, user_info):
        super().__init__()
        
        # İstifadəçi məlumatını saxla
        self.current_user = user_info
        
        # Səs parametrləri
        self.voice_settings = {
            'tts_engine': 'edge',
            'language': 'az-AZ',
            'voice_gender': 'male'
        }
        
        # İstifadəçinin səs parametrlərini yüklə
        self.load_voice_settings()
        
        # Səs xəritələndirməsi
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
        
        # Tanıma dili xəritələndirməsi
        self.recognition_languages = {
            'az-AZ': 'az-AZ',
            'tr-TR': 'tr-TR'
        }
        
        # Tanıma dilini yenilə
        self.recognition_language = self.recognition_languages[self.voice_settings['language']]
        
        # Cavab dinləmə dəyişənləri
        self.waiting_for_response = False
        self.text_response = None
        
        # Əmr emal etmə vəziyyəti
        self.processing_command = False
        
        # Yükləmə ekranını göstər
        self.loading_screen = LoadingScreen()
        self.loading_screen.show()
        
        # Dəyişənləri başlat
        self.wake_word_listening = True
        self.listening = False
        self.current_speech = ""
        self.speech_active = False
        self.speech_fade_time = 0
        self.continuous_listening = False
        
        self.setup_window()
        self.setup_audio()
        self.create_interface()
        self.initialize_voice()
        self.commands = Azer_AICommands(self)
        
        # Plugin meneceri başlat
        self.plugin_manager = PluginManager(self)
        
        # Lisenziya statusu yeniləmə taymerini başlat (hər 60 saniyədə)
        self.license_timer = QTimer()
        self.license_timer.timeout.connect(self.update_user_label_with_license)
        self.license_timer.start(60000)  # 60 saniyə
        
        # Oyanış sözü aşkarlanmasını başlat
        self.wake_word_listening = True
        self.start_wake_word_detection()
        
    def load_voice_settings(self):
        """İstifadəçinin səs parametrlərini verilənlər bazasından yüklə"""
        try:
            # İstifadəçi obyektində səs parametrləri olub-olmadığını yoxla
            if 'voice_settings' in self.current_user:
                self.voice_settings = self.current_user['voice_settings']
            else:
                # Verilənlər bazasından yüklə
                settings = db_manager.get_voice_settings(self.current_user['id'])
                if settings:
                    self.voice_settings = {
                        'tts_engine': settings['tts_engine'],
                        'language': settings['language'],
                        'voice_gender': settings['voice_gender']
                    }
                else:
                    # Əgər parametr tapılmayıbsa, standart parametrlər yarat
                    db_manager.update_voice_settings(
                        self.current_user['id'],
                        self.voice_settings['tts_engine'],
                        self.voice_settings['language'],
                        self.voice_settings['voice_gender']
                    )
                
                # İstifadəçi obyektini yenilə
                if 'voice_settings' not in self.current_user:
                    self.current_user['voice_settings'] = {}
                self.current_user['voice_settings'] = self.voice_settings
                
        except Exception as e:
            self.Azer_AI.speak(f"Səs parametrləri yükləmə xətası: {str(e)}" if self.voice_settings['language'] == 'az-AZ' else f"Ses parametreleri yükleme hatası: {str(e)}")
            
    def save_voice_settings(self):
        """İstifadəçinin səs parametrlərini verilənlər bazasına saxla"""
        try:
            db_manager.update_voice_settings(
                self.current_user['id'],
                self.voice_settings['tts_engine'],
                self.voice_settings['language'],
                self.voice_settings['voice_gender']
            )
            
            # İstifadəçi obyektini yenilə
            if 'voice_settings' not in self.current_user:
                self.current_user['voice_settings'] = {}
            self.current_user['voice_settings'] = self.voice_settings
            
        except Exception as e:
            self.Azer_AI.speak(f"Səs parametrləri saxlama xətası: {str(e)}" if self.voice_settings['language'] == 'az-AZ' else f"Ses parametreleri kaydetme hatası: {str(e)}")
        
    def setup_window(self):
        # Rənglər
        self.colors = {
            'bg': '#000001',
            'primary': '#00A3FF',
            'accent': '#00FF99',
            'listening': '#FF4444',
            'wave': '#00A3FF',
            'text': '#FFFFFF',
            'error': '#FF4444'
        }
        
        # Pəncərə parametrləri
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # Pəncərə ölçüsü
        self.width = 300
        self.height = 300
        
        self.setWindowIcon(QIcon('images/logo.ico'))
        
        # Sağ alt küncdə yerləşdir
        screen = QApplication.primaryScreen().geometry()
        x = screen.width() - self.width - 20
        y = screen.height() - self.height - 60
        
        self.setGeometry(x, y, self.width, self.height)
        
    def setup_audio(self):
        self.CHUNK = 1024
        self.FORMAT = pyaudio.paFloat32
        self.CHANNELS = 1
        self.RATE = 44100
        self.audio = pyaudio.PyAudio()
        
        self.stream = self.audio.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,
            frames_per_buffer=self.CHUNK,
            stream_callback=self.audio_callback
        )
        self.stream.start_stream()
        self.audio_data = np.zeros(128)
        
    def audio_callback(self, in_data, frame_count, time_info, status):
        data = np.frombuffer(in_data, dtype=np.float32)
        self.audio_data = np.abs(data[:128])
        return (in_data, pyaudio.paContinue)
        
    def create_interface(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # İstifadəçi məlumatı etiketi
        self.user_label = QLabel(f"👤 {self.current_user['name']}", self)
        self.user_label.setStyleSheet(f"color: {self.colors['text']}; font-size: 10px; background-color: rgba(0, 0, 0, 0.7); padding: 5px; border-radius: 10px;")
        self.user_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # İstifadəçi etiketini lisenziya statusu ilə yenilə
        self.update_user_label_with_license()
        

        
        # Dil düyməsi
        self.lang_button = QPushButton("⚙️", self)
        self.lang_button.setFixedSize(40, 40)
        self.lang_button.clicked.connect(self.show_language_menu)
        self.lang_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.colors['primary']};
                border-radius: 20px;
                color: white;
                font-size: 16px;
            }}
            QPushButton:hover {{
                background-color: {self.colors['accent']};
            }}
        """)
        
        # Bağla düyməsi
        self.close_button = QPushButton("✖️", self)
        self.close_button.setFixedSize(40, 40)
        self.close_button.clicked.connect(self.close)
        self.close_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.colors['error']};
                border-radius: 20px;
                color: white;
                font-size: 16px;
            }}
            QPushButton:hover {{
                background-color: #FF0000;
            }}
        """)
        

        
        # Status etiketi
        self.status_label = QLabel("🎧 Sizi Dinləyirəm...", self)
        self.status_label.setStyleSheet(f"color: {self.colors['accent']}; font-size: 10px; background-color: rgba(0, 0, 0, 0.7); padding: 5px; border-radius: 10px;")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Düzən təşkili
        top_layout = QVBoxLayout()
        
        layout.addLayout(top_layout)
        
        # Səs dalğasının mərkəzində yerləşəcək mikrofon düyməsini yarat
        self.mic_button = QPushButton("🎤", self)
        self.mic_button.setFixedSize(60, 60)
        self.mic_button.clicked.connect(self.toggle_continuous_listening)
        self.mic_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.colors['primary']};
                border-radius: 30px;
                color: white;
                font-size: 20px;
                border: 2px solid {self.colors['accent']};
            }}
            QPushButton:hover {{
                background-color: {self.colors['accent']};
                border: 2px solid {self.colors['primary']};
            }}
        """)
        
        # Animasiya taymerini başlat
        self.animation_timer = QTimer()
        self.animation_timer.timeout.connect(self.update)
        self.animation_timer.start(50)
        
        # Fırlanan taymer
        self.spinner_rotation = 0
        self.spinner_timer = QTimer()
        self.spinner_timer.timeout.connect(self.update_spinner)
        self.spinner_timer.start(16)  # ~60 FPS səlis fırlanma üçün
        
        # Mətn animasiyası dəyişənləri
        self.text_animation_index = 0
        self.text_animation_speed = 2  # Hər kadrda simvol sayı
        self.last_text_animation_time = 0
        
    def update_user_label_with_license(self):
        """İstifadəçi etiketini lisenziya statusu ilə yenilə"""
        import datetime
        
        # Lisenziya statusunu al
        license_status = self.current_user.get('license_status', 'free')
        
        # İstifadəçinin admin olub-olmadığını yoxla
        if self.current_user.get('role') == 'admin':
            self.user_label.setText(f"👤 {self.current_user['name']} 👑 (Limitsiz)")
            return
        
        # İstifadəçinin pro olub-olmadığını yoxla
        if license_status == 'pro':
            # Pro bitmə tarixinin olub-olmadığını yoxla
            if 'pro_expiry' in self.current_user and self.current_user['pro_expiry']:
                try:
                    expiry_date = datetime.datetime.strptime(
                        self.current_user['pro_expiry'], 
                        "%Y-%m-%d %H:%M:%S"
                    )
                    now = datetime.datetime.now()
                    
                    if expiry_date > now:
                        # Qalan vaxtı hesabla
                        remaining = expiry_date - now
                        days = remaining.days
                        hours = remaining.seconds // 3600
                        
                        if days > 0:
                            self.user_label.setText(f"👤 {self.current_user['name']} 💎 ({days}g)")
                        elif hours > 0:
                            self.user_label.setText(f"👤 {self.current_user['name']} 💎 ({hours}s)")
                        else:
                            self.user_label.setText(f"👤 {self.current_user['name']} 💎")
                    else:
                        # Pro bitdi, pulsuz kimi göstər
                        self.user_label.setText(f"👤 {self.current_user['name']} 🆓")
                        # Verilənlər bazasını yenilə
                        from db_manager import db_manager
                        db_manager.update_license_status(self.current_user['id'], 'free')
                        self.current_user['license_status'] = 'free'
                except:
                    # Əgər tarix təhlili uğursuz olarsa, limitsiz pro kimi göstər
                    self.user_label.setText(f"👤 {self.current_user['name']} 💎 (Limitsiz)")
            else:
                # Bitmə tarixi yoxdur, limitsiz pro kimi göstər
                self.user_label.setText(f"👤 {self.current_user['name']} 💎 (Limitsiz)")
        else:
            # Pulsuz istifadəçi
            if 'pro_expiry' in self.current_user and self.current_user['pro_expiry']:
                # İstifadəçinin əvvəl pro olduğu amma bitdiyi
                self.user_label.setText(f"👤 {self.current_user['name']} 🆓 (Pro müddətiniz bitdi)")
            else:
                # Normal pulsuz istifadəçi
                self.user_label.setText(f"👤 {self.current_user['name']} 🆓")
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Səs dalğalarını çək
        cx = self.width // 2
        cy = self.height // 2
        num_points = len(self.audio_data)
        radius = 90
        
        for i in range(num_points):
            angle = (i * 360 / num_points) * math.pi / 180
            amplitude = self.audio_data[i] * 40
            
            r1 = int(radius - 15 + amplitude)
            r2 = int(radius + 15 + amplitude)
            
            x1 = int(cx + math.cos(angle) * r1)
            y1 = int(cy + math.sin(angle) * r1)
            x2 = int(cx + math.cos(angle) * r2)
            y2 = int(cy + math.sin(angle) * r2)
            
            pen = QPen(QColor(self.colors['wave']))
            pen.setWidth(2)
            painter.setPen(pen)
            painter.drawLine(x1, y1, x2, y2)
        
        # Səs dalğasının ətrafında fırlanan yükləyicini çək
        self.draw_spinner(painter, cx, cy, radius)
        
        # Mikrofon düyməsini səs dalğasının mərkəzində yerləşdir
        if hasattr(self, 'mic_button'):
            button_x = cx - 30  # Düyməni mərkəzləşdir (60px genişlik / 2)
            button_y = cy - 30  # Düyməni mərkəzləşdir (60px hündürlük / 2)
            self.mic_button.move(button_x, button_y)
        
        # Status etiketini mikrofon düyməsinin altında yerləşdir
        if hasattr(self, 'status_label'):
            # Status etiketinin mövqeyini hesabla (mikrofon düyməsinin altında)
            status_x = cx - 80  # Etiketi mərkəzləşdir (160px genişlik / 2)
            status_y = cy + 40  # Mikrofon düyməsinin altında
            self.status_label.move(status_x, status_y)
            self.status_label.setFixedWidth(160)  # Daha yaxşı görünüş üçün sabit genişlik təyin et
        
        # İstifadəçi etiketini yuxarıda yerləşdir
        if hasattr(self, 'user_label'):
            user_x = cx - 60  # Etiketi mərkəzləşdir (120px genişlik / 2)
            user_y = 60  # Yuxarıda, yuxarı düymələrin altında
            self.user_label.move(user_x, user_y)
            self.user_label.setFixedWidth(120)  # Daha yaxşı görünüş üçün sabit genişlik təyin et
        
        # Dil düyməsini yuxarı sol küncdə yerləşdir
        if hasattr(self, 'lang_button'):
            lang_x = 10  # Sol kənardan 10px
            lang_y = 10  # Yuxarı kənardan 10px
            self.lang_button.move(lang_x, lang_y)
        
        # Bağla düyməsini yuxarı sağ küncdə yerləşdir
        if hasattr(self, 'close_button'):
            close_x = self.width - 50  # Sağ kənardan 10px
            close_y = 10  # Yuxarı kənardan 10px
            self.close_button.move(close_x, close_y)
        
        # Pəncərənin altında danışıq mətnini çək
        if self.speech_active or time.time() < self.speech_fade_time:
            opacity = 255
            if not self.speech_active:
                remaining_time = self.speech_fade_time - time.time()
                opacity = int(min(255, remaining_time * 255))
            
            # Mətni pəncərənin altında yerləşdir
            text_y = self.height - 80  # Alt kənardan 80px
            text_height = 60  # Mətn sahəsi üçün hündürlük
            
            # Daha yaxşı oxunaqlıq üçün arxa fon çək
            bg_rect = QRect(10, text_y - 10, self.width - 20, text_height + 20)
            painter.setBrush(QColor(0, 0, 0, 180))  # Yarı şəffaf qara arxa fon
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRoundedRect(bg_rect, 10, 10)
            
            # Mətn yazma effektini animasiya et
            current_time = time.time()
            if self.speech_active:
                # Hər kadrda simvolları artır
                if current_time - self.last_text_animation_time > 0.05:  # 50ms gecikmə
                    self.text_animation_index = min(
                        self.text_animation_index + self.text_animation_speed,
                        len(self.current_speech)
                    )
                    self.last_text_animation_time = current_time
            else:
                # Danışıq bitəndə bütün mətni göstər
                self.text_animation_index = len(self.current_speech)
            
            # Animasiya edilmiş mətni çək
            animated_text = self.current_speech[:self.text_animation_index]
            
            # Mətni çək
            text_color = QColor(opacity, opacity, opacity)
            painter.setPen(text_color)
            painter.drawText(
                10, text_y, self.width - 20, text_height,
                Qt.AlignmentFlag.AlignCenter | Qt.TextFlag.TextWordWrap,
                animated_text
            )
    
    def update_spinner(self):
        """Fırlanan yükləyicinin fırlanmasını yenilə"""
        # CSS keyframes kimi səlis fırlanma (1 saniyədə 360 dərəcə)
        self.spinner_rotation = (self.spinner_rotation + 3.6) % 360  # 60fps-də hər kadrda 3.6 dərəcə = 216°/saniyə
        self.update()
    
    def draw_spinner(self, painter, cx, cy, radius):
        """Səs dalğasının ətrafında fırlanan yükləyicini çək"""
        # Xarici fırlanan radius (səs dalğasından böyük)
        spinner_radius = radius + 30
        
        # Rəssam vəziyyətini saxla
        painter.save()
        
        # Mərkəzə köçür və fırlat
        painter.translate(cx, cy)
        painter.rotate(self.spinner_rotation)
        
        # CSS border-top və border-right kimi fırlanan yükləyicini çək
        # Boşluq olan dairəvi fırlanan yükləyici yarat (CSS versiyası kimi)
        spinner_width = 4
        gap_angle = 270  # 270 dərəcə fırlanan, 90 dərəcə boşluq
        
        # Əsas fırlanan yayı çək
        # Vəziyyətə görə fərqli rənglər istifadə et:
        # - Cavab gözləyərkən qırmızı
        # - Əmr emal edərkən sarı
        # - Əks halda normal vurğu rəngi
        if self.waiting_for_response:
            spinner_color = QColor('#FF4444')  # Cavab gözləmək üçün qırmızı
        elif self.processing_command:
            spinner_color = QColor('#FFD700')  # Əmr emal etmək üçün sarı
        else:
            spinner_color = QColor(self.colors['accent'])  # Normal vurğu rəngi
        
        pen = QPen(spinner_color, spinner_width)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(pen)
        
        # Fırlanan yayı çək (270 dərəcə)
        start_angle = 0
        span_angle = gap_angle * 16  # Qt dərəcənin 1/16-nı istifadə edir
        
        # Yay üçün yol yarat
        path = QPainterPath()
        path.arcMoveTo(-spinner_radius, -spinner_radius, spinner_radius * 2, spinner_radius * 2, start_angle)
        path.arcTo(-spinner_radius, -spinner_radius, spinner_radius * 2, spinner_radius * 2, start_angle, gap_angle)
        
        painter.drawPath(path)
        
        # Rəssam vəziyyətini bərpa et
        painter.restore()
            
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            
    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self.drag_position)
            
    def initialize_voice(self):
        self.recognizer = sr.Recognizer()
        
    def start_wake_word_detection(self):
        try:
            # Əgər artıq wake word thread-i işləyirsə, onu dayandır
            if hasattr(self, 'wake_word_thread') and self.wake_word_thread.is_alive():
                self.wake_word_listening = False
                time.sleep(1.0)  # Thread-in dayanması üçün gözlə
            
            # Yeni wake word thread-ini başlat
            self.wake_word_thread = threading.Thread(target=self.listen_for_wake_word, daemon=True)
            self.wake_word_thread.start()
            
        except Exception as e:
            self.Azer_AI.speak(f"Wake word thread başlatma xətası: {e}" if self.voice_settings['language'] == 'az-AZ' else f"Wake word thread başlatma hatası: {e}")
        
    def listen_for_wake_word(self):
        try:
            # Verilənlər bazasından wake word-ləri al
            wake_word_settings = db_manager.get_wake_word_settings(self.current_user['id'])
            
            # Əgər verilənlər bazasında wake word yoxdursa, standart istifadə et
            if wake_word_settings:
                wake_words = {
                    'az-AZ': [wake_word_settings['az_word'], f"hey {wake_word_settings['az_word']}", f"{wake_word_settings['az_word']} ai"],
                    'tr-TR': [wake_word_settings['tr_word'], f"hey {wake_word_settings['tr_word']}", f"{wake_word_settings['tr_word']} ai"]
                }
            else:
                # Standart wake word-lər
                wake_words = {
                    'az-AZ': ["azər", "hey azər", "azər ai"],
                    'tr-TR': ["azer", "hey azer", "azer ai"]
                }
        
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source)
                
                while self.wake_word_listening:
                    # Davamlı dinləmə aktivdirsə wake word dinləməni dayandır
                    if self.continuous_listening:
                        time.sleep(0.2)
                        continue
                        
                    try:
                        audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=None)
                        
                        # Əgər wake word dinləmə dayandırılıbsa, çıx
                        if not self.wake_word_listening:
                            break
                            
                        try:
                            text = self.recognizer.recognize_google(
                                audio, 
                                language=self.recognition_language
                            ).lower()
                            
                            current_wake_words = wake_words[self.voice_settings['language']]
                            if any(word in text for word in current_wake_words):
                                self.activate_assistant()
                                
                        except sr.UnknownValueError:
                            continue
                        except sr.RequestError:
                            continue
                            
                    except sr.WaitTimeoutError:
                        continue
                        
        except Exception as e:
            self.Azer_AI.speak(f"Wake word dinləmə xətası: {e}" if self.voice_settings['language'] == 'az-AZ' else f"Wake word dinleme hatası: {e}")
                    
    def activate_assistant(self):
        try:
            song = AudioSegment.from_wav("wav/listen.wav")
            play(song)
        except Exception as e:
            self.Azer_AI.speak(f"Səs faylı çalma xətası: {e}" if self.voice_settings['language'] == 'az-AZ' else f"Ses dosyası çalma hatası: {e}")
            
        self.mic_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.colors['listening']};
                border-radius: 30px;
                color: white;
                font-size: 20px;
            }}
            QPushButton:hover {{
                background-color: {self.colors['accent']};
            }}
        """)
        
        self.speak(random.choice([
            "Hə, sizi dinləyirəm." if self.voice_settings['language'] == 'az-AZ' else "Evet, sizi dinliyorum.",
            "Buyurun." if self.voice_settings['language'] == 'az-AZ' else "Buyurun.",
            "Əmrinizdəyəm." if self.voice_settings['language'] == 'az-AZ' else "Emrinizdeyim.",
            "Sizi eşidirəm." if self.voice_settings['language'] == 'az-AZ' else "Sizi duyuyorum."
        ]))
        self.listen_once_for_command()
        
    def listen_once_for_command(self):
        with sr.Microphone() as source:
            try:
                audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=None)
                
                try:
                    song = AudioSegment.from_wav("wav/start.wav")
                    play(song)
                except Exception as e:
                    self.Azer_AI.speak(f"Səs faylı çalma xətası: {e}" if self.voice_settings['language'] == 'az-AZ' else f"Ses dosyası çalma hatası: {e}")
                
                text = self.recognizer.recognize_google(
                    audio, 
                    language=self.recognition_language
                )
                self.process_command(text)
                
            except (sr.UnknownValueError, sr.RequestError, sr.WaitTimeoutError):
                self.speak(
                    "Sizi başa düşə bilmədim" 
                    if self.voice_settings['language'] == 'az-AZ' 
                    else "Sizi anlayamadım"
                )
            finally:
                self.mic_button.setStyleSheet(f"""
                    QPushButton {{
                        background-color: {self.colors['primary']};
                        border-radius: 30px;
                        color: white;
                        font-size: 20px;
                    }}
                    QPushButton:hover {{
                        background-color: {self.colors['accent']};
                    }}
                """)
                
    def process_command(self, command):
        # Emal etmə vəziyyətini sarı fırlanan yükləyicini göstərmək üçün True et
        self.processing_command = True
        self.update()  # Sarı fırlanan yükləyicini göstərmək üçün UI-ni məcburi yenilə
        
        try:
            self.commands.process_command(command)
        finally:
            # Emal etmə vəziyyətini yenidən False et
            self.processing_command = False
            self.update()  # Normal fırlanan yükləyicini göstərmək üçün UI-ni məcburi yenilə
        
    def toggle_continuous_listening(self):
        """Davamlı dinləmə rejimini dəyişdir"""
        import threading
        import time
        
        self.continuous_listening = not self.continuous_listening
        
        if self.continuous_listening:
            # Davamlı dinləməni başlat - qırmızı rənglər
            self.mic_button.setStyleSheet(f"""
                QPushButton {{
                    background-color: {self.colors['listening']};
                    border-radius: 30px;
                    color: white;
                    font-size: 20px;
                    border: 2px solid {self.colors['listening']};
                }}
                QPushButton:hover {{
                    background-color: {self.colors['accent']};
                    border: 2px solid {self.colors['accent']};
                }}
            """)
            self.status_label.setText(
                "🎧 Davamlı Dinləmə Aktivdir..."
            )
            self.status_label.setStyleSheet(f"color: {self.colors['listening']}; font-size: 10px; background-color: rgba(0, 0, 0, 0.7); padding: 5px; border-radius: 10px;")
            
            # Wake word dinləməni dayandır
            self.wake_word_listening = False
            
            # Əvvəlki thread-i təmizlə
            if hasattr(self, 'continuous_thread') and self.continuous_thread.is_alive():
                # Thread-in dayanması üçün qısa gözləmə
                time.sleep(0.5)
            
            # Davamlı dinləmə thread-ini başlat
            self.continuous_thread = threading.Thread(target=self.continuous_listen, daemon=True)
            self.continuous_thread.start()
        else:
            # Davamlı dinləməni dayandır - orijinal rənglər
            self.mic_button.setStyleSheet(f"""
                QPushButton {{
                    background-color: {self.colors['primary']};
                    border-radius: 30px;
                    color: white;
                    font-size: 20px;
                    border: 2px solid {self.colors['accent']};
                }}
                QPushButton:hover {{
                    background-color: {self.colors['accent']};
                    border: 2px solid {self.colors['primary']};
                }}
            """)
            self.status_label.setText(
                "🎧 Sizi Dinləyirəm..."
            )
            self.status_label.setStyleSheet(f"color: {self.colors['accent']}; font-size: 10px; background-color: rgba(0, 0, 0, 0.7); padding: 5px; border-radius: 10px;")
            
            # Thread-in dayanması üçün gözlə
            if hasattr(self, 'continuous_thread') and self.continuous_thread.is_alive():
                # Thread-in təhlükəsiz şəkildə dayanması üçün gözlə
                self.continuous_thread.join(timeout=2.0)  # Maksimum 2 saniyə gözlə
                if self.continuous_thread.is_alive():
                    pass  # Thread dayandırıla bilmədi, amma davam et
            
            # Wake word dinləməni yenidən başlat
            threading.Thread(target=self.restart_wake_word_detection, daemon=True).start()

    def restart_wake_word_detection(self):
        """Wake word dinləməni yenidən başlat"""
        import threading
        import time
        
        try:
            
            # Əvvəlki wake word thread-ini təmizlə
            if hasattr(self, 'wake_word_thread') and self.wake_word_thread.is_alive():
                # Thread-in dayanması üçün qısa gözləmə
                time.sleep(1.0)
            
            # Wake word dinləməni yenidən başlat
            self.wake_word_listening = True
            
            # Wake word dinləmə thread-ini yenidən başlat
            self.start_wake_word_detection()
            
            # Status mesajını yenilə
            self.status_label.setText("🎧 Sizi Dinləyirəm...")
            self.status_label.setStyleSheet(f"color: {self.colors['accent']}; font-size: 10px; background-color: rgba(0, 0, 0, 0.7); padding: 5px; border-radius: 10px;")
            
            
        except Exception as e:
            self.Azer_AI.speak(f"Wake word yenidən başlatma xətası: {e}" if self.voice_settings['language'] == 'az-AZ' else f"Wake word yeniden başlatma hatası: {e}")
            # Xəta zamanı yenidən cəhd et
            try:
                time.sleep(1.0)
                self.wake_word_listening = True
                self.start_wake_word_detection()
            except Exception as retry_error:
                self.Azer_AI.speak(f"Wake word yenidən başlatma cəhdi də uğursuz: {retry_error}" if self.voice_settings['language'] == 'az-AZ' else f"Wake word yeniden başlatma denemesi de başarısız: {retry_error}")
        
    def continuous_listen(self):
        """Davamlı dinləmə funksiyası"""
        import threading
        import time
        
        # Thread ID-ni saxla
        self.continuous_thread_id = threading.current_thread().ident
        
        try:
            with sr.Microphone() as source:
                # Ətraf səsə uyğunlaşma
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                
                # Thread dayandırma dəyişəni
                stop_listening = threading.Event()
                
                while self.continuous_listening and not stop_listening.is_set():
                    try:
                        # Daha qısa timeout ilə dinləmə (thread dayandırma üçün)
                        audio = self.recognizer.listen(source, timeout=0.5, phrase_time_limit=None)
                        
                        # Əgər davamlı dinləmə dayandırılıbsa, dərhal çıx
                        if not self.continuous_listening or stop_listening.is_set():
                            break
                            
                        try:
                            text = self.recognizer.recognize_google(
                                audio, 
                                language=self.recognition_language
                            ).lower()
                            
                            if text.strip():
                                try:
                                    song = AudioSegment.from_wav("wav/start.wav")
                                    play(song)
                                except Exception as e:
                                    self.Azer_AI.speak(f"Səs faylı çalma xətası: {e}" if self.voice_settings['language'] == 'az-AZ' else f"Ses dosyası çalma hatası: {e}")
                                    
                                self.process_command(text)
                                
                        except sr.UnknownValueError:
                            continue
                        except sr.RequestError:
                            self.speak(
                                "İnternetlə bağlı problemlərim var." 
                                if self.voice_settings['language'] == 'az-AZ' 
                                else "İnternet bağlantısında sorun var."
                            )
                            break
                    except sr.WaitTimeoutError:
                        # Timeout zamanı thread dayandırma yoxlaması
                        if not self.continuous_listening or stop_listening.is_set():
                            break
                        continue
                    except Exception as e:
                        self.Azer_AI.speak(f"Dinləmə xətası: {str(e)}" if self.voice_settings['language'] == 'az-AZ' else f"Dinleme hatası: {str(e)}")
                        break
                        
        except Exception as e:
            self.Azer_AI.speak(f"Davamlı dinləmə xətası: {e}" if self.voice_settings['language'] == 'az-AZ' else f"Sürekli dinleme hatası: {e}")
        finally:
            # Thread bitəndə təmizlik işləri
            self.continuous_thread_id = None
                    
    def show_language_menu(self):
        """Dil və səs parametrləri menyusunu göstər"""
        menu = QMenu(self)
        menu.setStyleSheet(f"""
            QMenu {{
                background-color: {self.colors['bg']};
                color: {self.colors['text']};
                border: 1px solid {self.colors['primary']};
                border-radius: 5px;
                padding: 5px;
            }}
            QMenu::item {{
                padding: 8px 15px;
                border-radius: 3px;
            }}
            QMenu::item:selected {{
                background-color: {self.colors['primary']};
            }}
        """)
        
        # Dil altmenyusu
        lang_menu = QMenu("🌐 Dil seçimi", menu)
        lang_menu.setStyleSheet(menu.styleSheet())
        
        # Azərbaycan dili
        az_action = QAction("🇦🇿 Azərbaycan dili", lang_menu)
        az_action.triggered.connect(lambda: self.change_language('az-AZ'))
        lang_menu.addAction(az_action)
        
        # Türk dili
        tr_action = QAction("🇹🇷 Türk dili", lang_menu)
        tr_action.triggered.connect(lambda: self.change_language('tr-TR'))
        lang_menu.addAction(tr_action)
        
        menu.addMenu(lang_menu)
        
        # Səs cinsi altmenyusu
        voice_menu = QMenu("🎤 Səs cinsi", menu)
        voice_menu.setStyleSheet(menu.styleSheet())
        
        # Kişi səsi
        male_action = QAction("👨 Kişi səsi", voice_menu)
        male_action.triggered.connect(lambda: self.change_voice_gender('male'))
        voice_menu.addAction(male_action)
        
        # Qadın səsi
        female_action = QAction("👩 Qadın səsi", voice_menu)
        female_action.triggered.connect(lambda: self.change_voice_gender('female'))
        voice_menu.addAction(female_action)
        
        menu.addMenu(voice_menu)
        
        
        # Menyunu düymənin mövqeyində göstər
        button_pos = self.lang_button.mapToGlobal(self.lang_button.rect().bottomLeft())
        menu.exec(button_pos)
    
    def change_language(self, language):
        """Dili dəyiş"""
        self.voice_settings['language'] = language
        self.recognition_language = self.recognition_languages[language]
        self.save_voice_settings()
        
        # İstifadəçiyə məlumat ver
        if language == 'az-AZ':
            self.speak("Dil Azərbaycancaya dəyişdirildi")
        else:
            self.speak("Dil Türk dilinə dəyişdirildi")
    
    def change_voice_gender(self, gender):
        """Səs cinsini dəyiş"""
        self.voice_settings['voice_gender'] = gender
        self.save_voice_settings()
        
        # İstifadəçiyə məlumat ver
        if gender == 'male':
            if self.voice_settings['language'] == 'az-AZ':
                self.speak("Kişi səsi seçildi")
            else:
                self.speak("Erkek sesi seçildi")
        else:
            if self.voice_settings['language'] == 'az-AZ':
                self.speak("Qadın səsi seçildi")
            else:
                self.speak("Kadın sesi seçildi")
    
            
    def speak(self, text):
        self.current_speech = text
        self.speech_active = True
        
        # Mətn animasiyasını sıfırla
        self.text_animation_index = 0
        self.last_text_animation_time = time.time()
        
        # Seçilmiş TTS mühərriki istifadə edərək danış
        if self.voice_settings['tts_engine'] == 'edge':
            asyncio.run(self.edge_speak(text))
        else:
            self.gtts_speak(text)
            
        self.speech_active = False
        self.speech_fade_time = time.time()

    def listen_for_response(self, timeout=10):
        """İstifadəçidən səsli cavab gözləyir"""
        # Cavab gözləmə vəziyyətini başlat
        self.waiting_for_response = True
        self.text_response = None
        
        # Qırmızı fırlanan yükləyicini göstərmək üçün UI-ni məcburi yenilə
        self.update()
        
        try:
            # Statusu yenilə
            self.status_label.setText("🎤 Cavabınızı gözləyirəm...")
            self.status_label.setStyleSheet(f"color: {self.colors['error']}; font-size: 10px; background-color: rgba(0, 0, 0, 0.7); padding: 5px; border-radius: 10px;")
            
            # Mikrofon düyməsini qırmızı et
            self.mic_button.setStyleSheet(f"""
                QPushButton {{
                    background-color: {self.colors['error']};
                    border-radius: 30px;
                    color: white;
                    font-size: 20px;
                }}
                QPushButton:hover {{
                    background-color: {self.colors['accent']};
                }}
            """)
            
            # Səs effekti
            try:
                song = AudioSegment.from_wav("wav/listen.wav")
                play(song)
            except Exception as e:
                self.Azer_AI.speak(f"Səs faylı çalma xətası: {e}" if self.voice_settings['language'] == 'az-AZ' else f"Ses dosyası çalma hatası: {e}")
            
            # Mikrofon dinləmə threadini başlat
            mic_thread = threading.Thread(target=self.listen_mic_for_response, daemon=True)
            mic_thread.start()
            
            # Səsli cavab gələnə qədər və ya vaxt bitənə qədər gözlə
            start_time = time.time()
            while self.waiting_for_response and (time.time() - start_time < timeout):
                # GUI yeniləməsi
                QApplication.processEvents()
                
                # Səlis animasiya üçün hər 100ms-də fırlanan yükləyicini məcburi yenilə
                self.update()
                
                # Səsli cavab alındısa
                if self.text_response:
                    return self.text_response
                
                # Qısa bir gözləmə
                time.sleep(0.1)
            
            # Vaxt bitdi və ya cavab alındı
            if not self.text_response and self.waiting_for_response:
                self.speak("Cavab gözləmə müddəti bitdi." if self.voice_settings['language'] == 'az-AZ' else "Cevap bekleme süresi doldu.")
            
            return self.text_response
            
        finally:
            # Cavab gözləmə vəziyyətini sıfırla
            self.waiting_for_response = False
            
            # Normal fırlanan yükləyicini göstərmək üçün UI-ni məcburi yenilə
            self.update()
            
            # Mikrofon düyməsini vəziyyətə görə tənzimlə
            if self.continuous_listening:
                # Davamlı dinləmə aktivdirsə qırmızı rənglər
                self.mic_button.setStyleSheet(f"""
                    QPushButton {{
                        background-color: {self.colors['listening']};
                        border-radius: 30px;
                        color: white;
                        font-size: 20px;
                        border: 2px solid {self.colors['listening']};
                    }}
                    QPushButton:hover {{
                        background-color: {self.colors['accent']};
                        border: 2px solid {self.colors['accent']};
                    }}
                """)
                self.status_label.setText("🎧 Davamlı Dinləmə Aktivdir...")
                self.status_label.setStyleSheet(f"color: {self.colors['listening']}; font-size: 10px; background-color: rgba(0, 0, 0, 0.7); padding: 5px; border-radius: 10px;")
            else:
                # Normal dinləmə rejimində orijinal rənglər
                self.mic_button.setStyleSheet(f"""
                    QPushButton {{
                        background-color: {self.colors['primary']};
                        border-radius: 30px;
                        color: white;
                        font-size: 20px;
                        border: 2px solid {self.colors['accent']};
                    }}
                    QPushButton:hover {{
                        background-color: {self.colors['accent']};
                        border: 2px solid {self.colors['primary']};
                    }}
                """)
                self.status_label.setText("🎧 Sizi Dinləyirəm...")
                self.status_label.setStyleSheet(f"color: {self.colors['accent']}; font-size: 10px; background-color: rgba(0, 0, 0, 0.7); padding: 5px; border-radius: 10px;")

    def listen_mic_for_response(self):
        """Mikrofon ilə cavab dinləmə (ayrı threaddə işləyir)"""
        if not self.waiting_for_response:
            return
        
        try:
            with sr.Microphone() as source:
                # Ətraf səsə uyğunlaşma
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
                                self.Azer_AI.speak(f"Səs faylı çalma xətası: {e}" if self.voice_settings['language'] == 'az-AZ' else f"Ses dosyası çalma hatası: {e}")
                            
                            # Cavabı saxla
                            self.text_response = response.lower()
                            self.waiting_for_response = False
                            
                            # Normal fırlanan yükləyicini göstərmək üçün UI-ni məcburi yenilə
                            self.update()
                            
                        except sr.UnknownValueError:
                            self.speak("Üzr istəyirəm, dediyinizi başa düşə bilmədim." if self.voice_settings['language'] == 'az-AZ' else "Üzgünüm, söylediğinizi anlayamadım.")
                        except sr.RequestError:
                            self.speak("İnternetlə bağlı problemlərim var." if self.voice_settings['language'] == 'az-AZ' else "İnternet bağlantısında sorun var.")
                except sr.WaitTimeoutError:
                    pass
        except Exception as e:
            self.speak(f"Mikrofon dinləmə xətası: {str(e)}" if self.voice_settings['language'] == 'az-AZ' else f"Mikrofon dinleme hatası: {str(e)}")
            
    async def edge_speak(self, text):
        """Edge TTS istifadə edərək mətni səsə çevir"""
        try:
            # Dil və cinsə görə səsi seç
            voice = self.voice_options[self.voice_settings['language']][self.voice_settings['voice_gender']]
            
            communicate = edge_tts.Communicate(text, voice)
            
            # Müvəqqəti fayl yarat
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as fp:
                temp_filename = fp.name
                
            # Səsi saxla    
            await communicate.save(temp_filename)
            
            # Səsi çal
            pygame.mixer.init()
            pygame.mixer.music.load(temp_filename)
            pygame.mixer.music.play()
            
            # Səsin bitməsini gözlə
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
                
            pygame.mixer.quit()
            os.unlink(temp_filename)
            
        except Exception as e:
            self.Azer_AI.speak(f"Edge TTS xətası: {str(e)}" if self.voice_settings['language'] == 'az-AZ' else f"Edge TTS hatası: {str(e)}")
            # Xəta zamanı gTTS-ə keç
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
            self.Azer_AI.speak(f"gTTS xətası: {str(e)}" if self.voice_settings['language'] == 'az-AZ' else f"gTTS hatası: {str(e)}")
            
    def load_custom_commands(self):
        """Xüsusi əmrləri yüklə"""
        try:
            from db_manager import db_manager
            
            # İstifadəçinin xüsusi əmrlərini verilənlər bazasından al
            db_commands = db_manager.get_custom_commands(self.current_user['id'])
            
            if not db_commands:
                return []
                
            # Verilənlər bazası formatını tətbiq formatına çevir
            commands = []
            for cmd in db_commands:
                # Tətikləyiciləri siyahılara böl
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
            self.Azer_AI.speak(f"Xüsusi əmrlər yüklənərkən xəta: {e}" if self.voice_settings['language'] == 'az-AZ' else f"Özel komutlar yüklenirken hata: {e}")
            return []
            

            
    def closeEvent(self, event):
        import threading
        import time
        
        
        # Bütün dinləmə thread-lərini dayandır
        self.wake_word_listening = False
        self.continuous_listening = False
        
        # Davamlı dinləmə thread-ini təhlükəsiz şəkildə dayandır
        if hasattr(self, 'continuous_thread') and self.continuous_thread.is_alive():
            self.continuous_thread.join(timeout=3.0)  # 3 saniyə gözlə
            if self.continuous_thread.is_alive():
                pass  # Thread dayandırıla bilmədi, amma davam et
        
        # Wake word thread-ini təhlükəsiz şəkildə dayandır
        if hasattr(self, 'wake_word_thread') and self.wake_word_thread.is_alive():
            self.wake_word_thread.join(timeout=2.0)  # 2 saniyə gözlə
            if self.wake_word_thread.is_alive():
                pass  # Thread dayandırıla bilmədi, amma davam et
        
        # Audio stream-ləri təmizlə
        try:
            if hasattr(self, 'stream'):
                self.stream.stop_stream()
                self.stream.close()
            if hasattr(self, 'audio'):
                self.audio.terminate()
        except Exception as e:
            self.Azer_AI.speak(f"Audio stream təmizləmə xətası: {e}" if self.voice_settings['language'] == 'az-AZ' else f"Audio stream temizleme hatası: {e}")
        
        # Timer-ləri dayandır
        try:
            if hasattr(self, 'license_timer'):
                self.license_timer.stop()
            if hasattr(self, 'animation_timer'):
                self.animation_timer.stop()
            if hasattr(self, 'spinner_timer'):
                self.spinner_timer.stop()
        except Exception as e:
            self.Azer_AI.speak(f"Timer dayandırma xətası: {e}" if self.voice_settings['language'] == 'az-AZ' else f"Timer durdurma hatası: {e}")
        
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Daha müasir görünüş
    
    # Versiya yoxlaması
    if not check_version():
        sys.exit()
    
    
    # Əvvəlcə girişi idarə et
    login_screen = LoginScreen()
    login_success, user_info = login_screen.run()
    
    # Əgər giriş uğursuz oldu, tətbiqi bağla
    if not login_success:
        sys.exit()
    
    # Yükləmə ekranını yarat
    loading = LoadingScreen()
    
    # Əsas pəncərəni yarat amma hələ göstərmə
    window = MiniAzer_AI(user_info)
    
    # Yükləmə bitəndə nə baş verəcəyini təyin et
    def on_loading_finished():
        window.show()
    
    loading.on_finished = on_loading_finished
    loading.show()
    
    sys.exit(app.exec()) 