from datetime import datetime
import json
import os
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                            QLabel, QLineEdit, QPushButton, QFrame, QMessageBox)
from PyQt6.QtCore import Qt, QSize, QTimer
from PyQt6.QtGui import QFont, QIcon
from db_manager import db_manager
from register_screen import RegisterScreen
from encryption_utils import encrypt_data, decrypt_data
version_data = db_manager.get_version()

class LoginScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.is_success = False
        self.current_user = None  # Giriş edən istifadəçinin məlumatlarını saxlamaq üçün
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
        
        # Avtomatik giriş yoxlaması
        if self.check_auto_login():
            return
        
        self.setup_window()
        self.create_interface()
        
    def check_auto_login(self):
        """Avtomatik giriş yoxlaması edir"""
        try:
            if os.path.exists(self.login_file):
                with open(self.login_file, 'r', encoding='utf-8') as f:
                    wrapper = json.load(f)
                encrypted = wrapper.get('data')
                if not encrypted:
                    os.remove(self.login_file)
                    return False
                try:
                    login_json = decrypt_data(encrypted.encode('utf-8'))
                    login_data = json.loads(login_json)
                except Exception as e:
                    os.remove(self.login_file)
                    return False
                
                username = login_data.get('username')
                password = login_data.get('password')
                
                if username and password:
                    # Giriş məlumatlarını yoxla
                    user, expired_pro = db_manager.authenticate_user(username, password)
                    
                    if user:
                        # Avtomatik giriş uğurlu
                        self.current_user = user
                        self.is_success = True
                        return True
                    else:
                        # Giriş məlumatları yanlış, faylı sil
                        os.remove(self.login_file)
                        return False
                else:
                    # Faylda giriş məlumatları çatışmır, faylı sil
                    os.remove(self.login_file)
                    return False
            else:
                return False
        except Exception as e:
            # Xəta halında faylı sil
            if os.path.exists(self.login_file):
                os.remove(self.login_file)
            return False

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

    def clear_login_credentials(self):
        """Giriş məlumatlarını login.json faylından silir"""
        try:
            if os.path.exists(self.login_file):
                os.remove(self.login_file)
        except Exception as e:
            print(f"Giriş məlumatları silinərkən xəta: {str(e)}")
        
    def setup_window(self):
        self.setWindowTitle("Azer AI Giriş")
        self.setStyleSheet(f"background-color: {self.colors['bg']};")
        self.setWindowIcon(QIcon('images/logo.ico'))

        # Pəncərə ölçüsünü təyin edirik
        window_width = 400
        window_height = 500
        
        # Ekranın mərkəzində yerləşdirmə
        screen_geometry = QApplication.primaryScreen().geometry()
        center_x = int(screen_geometry.width()/2 - window_width/2)
        center_y = int(screen_geometry.height()/2 - window_height/2)
        
        self.setGeometry(center_x, center_y, window_width, window_height)
        self.setFixedSize(window_width, window_height)

    def create_interface(self):
        # Əsas layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(10)
        
        # Logo etiketi
        logo_label = QLabel("AZER AI " + version_data['version'])
        logo_label.setFont(QFont("Helvetica", 36, QFont.Weight.Bold))
        logo_label.setStyleSheet(f"color: {self.colors['primary']};")
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(logo_label)
        
        # Alt başlıq
        subtitle_label = QLabel("Süni intellekt köməkçisi")
        subtitle_label.setFont(QFont("Helvetica", 14))
        subtitle_label.setStyleSheet(f"color: {self.colors['text_secondary']};")
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(subtitle_label)
        
        # Boşluq əlavə et
        main_layout.addSpacing(40)
        
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
        
        # Boşluq əlavə et
        main_layout.addSpacing(20)
        
        # Giriş düyməsi
        self.login_button = QPushButton("Daxil Ol")
        self.login_button.setMinimumHeight(40)
        self.login_button.setStyleSheet(f"""
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
        self.login_button.clicked.connect(self.login)
        main_layout.addWidget(self.login_button)
        
        # Məni xatırla checkbox-ı
        from PyQt6.QtWidgets import QCheckBox
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
                background-color: {self.colors['bg_secondary']};
                color: {self.colors['text']};
                border: 1px solid {self.colors['primary']};
                border-radius: 5px;
                font-size: 12pt;
            }}
            QPushButton:hover {{
                background-color: {self.colors['secondary']};
                color: white;
                border: none;
            }}
        """)
        self.register_button.clicked.connect(self.show_register)
        main_layout.addWidget(self.register_button)
        
        # Xəta mesajı etiketi
        self.error_label = QLabel("")
        self.error_label.setStyleSheet(f"color: {self.colors['error']};")
        self.error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.error_label)
        
        # Enter düyməsinə basanda giriş et
        self.password_entry.returnPressed.connect(self.login)
        
        # Boşluq əlavə et
        main_layout.addStretch(1)

    def show_register(self):
        """Qeydiyyat ekranını göstər"""
        register_screen = RegisterScreen()
        self.hide()  # Giriş ekranını gizlə
        success = register_screen.run()
        if success:
            # Qeydiyyat uğurlu olarsa istifadəçi adını giriş ekranına yerləşdir
            self.username_entry.setText(register_screen.username_entry.text())
            self.password_entry.setText(register_screen.password_entry.text())
            self.login()  # Avtomatik giriş et
        self.show()  # Giriş ekranını yenidən göstər

    def login(self):
        username = self.username_entry.text()
        password = self.password_entry.text()
        
        if not username or not password:
            self.error_label.setText("Zəhmət olmasa bütün sahələri doldurun!")
            return
        
        # İstifadəçi yoxlanışı üçün db_manager istifadə et
        user, expired_pro = db_manager.authenticate_user(username, password)
        
        if not user:
            self.error_label.setText("İstifadəçi adı və ya şifrə yanlışdır!")
            return
            
        if user:
            # Giriş uğurlu - əgər "Məni xatırla" seçilibsə məlumatları yadda saxla
            if self.remember_me.isChecked():
                self.save_login_credentials(username, password)
            self.current_user = user
            
            # Rol və lisenziya vəziyyətinə görə mesaj
            if user['role'] == 'admin':
                welcome_text = f"Xoş gəldiniz, Admin! Pro (Limitsiz) istifadəçi olaraq"
            elif user['license_status'] == 'pro':
                if 'pro_expiry' in user:
                    # Pro müddətini hesabla və göstər
                    try:
                        expiry_date = datetime.strptime(user['pro_expiry'], "%Y-%m-%d %H:%M:%S")
                        now = datetime.now()
                        
                        if expiry_date > now:
                            # Qalan müddəti hesabla
                            remaining = expiry_date - now
                            days = remaining.days
                            seconds = remaining.seconds
                            
                            hours = seconds // 3600
                            seconds %= 3600
                            minutes = seconds // 60
                            seconds %= 60
                            
                            # Zaman vahidlərini hesabla
                            years = days // 365
                            months = (days % 365) // 30
                            weeks = (days % 30) // 7
                            days = days % 7
                            
                            # İki zaman vahidini göstər, ikinci vahid 0 olarsa növbəti vahidə keç
                            if years > 0:
                                if months > 0:
                                    time_text = f"{years} il {months} ay"
                                elif weeks > 0:
                                    time_text = f"{years} il {weeks} həftə"
                                elif days > 0:
                                    time_text = f"{years} il {days} gün"
                                elif hours > 0:
                                    time_text = f"{years} il {hours} saat"
                                elif minutes > 0:
                                    time_text = f"{years} il {minutes} dəq"
                                elif seconds > 0:
                                    time_text = f"{years} il {seconds} sn"
                                else:
                                    time_text = f"{years} il"
                            elif months > 0:
                                if weeks > 0:
                                    time_text = f"{months} ay {weeks} həftə"
                                elif days > 0:
                                    time_text = f"{months} ay {days} gün"
                                elif hours > 0:
                                    time_text = f"{months} ay {hours} saat"
                                elif minutes > 0:
                                    time_text = f"{months} ay {minutes} dəq"
                                elif seconds > 0:
                                    time_text = f"{months} ay {seconds} sn"
                                else:
                                    time_text = f"{months} ay"
                            elif weeks > 0:
                                if days > 0:
                                    time_text = f"{weeks} həftə {days} gün"
                                elif hours > 0:
                                    time_text = f"{weeks} həftə {hours} saat"
                                elif minutes > 0:
                                    time_text = f"{weeks} həftə {minutes} dəq"
                                elif seconds > 0:
                                    time_text = f"{weeks} həftə {seconds} sn"
                                else:
                                    time_text = f"{weeks} həftə"
                            elif days > 0:
                                if hours > 0:
                                    time_text = f"{days} gün {hours} saat"
                                elif minutes > 0:
                                    time_text = f"{days} gün {minutes} dəq"
                                elif seconds > 0:
                                    time_text = f"{days} gün {seconds} sn"
                                else:
                                    time_text = f"{days} gün"
                            elif hours > 0:
                                if minutes > 0:
                                    time_text = f"{hours} saat {minutes} dəq"
                                elif seconds > 0:
                                    time_text = f"{hours} saat {seconds} sn"
                                else:
                                    time_text = f"{hours} saat"
                            elif minutes > 0:
                                if seconds > 0:
                                    time_text = f"{minutes} dəq {seconds} sn"
                                else:
                                    time_text = f"{minutes} dəq"
                            else:
                                time_text = f"{seconds} sn"
                            
                            welcome_text = f"Xoş gəldiniz, Pro istifadəçi! ({time_text})"
                        else:
                            welcome_text = f"Xoş gəldiniz, Pro istifadəçi!"
                    except Exception as e:
                        self.speak(f"Müddət hesablamada xəta: {str(e)}")
                        welcome_text = f"Xoş gəldiniz, Pro istifadəçi!"
                else:
                    # Pro müddəti yoxdursa (limitsiz)
                    welcome_text = f"Xoş gəldiniz, Pro istifadəçi! (Limitsiz)"
            else:
                if expired_pro:
                    # Müddəti bitmiş pro istifadəçisi
                    welcome_text = f"Xoş gəldiniz, Free istifadəçi! Pro zamanınız bitdi"
                else:
                    # Normal free istifadəçi
                    welcome_text = f"Xoş gəldiniz, Free istifadəçi!"
            
            # Uğurlu mesajını göstər
            self.error_label.setStyleSheet(f"color: {self.colors['accent']};")
            
            # UI-ı yenilə
            self.login_button.setEnabled(False)
            self.login_button.setText("✓ Giriş Uğurlu")
            self.login_button.setStyleSheet(f"""
                QPushButton {{
                    background-color: {self.colors['accent']};
                    color: white;
                    border: none;
                    border-radius: 5px;
                    font-size: 12pt;
                    font-weight: bold;
                }}
            """)
            
            # Geri sayım başlat
            self.countdown = 5
            self.base_welcome_text = welcome_text
            self.update_countdown()
            self.countdown_timer = QTimer()
            self.countdown_timer.timeout.connect(self.update_countdown)
            self.countdown_timer.start(1000)  # Hər saniyə
            
            return True
        
        # Giriş uğursuz
        self.error_label.setText("İstifadəçi adı və ya parol səhvdir!")
        return False

    def update_countdown(self):
        """Geri sayımı yenilə"""
        if self.countdown > 0:
            self.error_label.setText(f"{self.base_welcome_text} {self.countdown} saniyə sonra yönləndirilirsiniz...")
            self.countdown -= 1
        else:
            self.countdown_timer.stop()
            self.complete_login()

    def complete_login(self):
        """Uğurlu girişi tamamla"""
        self.is_success = True
        self.close()

    def run(self):
        # Əgər avtomatik giriş uğurlu olarsa, birbaşa qaytar
        if self.is_success and self.current_user:
            return self.is_success, self.current_user
            
        self.show()
        app = QApplication.instance()
        if app is None:
            app = QApplication([])
        app.exec()
        return self.is_success, self.current_user