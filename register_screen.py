from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                            QLabel, QLineEdit, QPushButton, QFrame, QMessageBox, QCheckBox)
from PyQt6.QtCore import Qt, QSize, QTimer
from PyQt6.QtGui import QFont, QIcon
from db_manager import db_manager
import json
import os
version_data = db_manager.get_version()
from encryption_utils import encrypt_data

class RegisterScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.is_success = False
        self.countdown = 5  # Geri sayım üçün
        self.login_file = "login.json"
        
        # Rəng sxemi - GitHub Dark tema uyğun
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
        
        self.setup_window()
        self.create_interface()
        
    def save_login_credentials(self, username, password):
        """Giriş məlumatlarını login.json faylına şifrəli yadda saxlayır (data açarı ilə)"""
        try:
            login_data = {
                'username': username,
                'password': password
            }
            encrypted = encrypt_data(json.dumps(login_data)).decode('utf-8')
            wrapper = {'data': encrypted}
            with open(self.login_file, 'w', encoding='utf-8') as f:
                json.dump(wrapper, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Giriş məlumatları yadda saxlanarkən xəta: {str(e)}")
        
    def setup_window(self):
        self.setWindowTitle("Azer AI Qeydiyyat")
        self.setStyleSheet(f"background-color: {self.colors['bg']};")
        self.setWindowIcon(QIcon('images/logo.ico'))

        window_width = 400
        window_height = 500  # Bir az daha yüksək etdim
        
        screen_geometry = QApplication.primaryScreen().geometry()
        center_x = int(screen_geometry.width()/2 - window_width/2)
        center_y = int(screen_geometry.height()/2 - window_height/2)
        
        self.setGeometry(center_x, center_y, window_width, window_height)
        self.setFixedSize(window_width, window_height)

    def create_interface(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(10)
        
        # Başlıq
        title_label = QLabel("AZER AI " + version_data['version'])
        title_label.setFont(QFont("Helvetica", 36, QFont.Weight.Bold))
        title_label.setStyleSheet(f"color: {self.colors['primary']};")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)
        
        # Alt başlıq
        subtitle_label = QLabel("Qeydiyyat")
        subtitle_label.setFont(QFont("Helvetica", 14))
        subtitle_label.setStyleSheet(f"color: {self.colors['text_secondary']};")
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(subtitle_label)
        
        main_layout.addSpacing(40)
        
        # Ad daxiletməsi
        self.name_entry = QLineEdit()
        self.name_entry.setPlaceholderText("Ad")
        self.name_entry.setMinimumHeight(40)
        self.name_entry.setStyleSheet(f"""
            QLineEdit {{
                background-color: {self.colors['bg_secondary']};
                color: {self.colors['text']};
                border: 1px solid {self.colors['primary']};
                border-radius: 5px;
                padding: 5px;
                font-size: 12pt;
            }}
        """)
        main_layout.addWidget(self.name_entry)
        
        # İstifadəçi adı daxiletməsi
        self.username_entry = QLineEdit()
        self.username_entry.setPlaceholderText("İstifadəçi Adı")
        self.username_entry.setMinimumHeight(40)
        self.username_entry.setStyleSheet(f"""
            QLineEdit {{
                background-color: {self.colors['bg_tertiary']};
                color: {self.colors['text']};
                border: 1px solid {self.colors['border']};
                border-radius: 5px;
                padding: 5px;
                font-size: 12pt;
            }}
            QLineEdit:hover {{
                border: 1px solid {self.colors['primary']};
                background-color: {self.colors['bg_secondary']};
            }}
            QLineEdit:focus {{
                border: 2px solid {self.colors['accent']};
                background-color: {self.colors['bg_secondary']};
            }}
        """)
        main_layout.addWidget(self.username_entry)
        
        # Şifrə daxiletməsi
        self.password_entry = QLineEdit()
        self.password_entry.setPlaceholderText("Parol")
        self.password_entry.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_entry.setMinimumHeight(40)
        self.password_entry.setStyleSheet(f"""
            QLineEdit {{
                background-color: {self.colors['bg_tertiary']};
                color: {self.colors['text']};
                border: 1px solid {self.colors['border']};
                border-radius: 5px;
                padding: 5px;
                font-size: 12pt;
            }}
            QLineEdit:hover {{
                border: 1px solid {self.colors['primary']};
                background-color: {self.colors['bg_secondary']};
            }}
            QLineEdit:focus {{
                border: 2px solid {self.colors['accent']};
                background-color: {self.colors['bg_secondary']};
            }}
        """)
        main_layout.addWidget(self.password_entry)
        
        main_layout.addSpacing(20)
        
        # Məni xatırla checkbox-ı
        self.remember_me = QCheckBox("Məni xatırla")
        self.remember_me.setStyleSheet(f"""
            QCheckBox {{
                color: {self.colors['text']};
                font-size: 11pt;
            }}
            QCheckBox::indicator {{
                width: 18px;
                height: 18px;
            }}
            QCheckBox::indicator:unchecked {{
                border: 2px solid {self.colors['primary']};
                background-color: {self.colors['bg_secondary']};
                border-radius: 3px;
            }}
            QCheckBox::indicator:checked {{
                border: 2px solid {self.colors['primary']};
                background-color: {self.colors['primary']};
                border-radius: 3px;
            }}
        """)
        main_layout.addWidget(self.remember_me)
        
        # Qeydiyyat ol düyməsi
        self.register_button = QPushButton("Qeydiyyatdan keç")
        self.register_button.setMinimumHeight(40)
        self.register_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.colors['primary']};
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 12pt;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {self.colors['secondary']};
            }}
        """)
        self.register_button.clicked.connect(self.register)
        main_layout.addWidget(self.register_button)

        # Girişə qayıt düyməsi
        self.back_to_login_button = QPushButton("Girişə qayıt")
        self.back_to_login_button.setMinimumHeight(36)
        self.back_to_login_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.colors['bg_secondary']};
                color: {self.colors['primary']};
                border: 1px solid {self.colors['primary']};
                border-radius: 5px;
                font-size: 11pt;
            }}
            QPushButton:hover {{
                background-color: {self.colors['secondary']};
                color: white;
            }}
        """)
        self.back_to_login_button.clicked.connect(self.close)
        main_layout.addWidget(self.back_to_login_button)
        
        # Xəta mesajı etiketi
        self.error_label = QLabel("")
        self.error_label.setStyleSheet(f"color: {self.colors['error']};")
        self.error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.error_label)
        
        # Enter düyməsinə basanda qeydiyyat ol
        self.password_entry.returnPressed.connect(self.register)
        
        main_layout.addStretch(1)

    def register(self):
        name = self.name_entry.text()
        username = self.username_entry.text()
        password = self.password_entry.text()
        
        if not name or not username or not password:
            self.error_label.setText("Zəhmət olmasa bütün sahələri doldurun!")
            return
        
        # İstifadəçi adı yoxlaması
        if db_manager.user_exists(username):
            self.error_label.setText("Bu istifadəçi adı artıq mövcuddur!")
            return
        
        # Yeni istifadəçi yarat
        new_user = {
            'name': name,
            'username': username,
            'password': password,
            'role': 'user',
            'license_status': 'free'
        }
        
        if db_manager.create_user(new_user):
            # Əgər "Məni xatırla" seçilibsə giriş məlumatlarını yadda saxla
            if self.remember_me.isChecked():
                self.save_login_credentials(username, password)
                
            self.error_label.setStyleSheet(f"color: {self.colors['success']};")
            self.register_button.setEnabled(False)
            self.register_button.setText("✓ Qeydiyyat Uğurlu")
            self.register_button.setStyleSheet(f"""
                QPushButton {{
                    background-color: {self.colors['success']};
                    color: white;
                    border: none;
                    border-radius: 5px;
                    font-size: 12pt;
                    font-weight: bold;
                }}
            """)
            
            # Geri sayım başlat
            self.countdown = 5
            self.update_countdown()
            self.countdown_timer = QTimer()
            self.countdown_timer.timeout.connect(self.update_countdown)
            self.countdown_timer.start(1000)  # Hər saniyə
        else:
            self.error_label.setText("Qeydiyyat zamanı xəta baş verdi!")

    def update_countdown(self):
        """Geri sayımı yenilə"""
        if self.countdown > 0:
            self.error_label.setText(f"Qeydiyyat uğurla tamamlandı! {self.countdown} saniyə sonra yönləndirilirsiniz...")
            self.countdown -= 1
        else:
            self.countdown_timer.stop()
            self.is_success = True
            self.close()

    def run(self):
        self.show()
        while self.isVisible():
            QApplication.processEvents()
        return self.is_success 