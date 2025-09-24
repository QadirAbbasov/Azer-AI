from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
                            QTabWidget, QWidget, QComboBox, QFrame, QScrollArea,
                            QLineEdit, QMessageBox, QGridLayout)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap
import os

class UserSettings:
    def __init__(self, Azer_AI):
        self.Azer_AI = Azer_AI
        self.settings_window = None
        self.colors = Azer_AI.colors

    def show_settings(self):
        # Əgər pəncərə artıq açıqdırsa, yalnız önə gətir
        if self.settings_window is not None and self.settings_window.isVisible():
            self.settings_window.activateWindow()
            self.settings_window.raise_()
            return
        
        # Əgər pəncərə bağlıdırsa və ya heç yaradılmayıbsa, yeni bir dənə yarat
        self.settings_window = QDialog(self.Azer_AI)
        self.settings_window.setWindowTitle("İstifadəçi Parametrləri")
        self.settings_window.setMinimumSize(600, 700)
        self.settings_window.setStyleSheet(f"background-color: {self.colors['bg']};")
        
        # Əsas layout
        main_layout = QVBoxLayout(self.settings_window)
        
        # Tabview yarat
        tabview = QTabWidget()
        tabview.setStyleSheet(f"""
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
        
        # Sekmələri əlavə et
        tab_voice = QWidget()
        tab_assistant = QWidget()
        tab_appearance = QWidget()
        tab_commands = QWidget()
        tab_plugins = QWidget()
        
        tabview.addTab(tab_voice, "🔊 Səs Parametrləri")
        tabview.addTab(tab_assistant, "🤖 Asistan Parametrləri")
        tabview.addTab(tab_appearance, "🎨 Görünüş")
        tabview.addTab(tab_commands, "⚡ Əmrlər")
        tabview.addTab(tab_plugins, "🔌 Plugin-lər")
        
        # Sekmələri yarat
        self.create_voice_settings(tab_voice)
        self.create_assistant_settings(tab_assistant)
        self.create_appearance_settings(tab_appearance)
        self.create_command_settings(tab_commands)
        self.create_plugin_settings(tab_plugins)
        
        # Ana tətbiqdə əmrləri yenilə (pəncərə açıldığında)
        self.Azer_AI.refresh_custom_commands()
        
        main_layout.addWidget(tabview)
        
        # Alt düymələr üçün frame
        button_frame = QFrame()
        button_frame.setStyleSheet("background-color: transparent;")
        button_layout = QHBoxLayout(button_frame)
        
        # Saxla Düyməsi
        save_btn = QPushButton("💾 Bütün Parametrləri Saxla")
        save_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.colors['primary']};
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
                font-size: 12pt;
            }}
            QPushButton:hover {{
                background-color: {self.colors['secondary']};
            }}
        """)
        save_btn.clicked.connect(self.save_all_settings)
        button_layout.addWidget(save_btn)
        
        # Ləğv Et Düyməsi
        cancel_btn = QPushButton("❌ Ləğv et")
        cancel_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.colors['bg_tertiary']};
                color: {self.colors['text']};
                border: 1px solid {self.colors['border']};
                border-radius: 5px;
                padding: 10px;
                font-size: 12pt;
            }}
            QPushButton:hover {{
                background-color: {self.colors['bg_secondary']};
                border-color: {self.colors['primary']};
            }}
        """)
        cancel_btn.clicked.connect(self.close_settings)
        button_layout.addWidget(cancel_btn)
        
        main_layout.addWidget(button_frame)
        
        # Pəncərə bağlandığında self.settings_window-u None et
        self.settings_window.finished.connect(self.on_settings_closed)
        
        # Ana tətbiqdə əmrləri yenilə (pəncərə açıldığında)
        self.Azer_AI.refresh_custom_commands()
        
        # Pəncərəni göstər
        self.settings_window.exec()

    def on_settings_closed(self):
        """Parametrlər pəncərəsi bağlandığında çağırılır"""
        # Ana tətbiqdə əmrləri yenilə (pəncərə bağlandığında)
        self.Azer_AI.refresh_custom_commands()
        self.settings_window = None

    def create_voice_settings(self, parent):
        layout = QVBoxLayout(parent)
        
        # TTS Motoru seçimi
        engine_frame = QFrame()
        engine_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {self.colors['bg_secondary']};
                border-radius: 5px;
                padding: 10px;
            }}
        """)
        engine_layout = QVBoxLayout(engine_frame)
        
        engine_label = QLabel("TTS Motoru:")
        engine_label.setStyleSheet(f"color: {self.colors['text']};")
        engine_layout.addWidget(engine_label)
        
        self.tts_engine_combo = QComboBox()
        self.tts_engine_combo.addItems(["Edge TTS", "gTTS"])
        self.tts_engine_combo.setCurrentIndex(0 if self.Azer_AI.voice_settings['tts_engine'] == 'edge' else 1)
        self.tts_engine_combo.setStyleSheet(f"""
            QComboBox {{
                background-color: {self.colors['bg_tertiary']};
                color: {self.colors['text']};
                border: 1px solid {self.colors['border']};
                border-radius: 5px;
                padding: 5px;
            }}
            QComboBox:hover {{
                border: 1px solid {self.colors['primary']};
                background-color: {self.colors['bg_secondary']};
            }}
            QComboBox:focus {{
                border: 2px solid {self.colors['accent']};
                background-color: {self.colors['bg_secondary']};
            }}
            QComboBox::drop-down {{
                border: none;
            }}
            QComboBox QAbstractItemView {{
                background-color: {self.colors['bg_secondary']};
                color: {self.colors['text']};
                selection-background-color: {self.colors['primary']};
                border: 1px solid {self.colors['border']};
            }}
        """)
        engine_layout.addWidget(self.tts_engine_combo)
        
        layout.addWidget(engine_frame)
        
        # Dil seçimi
        language_frame = QFrame()
        language_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {self.colors['bg_secondary']};
                border-radius: 5px;
                padding: 10px;
            }}
        """)
        language_layout = QVBoxLayout(language_frame)
        
        language_label = QLabel("Dil:")
        language_label.setStyleSheet(f"color: {self.colors['text']};")
        language_layout.addWidget(language_label)
        
        self.language_combo = QComboBox()
        self.language_combo.addItems(["Azərbaycan dili (az-AZ)", "Türk dili (tr-TR)"])
        self.language_combo.setCurrentIndex(0 if self.Azer_AI.voice_settings['language'] == 'az-AZ' else 1)
        self.language_combo.setStyleSheet(f"""
            QComboBox {{
                background-color: {self.colors['bg_tertiary']};
                color: {self.colors['text']};
                border: 1px solid {self.colors['border']};
                border-radius: 5px;
                padding: 5px;
            }}
            QComboBox:hover {{
                border: 1px solid {self.colors['primary']};
                background-color: {self.colors['bg_secondary']};
            }}
            QComboBox:focus {{
                border: 2px solid {self.colors['accent']};
                background-color: {self.colors['bg_secondary']};
            }}
            QComboBox::drop-down {{
                border: none;
            }}
            QComboBox QAbstractItemView {{
                background-color: {self.colors['bg_secondary']};
                color: {self.colors['text']};
                selection-background-color: {self.colors['primary']};
                border: 1px solid {self.colors['border']};
            }}
        """)
        language_layout.addWidget(self.language_combo)
        
        layout.addWidget(language_frame)
        
        # Ses cinsiyet seçimi
        gender_frame = QFrame()
        gender_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {self.colors['bg_secondary']};
                border-radius: 5px;
                padding: 10px;
            }}
        """)
        gender_layout = QVBoxLayout(gender_frame)
        
        gender_label = QLabel("Səs Cinsi:")
        gender_label.setStyleSheet(f"color: {self.colors['text']};")
        gender_layout.addWidget(gender_label)
        
        self.gender_combo = QComboBox()
        self.gender_combo.addItems(["Kişi səsi", "Qadın səsi"])
        self.gender_combo.setCurrentIndex(0 if self.Azer_AI.voice_settings['voice_gender'] == 'male' else 1)
        self.gender_combo.setStyleSheet(f"""
            QComboBox {{
                background-color: {self.colors['bg_tertiary']};
                color: {self.colors['text']};
                border: 1px solid {self.colors['border']};
                border-radius: 5px;
                padding: 5px;
            }}
            QComboBox:hover {{
                border: 1px solid {self.colors['primary']};
                background-color: {self.colors['bg_secondary']};
            }}
            QComboBox:focus {{
                border: 2px solid {self.colors['accent']};
                background-color: {self.colors['bg_secondary']};
            }}
            QComboBox::drop-down {{
                border: none;
            }}
            QComboBox QAbstractItemView {{
                background-color: {self.colors['bg_secondary']};
                color: {self.colors['text']};
                selection-background-color: {self.colors['primary']};
                border: 1px solid {self.colors['border']};
            }}
        """)
        gender_layout.addWidget(self.gender_combo)
        
        layout.addWidget(gender_frame)
        
        # Test düyməsi
        test_btn = QPushButton("🔊 Səsi Test Et")
        test_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.colors['primary']};
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
            }}
            QPushButton:hover {{
                background-color: {self.colors['secondary']};
            }}
        """)
        test_btn.clicked.connect(self.test_voice)
        layout.addWidget(test_btn)
        
        # Boşluq əlavə et
        layout.addStretch()

    def create_assistant_settings(self, parent):
        layout = QVBoxLayout(parent)
        
        # Wake Word parametrləri
        wake_word_frame = QFrame()
        wake_word_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {self.colors['bg_secondary']};
                border-radius: 5px;
                padding: 10px;
            }}
        """)
        wake_word_layout = QVBoxLayout(wake_word_frame)
        
        # Başlıq
        title_label = QLabel("Wake Word Parametrləri")
        title_label.setStyleSheet(f"color: {self.colors['text']}; font-weight: bold;")
        wake_word_layout.addWidget(title_label)
        
        # Açıqlama
        desc_label = QLabel("Asistanı aktivləşdirmək üçün istifadə edəcəyiniz 'wake word'ləri fərdiləşdirə bilərsiniz. Hər dil üçün fərqli sözlər təyin edə bilərsiniz. Vergüllə ayıraraq çoxlu söz əlavə edə bilərsiniz.")
        desc_label.setStyleSheet(f"color: {self.colors['text_secondary']};")
        desc_label.setWordWrap(True)
        wake_word_layout.addWidget(desc_label)
        
        # Əsas Wake Word parametrləri
        base_words_frame = QFrame()
        base_words_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {self.colors['bg']};
                border-radius: 5px;
                padding: 10px;
                margin-top: 5px;
                margin-bottom: 10px;
            }}
        """)
        base_words_layout = QGridLayout(base_words_frame)
        
        # Əsas Wake Words başlıq
        base_title = QLabel("Əsas Wake Word'lər")
        base_title.setStyleSheet(f"color: {self.colors['primary']}; font-weight: bold;")
        base_words_layout.addWidget(base_title, 0, 0, 1, 2)
        
        # Azərbaycan dili əsas wake word
        az_base_label = QLabel("Azərbaycan dili:")
        az_base_label.setStyleSheet(f"color: {self.colors['text']};")
        base_words_layout.addWidget(az_base_label, 1, 0)
        
        self.az_base_word = QLineEdit()
        self.az_base_word.setPlaceholderText("Məsəl: azər, samir, asistan (vergüllə ayırın)")
        self.az_base_word.setStyleSheet(f"""
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
        
        # Mövcud az_word dəyərini yüklə
        if 'wake_word_settings' in self.Azer_AI.current_user and 'az_word' in self.Azer_AI.current_user['wake_word_settings']:
            self.az_base_word.setText(self.Azer_AI.current_user['wake_word_settings']['az_word'])
        else:
            # Standart dəyər
            self.az_base_word.setText('azər')
        
        base_words_layout.addWidget(self.az_base_word, 1, 1)
        
        # Türk dili əsas wake word
        tr_base_label = QLabel("Türk dili:")
        tr_base_label.setStyleSheet(f"color: {self.colors['text']};")
        base_words_layout.addWidget(tr_base_label, 2, 0)
        
        self.tr_base_word = QLineEdit()
        self.tr_base_word.setPlaceholderText("Nümunə: azer, samir, asistan (vergüllə ayırın)")
        self.tr_base_word.setStyleSheet(f"""
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
        
        # Mövcud tr_word dəyərini yüklə
        if 'wake_word_settings' in self.Azer_AI.current_user and 'tr_word' in self.Azer_AI.current_user['wake_word_settings']:
            self.tr_base_word.setText(self.Azer_AI.current_user['wake_word_settings']['tr_word'])
        else:
            # Standart dəyər
            self.tr_base_word.setText('azer')
        
        base_words_layout.addWidget(self.tr_base_word, 2, 1)
        
        # Açıqlama mətni
        base_info = QLabel("Bu sözlər, vergüllə ayrılmış şəkildə, asistanınızı təyin etdiyiniz sözlərlə aktivləşdirmək üçün istifadə ediləcək.")
        base_info.setStyleSheet(f"color: {self.colors['text_secondary']}; font-style: italic; font-size: 10px;")
        base_info.setWordWrap(True)
        base_words_layout.addWidget(base_info, 3, 0, 1, 2)
        
        wake_word_layout.addWidget(base_words_frame)
        
        # Xəbərdarlıq
        note_label = QLabel("Qeyd: Wake word dəyişiklikləri tətbiqi yenidən başlatdıqdan sonra aktivləşir.")
        note_label.setStyleSheet(f"color: {self.colors['warning']}; font-style: italic;")
        note_label.setWordWrap(True)
        wake_word_layout.addWidget(note_label)
        
        layout.addWidget(wake_word_frame)
        
        # Boşluq əlavə et
        layout.addStretch()

    def create_appearance_settings(self, parent):
        layout = QVBoxLayout(parent)
        
        # Görünüş parametrləri burada olacaq
        # İndi boş buraxırıq
        layout.addWidget(QLabel("Görünüş parametrləri tezliklə əlavə ediləcək..."))
        
    def create_command_settings(self, parent):
        layout = QVBoxLayout(parent)
        
        # İstifadəçi lisenziya vəziyyətini yoxla
        is_pro = self.Azer_AI.current_user['license_status'] == "pro"
        
        # Başlıq
        title = QLabel("Xüsusi Əmrlər")
        title.setFont(QFont("Helvetica", 14, QFont.Weight.Bold))
        title.setStyleSheet(f"color: {self.colors['text']};")
        layout.addWidget(title)
        
        if not is_pro:
            # Free istifadəçilər üçün Pro xüsusiyyəti mesajı
            pro_message = QLabel("Bu xüsusiyyət yalnız Pro istifadəçilərə aiddir.")
            pro_message.setStyleSheet(f"color: {self.colors['error']}; font-size: 12pt;")
            pro_message.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(pro_message)
            
            # Pro versiya alma düyməsi
            upgrade_btn = QPushButton("Pro Versiyaya Yüksəlt")
            upgrade_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {self.colors['primary']};
                    color: white;
                    border: none;
                    border-radius: 5px;
                    padding: 10px;
                    font-size: 12pt;
                }}
                QPushButton:hover {{
                    background-color: {self.colors['secondary']};
                }}
            """)
            upgrade_btn.clicked.connect(self.show_upgrade_dialog)
            layout.addWidget(upgrade_btn)
            
            # Boşluq əlavə et
            layout.addStretch()
            return
        
        # Pro istifadəçilər üçün xüsusi əmr interfeysi
        # Açıqlama
        desc = QLabel("Xüsusi əmrlərinizi əlavə edin, düzənləyin və ya silin.")
        desc.setStyleSheet(f"color: {self.colors['text_secondary']};")
        layout.addWidget(desc)
        
        # Əmr siyahısı
        self.command_list_frame = QScrollArea()
        self.command_list_frame.setWidgetResizable(True)
        self.command_list_frame.setStyleSheet(f"""
            QScrollArea {{
                border: 1px solid {self.colors['primary']};
                border-radius: 5px;
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
        
        # Əmr siyahısını yarat
        self.command_list_content = QWidget()
        self.command_list_layout = QVBoxLayout(self.command_list_content)
        self.command_list_frame.setWidget(self.command_list_content)
        
        # Əmrləri yüklə
        self.update_command_list()
        
        # Ana tətbiqdə əmrləri yenilə (mövcud dəyişiklikləri yükləmək üçün)
        self.Azer_AI.refresh_custom_commands()
        
        layout.addWidget(self.command_list_frame)
        
        # Yeni əmr əlavə et düyməsi
        add_btn = QPushButton("➕ Yeni Əmr Əlavə Et")
        add_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.colors['primary']};
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
            }}
            QPushButton:hover {{
                background-color: {self.colors['secondary']};
            }}
        """)
        add_btn.clicked.connect(lambda: self.show_command_dialog())
        layout.addWidget(add_btn)
        
    def update_command_list(self):
        """Əmr siyahısını yenilə"""
        # Mövcud əmrləri təmizlə
        for i in reversed(range(self.command_list_layout.count())):
            widget = self.command_list_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()
        
        # Əmrləri yüklə
        custom_commands = self.Azer_AI.load_custom_commands()
        
        if not custom_commands:
            empty_label = QLabel("Hələ xüsusi əmr əlavə edilməyib.")
            empty_label.setStyleSheet(f"color: {self.colors['text_secondary']};")
            empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.command_list_layout.addWidget(empty_label)
            return
        
        # Hər əmr üçün bir frame yarat
        for command in custom_commands:
            cmd_frame = QFrame()
            cmd_frame.setStyleSheet(f"""
                QFrame {{
                    background-color: {self.colors['bg']};
                    border-radius: 5px;
                    margin: 2px;
                    padding: 5px;
                }}
            """)
            cmd_layout = QVBoxLayout(cmd_frame)
            
            # Yuxarı sətir - Əmr adı və növü
            top_layout = QHBoxLayout()
            
            # Əmr adı
            cmd_name = QLabel(command['name'])
            cmd_name.setStyleSheet(f"color: {self.colors['text']}; font-weight: bold;")
            top_layout.addWidget(cmd_name)
            
            # Əmr növü
            cmd_type = QLabel(command['action'])
            cmd_type.setStyleSheet(f"color: {self.colors['text_secondary']};")
            top_layout.addWidget(cmd_type)
            
            # Boşluq əlavə et
            top_layout.addStretch()
            
            # Düzənlə düyməsi
            edit_btn = QPushButton("✏️")
            edit_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {self.colors['primary']};
                    color: white;
                    border: none;
                    border-radius: 5px;
                    padding: 5px;
                }}
            """)
            edit_btn.clicked.connect(lambda checked, cmd=command: self.edit_command(cmd))
            top_layout.addWidget(edit_btn)
            
            # Sil düyməsi
            delete_btn = QPushButton("🗑️")
            delete_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {self.colors['error']};
                    color: white;
                    border: none;
                    border-radius: 5px;
                    padding: 5px;
                }}
            """)
            delete_btn.clicked.connect(lambda checked, cmd=command: self.delete_command(cmd))
            top_layout.addWidget(delete_btn)
            
            cmd_layout.addLayout(top_layout)
            
            # Alt sətir - Tətikləyicilər
            triggers_layout = QVBoxLayout()
            triggers_layout.setSpacing(5)  # Sətirlər arası boşluq
            
            # Azərbaycan dili tətikləyiciləri
            az_triggers = command['triggers'].get('az-AZ', [])
            if az_triggers:
                az_row = QHBoxLayout()
                az_row.setSpacing(5)  # Bayraq və mətn arası boşluq
                az_icon = QLabel()
                az_icon.setPixmap(QPixmap("resim/AZ.png").scaled(30, 20, Qt.AspectRatioMode.KeepAspectRatio))
                az_row.addWidget(az_icon)
                az_label = QLabel(", ".join(az_triggers))
                az_label.setStyleSheet(f"color: {self.colors['text_secondary']};")
                az_row.addWidget(az_label)
                az_row.addStretch()  # Sağa doğru genişlənmə
                triggers_layout.addLayout(az_row)
            
            # Türk dili tətikləyiciləri
            tr_triggers = command['triggers'].get('tr-TR', [])
            if tr_triggers:
                tr_row = QHBoxLayout()
                tr_row.setSpacing(5)  # Bayraq və mətn arası boşluq
                tr_icon = QLabel()
                tr_icon.setPixmap(QPixmap("resim/TR.png").scaled(30, 20, Qt.AspectRatioMode.KeepAspectRatio))
                tr_row.addWidget(tr_icon)
                tr_label = QLabel(", ".join(tr_triggers))
                tr_label.setStyleSheet(f"color: {self.colors['text_secondary']};")
                tr_row.addWidget(tr_label)
                tr_row.addStretch()  # Sağa doğru genişlənmə
                triggers_layout.addLayout(tr_row)
            
            cmd_layout.addLayout(triggers_layout)
            
            self.command_list_layout.addWidget(cmd_frame)
            
            # Ayırıcı xətt əlavə et (son əmr deyilsə)
            if command != custom_commands[-1]:
                divider = QFrame()
                divider.setFrameShape(QFrame.Shape.HLine)
                divider.setStyleSheet(f"""
                    QFrame {{
                        border: none;
                        background-color: {self.colors['bg_secondary']};
                        max-height: 1px;
                        margin: 5px 0px;
                    }}
                """)
                self.command_list_layout.addWidget(divider)
        
        # Boşluq əlavə et
        self.command_list_layout.addStretch()
        
    def show_command_dialog(self, command=None):
        """Əmr əlavə etmə/düzənləmə dialogunu göstər"""
        dialog = QDialog(self.settings_window)
        dialog.setWindowTitle("Əmr Əlavə Et" if command is None else "Əmri Düzənlə")
        dialog.setMinimumWidth(500)
        dialog.setStyleSheet(f"background-color: {self.colors['bg']};")
        
        layout = QVBoxLayout(dialog)
        
        # Əmr adı
        name_layout = QHBoxLayout()
        name_label = QLabel("Əmr Adı:")
        name_label.setStyleSheet(f"color: {self.colors['text']};")
        name_layout.addWidget(name_label)
        
        self.cmd_name_entry = QLineEdit()
        self.cmd_name_entry.setStyleSheet(f"""
            QLineEdit {{
                background-color: {self.colors['bg_secondary']};
                color: {self.colors['text']};
                border: 1px solid {self.colors['primary']};
                border-radius: 5px;
                padding: 5px;
            }}
        """)
        if command:
            self.cmd_name_entry.setText(command['name'])
        name_layout.addWidget(self.cmd_name_entry)
        
        layout.addLayout(name_layout)
        
        # Əmr növü
        action_layout = QHBoxLayout()
        action_label = QLabel("Əmr Növü:")
        action_label.setStyleSheet(f"color: {self.colors['text']};")
        action_layout.addWidget(action_label)
        
        self.cmd_action_combo = QComboBox()
        self.cmd_action_combo.addItems([
            "Proqram Aç", "Proqram Bağla", "Veb Sayt Aç", "Skript İşlət", "Veb Axtarış", "Klaviatura Qısayolu"
        ])
        self.cmd_action_combo.setStyleSheet(f"""
            QComboBox {{
                background-color: {self.colors['bg_secondary']};
                color: {self.colors['text']};
                border: 1px solid {self.colors['primary']};
                border-radius: 5px;
                padding: 5px;
            }}
            QComboBox::drop-down {{
                border: none;
            }}
            QComboBox QAbstractItemView {{
                background-color: {self.colors['bg']};
                color: {self.colors['text']};
                selection-background-color: {self.colors['primary']};
            }}
        """)
        if command:
            self.cmd_action_combo.setCurrentText(command['action'])
        action_layout.addWidget(self.cmd_action_combo)
        
        layout.addLayout(action_layout)
        
        # Hədəf
        target_layout = QHBoxLayout()
        self.target_label = QLabel("Hədəf:")
        self.target_label.setStyleSheet(f"color: {self.colors['text']};")
        target_layout.addWidget(self.target_label)
        
        self.cmd_target_entry = QLineEdit()
        self.cmd_target_entry.setStyleSheet(f"""
            QLineEdit {{
                background-color: {self.colors['bg_secondary']};
                color: {self.colors['text']};
                border: 1px solid {self.colors['primary']};
                border-radius: 5px;
                padding: 5px;
            }}
        """)
        if command:
            self.cmd_target_entry.setText(command['target'])
        target_layout.addWidget(self.cmd_target_entry)
        
        # Fayl seçmə düyməsi
        self.browse_btn = QPushButton("...")
        self.browse_btn.setFixedWidth(40)
        self.browse_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.colors['primary']};
                color: white;
                border: none;
                border-radius: 5px;
                padding: 5px;
            }}
            QPushButton:hover {{
                background-color: {self.colors['secondary']};
            }}
        """)
        self.browse_btn.clicked.connect(self.browse_file)
        self.browse_btn.setVisible(False)  # Başlanğıcda gizli
        target_layout.addWidget(self.browse_btn)
        
        layout.addLayout(target_layout)
        
        # Klaviatura qısayolu üçün kömək mətni
        self.shortcut_help = QLabel("Nümunə: win+v, ctrl+c, alt+tab, ctrl+shift+esc")
        self.shortcut_help.setStyleSheet(f"color: {self.colors['text_secondary']}; font-size: 10px;")
        self.shortcut_help.setVisible(False)
        layout.addWidget(self.shortcut_help)
        
        # Fayl seçimi üçün kömək mətni
        self.file_help = QLabel("Fayl yerini daxil edin və ya '...' düyməsinə basaraq seçin")
        self.file_help.setStyleSheet(f"color: {self.colors['text_secondary']}; font-size: 10px;")
        self.file_help.setVisible(False)
        layout.addWidget(self.file_help)
        
        # Əmr növü dəyişdiyində hədəf etiketini yenilə
        self.cmd_action_combo.currentTextChanged.connect(self.update_target_label)
        
        # Tətikləyicilər
        triggers_label = QLabel("Tətikləyicilər:")
        triggers_label.setStyleSheet(f"color: {self.colors['text']};")
        layout.addWidget(triggers_label)
        
        # Azərbaycan dili tətikləyiciləri
        az_layout = QHBoxLayout()
        az_label = QLabel("Azərbaycan:")
        az_label.setStyleSheet(f"color: {self.colors['text']};")
        az_layout.addWidget(az_label)
        
        self.cmd_az_triggers = QLineEdit()
        self.cmd_az_triggers.setPlaceholderText("Vergüllə ayırın")
        self.cmd_az_triggers.setStyleSheet(f"""
            QLineEdit {{
                background-color: {self.colors['bg_secondary']};
                color: {self.colors['text']};
                border: 1px solid {self.colors['primary']};
                border-radius: 5px;
                padding: 5px;
            }}
        """)
        if command and 'triggers' in command and 'az-AZ' in command['triggers']:
            self.cmd_az_triggers.setText(", ".join(command['triggers']['az-AZ']))
        az_layout.addWidget(self.cmd_az_triggers)
        
        layout.addLayout(az_layout)
        
        # Türk dili tətikləyiciləri
        tr_layout = QHBoxLayout()
        tr_label = QLabel("Türk dili:")
        tr_label.setStyleSheet(f"color: {self.colors['text']};")
        tr_layout.addWidget(tr_label)
        
        self.cmd_tr_triggers = QLineEdit()
        self.cmd_tr_triggers.setPlaceholderText("Vergüllə ayırın")
        self.cmd_tr_triggers.setStyleSheet(f"""
            QLineEdit {{
                background-color: {self.colors['bg_secondary']};
                color: {self.colors['text']};
                border: 1px solid {self.colors['primary']};
                border-radius: 5px;
                padding: 5px;
            }}
        """)
        if command and 'triggers' in command and 'tr-TR' in command['triggers']:
            self.cmd_tr_triggers.setText(", ".join(command['triggers']['tr-TR']))
        tr_layout.addWidget(self.cmd_tr_triggers)
        
        layout.addLayout(tr_layout)
        
        # Düymələr
        button_layout = QHBoxLayout()
        
        save_btn = QPushButton("Yadda Saxla")
        save_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.colors['primary']};
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
            }}
            QPushButton:hover {{
                background-color: {self.colors['secondary']};
            }}
        """)
        save_btn.clicked.connect(lambda: self.save_command(dialog, command))
        button_layout.addWidget(save_btn)
        
        cancel_btn = QPushButton("Ləğv Et")
        cancel_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.colors['bg_tertiary']};
                color: {self.colors['text']};
                border: 1px solid {self.colors['border']};
                border-radius: 5px;
                padding: 10px;
            }}
            QPushButton:hover {{
                background-color: {self.colors['bg_secondary']};
                border-color: {self.colors['primary']};
            }}
        """)
        cancel_btn.clicked.connect(dialog.reject)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
        
        # Başlanğıcda hədəf etiketini yenilə
        self.update_target_label(self.cmd_action_combo.currentText())
        
        dialog.exec()
    
    def update_target_label(self, action_text):
        """Seçilən əmr növünə görə hədəf etiketini yenilə"""
        if action_text == "Klaviatura Qısayolu":
            self.target_label.setText("Qısayol:")
            self.cmd_target_entry.setPlaceholderText("Nümunə: win+v, ctrl+c, alt+tab")
            self.shortcut_help.setVisible(True)
            self.file_help.setVisible(False)
            self.browse_btn.setVisible(False)
        elif action_text == "Veb Axtarış":
            self.target_label.setText("URL:")
            self.cmd_target_entry.setPlaceholderText("Nümunə: https://www.google.com/search?q={}")
            self.shortcut_help.setVisible(False)
            self.file_help.setText("URL içindəki {} işarəti, axtarış sorğusunun yerləşdiriləcəyi yeri göstərir")
            self.file_help.setVisible(True)
            self.browse_btn.setVisible(False)
        elif action_text == "Proqram Aç" or action_text == "Proqram Bağla":
            self.target_label.setText("Proqram Yolu:")
            self.cmd_target_entry.setPlaceholderText("Nümunə: C:\\Program Files\\app.exe")
            self.shortcut_help.setVisible(False)
            self.file_help.setText("Fayl yerini daxil edin və ya '...' düyməsinə basaraq seçin")
            self.file_help.setVisible(True)
            self.browse_btn.setVisible(True)
        elif action_text == "Veb Sayt Aç":
            self.target_label.setText("URL:")
            self.cmd_target_entry.setPlaceholderText("Nümunə: https://www.example.com")
            self.shortcut_help.setVisible(False)
            self.file_help.setText("Tam URL ünvanını daxil edin (https:// ilə başlamalı)")
            self.file_help.setVisible(True)
            self.browse_btn.setVisible(False)
        elif action_text == "Skript İşlət":
            self.target_label.setText("Skript Yolu:")
            self.cmd_target_entry.setPlaceholderText("Nümunə: C:\\scripts\\myscript.py")
            self.shortcut_help.setVisible(False)
            self.file_help.setText("Fayl yerini daxil edin və ya '...' düyməsinə basaraq seçin")
            self.file_help.setVisible(True)
            self.browse_btn.setVisible(True)
        else:
            self.target_label.setText("Hədəf:")
            self.cmd_target_entry.setPlaceholderText("")
            self.shortcut_help.setVisible(False)
            self.file_help.setVisible(False)
            self.browse_btn.setVisible(False)
    
    def browse_file(self):
        """Fayl seçmə dialogunu göstər"""
        from PyQt6.QtWidgets import QFileDialog
        
        action = self.cmd_action_combo.currentText()
        
        if action == "Proqram Aç" or action == "Proqram Bağla":
            # Proqram seçmə dialogu
            file_path, _ = QFileDialog.getOpenFileName(
                self.settings_window,
                "Proqram Seç",
                "",
                "Tətbiqlər (*.exe);;Bütün Fayllar (*)"
            )
        elif action == "Skript İşlət":
            # Skript seçmə dialogu
            file_path, _ = QFileDialog.getOpenFileName(
                self.settings_window,
                "Skript Seç",
                "",
                "Python Faylları (*.py);;Bütün Fayllar (*)"
            )
        else:
            return
        
        if file_path:
            self.cmd_target_entry.setText(file_path)
        
    def save_command(self, dialog, old_command=None):
        """Əmri yadda saxla"""
        name = self.cmd_name_entry.text().strip()
        action = self.cmd_action_combo.currentText()
        target = self.cmd_target_entry.text().strip()
        az_triggers = [t.strip() for t in self.cmd_az_triggers.text().split(",") if t.strip()]
        tr_triggers = [t.strip() for t in self.cmd_tr_triggers.text().split(",") if t.strip()]
        
        if not name or not target:
            QMessageBox.warning(dialog, "Xəta", "Əmr adı və hədəf sahələri boş ola bilməz!")
            return
        
        if not az_triggers and not tr_triggers:
            QMessageBox.warning(dialog, "Xəta", "Ən azı bir tətikləyici əlavə etməlisiniz!")
            return
        
        # Veb saytı URL yoxlaması
        if action == "Veb Sayt Aç" and not (target.startswith("http://") or target.startswith("https://")):
            QMessageBox.warning(dialog, "Xəta", "Veb saytı URL-si http:// və ya https:// ilə başlamalıdır!")
            return
        
        # Veb axtarış URL yoxlaması
        if action == "Veb Axtarış":
            if "{}" not in target:
                QMessageBox.warning(dialog, "Xəta", "Axtarış URL-si içində {} işarəsi olmalıdır!")
                return
            if not (target.startswith("http://") or target.startswith("https://")):
                QMessageBox.warning(dialog, "Xəta", "Axtarış URL-si http:// və ya https:// ilə başlamalıdır!")
                return
        
        # Yeni əmr yarat
        new_command = {
            "name": name,
            "action": action,
            "target": target,
            "triggers": {
                "az-AZ": az_triggers,
                "tr-TR": tr_triggers
            }
        }
        
        # Əmrləri yüklə
        custom_commands = self.Azer_AI.load_custom_commands()
        
        # Əgər düzənləmə isə köhnə əmri çıxar
        if old_command:
            custom_commands = [cmd for cmd in custom_commands if cmd['name'] != old_command['name']]
        
        # Yeni əmri əlavə et
        custom_commands.append(new_command)
        
        # Dəyişiklikləri yadda saxla
        self.Azer_AI.save_custom_commands(custom_commands)
        
        # Əmr siyahısını yenilə
        self.update_command_list()
        
        # Ana tətbiqdə əmrləri yenilə
        self.Azer_AI.refresh_custom_commands()
        
        # Əmr əlavə edildi mesajı
        if old_command:
            QMessageBox.information(
                self.settings_window,
                "Əmr Yeniləndi",
                f"{name} Əmri uğurla yeniləndi."
            )
        else:
            QMessageBox.information(
                self.settings_window,
                "Əmr Əlavə Edildi",
                f"{name} Əmri uğurla əlavə edildi."
            )
        
        # Dialogu bağla
        dialog.accept()
        
    def edit_command(self, command):
        """Əmri düzənlə"""
        self.show_command_dialog(command)

    def delete_command(self, command):
        """Əmri sil"""
        # Təsdiq pəncərəsi
        result = QMessageBox.question(
            self.settings_window,
            "Əmri Sil",
            f"'{command['name']}' əmrini silmək istədiyinizə əminsiniz?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if result != QMessageBox.StandardButton.Yes:
            return
        
        # Əmri siyahıdan çıxar
        custom_commands = self.Azer_AI.load_custom_commands()
        custom_commands = [cmd for cmd in custom_commands if cmd['name'] != command['name']]
        
        # Dəyişiklikləri yadda saxla
        self.Azer_AI.save_custom_commands(custom_commands)
        self.update_command_list()
        
        # Ana tətbiqdə əmrləri yenilə
        self.Azer_AI.refresh_custom_commands()
        
        QMessageBox.information(
            self.settings_window,
            "Əmr Silindi",
            f"{command['name']} Əmri uğurla silindi."
        )

    def test_voice(self):
        """Səs parametrlərini test et"""
        # Müvəqqəti parametrləri yarat
        temp_settings = {
            'tts_engine': 'edge' if self.tts_engine_combo.currentIndex() == 0 else 'gtts',
            'language': 'az-AZ' if self.language_combo.currentIndex() == 0 else 'tr-TR',
            'voice_gender': 'male' if self.gender_combo.currentIndex() == 0 else 'female'
        }
        
        # Müvəqqəti parametrlərlə danış
        current_settings = self.Azer_AI.voice_settings.copy()
        self.Azer_AI.voice_settings = temp_settings
        
        if temp_settings['language'] == 'az-AZ':
            self.Azer_AI.speak("Salam! Bu test mesajıdır. Səs parametrləri bu şəkildə olacaq.")
        else:
            self.Azer_AI.speak("Merhaba! Bu bir test mesajıdır. Ses ayarları bu şekilde olacak.")
        
        # Parametrləri geri yüklə
        self.Azer_AI.voice_settings = current_settings
        
    def save_all_settings(self):
        """Bütün parametrləri yadda saxla"""
        from db_manager import db_manager
        
        # Səs parametrlərini yarat
        voice_settings = {
            'tts_engine': 'edge' if self.tts_engine_combo.currentIndex() == 0 else 'gtts',
            'language': 'az-AZ' if self.language_combo.currentIndex() == 0 else 'tr-TR',
            'voice_gender': 'male' if self.gender_combo.currentIndex() == 0 else 'female'
        }
        
        # Wake word əsas dəyərlərini al (vergüllə ayrılmış)
        az_words_text = self.az_base_word.text().strip() if self.az_base_word.text().strip() else "azər"
        tr_words_text = self.tr_base_word.text().strip() if self.tr_base_word.text().strip() else "azer"
        
        # Verilənlər bazasına yadda saxlamaq üçün vergüllə ayrılmış dəyərləri istifadə et
        # İstifadəçinin daxil etdiyi xam mətni yadda saxlayırıq, beləliklə birdən çox söz dəstəklənir
        
        # Hər bir əsas sözdən variantlar yarat
        az_base_words = [word.strip() for word in az_words_text.split(',') if word.strip()]
        tr_base_words = [word.strip() for word in tr_words_text.split(',') if word.strip()]
        
        if not az_base_words:
            az_base_words = ["azər"]
        if not tr_base_words:
            tr_base_words = ["azer"]
        
        # Hər dil üçün variantları yarat
        az_variants = []
        for word in az_base_words:
            az_variants.append(word)
            az_variants.append(f"hey {word}")
            az_variants.append(f"hey {word} ai")
            az_variants.append(f"{word} ai")
        
        tr_variants = []
        for word in tr_base_words:
            tr_variants.append(word)
            tr_variants.append(f"hey {word}")
            tr_variants.append(f"hey {word} ai")
            tr_variants.append(f"{word} ai")
        
        # Wake words lüğətini yarat
        wake_words = {
            'az-AZ': az_variants,
            'tr-TR': tr_variants
        }
        
        try:
            # Verilənlər bazasına səs parametrlərini yadda saxla
            db_manager.update_voice_settings(
                self.Azer_AI.current_user['id'],
                voice_settings['tts_engine'],
                voice_settings['language'],
                voice_settings['voice_gender']
            )
            
            # Azer_AI-in səs parametrlərini yenilə
            self.Azer_AI.update_voice_settings(voice_settings)
            
            # İstifadəçi wake words parametrini yenilə
            if 'wake_words' not in self.Azer_AI.current_user:
                self.Azer_AI.current_user['wake_words'] = {}
            
            self.Azer_AI.current_user['wake_words'] = wake_words
            
            # Verilənlər bazasına wake word parametrlərini yadda saxla
            # Burada vergüllə ayrılmış xam mətni yadda saxlayırıq
            db_manager.update_wake_word_settings(
                self.Azer_AI.current_user['id'],
                az_words_text,
                tr_words_text
            )
            
            # Azer_AI-in wake word parametrlərini yenilə
            self.Azer_AI.wake_word_settings = {
                'az_word': az_words_text,
                'tr_word': tr_words_text
            }
            
            # İstifadəçi wake word settings-i yenilə
            if 'wake_word_settings' not in self.Azer_AI.current_user:
                self.Azer_AI.current_user['wake_word_settings'] = {}
                
            self.Azer_AI.current_user['wake_word_settings'] = {
                'az_word': az_words_text,
                'tr_word': tr_words_text
            }
            
            # Ana tətbiqdə əmrləri yenilə
            self.Azer_AI.refresh_custom_commands()
            
            # Uğur mesajı
            QMessageBox.information(
                self.settings_window,
                "Parametrlər Saxlanıldı",
                "Bütün parametrlər uğurla saxlanıldı!"
            )
            
            # Pəncərəni bağla
            self.close_settings()
            
        except Exception as e:
            QMessageBox.critical(
                self.settings_window,
                "Xəta",
                f"Parametrlər saxlanılarkən xəta baş verdi: {str(e)}"
            )
        
    def close_settings(self):
        """Parametrlər pəncərəsini bağla"""
        if self.settings_window:
            self.settings_window.close()

    def show_upgrade_dialog(self):
        """Pro versiyaya yüksəltmə dialogunu göstər"""
        # Azer_AI-in subscription_manager-ını istifadə edərək yüksəltmə dialogunu göstər
        self.Azer_AI.subscription_manager.show_upgrade_dialog()
        
    def create_plugin_settings(self, parent):
        """Plugin idarəetməsi sekmesini yarat"""
        layout = QVBoxLayout(parent)
        
        # Başlıq
        title = QLabel("Plugin İdarəetməsi")
        title.setFont(QFont("Helvetica", 14, QFont.Weight.Bold))
        title.setStyleSheet(f"color: {self.colors['text']};")
        layout.addWidget(title)
        
        # Açıqlama
        desc = QLabel("Yalnız Python (.py) formatında əlavə plugin-ləri yükləyin, idarə edin və ya silin.")
        desc.setStyleSheet(f"color: {self.colors['text_secondary']};")
        desc.setWordWrap(True)
        layout.addWidget(desc)
        
        # Dəstəklənən formatlar məlumatı
        formats_frame = QFrame()
        formats_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {self.colors['bg_secondary']};
                border-radius: 5px;
                padding: 10px;
                margin: 5px 0px;
            }}
        """)
        formats_layout = QVBoxLayout(formats_frame)
        
        formats_title = QLabel("📋 Dəstəklənən Plugin Formatları:")
        formats_title.setStyleSheet(f"color: {self.colors['primary']}; font-weight: bold;")
        formats_layout.addWidget(formats_title)
        
        # Python formatı
        python_format = QLabel("🐍 Python (.py): Birbaşa Python skriptləri")
        python_format.setStyleSheet(f"color: {self.colors['text']};")
        formats_layout.addWidget(python_format)
        
        
        
        layout.addWidget(formats_frame)
        
        # Plugin siyahısı
        self.plugin_list_frame = QScrollArea()
        self.plugin_list_frame.setWidgetResizable(True)
        self.plugin_list_frame.setStyleSheet(f"""
            QScrollArea {{
                border: 1px solid {self.colors['primary']};
                border-radius: 5px;
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
        
        # Plugin siyahısını yarat
        self.plugin_list_content = QWidget()
        self.plugin_list_layout = QVBoxLayout(self.plugin_list_content)
        self.plugin_list_frame.setWidget(self.plugin_list_content)
        
        # Plugin-ləri yüklə
        self.update_plugin_list()
        
        layout.addWidget(self.plugin_list_frame)
        
        # Düymələr üçün frame
        button_frame = QFrame()
        button_frame.setStyleSheet("background-color: transparent;")
        button_layout = QHBoxLayout(button_frame)
        
        # Plugin yüklə düyməsi
        install_btn = QPushButton("📦 Plugin Yüklə")
        install_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.colors['primary']};
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
            }}
            QPushButton:hover {{
                background-color: {self.colors['secondary']};
            }}
        """)
        install_btn.clicked.connect(self.install_plugin)
        button_layout.addWidget(install_btn)
        

        
        # Plugin siyahısını yenilə düyməsi
        refresh_btn = QPushButton("🔄 Yenilə")
        refresh_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.colors['success']};
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
            }}
            QPushButton:hover {{
                background-color: {self.colors['primary']};
            }}
        """)
        refresh_btn.clicked.connect(self.update_plugin_list)
        button_layout.addWidget(refresh_btn)
        
        layout.addWidget(button_frame)
        
    def update_plugin_list(self):
        """Plugin siyahısını yenilə"""
        # Mövcud plugin-ləri təmizlə
        for i in reversed(range(self.plugin_list_layout.count())):
            widget = self.plugin_list_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()
        
        # Plugin-ləri yüklə
        plugins = self.Azer_AI.plugin_manager.get_all_plugins()
        
        if not plugins:
            empty_label = QLabel("Hələ plugin yüklənməyib.")
            empty_label.setStyleSheet(f"color: {self.colors['text_secondary']};")
            empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.plugin_list_layout.addWidget(empty_label)
            return
        
        # Hər plugin üçün bir frame yarat
        for plugin in plugins:
            plugin_frame = QFrame()
            plugin_frame.setStyleSheet(f"""
                QFrame {{
                    background-color: {self.colors['bg']};
                    border-radius: 5px;
                    margin: 2px;
                    padding: 10px;
                }}
            """)
            plugin_layout = QVBoxLayout(plugin_frame)
            
            # Yuxarı sətir - Plugin adı və lisenziya növü
            top_layout = QHBoxLayout()
            
            # Plugin logosu
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
                            top_layout.addWidget(logo_label)
                        else:
                            # Logo yüklənə bilmədi, standart ikon göstər
                            logo_label.setText("🔌")
                            logo_label.setStyleSheet(f"color: {self.colors['primary']}; font-size: 16px;")
                            top_layout.addWidget(logo_label)
                    else:
                        # Logo faylı tapılmadı, standart ikon göstər
                        logo_label.setText("🔌")
                        logo_label.setStyleSheet(f"color: {self.colors['primary']}; font-size: 16px;")
                        top_layout.addWidget(logo_label)
                except Exception as e:
                    # Xəta halında standart ikon göstər
                    logo_label.setText("🔌")
                    logo_label.setStyleSheet(f"color: {self.colors['primary']}; font-size: 16px;")
                    top_layout.addWidget(logo_label)
            else:
                # Logo yoxdursa standart ikon göstər
                logo_label = QLabel("🔌")
                logo_label.setStyleSheet(f"color: {self.colors['primary']}; font-size: 16px;")
                top_layout.addWidget(logo_label)
            
            # Əlavə adı
            plugin_name = QLabel(plugin['name'])
            plugin_name.setStyleSheet(f"color: {self.colors['text']}; font-weight: bold;")
            top_layout.addWidget(plugin_name)
            
            # Plugin növü
            plugin_type = "🐍 PYTHON"
            
            type_label = QLabel(plugin_type)
            type_label.setStyleSheet(f"color: {self.colors['primary']}; font-weight: bold; font-size: 10px;")
            top_layout.addWidget(type_label)
            
            # Lisenziya növü
            license_type = "PRO" if plugin['license_type'] == 'pro' else "FREE"
            license_label = QLabel(license_type)
            license_label.setStyleSheet(f"color: {self.colors['accent'] if plugin['license_type'] == 'pro' else self.colors['success']}; font-weight: bold;")
            top_layout.addWidget(license_label)
            
            # Boşluq əlavə et
            top_layout.addStretch()
            
            # Sil düyməsi
            uninstall_btn = QPushButton("🗑️")
            uninstall_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {self.colors['error']};
                    color: white;
                    border: none;
                    border-radius: 5px;
                    padding: 5px;
                }}
            """)
            uninstall_btn.clicked.connect(lambda checked, p=plugin: self.uninstall_plugin(p))
            top_layout.addWidget(uninstall_btn)
            
            plugin_layout.addLayout(top_layout)
            
            # Orta sətir - Açıqlama
            desc_label = QLabel(plugin['description'])
            desc_label.setStyleSheet(f"color: {self.colors['text_secondary']};")
            plugin_layout.addWidget(desc_label)
            
            # Alt sətir - Məlumatlar
            info_layout = QHBoxLayout()
            
            # Müəllif
            author_label = QLabel(f"Müəllif: {plugin['author']}")
            author_label.setStyleSheet(f"color: {self.colors['text_secondary']}; font-size: 10px;")
            info_layout.addWidget(author_label)
            
            # Versiya
            version_label = QLabel(f"Versiya: {plugin['version']}")
            version_label.setStyleSheet(f"color: {self.colors['text_secondary']}; font-size: 10px;")
            info_layout.addWidget(version_label)
            
            info_layout.addStretch()
            plugin_layout.addLayout(info_layout)
            
            # Tətikləyicilər
            triggers_layout = QVBoxLayout()
            triggers_layout.setSpacing(5)
            
            # Azərbaycan dili tətikləyiciləri
            az_triggers = plugin['triggers'].get('az-AZ', [])
            if az_triggers:
                az_row = QHBoxLayout()
                az_row.setSpacing(5)
                az_icon = QLabel()
                az_icon.setPixmap(QPixmap("resim/AZ.png").scaled(30, 20, Qt.AspectRatioMode.KeepAspectRatio))
                az_row.addWidget(az_icon)
                az_label = QLabel(", ".join(az_triggers))
                az_label.setStyleSheet(f"color: {self.colors['text_secondary']}; font-size: 10px;")
                az_row.addWidget(az_label)
                az_row.addStretch()
                triggers_layout.addLayout(az_row)
            
            # Türk dili tətikləyiciləri
            tr_triggers = plugin['triggers'].get('tr-TR', [])
            if tr_triggers:
                tr_row = QHBoxLayout()
                tr_row.setSpacing(5)
                tr_icon = QLabel()
                tr_icon.setPixmap(QPixmap("resim/TR.png").scaled(30, 20, Qt.AspectRatioMode.KeepAspectRatio))
                tr_row.addWidget(tr_icon)
                tr_label = QLabel(", ".join(tr_triggers))
                tr_label.setStyleSheet(f"color: {self.colors['text_secondary']}; font-size: 10px;")
                tr_row.addWidget(tr_label)
                tr_row.addStretch()
                triggers_layout.addLayout(tr_row)
            
            plugin_layout.addLayout(triggers_layout)
            
            self.plugin_list_layout.addWidget(plugin_frame)
            
            # Ayırıcı xətt əlavə et (son əlavə deyilsə)
            if plugin != plugins[-1]:
                divider = QFrame()
                divider.setFrameShape(QFrame.Shape.HLine)
                divider.setStyleSheet(f"""
                    QFrame {{
                        border: none;
                        background-color: {self.colors['bg_secondary']};
                        max-height: 1px;
                        margin: 5px 0px;
                    }}
                """)
                self.plugin_list_layout.addWidget(divider)
        
        # Boşluq əlavə et
        self.plugin_list_layout.addStretch()
        
    def install_plugin(self):
        """Plugin yükləmə dialogunu göstər"""
        from PyQt6.QtWidgets import QFileDialog
        
        file_path, _ = QFileDialog.getOpenFileName(
            self.settings_window,
            "Plugin Faylı Seç",
            "",
            "Plugin Faylları (*.zip);;Bütün Fayllar (*)"
        )
        
        if file_path:
            try:
                # Yükləmə əməliyyatını başlat
                success = self.Azer_AI.plugin_manager.install_plugin(file_path)
                
                if success:
                    self.update_plugin_list()
                    QMessageBox.information(
                        self.settings_window,
                        "Uğurlu",
                        "Plugin uğurla yükləndi!"
                    )
                else:
                    QMessageBox.warning(
                        self.settings_window,
                        "Xəta",
                        "Plugin yüklənərkən xəta baş verdi!\n\nZəhmət olmasa plugin faylının düzgün formatda olduğundan əmin olun:\n• manifest.json faylı lazımdır\n• main_file sahəsi düzgün olmalıdır\n• Yalnız .py faylları dəstəklənir"
                    )
            except Exception as e:
                error_message = f"Plugin yükləmə xətası:\n{str(e)}"
                QMessageBox.critical(
                    self.settings_window,
                    "Xəta",
                    error_message
                )
                
    def uninstall_plugin(self, plugin):
        """Plugin sil"""
        # Təsdiq pəncərəsi
        result = QMessageBox.question(
            self.settings_window,
            "Plugin Sil",
            f"'{plugin['name']}' pluginini silmək istədiyinizdən əmin misiniz?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if result != QMessageBox.StandardButton.Yes:
            return
        
        try:
            if self.Azer_AI.plugin_manager.uninstall_plugin(plugin['name']):
                self.update_plugin_list()
                QMessageBox.information(
                    self.settings_window,
                    "Uğurlu",
                    "Plugin uğurla silindi!"
                )
            else:
                QMessageBox.warning(
                    self.settings_window,
                    "Xəta",
                    "Plugin silinərkən xəta baş verdi!"
                )
        except Exception as e:
            QMessageBox.critical(
                self.settings_window,
                "Xəta",
                f"Plugin silmə xətası: {str(e)}"
            )
    
