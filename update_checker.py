"""
update_checker.py

Bu modul, Azer AI tətbiqinin yeniləmələrini yoxlamaq üçün bir interfeys təqdim edir.
Verilənlər bazasındakı son versiya ilə mövcud versiyanı müqayisə edir və yeni bir versiya varsa istifadəçiyə bildirir.
İstifadəçi yeniləmə etmək istəsə müvafiq veb səhifə açılır.
"""
import sys
import webbrowser
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QLabel, QPushButton, QMessageBox, QHBoxLayout, QFrame)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QIcon
from db_manager import db_manager

class UpdateChecker(QMainWindow):
    """
    Azer AI tətbiqi üçün yeniləmə yoxlama pəncərəsini göstərən əsas pəncərə sinifi.
    İstifadəçiyə mövcud və yeni versiya məlumatlarını təqdim edir, yeniləmə və ya daha sonra seçimi verir.
    """
    def __init__(self):
        super().__init__()
        
        # GitHub Dark tema rəng sxemi
        self.colors = {
            'bg': '#0D1117',  # GitHub Dark tema arxa fon
            'bg_secondary': '#161B22',  # GitHub Dark tema ikincil arxa fon
            'bg_tertiary': '#21262D',  # Üçüncül arxa fon
            'primary': '#58A6FF',  # GitHub Dark tema primary
            'secondary': '#79C0FF',  # Daha açıq primary
            'accent': '#1F6FEB',  # GitHub Dark tema accent
            'warning': '#D29922',  # GitHub Dark tema warning
            'error': '#F85149',  # GitHub Dark tema error
            'success': '#238636',  # GitHub Dark tema success
            'text': '#F0F6FC',  # GitHub Dark tema mətn
            'text_secondary': '#8B949E',  # GitHub Dark tema secondary mətn
            'text_muted': '#6E7681',  # GitHub Dark tema muted mətn
            'border': '#30363D',  # GitHub Dark tema border
            'border_secondary': '#21262D',  # İkincil border
            'overlay': '#161B22',  # Overlay rəngi
            'shadow': '#000000'  # Kölgə rəngi
        }
        
        self.setWindowTitle("Azer AI - Yeniləmə Kontrolü")
        self.setFixedSize(400, 600)
        self.setWindowIcon(QIcon('images/logo.ico'))
        self.setStyleSheet(f"background-color: {self.colors['bg']};")

        # Pəncərə ölçüsünü təyin edirik
        window_width = 400
        window_height = 600
        
        # Ekranın mərkəzində yerləşdirmə
        screen_geometry = QApplication.primaryScreen().geometry()
        center_x = int(screen_geometry.width()/2 - window_width/2)
        center_y = int(screen_geometry.height()/2 - window_height/2)
        
        self.setGeometry(center_x, center_y, window_width, window_height)
        self.setFixedSize(window_width, window_height)
        
        # Əsas widget və layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)
        
        # Logo etiketi
        logo_label = QLabel("AZER AI")
        logo_label.setFont(QFont("Helvetica", 36, QFont.Weight.Bold))
        logo_label.setStyleSheet(f"color: {self.colors['primary']};")
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(logo_label)
        
        # Alt başlıq
        subtitle_label = QLabel("Yeniləmə Kontrolü")
        subtitle_label.setFont(QFont("Helvetica", 14))
        subtitle_label.setStyleSheet(f"color: {self.colors['text_secondary']};")
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(subtitle_label)
        
        # Boşluq əlavə et
        layout.addSpacing(40)
        
        # Başlıq və versiya qutusu
        info_frame = QFrame()
        info_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {self.colors['bg_secondary']};
                border: 1px solid {self.colors['border']};
                border-radius: 5px;
                padding: 15px;
            }}
        """)
        info_layout = QVBoxLayout(info_frame)
        info_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info_layout.setSpacing(10)
        
        # Başlıq
        title = QLabel("Yeniləmə Mövcuddur!")
        title.setFont(QFont('Helvetica', 16, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(f"color: {self.colors['text']};")
        info_layout.addWidget(title)
        
        # Versiya məlumatı
        from version import VERSION
        version_data = db_manager.get_version()
        db_version = version_data['version']
        
        version_info = QLabel(f"""
        <b style='color:{self.colors['text']};'>Cari versiya:</b> <span style='color:{self.colors['text_secondary']};'>{VERSION}</span><br>
        <b style='color:{self.colors['text']};'>Yeni versiya:</b> <span style='color:{self.colors['text_secondary']};'>{db_version}</span><br><br>
        <span style='color:{self.colors['text_muted']};'>{version_data['info']}</span>
        """)
        version_info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        version_info.setWordWrap(True)
        version_info.setFont(QFont('Helvetica', 11))
        info_layout.addWidget(version_info)
        
        layout.addWidget(info_frame)
        
        # Boşluq əlavə et
        layout.addSpacing(20)
        
        # Yeniləmə düyməsi
        update_btn = QPushButton("Yenilə")
        update_btn.setMinimumHeight(50)
        update_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.colors['success']};
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 12pt;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: #2EA043;
            }}
        """)
        update_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        update_btn.clicked.connect(self.update_version)
        layout.addWidget(update_btn)
        
        # Daha sonra düyməsi
        later_btn = QPushButton("Daha Sonra")
        later_btn.setMinimumHeight(50)
        later_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.colors['bg_secondary']};
                color: {self.colors['text']};
                border: 1px solid {self.colors['primary']};
                border-radius: 5px;
                font-size: 12pt;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {self.colors['secondary']};
                color: white;
                border: none;
            }}
        """)
        later_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        later_btn.clicked.connect(self.close)
        layout.addWidget(later_btn)
        
        # Boşluq əlavə et
        layout.addStretch(1)

    def update_version(self):
        """
        İstifadəçi yeniləmə düyməsinə basdığında, yeniləmə veb səhifəsini açır.
        Xəta baş verərsə istifadəçiyə mesaj qutusu ilə bildirir.
        """
        try:
            # Veb səhifəni aç
            version_data = db_manager.get_version()
            webbrowser.open(version_data['web_url'])
            self.close()
            
        except Exception as e:
            QMessageBox.critical(self, "Xəta", f"Səhifə açılarkən xəta baş verdi: {str(e)}")

def check_version():
    """
    Tətbiqin mövcud versiyasını verilənlər bazasındakı son versiya ilə müqayisə edir.
    Əgər yeni bir versiya varsa yeniləmə pəncərəsini göstərir, əks halda True qaytarır.
    """
    from version import VERSION
    version_data = db_manager.get_version()
    db_version = version_data['version']
    
    if VERSION != db_version:
        app = QApplication(sys.argv)
        app.setStyle('Fusion')
        window = UpdateChecker()
        window.show()
        sys.exit(app.exec())
    else:
        return True 