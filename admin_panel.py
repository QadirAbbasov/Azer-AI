from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
                            QTabWidget, QWidget, QScrollArea, QFrame, QGridLayout,
                            QLineEdit, QMessageBox, QTableWidget, QTableWidgetItem,
                            QHeaderView)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor
from db_manager import db_manager

class AdminPanel:
    def __init__(self, parent, colors):
        self.parent = parent
        self.colors = colors
        
    def create_admin_panel(self):
        """Modern admin panel oluştur"""
        # Ana admin panel penceresi
        admin_window = QDialog(self.parent)
        admin_window.setWindowTitle("👑 Admin Panel - Azer AI")
        admin_window.setMinimumSize(650, 450)
        admin_window.setStyleSheet(f"background-color: {self.colors['bg']};")
        admin_window.setWindowFlags(admin_window.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)
        
        # Ana layout
        main_layout = QVBoxLayout(admin_window)
        main_layout.setContentsMargins(8, 8, 8, 8)
        main_layout.setSpacing(8)
        
        # Başlıq
        title_label = QLabel("👑 Admin Panel")
        title_label.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        title_label.setStyleSheet(f"color: {self.colors['primary']}; margin: 3px 0px;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)
        
        # Alt başlıq
        subtitle_label = QLabel("Sistem İdarəetməsi və İstifadəçi Əməliyyatları")
        subtitle_label.setFont(QFont("Segoe UI", 8))
        subtitle_label.setStyleSheet(f"color: {self.colors['text_secondary']}; margin: 3px 0px 8px 0px;")
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(subtitle_label)
        
        # Nişan widget yaradın
        tab_widget = QTabWidget()
        tab_widget.setStyleSheet(f"""
            QTabWidget::pane {{
                border: 1px solid {self.colors['border']};
                background-color: {self.colors['bg_secondary']};
                border-radius: 8px;
            }}
            QTabBar::tab {{
                background-color: {self.colors['bg_tertiary']};
                color: {self.colors['text']};
                padding: 6px 10px;
                margin-right: 2px;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
                font-weight: bold;
                font-size: 9px;
            }}
            QTabBar::tab:selected {{
                background-color: {self.colors['primary']};
                color: white;
            }}
            QTabBar::tab:hover:!selected {{
                background-color: {self.colors['bg_secondary']};
            }}
        """)
        
        # İstifadəçi idarəetməsi tab'ı
        users_tab = QWidget()
        self.create_users_management_tab(users_tab)
        tab_widget.addTab(users_tab, "👥 İstifadəçi İdarəetməsi")
        
        # Key idarəetməsi tab'ı
        keys_tab = QWidget()
        self.create_keys_management_tab(keys_tab)
        tab_widget.addTab(keys_tab, "🔑 Pro Key İdarəetməsi")
        
        # Versiya idarəetməsi tab'ı
        version_tab = QWidget()
        self.create_version_management_tab(version_tab)
        tab_widget.addTab(version_tab, "📦 Versiya İdarəetməsi")
        
        main_layout.addWidget(tab_widget)
        
        # Alt məlumat və bağlama düyməsi
        bottom_layout = QHBoxLayout()
        
        info_label = QLabel("Azer AI Admin Panel v1.0 - Təhlükəsiz sistem idarəetməsi")
        info_label.setStyleSheet(f"color: {self.colors['text_muted']}; font-size: 7px;")
        bottom_layout.addWidget(info_label)
        
        bottom_layout.addStretch()
        
        close_btn = QPushButton("❌ Bağla")
        close_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.colors['error']};
                color: white;
                border: none;
                border-radius: 5px;
                padding: 5px 12px;
                font-size: 10px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: #D32F2F;
            }}
            QPushButton:pressed {{
                background-color: #B71C1C;
            }}
        """)
        close_btn.clicked.connect(admin_window.close)
        bottom_layout.addWidget(close_btn)
        
        main_layout.addLayout(bottom_layout)
        
        # Pencereyi göster ve düzgün kapatılmasını sağla
        admin_window.setModal(True)
        
        # Close event handler ekle
        def close_event(event):
            admin_window.deleteLater()
            event.accept()
        
        admin_window.closeEvent = close_event
        admin_window.exec()

    def create_users_management_tab(self, parent):
        """İstifadəçi idarəetməsi tab'ını yarat"""
        # Ana scroll area oluştur
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet(f"""
            QScrollArea {{
                background-color: {self.colors['bg']};
                border: none;
            }}
            QScrollBar:vertical {{
                background-color: {self.colors['bg_secondary']};
                width: 12px;
                border-radius: 6px;
            }}
            QScrollBar::handle:vertical {{
                background-color: {self.colors['primary']};
                border-radius: 6px;
                min-height: 20px;
            }}
            QScrollBar::handle:vertical:hover {{
                background-color: {self.colors['accent']};
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0px;
            }}
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
                background-color: {self.colors['bg_secondary']};
            }}
        """)
        
        # Scroll area için widget oluştur
        scroll_widget = QWidget()
        layout = QVBoxLayout(scroll_widget)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(8)
        
        # Başlıq
        title = QLabel("👥 İstifadəçi İdarəetməsi")
        title.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        title.setStyleSheet(f"color: {self.colors['text']}; margin-bottom: 5px;")
        layout.addWidget(title)
        
        # Statistika frame
        stats_frame = QFrame()
        stats_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {self.colors['bg_tertiary']};
                border-radius: 8px;
                padding: 15px;
                border: 1px solid {self.colors['border']};
            }}
        """)
        stats_layout = QHBoxLayout(stats_frame)
        stats_layout.setSpacing(10)
        
        # İstifadəçi statistikasını al
        users = db_manager.get_all_users()
        total_users = len(users) if users else 0
        pro_users = len([u for u in users if u['license_status'] == 'pro']) if users else 0
        free_users = total_users - pro_users
        
        # Ümumi istifadəçi
        total_label = QLabel(f"📊 Ümumi: {total_users}")
        total_label.setStyleSheet(f"color: {self.colors['text']}; font-weight: bold; font-size: 11px; padding: 3px 6px;")
        stats_layout.addWidget(total_label)
        
        # Pro istifadəçilər
        pro_label = QLabel(f"👑 Pro: {pro_users}")
        pro_label.setStyleSheet(f"color: {self.colors['success']}; font-weight: bold; font-size: 11px; padding: 3px 6px;")
        stats_layout.addWidget(pro_label)
        
        # Free istifadəçilər
        free_label = QLabel(f"🆓 Free: {free_users}")
        free_label.setStyleSheet(f"color: {self.colors['text_secondary']}; font-weight: bold; font-size: 11px; padding: 3px 6px;")
        stats_layout.addWidget(free_label)
        
        stats_layout.addStretch()
        layout.addWidget(stats_frame)
        
        # İstifadəçi cədvəli
        table_frame = QFrame()
        table_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {self.colors['bg_secondary']};
                border-radius: 8px;
                border: 1px solid {self.colors['border']};
            }}
        """)
        table_layout = QVBoxLayout(table_frame)
        
        # Cədvəl başlığı
        table_title = QLabel("📋 İstifadəçi Siyahısı")
        table_title.setStyleSheet(f"color: {self.colors['text']}; font-weight: bold; font-size: 13px; margin: 6px 0px;")
        table_layout.addWidget(table_title)
        
        # İstifadəçi cədvəli
        self.users_table = QTableWidget()
        self.users_table.setColumnCount(7)
        self.users_table.setHorizontalHeaderLabels([
            "ID", "İstifadəçi Adı", "Ad", "Rol", "Lisenziya", "Son Giriş", "Əməliyyatlar"
        ])
        self.users_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.users_table.setStyleSheet(f"""
            QTableWidget {{
                background-color: {self.colors['bg_tertiary']};
                color: {self.colors['text']};
                gridline-color: {self.colors['border']};
                            border: none;
                border-radius: 5px;
            }}
            QHeaderView::section {{
                background-color: {self.colors['bg_tertiary']};
                color: {self.colors['text']};
                padding: 10px;
                border: none;
                border-bottom: 1px solid {self.colors['border']};
                font-weight: bold;
            }}
            QTableWidget::item {{
                padding: 8px;
                border-bottom: 1px solid {self.colors['border_secondary']};
            }}
            QTableWidget::item:selected {{
                background-color: {self.colors['primary']};
                        color: white;
                    }}
            QTableWidget::item:hover {{
                background-color: {self.colors['bg_secondary']};
                    }}
                """)
                
        self.load_users_table()
        table_layout.addWidget(self.users_table)
        
        # Yeni istifadəçi əlavə etmə bölməsi
        add_user_frame = QFrame()
        add_user_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {self.colors['bg_tertiary']};
                border-radius: 8px;
                padding: 8px;
                border: 1px solid {self.colors['border']};
            }}
        """)
        add_user_layout = QGridLayout(add_user_frame)
        
        # Başlıq
        add_title = QLabel("➕ Yeni İstifadəçi Əlavə Et")
        add_title.setStyleSheet(f"color: {self.colors['text']}; font-weight: bold; font-size: 13px; margin-bottom: 6px;")
        add_user_layout.addWidget(add_title, 0, 0, 1, 4)
        
        # İstifadəçi adı
        username_label = QLabel("İstifadəçi Adı:")
        username_label.setStyleSheet(f"color: {self.colors['text']};")
        add_user_layout.addWidget(username_label, 1, 0)
        
        self.new_username = QLineEdit()
        self.new_username.setPlaceholderText("İstifadəçi adını daxil edin")
        self.new_username.setStyleSheet(f"""
            QLineEdit {{
                background-color: {self.colors['bg_secondary']};
                color: {self.colors['text']};
                border: 1px solid {self.colors['border']};
                border-radius: 5px;
                padding: 8px;
            }}
            QLineEdit:hover {{
                border: 1px solid {self.colors['primary']};
            }}
            QLineEdit:focus {{
                border: 2px solid {self.colors['accent']};
            }}
        """)
        add_user_layout.addWidget(self.new_username, 1, 1)
        
        # Şifrə
        password_label = QLabel("Şifrə:")
        password_label.setStyleSheet(f"color: {self.colors['text']};")
        add_user_layout.addWidget(password_label, 1, 2)
        
        self.new_password = QLineEdit()
        self.new_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.new_password.setPlaceholderText("Şifrə daxil edin")
        self.new_password.setStyleSheet(f"""
            QLineEdit {{
                background-color: {self.colors['bg_secondary']};
                color: {self.colors['text']};
                border: 1px solid {self.colors['border']};
                border-radius: 5px;
                padding: 8px;
            }}
            QLineEdit:hover {{
                border: 1px solid {self.colors['primary']};
            }}
            QLineEdit:focus {{
                border: 2px solid {self.colors['accent']};
            }}
        """)
        add_user_layout.addWidget(self.new_password, 1, 3)
        
        # Ad
        name_label = QLabel("Ad:")
        name_label.setStyleSheet(f"color: {self.colors['text']};")
        add_user_layout.addWidget(name_label, 2, 0)
        
        self.new_name = QLineEdit()
        self.new_name.setPlaceholderText("Ad daxil edin")
        self.new_name.setStyleSheet(f"""
            QLineEdit {{
                background-color: {self.colors['bg_secondary']};
                color: {self.colors['text']};
                border: 1px solid {self.colors['border']};
                border-radius: 5px;
                padding: 8px;
            }}
            QLineEdit:hover {{
                border: 1px solid {self.colors['primary']};
            }}
            QLineEdit:focus {{
                border: 2px solid {self.colors['accent']};
            }}
        """)
        add_user_layout.addWidget(self.new_name, 2, 1)
        
        # Əlavə et düyməsi
        add_btn = QPushButton("➕ İstifadəçi Əlavə Et")
        add_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.colors['success']};
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
                font-weight: bold;
                font-size: 11px;
            }}
            QPushButton:hover {{
                background-color: #2EA043;
            }}
            QPushButton:pressed {{
                background-color: #238636;
            }}
        """)
        add_btn.clicked.connect(self.add_user)
        add_user_layout.addWidget(add_btn, 3, 0, 1, 4)
        
        layout.addWidget(add_user_frame)
        
        # Yenilə düyməsi
        refresh_btn = QPushButton("🔄 Cədvəli Yenilə")
        refresh_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.colors['primary']};
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
                font-weight: bold;
                font-size: 11px;
            }}
            QPushButton:hover {{
                background-color: {self.colors['secondary']};
            }}
            QPushButton:pressed {{
                background-color: {self.colors['accent']};
            }}
        """)
        refresh_btn.clicked.connect(self.load_users_table)
        layout.addWidget(refresh_btn)
        
        # Scroll yarat
        scroll_area.setWidget(scroll_widget)
        parent_layout = QVBoxLayout(parent)
        parent_layout.setContentsMargins(0, 0, 0, 0)
        parent_layout.addWidget(scroll_area)

    def create_keys_management_tab(self, parent):
        """Key idarəetməsi tab'ını yarat"""
        # Ana scroll yarat
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet(f"""
            QScrollArea {{
                background-color: {self.colors['bg']};
                border: none;
            }}
            QScrollBar:vertical {{
                background-color: {self.colors['bg_secondary']};
                width: 12px;
                border-radius: 6px;
            }}
            QScrollBar::handle:vertical {{
                background-color: {self.colors['primary']};
                border-radius: 6px;
                min-height: 20px;
            }}
            QScrollBar::handle:vertical:hover {{
                background-color: {self.colors['accent']};
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0px;
            }}
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
                background-color: {self.colors['bg_secondary']};
            }}
        """)
        
        # Scroll üçün widget yarat
        scroll_widget = QWidget()
        layout = QVBoxLayout(scroll_widget)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(8)
        
        # Başlıq
        title = QLabel("🔑 Pro Key İdarəetməsi")
        title.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        title.setStyleSheet(f"color: {self.colors['text']}; font-weight: bold; margin-bottom: 5px;")
        layout.addWidget(title)
        
        # Statistika çərçivəsi
        stats_frame = QFrame()
        stats_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {self.colors['bg_tertiary']};
                border-radius: 8px;
                padding: 15px;
                border: 1px solid {self.colors['border']};
            }}
        """)
        stats_layout = QHBoxLayout(stats_frame)
        stats_layout.setSpacing(10)
        
        # Key statistikasını al
        keys = db_manager.get_pro_keys()
        total_keys = len(keys) if keys else 0
        used_keys = len([k for k in keys if k['status'] == 'used']) if keys else 0
        unused_keys = total_keys - used_keys
        
        # Ümumi key
        total_label = QLabel(f"🔑 Ümumi: {total_keys}")
        total_label.setStyleSheet(f"color: {self.colors['text']}; font-weight: bold; font-size: 12px; padding: 4px 8px;")
        stats_layout.addWidget(total_label)
        
        # İstifadə edilmiş keylər
        used_label = QLabel(f"✅ İstifadə edilmiş: {used_keys}")
        used_label.setStyleSheet(f"color: {self.colors['success']}; font-weight: bold; font-size: 12px; padding: 4px 8px;")
        stats_layout.addWidget(used_label)
        
        # İstifadə edilməmiş keylər
        unused_label = QLabel(f"⏳ İstifadə edilməmiş: {unused_keys}")
        unused_label.setStyleSheet(f"color: {self.colors['warning']}; font-weight: bold; font-size: 12px; padding: 4px 8px;")
        stats_layout.addWidget(unused_label)
        
        stats_layout.addStretch()
        layout.addWidget(stats_frame)
        
        # Yeni key əlavə etmə bölməsi
        add_key_frame = QFrame()
        add_key_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {self.colors['bg_tertiary']};
                border-radius: 8px;
                padding: 10px;
                border: 1px solid {self.colors['border']};
            }}
        """)
        add_key_layout = QGridLayout(add_key_frame)
        
        # Başlıq
        add_title = QLabel("➕ Yeni Pro Key Əlavə Et")
        add_title.setStyleSheet(f"color: {self.colors['text']}; font-weight: bold; font-size: 14px; margin-bottom: 8px;")
        add_key_layout.addWidget(add_title, 0, 0, 1, 4)
        
        # Key kodu
        key_label = QLabel("Key Kodu:")
        key_label.setStyleSheet(f"color: {self.colors['text']};")
        add_key_layout.addWidget(key_label, 1, 0)
        
        self.new_key = QLineEdit()
        self.new_key.setPlaceholderText("PRO123-456-789")
        self.new_key.setStyleSheet(f"""
            QLineEdit {{
                background-color: {self.colors['bg_secondary']};
                color: {self.colors['text']};
                border: 1px solid {self.colors['border']};
                border-radius: 5px;
                padding: 8px;
            }}
            QLineEdit:hover {{
                border: 1px solid {self.colors['primary']};
            }}
            QLineEdit:focus {{
                border: 2px solid {self.colors['accent']};
            }}
        """)
        add_key_layout.addWidget(self.new_key, 1, 1)
        
        # Müddət
        duration_label = QLabel("Müddət (gün):")
        duration_label.setStyleSheet(f"color: {self.colors['text']};")
        add_key_layout.addWidget(duration_label, 1, 2)
        
        self.key_duration = QLineEdit()
        self.key_duration.setPlaceholderText("30")
        self.key_duration.setStyleSheet(f"""
            QLineEdit {{
                background-color: {self.colors['bg_secondary']};
                color: {self.colors['text']};
                border: 1px solid {self.colors['border']};
                border-radius: 5px;
                padding: 8px;
            }}
            QLineEdit:hover {{
                border: 1px solid {self.colors['primary']};
            }}
            QLineEdit:focus {{
                border: 2px solid {self.colors['accent']};
            }}
        """)
        add_key_layout.addWidget(self.key_duration, 1, 3)
        
        # Əlavə et düyməsi
        add_key_btn = QPushButton("➕ Key Əlavə Et")
        add_key_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.colors['success']};
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
                font-weight: bold;
                font-size: 11px;
            }}
            QPushButton:hover {{
                background-color: #2EA043;
            }}
            QPushButton:pressed {{
                background-color: #238636;
            }}
        """)
        add_key_btn.clicked.connect(self.add_pro_key)
        add_key_layout.addWidget(add_key_btn, 2, 0, 1, 4)
        
        layout.addWidget(add_key_frame)
        
        # Key cədvəli
        keys_table_frame = QFrame()
        keys_table_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {self.colors['bg_secondary']};
                border-radius: 8px;
                border: 1px solid {self.colors['border']};
            }}
        """)
        keys_table_layout = QVBoxLayout(keys_table_frame)
        
        # Cədvəl başlığı
        keys_table_title = QLabel("📋 Pro Key Siyahısı")
        keys_table_title.setStyleSheet(f"color: {self.colors['text']}; font-weight: bold; font-size: 14px; margin: 8px 0px;")
        keys_table_layout.addWidget(keys_table_title)
        
        # Key cədvəli
        self.keys_table = QTableWidget()
        self.keys_table.setColumnCount(5)
        self.keys_table.setHorizontalHeaderLabels([
            "Key Kodu", "Müddət (gün)", "Vəziyyət", "Aktivasiya Tarixi", "İstifadə edən"
        ])
        self.keys_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.keys_table.setStyleSheet(f"""
            QTableWidget {{
                background-color: {self.colors['bg_tertiary']};
                color: {self.colors['text']};
                gridline-color: {self.colors['border']};
                border: none;
                border-radius: 5px;
            }}
            QHeaderView::section {{
                background-color: {self.colors['bg_tertiary']};
                color: {self.colors['text']};
                padding: 10px;
                border: none;
                border-bottom: 1px solid {self.colors['border']};
                font-weight: bold;
            }}
            QTableWidget::item {{
                padding: 8px;
                border-bottom: 1px solid {self.colors['border_secondary']};
            }}
            QTableWidget::item:selected {{
                background-color: {self.colors['primary']};
                color: white;
            }}
            QTableWidget::item:hover {{
                background-color: {self.colors['bg_secondary']};
            }}
        """)
        
        self.load_keys_table()
        keys_table_layout.addWidget(self.keys_table)
        layout.addWidget(keys_table_frame)
        
        # Yenilə düyməsi
        refresh_keys_btn = QPushButton("🔄 Key Siyahısını Yenilə")
        refresh_keys_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.colors['primary']};
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
                font-weight: bold;
                font-size: 11px;
            }}
            QPushButton:hover {{
                background-color: {self.colors['secondary']};
            }}
            QPushButton:pressed {{
                background-color: {self.colors['accent']};
            }}
        """)
        refresh_keys_btn.clicked.connect(self.load_keys_table)
        layout.addWidget(refresh_keys_btn)
        
        # Scroll yarat
        scroll_area.setWidget(scroll_widget)
        parent_layout = QVBoxLayout(parent)
        parent_layout.setContentsMargins(0, 0, 0, 0)
        parent_layout.addWidget(scroll_area)
        
    def load_users_table(self):
        """İstifadəçi cədvəlini yüklə"""
        try:
            users = db_manager.get_all_users()
            
            if users:
                self.users_table.setRowCount(len(users))
            
            for row, user in enumerate(users):
                # ID
                id_item = QTableWidgetItem(str(user['id']))
                id_item.setFlags(id_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.users_table.setItem(row, 0, id_item)
                
                # İstifadəçi adı
                username_item = QTableWidgetItem(user['username'])
                username_item.setFlags(username_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.users_table.setItem(row, 1, username_item)
                
                # Ad
                name_item = QTableWidgetItem(user['name'])
                name_item.setFlags(name_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.users_table.setItem(row, 2, name_item)
                
                # Rol
                role_item = QTableWidgetItem("👑 Admin" if user['role'] == 'admin' else "👤 İstifadəçi")
                role_item.setFlags(role_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.users_table.setItem(row, 3, role_item)
                
                # Lisenziya vəziyyəti
                license_text = "👑 Pro" if user['license_status'] == 'pro' else "🆓 Free"
                license_item = QTableWidgetItem(license_text)
                license_item.setFlags(license_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.users_table.setItem(row, 4, license_item)
                
                # Son giriş
                last_login_text = ""
                if user['last_login'] is not None:
                    if isinstance(user['last_login'], str):
                        last_login_text = user['last_login']
                    else:
                        last_login_text = user['last_login'].strftime("%Y-%m-%d %H:%M:%S")
                        
                last_login_item = QTableWidgetItem(last_login_text)
                last_login_item.setFlags(last_login_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.users_table.setItem(row, 5, last_login_item)
                
                # Əməliyyat düymələri
                actions_widget = QWidget()
                actions_layout = QHBoxLayout(actions_widget)
                actions_layout.setContentsMargins(8, 4, 8, 4)
                actions_layout.setSpacing(8)
                actions_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
                
                # Pro et düyməsi
                if user['license_status'] != 'pro':
                    pro_btn = QPushButton("👑 Pro")
                    pro_btn.setStyleSheet(f"""
                        QPushButton {{
                            background-color: {self.colors['success']};
                            color: white;
                            border: none;
                            border-radius: 3px;
                            padding: 4px 6px;
                            font-size: 10px;
                            font-weight: bold;
                        }}
                        QPushButton:hover {{
                            background-color: #2EA043;
                        }}
                        QPushButton:pressed {{
                            background-color: #238636;
                        }}
                    """)
                    pro_btn.clicked.connect(lambda checked, u=user: self.make_pro(u))
                    actions_layout.addWidget(pro_btn)
                
                # Sil düyməsi
                delete_btn = QPushButton("🗑️ Sil")
                delete_btn.setStyleSheet(f"""
                    QPushButton {{
                        background-color: {self.colors['error']};
                        color: white;
                        border: none;
                        border-radius: 3px;
                                                    padding: 4px 6px;
                        font-size: 10px;
                        font-weight: bold;
                    }}
                    QPushButton:hover {{
                        background-color: #D32F2F;
                    }}
                    QPushButton:pressed {{
                        background-color: #B71C1C;
                    }}
                """)
                delete_btn.clicked.connect(lambda checked, u=user: self.delete_user(u))
                actions_layout.addWidget(delete_btn)
                
                self.users_table.setCellWidget(row, 6, actions_widget)
        except Exception as e:
            print(f"İstifadəçi cədvəli yüklənərkən xəta: {str(e)}")
            # Xəta halında boş cədvəl göstər
            self.users_table.setRowCount(0)

    def load_keys_table(self):
        """Key cədvəlini yüklə"""
        try:
            keys = db_manager.get_pro_keys()
            
            if keys:
                self.keys_table.setRowCount(len(keys))
            
            for row, key in enumerate(keys):
                # Key kodu
                key_item = QTableWidgetItem(key['key_code'])
                key_item.setFlags(key_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.keys_table.setItem(row, 0, key_item)
                
                # Süre
                duration_item = QTableWidgetItem(str(key['duration']))
                duration_item.setFlags(duration_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.keys_table.setItem(row, 1, duration_item)
                
                # Vəziyyət
                status_text = "✅ İstifadə edilmiş" if key['status'] == 'used' else "⏳ İstifadə edilməmiş"
                status_item = QTableWidgetItem(status_text)
                status_item.setFlags(status_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.keys_table.setItem(row, 2, status_item)
                
                # Aktivasiya tarixi
                activation_date_text = ""
                if key['activation_date'] is not None:
                    if isinstance(key['activation_date'], str):
                        activation_date_text = key['activation_date']
                    else:
                        activation_date_text = key['activation_date'].strftime("%Y-%m-%d %H:%M:%S")
                        
                activation_date_item = QTableWidgetItem(activation_date_text)
                activation_date_item.setFlags(activation_date_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.keys_table.setItem(row, 3, activation_date_item)
                
                # İstifadə edən
                used_by_item = QTableWidgetItem(key.get('used_by_username', ''))
                used_by_item.setFlags(used_by_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.keys_table.setItem(row, 4, used_by_item)
        except Exception as e:
            print(f"Key cədvəli yüklənərkən xəta: {str(e)}")
            # Xəta halında boş cədvəl göstər
            self.keys_table.setRowCount(0)

    def add_user(self):
        """Yeni istifadəçi əlavə et"""
        try:
            username = self.new_username.text().strip()
            password = self.new_password.text().strip()
            name = self.new_name.text().strip()
            
            if not username or not password or not name:
                msg = QMessageBox()
                msg.setWindowFlags(msg.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)
                msg.setModal(True)
                msg.setIcon(QMessageBox.Icon.Warning)
                msg.setWindowTitle("Xəta")
                msg.setText("Zəhmət olmasa bütün sahələri doldurun!")
                msg.exec()
                return
                
            # İstifadəçi adı yoxlaması
            if db_manager.user_exists(username):
                msg = QMessageBox()
                msg.setWindowFlags(msg.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)
                msg.setModal(True)
                msg.setIcon(QMessageBox.Icon.Warning)
                msg.setWindowTitle("Xəta")
                msg.setText("Bu istifadəçi adı artıq mövcuddur!")
                msg.exec()
                return
            
            # Yeni istifadəçini verilənlər bazasına əlavə et
            user_data = {
                'username': username,
                'password': password,
                'name': name,
                'role': 'user',
                'license_status': 'free'
            }
            
            success = db_manager.create_user(user_data)
            
            if success:
                msg = QMessageBox()
                msg.setWindowFlags(msg.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)
                msg.setModal(True)
                msg.setIcon(QMessageBox.Icon.Information)
                msg.setWindowTitle("Uğurlu")
                msg.setText("İstifadəçi uğurla əlavə edildi!")
                msg.exec()
                
                # Form sahələrini təmizlə
                self.new_username.clear()
                self.new_password.clear()
                self.new_name.clear()
                
                # Cədvəli yenilə
                try:
                    self.load_users_table()
                except Exception as table_error:
                    print(f"Cədvəl yenilənərkən xəta: {str(table_error)}")
            else:
                msg = QMessageBox()
                msg.setWindowFlags(msg.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)
                msg.setModal(True)
                msg.setIcon(QMessageBox.Icon.Critical)
                msg.setWindowTitle("Xəta")
                msg.setText("İstifadəçi əlavə edilərkən xəta baş verdi!")
                msg.exec()
                
        except Exception as e:
            print(f"İstifadəçi əlavə etmə xətası: {str(e)}")
            msg = QMessageBox()
            msg.setWindowFlags(msg.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)
            msg.setModal(True)
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setWindowTitle("Xəta")
            msg.setText(f"Gözlənilməz xəta: {str(e)}")
            msg.exec()

    def make_pro(self, user):
        """İstifadəçini pro et"""
        success = db_manager.make_user_pro(user['id'], 30)  # 30 günlük pro
        
        if success:
            msg = QMessageBox()
            msg.setWindowFlags(msg.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)
            msg.setModal(True)
            msg.setIcon(QMessageBox.Icon.Information)
            msg.setWindowTitle("Uğurlu")
            msg.setText("İstifadəçi Pro oldu!")
            msg.exec()
            self.load_users_table()
        else:
            msg = QMessageBox()
            msg.setWindowFlags(msg.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)
            msg.setModal(True)
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setWindowTitle("Xəta")
            msg.setText("Pro etmə xətası!")
            msg.exec()

    def delete_user(self, user):
        """İstifadəçini sil"""
        msg = QMessageBox()
        msg.setWindowFlags(msg.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)
        msg.setModal(True)
        msg.setIcon(QMessageBox.Icon.Question)
        msg.setWindowTitle("İstifadəçini Sil")
        msg.setText(f"'{user['username']}' istifadəçisini silmək istədiyinizdən əminmisiniz?")
        msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        result = msg.exec()
        
        if result != QMessageBox.StandardButton.Yes:
            return
        
        success = db_manager.delete_user(user['id'])
        
        if success:
            msg = QMessageBox()
            msg.setWindowFlags(msg.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)
            msg.setModal(True)
            msg.setIcon(QMessageBox.Icon.Information)
            msg.setWindowTitle("Uğurlu")
            msg.setText("İstifadəçi silindi!")
            msg.exec()
            self.load_users_table()
        else:
            msg = QMessageBox()
            msg.setWindowFlags(msg.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)
            msg.setModal(True)
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setWindowTitle("Xəta")
            msg.setText("İstifadəçi silmə xətası!")
            msg.exec()
        
    def add_pro_key(self):
        """Yeni pro key əlavə et"""
        key_code = self.new_key.text().strip()
        duration_text = self.key_duration.text().strip()
        
        if not key_code:
            msg = QMessageBox()
            msg.setWindowFlags(msg.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)
            msg.setModal(True)
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle("Xəta")
            msg.setText("Key kodunu daxil edin!")
            msg.exec()
            return
            
        try:
            duration = int(duration_text) if duration_text else 30
        except ValueError:
            msg = QMessageBox()
            msg.setWindowFlags(msg.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)
            msg.setModal(True)
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle("Xəta")
            msg.setText("Müddət rəqəm olmalıdır!")
            msg.exec()
            return
            
        success = db_manager.add_pro_key(key_code, duration)
        
        if success:
            msg = QMessageBox()
            msg.setWindowFlags(msg.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)
            msg.setModal(True)
            msg.setIcon(QMessageBox.Icon.Information)
            msg.setWindowTitle("Uğurlu")
            msg.setText("Pro key uğurla əlavə edildi!")
            msg.exec()
            
            # Form sahələrini təmizlə
            self.new_key.clear()
            self.key_duration.clear()
            
            # Cədvəli yenilə
            self.load_keys_table()
        else:
            msg = QMessageBox()
            msg.setWindowFlags(msg.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)
            msg.setModal(True)
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setWindowTitle("Xəta")
            msg.setText("Pro key əlavə etmə xətası!")
            msg.exec()

    def create_version_management_tab(self, parent):
        """Versiya idarəetməsi tab'ını yarat"""
        # Ana scroll yarat
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet(f"""
            QScrollArea {{
                background-color: {self.colors['bg']};
                border: none;
            }}
            QScrollBar:vertical {{
                background-color: {self.colors['bg_secondary']};
                width: 12px;
                border-radius: 6px;
            }}
            QScrollBar::handle:vertical {{
                background-color: {self.colors['primary']};
                border-radius: 6px;
                min-height: 20px;
            }}
            QScrollBar::handle:vertical:hover {{
                background-color: {self.colors['accent']};
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0px;
            }}
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
                background-color: {self.colors['bg_secondary']};
            }}
        """)
        
        # Scroll ücün widget yarat
        scroll_widget = QWidget()
        layout = QVBoxLayout(scroll_widget)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(8)
        
        # Başlıq
        title = QLabel("📦 Versiya İdarəetməsi")
        title.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        title.setStyleSheet(f"color: {self.colors['text']}; margin-bottom: 5px;")
        layout.addWidget(title)
        
        # Versiya məlumatlarını al
        version_data = db_manager.get_version()
        current_version = version_data.get('version', '1.0.0')
        web_url = version_data.get('web_url', 'https://github.com/QadirAbbasov/Azer-AI')
        google_drive_id = version_data.get('google_drive_id', '1fdICCmiQiYVJxyI6hQSh7zXCQAjQw4BN')
        changelog = version_data.get('info', 'Dəyişiklik qeydi tapılmadı.')
        
        # Tarix məlumatını al (verilənlər bazasından və ya bugünkü tarixi istifadə et)
        try:
            from datetime import datetime
            db_date = version_data.get('created_at')
            if db_date:
                # Verilənlər bazasından gələn tarixi formatla
                if isinstance(db_date, str):
                    # String isə birbaşa istifadə et
                    release_date = db_date.split(' ')[0]  # Yalnız tarix hissəsini al
                else:
                    # Datetime obyekti isə formatla
                    release_date = db_date.strftime('%Y-%m-%d')
            else:
                # Verilənlər bazasında tarix yoxdursa bugünkü tarixi istifadə et
                release_date = datetime.now().strftime('%Y-%m-%d')
        except:
            release_date = '2024-01-01'
        
        # Mövcud versiya məlumatı - Kompakt kart dizaynı
        current_version_frame = QFrame()
        current_version_frame.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {self.colors['bg_tertiary']}, 
                    stop:1 {self.colors['bg_secondary']});
                border-radius: 8px;
                padding: 8px;
                border: 1px solid {self.colors['primary']};
            }}
        """)
        current_version_layout = QVBoxLayout(current_version_frame)
        
        # Mövcud versiya başlığı - Kompakt başlıq
        current_title = QLabel("🔄 Mövcud Versiya")
        current_title.setStyleSheet(f"""
            color: {self.colors['primary']}; 
            font-weight: bold; 
            font-size: 11px; 
            margin-bottom: 5px;
            padding: 3px 0px;
            border-bottom: 1px solid {self.colors['primary']};
        """)
        current_version_layout.addWidget(current_title)
        
        # Versiya nömrəsi - Kompakt badge dizaynı
        version_info_layout = QHBoxLayout()
        version_label = QLabel("📦 Versiya:")
        version_label.setStyleSheet(f"color: {self.colors['text']}; font-weight: bold; font-size: 10px;")
        version_info_layout.addWidget(version_label)
        
        version_value = QLabel(current_version)
        version_value.setStyleSheet(f"""
            color: white; 
            font-weight: bold; 
            font-size: 11px;
            background-color: {self.colors['primary']};
            padding: 2px 8px;
            border-radius: 10px;
            border: 1px solid {self.colors['accent']};
        """)
        version_info_layout.addWidget(version_value)
        version_info_layout.addStretch()
        current_version_layout.addLayout(version_info_layout)
        
        # Yayım tarixi - Kompakt tarix göstərilməsi
        date_info_layout = QHBoxLayout()
        date_label = QLabel("📅 Yayım Tarixi:")
        date_label.setStyleSheet(f"color: {self.colors['text']}; font-weight: bold; font-size: 10px;")
        date_info_layout.addWidget(date_label)
        
        date_value = QLabel(release_date)
        date_value.setStyleSheet(f"""
            color: {self.colors['text_secondary']}; 
            font-size: 10px;
            background-color: {self.colors['bg_secondary']};
            padding: 2px 6px;
            border-radius: 6px;
            border: 1px solid {self.colors['border']};
        """)
        date_info_layout.addWidget(date_value)
        date_info_layout.addStretch()
        current_version_layout.addLayout(date_info_layout)
        
        # Web URL - Kompakt URL göstərilməsi
        web_url_layout = QHBoxLayout()
        web_url_label = QLabel("🌐 Web URL:")
        web_url_label.setStyleSheet(f"color: {self.colors['text']}; font-weight: bold; font-size: 10px;")
        web_url_layout.addWidget(web_url_label)
        
        web_url_value = QLabel(web_url[:50] + "..." if len(web_url) > 50 else web_url)
        web_url_value.setStyleSheet(f"""
            color: {self.colors['text_secondary']}; 
            font-size: 9px;
            background-color: {self.colors['bg_secondary']};
            padding: 2px 6px;
            border-radius: 6px;
            border: 1px solid {self.colors['border']};
        """)
        web_url_layout.addWidget(web_url_value)
        web_url_layout.addStretch()
        current_version_layout.addLayout(web_url_layout)
        
        # Google Drive ID - Kompakt ID göstərilməsi
        drive_id_layout = QHBoxLayout()
        drive_id_label = QLabel("☁️ Drive ID:")
        drive_id_label.setStyleSheet(f"color: {self.colors['text']}; font-weight: bold; font-size: 10px;")
        drive_id_layout.addWidget(drive_id_label)
        
        drive_id_value = QLabel(google_drive_id[:20] + "..." if len(google_drive_id) > 20 else google_drive_id)
        drive_id_value.setStyleSheet(f"""
            color: {self.colors['text_secondary']}; 
            font-size: 9px;
            background-color: {self.colors['bg_secondary']};
            padding: 2px 6px;
            border-radius: 6px;
            border: 1px solid {self.colors['border']};
        """)
        drive_id_layout.addWidget(drive_id_value)
        drive_id_layout.addStretch()
        current_version_layout.addLayout(drive_id_layout)
        
        # Changelog - Kompakt kart dizaynı
        changelog_label = QLabel("📝 Dəyişikliklər:")
        changelog_label.setStyleSheet(f"color: {self.colors['text']}; font-weight: bold; font-size: 10px; margin-top: 5px;")
        current_version_layout.addWidget(changelog_label)
        
        changelog_text = QLabel(changelog)
        changelog_text.setWordWrap(True)
        changelog_text.setStyleSheet(f"""
            color: {self.colors['text']}; 
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {self.colors['bg_secondary']}, 
                stop:1 {self.colors['bg_tertiary']});
            padding: 5px; 
            border-radius: 6px; 
            border: 1px solid {self.colors['border']};
            font-size: 9px;
            line-height: 1.3;
        """)
        current_version_layout.addWidget(changelog_text)
        
        layout.addWidget(current_version_frame)
        
        # Mövcud versiya yeniləmə bölməsi - Kompakt form dizaynı
        update_version_frame = QFrame()
        update_version_frame.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {self.colors['bg_secondary']}, 
                    stop:1 {self.colors['bg_tertiary']});
                border-radius: 8px;
                padding: 8px;
                border: 1px solid {self.colors['accent']};
            }}
        """)
        update_version_layout = QGridLayout(update_version_frame)
        update_version_layout.setSpacing(6)
        
        # Başlıq - Kompakt form başlığı
        update_title = QLabel("✏️ Versiya Yeniləmə")
        update_title.setStyleSheet(f"""
            color: {self.colors['accent']}; 
            font-weight: bold; 
            font-size: 11px; 
            margin-bottom: 5px;
            padding: 3px 0px;
            border-bottom: 1px solid {self.colors['accent']};
        """)
        update_version_layout.addWidget(update_title, 0, 0, 1, 4)
        
        # Versiya nömrəsi - Kompakt form sahəsi
        update_version_label = QLabel("📦 Yeni Versiya:")
        update_version_label.setStyleSheet(f"color: {self.colors['text']}; font-weight: bold; font-size: 9px;")
        update_version_layout.addWidget(update_version_label, 1, 0)
        
        self.update_version_number = QLineEdit()
        self.update_version_number.setPlaceholderText("1.0.1")
        self.update_version_number.setText(current_version)  # Mövcud versiyanı göstər
        self.update_version_number.setStyleSheet(f"""
            QLineEdit {{
                background-color: {self.colors['bg_tertiary']};
                color: {self.colors['text']};
                border: 1px solid {self.colors['border']};
                border-radius: 6px;
                padding: 4px 8px;
                font-size: 9px;
            }}
            QLineEdit:hover {{
                border: 1px solid {self.colors['primary']};
                background-color: {self.colors['bg_secondary']};
            }}
            QLineEdit:focus {{
                border: 1px solid {self.colors['accent']};
                background-color: {self.colors['bg_secondary']};
            }}
        """)
        update_version_layout.addWidget(self.update_version_number, 1, 1)
        
        # Yayım tarixi - Kompakt form sahəsi
        update_date_label = QLabel("📅 Yayım Tarixi:")
        update_date_label.setStyleSheet(f"color: {self.colors['text']}; font-weight: bold; font-size: 9px;")
        update_version_layout.addWidget(update_date_label, 1, 2)
        
        self.update_release_date = QLineEdit()
        self.update_release_date.setPlaceholderText("2024-01-15")
        self.update_release_date.setText(release_date)  # Mövcud tarixi göstər
        self.update_release_date.setStyleSheet(f"""
            QLineEdit {{
                background-color: {self.colors['bg_tertiary']};
                color: {self.colors['text']};
                border: 1px solid {self.colors['border']};
                border-radius: 6px;
                padding: 4px 8px;
                font-size: 9px;
            }}
            QLineEdit:hover {{
                border: 1px solid {self.colors['primary']};
                background-color: {self.colors['bg_secondary']};
            }}
            QLineEdit:focus {{
                border: 1px solid {self.colors['accent']};
                background-color: {self.colors['bg_secondary']};
            }}
        """)
        update_version_layout.addWidget(self.update_release_date, 1, 3)
        
        # Changelog - Kompakt form sahəsi
        update_changelog_label = QLabel("📝 Dəyişikliklər:")
        update_changelog_label.setStyleSheet(f"color: {self.colors['text']}; font-weight: bold; font-size: 9px;")
        update_version_layout.addWidget(update_changelog_label, 2, 0)
        
        self.update_changelog = QLineEdit()
        self.update_changelog.setPlaceholderText("Yeni xüsusiyyətlər və düzəlişlər...")
        self.update_changelog.setText(changelog)  # Mövcud changelog'u göstər
        self.update_changelog.setStyleSheet(f"""
            QLineEdit {{
                background-color: {self.colors['bg_tertiary']};
                color: {self.colors['text']};
                border: 1px solid {self.colors['border']};
                border-radius: 6px;
                padding: 4px 8px;
                font-size: 9px;
            }}
            QLineEdit:hover {{
                border: 1px solid {self.colors['primary']};
                background-color: {self.colors['bg_secondary']};
            }}
            QLineEdit:focus {{
                border: 1px solid {self.colors['accent']};
                background-color: {self.colors['bg_secondary']};
            }}
        """)
        update_version_layout.addWidget(self.update_changelog, 2, 1, 1, 3)
        
        # Web URL - Kompakt form alanı
        update_web_url_label = QLabel("🌐 Web URL:")
        update_web_url_label.setStyleSheet(f"color: {self.colors['text']}; font-weight: bold; font-size: 9px;")
        update_version_layout.addWidget(update_web_url_label, 3, 0)
        
        self.update_web_url = QLineEdit()
        self.update_web_url.setPlaceholderText("https://github.com/QadirAbbasov/Azer-AI")
        self.update_web_url.setText(web_url)  # Mevcut URL'yi göster
        self.update_web_url.setStyleSheet(f"""
            QLineEdit {{
                background-color: {self.colors['bg_tertiary']};
                color: {self.colors['text']};
                border: 1px solid {self.colors['border']};
                border-radius: 6px;
                padding: 4px 8px;
                font-size: 9px;
            }}
            QLineEdit:hover {{
                border: 1px solid {self.colors['primary']};
                background-color: {self.colors['bg_secondary']};
            }}
            QLineEdit:focus {{
                border: 1px solid {self.colors['accent']};
                background-color: {self.colors['bg_secondary']};
            }}
        """)
        update_version_layout.addWidget(self.update_web_url, 3, 1, 1, 3)
        
        # Google Drive ID - Kompakt form alanı
        update_drive_id_label = QLabel("☁️ Drive ID:")
        update_drive_id_label.setStyleSheet(f"color: {self.colors['text']}; font-weight: bold; font-size: 9px;")
        update_version_layout.addWidget(update_drive_id_label, 4, 0)
        
        self.update_google_drive_id = QLineEdit()
        self.update_google_drive_id.setPlaceholderText("1fdICCmiQiYVJxyI6hQSh7zXCQAjQw4BN")
        self.update_google_drive_id.setText(google_drive_id)  # Mevcut Drive ID'yi göster
        self.update_google_drive_id.setStyleSheet(f"""
            QLineEdit {{
                background-color: {self.colors['bg_tertiary']};
                color: {self.colors['text']};
                border: 1px solid {self.colors['border']};
                border-radius: 6px;
                padding: 4px 8px;
                font-size: 9px;
            }}
            QLineEdit:hover {{
                border: 1px solid {self.colors['primary']};
                background-color: {self.colors['bg_secondary']};
            }}
            QLineEdit:focus {{
                border: 1px solid {self.colors['accent']};
                background-color: {self.colors['bg_secondary']};
            }}
        """)
        update_version_layout.addWidget(self.update_google_drive_id, 4, 1, 1, 3)
        
        # Yenilə düyməsi - Kompakt gradient düymə
        update_version_btn = QPushButton("🚀 Versiyanı Yenilə")
        update_version_btn.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {self.colors['primary']}, 
                    stop:1 {self.colors['accent']});
                color: white;
                border: none;
                border-radius: 6px;
                padding: 6px 12px;
                font-weight: bold;
                font-size: 10px;
                margin-top: 5px;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {self.colors['accent']}, 
                    stop:1 {self.colors['primary']});
            }}
            QPushButton:pressed {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {self.colors['secondary']}, 
                    stop:1 {self.colors['primary']});
            }}
        """)
        update_version_btn.clicked.connect(self.update_current_version)
        update_version_layout.addWidget(update_version_btn, 5, 0, 1, 4)
        
        layout.addWidget(update_version_frame)
        
        # Ən son versiya məlumatı - Kompakt xülasə kartı
        latest_version_frame = QFrame()
        latest_version_frame.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {self.colors['bg_tertiary']}, 
                    stop:1 {self.colors['bg_secondary']});
                border-radius: 8px;
                padding: 8px;
                border: 1px solid {self.colors['success']};
            }}
        """)
        latest_version_layout = QVBoxLayout(latest_version_frame)
        
        # Ən son versiya başlığı - Kompakt başlıq
        latest_title = QLabel("⭐ Güncəl Versiya Xülasəsi")
        latest_title.setStyleSheet(f"""
            color: {self.colors['success']}; 
            font-weight: bold; 
            font-size: 11px; 
            margin: 4px 0px;
            padding: 3px 0px;
            border-bottom: 1px solid {self.colors['success']};
        """)
        latest_version_layout.addWidget(latest_title)
        
        # Ən son versiya məlumatları - Kompakt badge'lər
        latest_version_info = QLabel(f"📦 Versiya: {current_version}")
        latest_version_info.setStyleSheet(f"""
            color: white; 
            font-weight: bold; 
            font-size: 11px; 
            margin: 3px 0px;
            background-color: {self.colors['success']};
            padding: 2px 8px;
            border-radius: 10px;
            border: 1px solid {self.colors['primary']};
        """)
        latest_version_layout.addWidget(latest_version_info)
        
        latest_date_info = QLabel(f"📅 Yayım Tarixi: {release_date}")
        latest_date_info.setStyleSheet(f"""
            color: {self.colors['text_secondary']}; 
            font-size: 10px; 
            margin: 3px 0px;
            background-color: {self.colors['bg_tertiary']};
            padding: 2px 6px;
            border-radius: 6px;
            border: 1px solid {self.colors['border']};
        """)
        latest_version_layout.addWidget(latest_date_info)
        
        latest_changelog_info = QLabel(f"📝 Dəyişikliklər: {changelog}")
        latest_changelog_info.setWordWrap(True)
        latest_changelog_info.setStyleSheet(f"""
            color: {self.colors['text']}; 
            font-size: 9px; 
            margin: 5px 0px;
            background-color: {self.colors['bg_secondary']};
            padding: 4px;
            border-radius: 4px;
            border: 1px solid {self.colors['border']};
            line-height: 1.2;
        """)
        latest_version_layout.addWidget(latest_changelog_info)
        
        # Web URL özeti
        latest_web_url_info = QLabel(f"🌐 Web URL: {web_url[:30]}..." if len(web_url) > 30 else f"🌐 Web URL: {web_url}")
        latest_web_url_info.setStyleSheet(f"""
            color: {self.colors['text_secondary']}; 
            font-size: 9px; 
            margin: 3px 0px;
            background-color: {self.colors['bg_tertiary']};
            padding: 2px 6px;
            border-radius: 6px;
            border: 1px solid {self.colors['border']};
        """)
        latest_version_layout.addWidget(latest_web_url_info)
        
        # Drive ID özeti
        latest_drive_id_info = QLabel(f"☁️ Drive ID: {google_drive_id[:15]}..." if len(google_drive_id) > 15 else f"☁️ Drive ID: {google_drive_id}")
        latest_drive_id_info.setStyleSheet(f"""
            color: {self.colors['text_secondary']}; 
            font-size: 9px; 
            margin: 3px 0px;
            background-color: {self.colors['bg_tertiary']};
            padding: 2px 6px;
            border-radius: 6px;
            border: 1px solid {self.colors['border']};
        """)
        latest_version_layout.addWidget(latest_drive_id_info)
        
        layout.addWidget(latest_version_frame)
        
        # Yenilə düyməsi - Kompakt refresh düyməsi
        refresh_version_btn = QPushButton("🔄 Versiya Məlumatlarını Yenilə")
        refresh_version_btn.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {self.colors['warning']}, 
                    stop:1 {self.colors['primary']});
                color: white;
                border: none;
                border-radius: 6px;
                padding: 6px 12px;
                font-weight: bold;
                font-size: 10px;
                margin-top: 5px;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {self.colors['primary']}, 
                    stop:1 {self.colors['warning']});
            }}
            QPushButton:pressed {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {self.colors['accent']}, 
                    stop:1 {self.colors['warning']});
            }}
        """)
        refresh_version_btn.clicked.connect(self.refresh_version_info)
        layout.addWidget(refresh_version_btn)
        
        # Scroll yarat
        scroll_area.setWidget(scroll_widget)
        parent_layout = QVBoxLayout(parent)
        parent_layout.setContentsMargins(0, 0, 0, 0)
        parent_layout.addWidget(scroll_area)

    def update_current_version(self):
        """Mövcud versiyanı yenilə"""
        version = self.update_version_number.text().strip()
        release_date = self.update_release_date.text().strip()
        changelog = self.update_changelog.text().strip()
        web_url = self.update_web_url.text().strip()
        google_drive_id = self.update_google_drive_id.text().strip()
        
        if not version or not release_date or not changelog:
            msg = QMessageBox()
            msg.setWindowFlags(msg.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)
            msg.setModal(True)
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle("Xəta")
            msg.setText("Zəhmət olmasa bütün sahələri doldurun!")
            msg.exec()
            return
        
        # Versiya formatı yoxlaması
        if not self.is_valid_version_format(version):
            msg = QMessageBox()
            msg.setWindowFlags(msg.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)
            msg.setModal(True)
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle("Xəta")
            msg.setText("Yanlış versiya formatı! (Nümunə: 1.0.1, V5.8, V1.0.1)")
            msg.exec()
            return
            
        # Tarix formatı yoxlaması
        if not self.is_valid_date_format(release_date):
            msg = QMessageBox()
            msg.setWindowFlags(msg.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)
            msg.setModal(True)
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle("Xəta")
            msg.setText("Yanlış tarix formatı! (Nümunə: 2024-01-15)")
            msg.exec()
            return
            
        # URL formatı yoxlaması
        if web_url and not web_url.startswith(('http://', 'https://')):
            msg = QMessageBox()
            msg.setWindowFlags(msg.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)
            msg.setModal(True)
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle("Xəta")
            msg.setText("Yanlış URL formatı! (http:// və ya https:// ilə başlamalı)")
            msg.exec()
            return
            
        # Mövcud versiyanı yenilə
        try:
            success = db_manager.update_version(version, web_url, google_drive_id, changelog, release_date)
            
            if success:
                msg = QMessageBox()
                msg.setWindowFlags(msg.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)
                msg.setModal(True)
                msg.setIcon(QMessageBox.Icon.Information)
                msg.setWindowTitle("Uğurlu")
                msg.setText("Versiya uğurla yeniləndi!")
                msg.exec()
                
                # Versiya məlumatlarını yenilə
                self.refresh_version_info()
            else:
                msg = QMessageBox()
                msg.setWindowFlags(msg.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)
                msg.setModal(True)
                msg.setIcon(QMessageBox.Icon.Critical)
                msg.setWindowTitle("Xəta")
                msg.setText("Versiya yeniləmə xətası! Zəhmət olmasa yenidən cəhd edin.")
                msg.exec()
        except Exception as e:
            msg = QMessageBox()
            msg.setWindowFlags(msg.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)
            msg.setModal(True)
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setWindowTitle("Xəta")
            msg.setText(f"Versiya yeniləmə xətası: {str(e)}")
            msg.exec()

    def refresh_version_info(self):
        """Versiya məlumatlarını yenilə"""
        try:
            # Mövcud versiya məlumatlarını yenilə
            version_data = db_manager.get_version()
            current_version = version_data.get('version', '1.0.0')
            web_url = version_data.get('web_url', 'https://github.com/QadirAbbasov/Azer-AI')
            google_drive_id = version_data.get('google_drive_id', '1fdICCmiQiYVJxyI6hQSh7zXCQAjQw4BN')
            changelog = version_data.get('info', 'Dəyişiklik qeydi tapılmadı.')
            
            # Tarix məlumatını al (verilənlər bazasından və ya bugünkü tarixi istifadə et)
            try:
                from datetime import datetime
                db_date = version_data.get('created_at')
                if db_date:
                    # Verilənlər bazasından gələn tarixi formatla
                    if isinstance(db_date, str):
                        # String isə birbaşa istifadə et
                        release_date = db_date.split(' ')[0]  # Yalnız tarix hissəsini al
                    else:
                        # Datetime obyekti isə formatla
                        release_date = db_date.strftime('%Y-%m-%d')
                else:
                    # Verilənlər bazasında tarix yoxdursa bugünkü tarixi istifadə et
                    release_date = datetime.now().strftime('%Y-%m-%d')
            except:
                release_date = '2024-01-01'
            
            # Form sahələrini yenilə
            self.update_version_number.setText(current_version)
            self.update_release_date.setText(release_date)
            self.update_changelog.setText(changelog)
            self.update_web_url.setText(web_url)
            self.update_google_drive_id.setText(google_drive_id)
            
            msg = QMessageBox()
            msg.setWindowFlags(msg.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)
            msg.setModal(True)
            msg.setIcon(QMessageBox.Icon.Information)
            msg.setWindowTitle("Uğurlu")
            msg.setText("Versiya məlumatları yeniləndi!")
            msg.exec()
        except Exception as e:
            msg = QMessageBox()
            msg.setWindowFlags(msg.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)
            msg.setModal(True)
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setWindowTitle("Xəta")
            msg.setText(f"Versiya məlumatları yenilənərkən xəta: {str(e)}")
            msg.exec()

    def is_valid_version_format(self, version):
        """Versiya formatını yoxla"""
        import re
        # V5.8, 1.0.1, V1.0.1 kimi formatları qəbul et
        pattern = r'^V?\d+\.\d+(\.\d+)?$'
        return re.match(pattern, version) is not None

    def is_valid_date_format(self, date):
        """Tarix formatını yoxla"""
        import re
        pattern = r'^\d{4}-\d{2}-\d{2}$'
        return re.match(pattern, date) is not None 