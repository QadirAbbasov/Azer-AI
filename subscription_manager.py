import datetime
import os
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
                            QLineEdit, QTabWidget, QWidget, QScrollArea, QFrame,
                            QMessageBox)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QPixmap
from db_manager import db_manager

class SubscriptionManager:
    def __init__(self, main_app):
        self.main_app = main_app
        self.colors = main_app.colors
        self.current_user = main_app.current_user
        self.pro_expiry = None
        
        # Pro və free əmrləri yüklə
        self.command_list = self.load_commands()
        
        # Pro vəziyyətini yoxla
        self.check_pro_status()
        
        # Canlı müddət göstərilməsi üçün timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_pro_status)
        self.timer.start(1000)  # Hər saniyə yenilə
        
    def load_commands(self):
        """Pro və free əmrləri commands.py-dən yüklə"""
        from commands import Azer_AICommands
        
        # Müvəqqəti bir Azer_AICommands nümunəsi yarat
        temp_commands = Azer_AICommands(self.main_app)
        
        # Əmrləri lüğətə çevir
        commands = {
            "free_commands": {
                cmd: f"{cmd.title()} Əmri" 
                for cmd in temp_commands.free_command_aliases.keys()
            },
            "pro_commands": {
                cmd: f"{cmd.title()} Əmri"
                for cmd in temp_commands.pro_command_aliases.keys()
            }
        }
        
        return commands
            
    def show_command_list(self):
        """Əmrlər siyahısı pəncərəsini göstər"""
        dialog = QDialog(self.main_app)
        dialog.setWindowTitle("Əmrlər Siyahısı")
        dialog.setMinimumSize(600, 400)
        dialog.setStyleSheet(f"background-color: {self.colors['bg']};")
        
        # Əsas layout
        layout = QVBoxLayout(dialog)
        
        # Tab widget yarat
        tab_widget = QTabWidget()
        tab_widget.setStyleSheet(f"""
            QTabWidget::pane {{
                border: 1px solid {self.colors['primary']};
                background-color: {self.colors['bg_secondary']};
            }}
            QTabBar::tab {{
                background-color: {self.colors['bg_secondary']};
                color: {self.colors['text']};
                padding: 8px 12px;
                margin-right: 2px;
            }}
            QTabBar::tab:selected {{
                background-color: {self.colors['primary']};
                color: white;
            }}
        """)
        
        # Əmr saylarını hesabla
        free_count = len(self.command_list["free_commands"])
        pro_count = len(self.command_list["pro_commands"])
        
        # Free əmrlər tab-ı
        free_tab = QWidget()
        free_layout = QVBoxLayout(free_tab)
        
        # Scroll sahəsi
        free_scroll = QScrollArea()
        free_scroll.setWidgetResizable(True)
        free_scroll.setStyleSheet(f"""
            QScrollArea {{
                border: none;
                background-color: {self.colors['bg_secondary']};
            }}
            
            QScrollBar:vertical {{
                border: none;
                background-color: {self.colors['bg']};
                width: 12px;
                margin: 0px;
            }}
            
            QScrollBar::handle:vertical {{
                background-color: {self.colors['primary']};
                border-radius: 6px;
                min-height: 30px;
                margin: 2px;
            }}
            
            QScrollBar::handle:vertical:hover {{
                background-color: {self.colors['secondary']};
            }}
            
            QScrollBar::add-line:vertical {{
                height: 0px;
            }}
            
            QScrollBar::sub-line:vertical {{
                height: 0px;
            }}
            
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
                background-color: {self.colors['bg']};
                border-radius: 6px;
            }}
        """)
        
        # Scroll məzmunu
        free_content = QWidget()
        free_content_layout = QVBoxLayout(free_content)
        
        # Free əmrləri siyahıla
        for cmd, desc in self.command_list["free_commands"].items():
            cmd_frame = QFrame()
            cmd_frame.setStyleSheet(f"""
                QFrame {{
                    background-color: {self.colors['bg_secondary']};
                    border-radius: 5px;
                    margin: 2px;
                    padding: 5px;
                }}
            """)
            cmd_layout = QHBoxLayout(cmd_frame)
            
            # Əmr adı
            cmd_label = QLabel(f"✅ {cmd}")
            cmd_label.setStyleSheet(f"color: {self.colors['text']};")
            cmd_layout.addWidget(cmd_label)
            
            # Açıqlama
            desc_label = QLabel(desc)
            desc_label.setStyleSheet(f"color: {self.colors['text_secondary']};")
            cmd_layout.addWidget(desc_label)
            
            free_content_layout.addWidget(cmd_frame)
        
        free_scroll.setWidget(free_content)
        free_layout.addWidget(free_scroll)
        
        # Pro əmrlər tab-ı
        pro_tab = QWidget()
        pro_layout = QVBoxLayout(pro_tab)
        
        # Scroll sahəsi
        pro_scroll = QScrollArea()
        pro_scroll.setWidgetResizable(True)
        pro_scroll.setStyleSheet(f"""
            QScrollArea {{
                border: none;
                background-color: {self.colors['bg_secondary']};
            }}
            
            QScrollBar:vertical {{
                border: none;
                background-color: {self.colors['bg']};
                width: 12px;
                margin: 0px;
            }}
            
            QScrollBar::handle:vertical {{
                background-color: {self.colors['primary']};
                border-radius: 6px;
                min-height: 30px;
                margin: 2px;
            }}
            
            QScrollBar::handle:vertical:hover {{
                background-color: {self.colors['secondary']};
            }}
            
            QScrollBar::add-line:vertical {{
                height: 0px;
            }}
            
            QScrollBar::sub-line:vertical {{
                height: 0px;
            }}
            
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
                background-color: {self.colors['bg']};
                border-radius: 6px;
            }}
        """)
        
        # Scroll məzmunu
        pro_content = QWidget()
        pro_content_layout = QVBoxLayout(pro_content)
        
        # Pro əmrləri siyahıla
        for cmd, desc in self.command_list["pro_commands"].items():
            cmd_frame = QFrame()
            cmd_frame.setStyleSheet(f"""
                QFrame {{
                    background-color: {self.colors['bg_secondary']};
                    border-radius: 5px;
                    margin: 2px;
                    padding: 5px;
                }}
            """)
            cmd_layout = QHBoxLayout(cmd_frame)
            
            # Əmr adı və pro vəziyyətinə görə ikon
            is_pro = self.current_user['license_status'] == 'pro'
            icon = "✅" if is_pro else "🔒"
            cmd_label = QLabel(f"{icon} {cmd}")
            cmd_label.setStyleSheet(f"color: {self.colors['text']};")
            cmd_layout.addWidget(cmd_label)
            
            # Açıqlama
            desc_label = QLabel(desc)
            desc_label.setStyleSheet(f"color: {self.colors['text_secondary']};")
            cmd_layout.addWidget(desc_label)
            
            pro_content_layout.addWidget(cmd_frame)
        
        # Xüsusi əmrlər tab-ı
        special_tab = QWidget()
        special_layout = QVBoxLayout(special_tab)
        
        # Pro deyilsə yüksəltmə düyməsi əlavə et (xüsusi əmrlər üçün)
        if self.current_user['license_status'] != 'pro':
            # Xüsusi əmrlər tab-ı üçün məlumatlandırma və düymə
            special_info_label = QLabel("⭐ Xüsusi əmrləri istifadə etmək üçün Pro versiyaya keçin")
            special_info_label.setStyleSheet(f"""
                color: {self.colors['text']};
                padding: 10px;
                font-weight: bold;
            """)
            special_info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            special_layout.addWidget(special_info_label)
            
            special_upgrade_btn = QPushButton("👑 Pro Versiyaya Yüksəlin")
            special_upgrade_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {self.colors['warning']};
                    color: black;
                    border: none;
                    border-radius: 5px;
                    padding: 10px;
                    font-weight: bold;
                }}
                QPushButton:hover {{
                    background-color: #e6c200;
                }}
            """)
            special_upgrade_btn.clicked.connect(self.show_upgrade_dialog)
            special_layout.addWidget(special_upgrade_btn)
        
        # Scroll sahəsi
        special_scroll = QScrollArea()
        special_scroll.setWidgetResizable(True)
        special_scroll.setStyleSheet(f"""
            QScrollArea {{
                border: none;
                background-color: {self.colors['bg_secondary']};
            }}
            
            QScrollBar:vertical {{
                border: none;
                background-color: {self.colors['bg']};
                width: 12px;
                margin: 0px;
            }}
            
            QScrollBar::handle:vertical {{
                background-color: {self.colors['primary']};
                border-radius: 6px;
                min-height: 30px;
                margin: 2px;
            }}
            
            QScrollBar::handle:vertical:hover {{
                background-color: {self.colors['secondary']};
            }}
            
            QScrollBar::add-line:vertical {{
                height: 0px;
            }}
            
            QScrollBar::sub-line:vertical {{
                height: 0px;
            }}
            
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
                background-color: {self.colors['bg']};
                border-radius: 6px;
            }}
        """)
        
        # Scroll məzmunu
        special_content = QWidget()
        special_content_layout = QVBoxLayout(special_content)
        
        # Xüsusi əmrləri yüklə
        custom_commands = self.main_app.load_custom_commands()
        special_count = len(custom_commands)
        
        # Xüsusi əmrləri siyahıla
        if custom_commands:
            for cmd in custom_commands:
                cmd_frame = QFrame()
                cmd_frame.setStyleSheet(f"""
                    QFrame {{
                        background-color: {self.colors['bg_secondary']};
                        border-radius: 5px;
                        margin: 2px;
                        padding: 5px;
                    }}
                """)
                cmd_layout = QHBoxLayout(cmd_frame)
                cmd_layout.setSpacing(15)  # Əsas layout üçün spacing əlavə et
                
                # Sol tərəf üçün konteyner
                left_container = QHBoxLayout()
                left_container.setSpacing(5)
                
                # Əmr adı və pro vəziyyətinə görə ikon
                is_pro = self.current_user['license_status'] == 'pro'
                icon = "✅" if is_pro else "🔒"
                cmd_label = QLabel(f"{icon} {cmd['name']}")
                cmd_label.setStyleSheet(f"color: {self.colors['text']};")
                left_container.addWidget(cmd_label)
                
                # Açıqlama (Əməliyyat növü)
                desc_label = QLabel(cmd['action'])
                desc_label.setStyleSheet(f"color: {self.colors['text_secondary']};")
                left_container.addWidget(desc_label)
                
                cmd_layout.addLayout(left_container)
                
                # Kiçik bir boşluq əlavə et
                spacer = QLabel()
                spacer.setFixedWidth(20)  # 20 piksel boşluq
                cmd_layout.addWidget(spacer)
                
                # Tətikləyicilər üçün şaquli layout
                triggers_layout = QVBoxLayout()
                triggers_layout.setSpacing(5)  # Sətirlər arası boşluq
                
                # Azərbaycan dili tətikləyiciləri
                if 'triggers' in cmd and 'az-AZ' in cmd['triggers'] and cmd['triggers']['az-AZ']:
                    az_row = QHBoxLayout()
                    az_row.setSpacing(5)  # Bayraq və mətn arası boşluq
                    az_icon = QLabel()
                    az_icon.setPixmap(QPixmap("resim/AZ.png").scaled(30, 20, Qt.AspectRatioMode.KeepAspectRatio))
                    az_row.addWidget(az_icon)
                    az_triggers = ", ".join(cmd['triggers']['az-AZ'])
                    az_label = QLabel(az_triggers)
                    az_label.setStyleSheet(f"color: {self.colors['text_secondary']};")
                    az_row.addWidget(az_label)
                    triggers_layout.addLayout(az_row)
                
                # Türk dili tətikləyiciləri
                if 'triggers' in cmd and 'tr-TR' in cmd['triggers'] and cmd['triggers']['tr-TR']:
                    tr_row = QHBoxLayout()
                    tr_row.setSpacing(5)  # Bayraq və mətn arası boşluq
                    tr_icon = QLabel()
                    tr_icon.setPixmap(QPixmap("resim/TR.png").scaled(30, 20, Qt.AspectRatioMode.KeepAspectRatio))
                    tr_row.addWidget(tr_icon)
                    tr_triggers = ", ".join(cmd['triggers']['tr-TR'])
                    tr_label = QLabel(tr_triggers)
                    tr_label.setStyleSheet(f"color: {self.colors['text_secondary']};")
                    tr_row.addWidget(tr_label)
                    triggers_layout.addLayout(tr_row)
                
                # Tətikləyicilər layoutunu əsas layouta əlavə et
                cmd_layout.addLayout(triggers_layout)
                
                # Sağa qalan boşluğu doldur
                cmd_layout.addStretch()
                
                special_content_layout.addWidget(cmd_frame)
        else:
            # Xüsusi əmr yoxdursa məlumat mesajı göstər
            empty_label = QLabel("Hələ xüsusi əmr əlavə edilməyib.")
            empty_label.setStyleSheet(f"color: {self.colors['text_secondary']};")
            empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            special_content_layout.addWidget(empty_label)
        
        special_scroll.setWidget(special_content)
        special_layout.addWidget(special_scroll)
        
        # Pro deyilsə yüksəltmə düyməsi əlavə et (pro tab üçün)
        if self.current_user['license_status'] != 'pro':
            # Pro tab üçün məlumatlandırma və düymə
            pro_info_label = QLabel("👑 Pro əmrləri istifadə etmək üçün Pro versiyaya keçin")
            pro_info_label.setStyleSheet(f"""
                color: {self.colors['text']};
                padding: 10px;
                font-weight: bold;
            """)
            pro_info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            pro_layout.addWidget(pro_info_label)
            
            pro_upgrade_btn = QPushButton("👑 Pro Versiyaya Yüksəlin")
            pro_upgrade_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {self.colors['warning']};
                    color: black;
                    border: none;
                    border-radius: 5px;
                    padding: 10px;
                    font-weight: bold;
                }}
                QPushButton:hover {{
                    background-color: #e6c200;
                }}
            """)
            pro_upgrade_btn.clicked.connect(self.show_upgrade_dialog)
            pro_layout.addWidget(pro_upgrade_btn)
        
        pro_scroll.setWidget(pro_content)
        pro_layout.addWidget(pro_scroll)
        
        # Əlavələr tab-ı əlavə et
        plugin_tab = QWidget()
        plugin_layout = QVBoxLayout(plugin_tab)
        
        # Əlavələri yüklə
        plugins = self.main_app.plugin_manager.get_all_plugins()
        plugin_count = len(plugins)
        
        # Scroll sahəsi
        plugin_scroll = QScrollArea()
        plugin_scroll.setWidgetResizable(True)
        plugin_scroll.setStyleSheet(f"""
            QScrollArea {{
                border: none;
                background-color: {self.colors['bg_secondary']};
            }}
            
            QScrollBar:vertical {{
                border: none;
                background-color: {self.colors['bg']};
                width: 12px;
                margin: 0px;
            }}
            
            QScrollBar::handle:vertical {{
                background-color: {self.colors['primary']};
                border-radius: 6px;
                min-height: 30px;
                margin: 2px;
            }}
            
            QScrollBar::handle:vertical:hover {{
                background-color: {self.colors['secondary']};
            }}
            
            QScrollBar::add-line:vertical {{
                height: 0px;
            }}
            
            QScrollBar::sub-line:vertical {{
                height: 0px;
            }}
            
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
                background-color: {self.colors['bg']};
                border-radius: 6px;
            }}
        """)
        
        # Scroll məzmunu
        plugin_content = QWidget()
        plugin_content_layout = QVBoxLayout(plugin_content)
        
        # Əlavələri siyahıla
        if plugins:
            for plugin in plugins:
                plugin_frame = QFrame()
                plugin_frame.setStyleSheet(f"""
                    QFrame {{
                        background-color: {self.colors['bg_secondary']};
                        border-radius: 5px;
                        margin: 2px;
                        padding: 10px;
                    }}
                """)
                plugin_frame_layout = QVBoxLayout(plugin_frame)
                
                # Yuxarı sətir - Əlavə adı və lisenziya növü
                top_row = QHBoxLayout()
                
                # Əlavə loqosu
                if plugin.get('logo'):
                    logo_label = QLabel()
                    try:
                        # Logo yolunu yarat
                        logo_path = plugin['logo']
                        
                        # Əgər nisbi yol isə, plugin qovluğunu əlavə et
                        if not os.path.isabs(logo_path):
                            plugin_name = plugin['name']
                            plugin_dir = os.path.join("plugins", plugin_name)
                            logo_path = os.path.join(plugin_dir, logo_path)
                        
                        # Logo faylının mövcud olub-olmadığını yoxla
                        if os.path.exists(logo_path):
                            logo_pixmap = QPixmap(logo_path)
                            if not logo_pixmap.isNull():
                                logo_label.setPixmap(logo_pixmap.scaled(32, 32, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
                                top_row.addWidget(logo_label)
                            else:
                                # Logo yüklənə bilmədi, standart ikon göstər
                                logo_label.setText("🔌")
                                logo_label.setStyleSheet(f"color: {self.colors['primary']}; font-size: 16px;")
                                top_row.addWidget(logo_label)
                        else:
                            # Logo faylı tapılmadı, standart ikon göstər
                            logo_label.setText("🔌")
                            logo_label.setStyleSheet(f"color: {self.colors['primary']}; font-size: 16px;")
                            top_row.addWidget(logo_label)
                    except Exception as e:
                        # Xəta halında standart ikon göstər
                        logo_label.setText("🔌")
                        logo_label.setStyleSheet(f"color: {self.colors['primary']}; font-size: 16px;")
                        top_row.addWidget(logo_label)
                else:
                    # Logo yoxdursa standart ikon göstər
                    logo_label = QLabel("🔌")
                    logo_label.setStyleSheet(f"color: {self.colors['primary']}; font-size: 16px;")
                    top_row.addWidget(logo_label)
                
                # Əlavə adı
                plugin_name_label = QLabel(f"🔌 {plugin['name']}")
                plugin_name_label.setStyleSheet(f"color: {self.colors['text']}; font-weight: bold; font-size: 14px;")
                top_row.addWidget(plugin_name_label)
                
                # Plugin növü (Python/EXE) - plugin dict-indən alınan məlumata görə
                plugin_obj = self.main_app.plugin_manager.plugins.get(plugin['name'])
                if plugin_obj and plugin_obj.get('type') == 'exe':
                    plugin_type = "⚙️ EXE"
                else:
                    plugin_type = "🐍 PYTHON"
                
                type_label = QLabel(plugin_type)
                type_label.setStyleSheet(f"color: {self.colors['primary']}; font-weight: bold; font-size: 10px;")
                top_row.addWidget(type_label)
                
                # Lisenziya növü
                license_type = "PRO" if plugin['license_type'] == 'pro' else "FREE"
                license_color = self.colors['accent'] if plugin['license_type'] == 'pro' else self.colors['success']
                license_label = QLabel(license_type)
                license_label.setStyleSheet(f"color: {license_color}; font-weight: bold; background-color: rgba(0,0,0,0.2); padding: 2px 8px; border-radius: 10px;")
                top_row.addWidget(license_label)
                
                top_row.addStretch()
                plugin_frame_layout.addLayout(top_row)
                
                # Orta sətir - Açıqlama və versiya
                middle_row = QHBoxLayout()
                
                # Açıqlama
                desc_label = QLabel(plugin['description'])
                desc_label.setStyleSheet(f"color: {self.colors['text_secondary']}; font-style: italic;")
                middle_row.addWidget(desc_label)
                
                middle_row.addStretch()
                
                # Versiya
                version_label = QLabel(f"v{plugin['version']}")
                version_label.setStyleSheet(f"color: {self.colors['text_secondary']}; font-size: 12px;")
                middle_row.addWidget(version_label)
                
                plugin_frame_layout.addLayout(middle_row)
                
                # Nəşriyyatçı məlumatı
                author_label = QLabel(f"Nəşriyyatçı: {plugin['author']}")
                author_label.setStyleSheet(f"color: {self.colors['text_secondary']}; font-size: 12px;")
                plugin_frame_layout.addWidget(author_label)
                
                # Tətikləyicilər
                triggers_label = QLabel("Tətikləyicilər:")
                triggers_label.setStyleSheet(f"color: {self.colors['text']}; font-weight: bold; margin-top: 5px;")
                plugin_frame_layout.addWidget(triggers_label)
                
                # Azərbaycan dili tətikləyiciləri
                az_triggers = plugin['triggers'].get('az-AZ', [])
                if az_triggers:
                    az_row = QHBoxLayout()
                    az_row.setSpacing(5)
                    az_icon = QLabel()
                    az_icon.setPixmap(QPixmap("resim/AZ.png").scaled(25, 15, Qt.AspectRatioMode.KeepAspectRatio))
                    az_row.addWidget(az_icon)
                    az_triggers_text = ", ".join(az_triggers)
                    az_label = QLabel(az_triggers_text)
                    az_label.setStyleSheet(f"color: {self.colors['text_secondary']}; font-size: 11px;")
                    az_row.addWidget(az_label)
                    az_row.addStretch()
                    plugin_frame_layout.addLayout(az_row)
                
                # Türk dili tətikləyiciləri
                tr_triggers = plugin['triggers'].get('tr-TR', [])
                if tr_triggers:
                    tr_row = QHBoxLayout()
                    tr_row.setSpacing(5)
                    tr_icon = QLabel()
                    tr_icon.setPixmap(QPixmap("resim/TR.png").scaled(25, 15, Qt.AspectRatioMode.KeepAspectRatio))
                    tr_row.addWidget(tr_icon)
                    tr_triggers_text = ", ".join(tr_triggers)
                    tr_label = QLabel(tr_triggers_text)
                    tr_label.setStyleSheet(f"color: {self.colors['text_secondary']}; font-size: 11px;")
                    tr_row.addWidget(tr_label)
                    tr_row.addStretch()
                    plugin_frame_layout.addLayout(tr_row)
                
                plugin_content_layout.addWidget(plugin_frame)
                
                # Ayırıcı xətt əlavə et (son əlavə deyilsə)
                if plugin != plugins[-1]:
                    divider = QFrame()
                    divider.setFrameShape(QFrame.Shape.HLine)
                    divider.setStyleSheet(f"""
                        QFrame {{
                            border: none;
                            background-color: {self.colors['bg']};
                            max-height: 1px;
                            margin: 5px 0px;
                        }}
                    """)
                    plugin_content_layout.addWidget(divider)
        else:
            # Əlavə yoxdursa məlumat mesajı göstər
            empty_label = QLabel("Hələ əlavə yüklənməyib.")
            empty_label.setStyleSheet(f"color: {self.colors['text_secondary']};")
            empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            plugin_content_layout.addWidget(empty_label)
        
        plugin_scroll.setWidget(plugin_content)
        plugin_layout.addWidget(plugin_scroll)
        
        # Tabları əlavə et
        tab_widget.addTab(free_tab, f"🆓 Free Əmrlər ({free_count})")
        tab_widget.addTab(pro_tab, f"👑 Pro Əmrlər ({pro_count})")
        tab_widget.addTab(special_tab, f"⭐ Xüsusi Əmrlər ({special_count})")
        tab_widget.addTab(plugin_tab, f"🔌 Əlavələr ({plugin_count})")
        
        layout.addWidget(tab_widget)
        
        # Dialogu göstər
        dialog.exec()
        
    def show_upgrade_dialog(self):
        """Pro versiyaya yüksəltmə dialogunu göstər"""
        dialog = QDialog(self.main_app)
        dialog.setWindowTitle("Pro Versiyaya Yüksəlin")
        dialog.setMinimumSize(400, 300)
        dialog.setStyleSheet(f"background-color: {self.colors['bg']};")
        
        # Əsas layout
        layout = QVBoxLayout(dialog)
        
        # Başlıq
        title = QLabel("👑 Pro Versiyaya Yüksəlin")
        title.setFont(QFont("Helvetica", 16, QFont.Weight.Bold))
        title.setStyleSheet(f"color: {self.colors['warning']};")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Açıqlama
        desc = QLabel("Pro versiya ilə bütün əmrləri və xüsusiyyətləri əldə edin!")
        desc.setStyleSheet(f"color: {self.colors['text']};")
        desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(desc)
        
        # Aktivasiya kodu daxiletməsi
        key_layout = QHBoxLayout()
        key_label = QLabel("Aktivasiya Kodu:")
        key_label.setStyleSheet(f"color: {self.colors['text']};")
        key_layout.addWidget(key_label)
        
        self.key_entry = QLineEdit()
        self.key_entry.setPlaceholderText("PRO123-456-789")
        self.key_entry.setStyleSheet(f"""
            QLineEdit {{
                background-color: {self.colors['bg_tertiary']};
                color: {self.colors['text']};
                border: 1px solid {self.colors['border']};
                border-radius: 5px;
                padding: 5px;
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
        key_layout.addWidget(self.key_entry)
        
        layout.addLayout(key_layout)
        
        # Aktivasiya düyməsi
        activate_btn = QPushButton("Aktivləşdir")
        activate_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.colors['warning']};
                color: {self.colors['bg']};
                border: none;
                border-radius: 5px;
                padding: 10px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: #E6A700;
            }}
            QPushButton:pressed {{
                background-color: #B8860B;
            }}
        """)
        activate_btn.clicked.connect(lambda: self.activate_pro_key(dialog))
        layout.addWidget(activate_btn)
        
        # Dialogu göstər
        dialog.exec()
        
    def activate_pro_key(self, dialog):
        """Pro aktivasiya kodunu yoxla və aktivləşdir"""
        key = self.key_entry.text().strip()
        
        if not key:
            QMessageBox.warning(dialog, "Xəta", "Zəhmət olmasa aktivasiya kodunu daxil edin.")
            return
        
        # MySQL-dən key-i aktivləşdir
        success, message = db_manager.activate_pro_key(key, self.current_user['id'])
        
        if success:
            # İstifadəçi məlumatlarını yenilə
            self.current_user['license_status'] = 'pro'
            
            # Key-in müddətini öyrən
            key_info = db_manager.get_pro_key(key)
            if key_info:
                # Pro müddətini hesabla
                expiry_date = datetime.datetime.now() + datetime.timedelta(days=key_info['duration'])
                self.current_user['pro_expiry'] = expiry_date.strftime("%Y-%m-%d %H:%M:%S")
                self.pro_expiry = expiry_date
            
            # UI-ı yenilə
            self.update_pro_status()
            
            # Uğur mesajı
            QMessageBox.information(dialog, "Uğurlu Aktivasiya", 
                                  f"Pro versiya uğurla aktivləşdirildi! {key_info['duration']} gün müddətində bütün xüsusiyyətlərdən istifadə edə bilərsiniz.")
            
            # Dialogu bağla
            dialog.accept()
        else:
            # Xəta mesajı
            QMessageBox.warning(dialog, "Xəta", message)

    def update_pro_status(self):
        """Pro vəziyyətini UI-da yenilə"""
        if self.current_user['license_status'] == 'pro':
            # Admin yoxlaması əlavə etdik
            if self.current_user.get('role') == 'admin':
                self.main_app.user_label.setText(f"👤 {self.current_user['name']} 👑 (Limitsiz)")
            # Pro_expiry yoxdursa və ya boşdursa limitsiz göstər
            elif 'pro_expiry' not in self.current_user or not self.current_user['pro_expiry']:
                self.main_app.user_label.setText(f"👤 {self.current_user['name']} 💎 (Limitsiz)")
            else:
                remaining_days, remaining_hours, remaining_minutes, remaining_seconds = self.get_remaining_pro_time()
                
                # Müddət bitibsə free-yə keçir
                if remaining_days <= 0 and remaining_hours <= 0 and remaining_minutes <= 0 and remaining_seconds <= 0:
                    # Pro müddəti bitəndə bildiriş göstər (yalnız pro_expiry varsa)
                    if 'pro_expiry' in self.current_user:
                        self.main_app.user_label.setText(f"👤 {self.current_user['name']} 🆓 (Pro müddətiniz bitdi)")
                    else:
                        self.main_app.user_label.setText(f"👤 {self.current_user['name']} 🆓")
                    
                    self.current_user['license_status'] = 'free'
                    self.pro_expiry = None
                    # Verilənlər bazasını yenilə
                    db_manager.update_license_status(self.current_user['id'], 'free')
                    return
                
                badge_icon = "💎"
                
                # Zaman vahidlərini hesabla
                years = remaining_days // 365
                months = (remaining_days % 365) // 30
                weeks = (remaining_days % 30) // 7
                days = remaining_days % 7
                
                # İki zaman vahidini göstər, ikinci vahid 0 olarsa növbəti vahidə keç
                if years > 0:
                    if months > 0:
                        time_text = f"{years} il {months} ay"
                    elif weeks > 0:
                        time_text = f"{years} il {weeks} həftə"
                    elif days > 0:
                        time_text = f"{years} il {days} gün"
                    elif remaining_hours > 0:
                        time_text = f"{years} il {remaining_hours} saat"
                    elif remaining_minutes > 0:
                        time_text = f"{years} il {remaining_minutes} dəq"
                    elif remaining_seconds > 0:
                        time_text = f"{years} il {remaining_seconds} sn"
                    else:
                        time_text = f"{years} il"
                elif months > 0:
                    if weeks > 0:
                        time_text = f"{months} ay {weeks} həftə"
                    elif days > 0:
                        time_text = f"{months} ay {days} gün"
                    elif remaining_hours > 0:
                        time_text = f"{months} ay {remaining_hours} saat"
                    elif remaining_minutes > 0:
                        time_text = f"{months} ay {remaining_minutes} dəq"
                    elif remaining_seconds > 0:
                        time_text = f"{months} ay {remaining_seconds} sn"
                    else:
                        time_text = f"{months} ay"
                elif weeks > 0:
                    if days > 0:
                        time_text = f"{weeks} həftə {days} gün"
                    elif remaining_hours > 0:
                        time_text = f"{weeks} həftə {remaining_hours} saat"
                    elif remaining_minutes > 0:
                        time_text = f"{weeks} həftə {remaining_minutes} dəq"
                    elif remaining_seconds > 0:
                        time_text = f"{weeks} həftə {remaining_seconds} sn"
                    else:
                        time_text = f"{weeks} həftə"
                elif days > 0:
                    if remaining_hours > 0:
                        time_text = f"{days} gün {remaining_hours} saat"
                    elif remaining_minutes > 0:
                        time_text = f"{days} gün {remaining_minutes} dəq"
                    elif remaining_seconds > 0:
                        time_text = f"{days} gün {remaining_seconds} sn"
                    else:
                        time_text = f"{days} gün"
                elif remaining_hours > 0:
                    if remaining_minutes > 0:
                        time_text = f"{remaining_hours} saat {remaining_minutes} dəq"
                    elif remaining_seconds > 0:
                        time_text = f"{remaining_hours} saat {remaining_seconds} sn"
                    else:
                        time_text = f"{remaining_hours} saat"
                elif remaining_minutes > 0:
                    if remaining_seconds > 0:
                        time_text = f"{remaining_minutes} dəq {remaining_seconds} sn"
                    else:
                        time_text = f"{remaining_minutes} dəq"
                else:
                    time_text = f"{remaining_seconds} sn"
                
                self.main_app.user_label.setText(f"👤 {self.current_user['name']} {badge_icon} ({time_text})")
        else:
            # Free istifadəçi üçün pro_expiry yoxlaması
            if 'pro_expiry' in self.current_user and self.current_user['pro_expiry']:
                # Pro müddəti əvvəlcədən varmış və bitmiş
                self.main_app.user_label.setText(f"👤 {self.current_user['name']} 🆓 (Pro müddətiniz bitdi)")
            else:
                # Normal free istifadəçi
                self.main_app.user_label.setText(f"👤 {self.current_user['name']} 🆓")

    def get_remaining_pro_days(self):
        """Pro versiyanın qalan gün sayını hesabla"""
        try:
            # Əvvəlcə pro_expiry-nin None olub-olmadığını yoxla
            if self.pro_expiry is None:
                return 0
            
            # Pro müddətinin dolub-dolmadığını yoxla
            remaining = self.pro_expiry - datetime.datetime.now()
            return max(0, remaining.days)
        except:
            return 0

    def get_remaining_pro_time(self):
        """Pro versiyanın qalan zamanını gün, saat, dəqiqə və saniyə olaraq hesabla"""
        try:
            # Əvvəlcə pro_expiry-nin None olub-olmadığını yoxla
            if self.pro_expiry is None:
                return 0, 0, 0, 0
            
            # Pro müddətinin dolub-dolmadığını yoxla
            now = datetime.datetime.now()
            if self.pro_expiry <= now:
                return 0, 0, 0, 0
                
            remaining = self.pro_expiry - now
            days = remaining.days
            seconds = remaining.seconds
            
            hours = seconds // 3600
            seconds %= 3600
            minutes = seconds // 60
            seconds %= 60
            
            return days, hours, minutes, seconds
        except:
            return 0, 0, 0, 0

    def check_pro_status(self):
        """İstifadəçinin pro vəziyyətini yoxla"""
        try:
            # Admin yoxlaması əlavə etdik
            if self.current_user.get('role') == 'admin':
                self.current_user['license_status'] = 'pro'
                self.pro_expiry = datetime.datetime.max
                # Admin üçün UI yenilə
                if hasattr(self.main_app, 'user_label'):
                    self.main_app.user_label.setText(f"👤 {self.current_user['name']} 👑 (Limitsiz)")
                return  # Admin üçün digər yoxlamaları atla
            
            # Normal istifadəçi yoxlamaları...
            if 'pro_expiry' in self.current_user and self.current_user['pro_expiry']:
                expiry_date = datetime.datetime.strptime(
                    self.current_user['pro_expiry'],
                    "%Y-%m-%d %H:%M:%S"
                )
                if expiry_date > datetime.datetime.now():
                    # Müddət dolmayıbsa pro et
                    self.current_user['license_status'] = 'pro'
                    self.pro_expiry = expiry_date
                else:
                    # Müddət dolmuşdursa free et
                    self.current_user['license_status'] = 'free'
                    self.pro_expiry = None
                    # Verilənlər bazasını yenilə
                    db_manager.update_license_status(self.current_user['id'], 'free')
            else:
                # Pro_expiry yoxdursa mövcud lisenziya vəziyyətini qoru
                # Pro olarsa limitsiz olaraq təyin et
                if self.current_user.get('license_status') == 'pro':
                    self.pro_expiry = datetime.datetime.max
                else:
                    self.pro_expiry = None
            
            # UI yenilə
            if hasattr(self.main_app, 'user_label'):
                self.update_pro_status()
            
        except Exception as e:
            # Dilə görə xəta mesajı
            if hasattr(self.main_app, 'voice_settings') and self.main_app.voice_settings.get('language') == 'tr-TR':
                print(f"Pro durum kontrolünde hata: {str(e)}")
            else:
                print(f"Pro vəziyyət yoxlamasında xəta: {str(e)}")
            self.pro_expiry = None