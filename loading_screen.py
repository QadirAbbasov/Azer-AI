import time
import threading
import math
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel, 
                            QProgressBar, QFrame)
from PyQt6.QtCore import Qt, QTimer, QSize, pyqtSignal, QObject
from PyQt6.QtGui import QFont, QPainter, QPen, QColor, QIcon
from db_manager import db_manager
version_data = db_manager.get_version()

class SignalEmitter(QObject):
    """PyQt siqnalları üçün köməkçi sinif"""
    progress_updated = pyqtSignal(int)
    message_updated = pyqtSignal(str)
    loading_finished = pyqtSignal()

class LoadingScreen(QWidget):
    def __init__(self):
        super().__init__()
        
        # Rənglər - GitHub Dark tema uyğun
        self.colors = {
            'bg': '#0D1117',  # GitHub Dark tema arxa fon
            'fg': '#58A6FF',  # GitHub Dark tema primary
            'text': '#F0F6FC'  # GitHub Dark tema mətn
        }
        
        # İdarəetmə dəyişənləri
        self.is_running = True
        self.progress = 0
        self.current_message = 0
        
        # Yükləmə mesajları
        self.loading_messages = [
            "Sistemlər başladılır...",
            "Azer AI " + version_data['version'] + " başladılır...",
            "Süni intellekt modulları yüklənir...",
            "Səsin tanınması sistemi hazırlanır...",
            "Vizual interfeysin yaradılması...",
            "Son yoxlamalar aparılır..."
        ]
        
        # Sinyal emitter
        self.signals = SignalEmitter()
        self.signals.progress_updated.connect(self.update_progress)
        self.signals.message_updated.connect(self.update_message)
        self.signals.loading_finished.connect(self.close_window)
        
        self.setup_window()
        self.create_widgets()
        
    def setup_window(self):
        self.setWindowTitle("Azer AI Gözləyin")
        self.setStyleSheet(f"background-color: {self.colors['bg']};")
        self.setWindowIcon(QIcon('images/logo.ico'))
        
        # Pəncərəni pəncərəsiz et
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        
        # Pəncərə ölçüsünü təyin et
        self.width = 600
        self.height = 400
        
        # Ekranın mərkəzində yerləşdirmə
        screen_geometry = QApplication.primaryScreen().geometry()
        center_x = int(screen_geometry.width()/2 - self.width/2)
        center_y = int(screen_geometry.height()/2 - self.height/2)
        
        self.setGeometry(center_x, center_y, self.width, self.height)
        
        # Həmişə yuxarıda
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)
        
    def create_widgets(self):
        # Əsas layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Logo canvas əvəzinə QFrame istifadə edirik
        self.logo_frame = QFrame()
        self.logo_frame.setMinimumSize(150, 150)
        self.logo_frame.setStyleSheet(f"background-color: {self.colors['bg']};")
        self.logo_frame.paintEvent = self.paint_logo
        main_layout.addWidget(self.logo_frame, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Yüklənir mesajı
        self.loading_label = QLabel(self.loading_messages[0])
        self.loading_label.setFont(QFont("Helvetica", 14))
        self.loading_label.setStyleSheet(f"color: {self.colors['text']};")
        self.loading_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.loading_label)
        
        # İrəliləmə çubuğu
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setFixedHeight(15)
        self.progress_bar.setStyleSheet(f"""
            QProgressBar {{
                background-color: #2A2A2A;
                border-radius: 7px;
            }}
            QProgressBar::chunk {{
                background-color: {self.colors['fg']};
                border-radius: 7px;
            }}
        """)
        main_layout.addWidget(self.progress_bar)
        
        # Faiz etiketi
        self.percentage_label = QLabel("0%")
        self.percentage_label.setFont(QFont("Helvetica", 12))
        self.percentage_label.setStyleSheet(f"color: {self.colors['fg']};")
        self.percentage_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.percentage_label)
        
        # Logo animasiyası üçün timer
        self.animation_timer = QTimer(self)
        self.animation_timer.timeout.connect(self.update_logo)
        self.animation_angle = 0
        
    def paint_logo(self, event):
        """Logo çəkimi"""
        painter = QPainter(self.logo_frame)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Mərkəz nöqtəsi
        center_x = self.logo_frame.width() // 2
        center_y = self.logo_frame.height() // 2
        
        # Xarici dairə
        painter.setPen(QPen(QColor(self.colors['fg']), 2))
        painter.drawEllipse(center_x - 60, center_y - 60, 120, 120)
        
        # Fırlanan nöqtə
        x = center_x + 60 * math.cos(math.radians(self.animation_angle))
        y = center_y + 60 * math.sin(math.radians(self.animation_angle))
        painter.setBrush(QColor(self.colors['fg']))
        painter.drawEllipse(int(x) - 5, int(y) - 5, 10, 10)
        
        # Daxili dairə
        painter.setPen(QPen(QColor(self.colors['fg']), 2))
        painter.drawEllipse(center_x - 30, center_y - 30, 60, 60)
        
    def update_logo(self):
        """Logo animasiyasını yenilə"""
        self.animation_angle += 10
        if self.animation_angle >= 360:
            self.animation_angle = 0
        self.logo_frame.update()
        
    def update_progress(self, value):
        """İrəliləmə çubuğunu yenilə"""
        self.progress_bar.setValue(value)
        self.percentage_label.setText(f"{value}%")
        
    def update_message(self, message):
        """Yükləmə mesajını yenilə"""
        self.loading_label.setText(message)
        
    def close_window(self):
        """Pəncərəni bağla"""
        self.animation_timer.stop()
        self.close()
        
    def update_loading(self):
        """Yükləmə əməliyyatını yenilə (ayrı thread-də işləyir)"""
        while self.is_running and self.progress < 100:
            time.sleep(0.1)
            self.progress += 1
            
            # Siqnal göndər
            self.signals.progress_updated.emit(self.progress)
            
            # Hər %20-də bir mesajı dəyişdir
            if self.progress % 20 == 0:
                self.current_message = (self.current_message + 1) % len(self.loading_messages)
                self.signals.message_updated.emit(self.loading_messages[self.current_message])
                
        if self.is_running:
            # Yükləmə tamamlandı, pəncərəni bağla
            time.sleep(0.5)
            self.signals.loading_finished.emit()
        
    def start(self):
        """Yükləmə ekranını başlat"""
        try:
            # Logo animasiyasını başlat
            self.animation_timer.start(50)
            
            # Yükləmə əməliyyatını ayrı thread-də başlat
            threading.Thread(target=self.update_loading, daemon=True).start()
            
            # Pəncərəni göstər
            self.show()
            
            # Tətbiq döngüsünü başlat
            app = QApplication.instance()
            if app is None:
                app = QApplication([])
            app.exec()
            
        except Exception as e:
            # Yükləmə ekranı xətası:
            self.close() 