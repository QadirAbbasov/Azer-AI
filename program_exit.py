from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap, QIcon, QColor

class ProgramExit:
    def __init__(self, parent, colors):
        self.parent = parent
        self.colors = colors
        
    def show_exit_dialog(self):
        """Proqramdan çıxış üçün modern təsdiq dialoqu göstər"""
        from PyQt6.QtWidgets import QGraphicsDropShadowEffect
        dialog = QDialog(self.parent)
        dialog.setWindowTitle("Çıxış")
        dialog.setFixedSize(420, 260)
        dialog.setStyleSheet(f"""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 {self.colors['bg']}, stop:1 {self.colors['bg_secondary']});
            border: 1.5px solid {self.colors['primary']};
            border-radius: 18px;
        """)
        # Həqiqi kölgə effekti əlavə et
        shadow = QGraphicsDropShadowEffect(dialog)
        shadow.setBlurRadius(32)
        shadow.setOffset(0, 8)
        shadow.setColor(QColor(0, 0, 0, 80))
        dialog.setGraphicsEffect(shadow)
        
        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(28, 24, 28, 24)
        layout.setSpacing(18)
        
        # Başlıq
        title_label = QLabel("Proqramdan Çıxış")
        title_label.setStyleSheet(f"""
            color: {self.colors['primary']};
            font-size: 22px;
            font-weight: bold;
            font-family: 'Segoe UI', Arial, sans-serif;
            padding-bottom: 8px;
        """)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)
        
        # İkon və mesaj üçün konteyner
        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(22)
        
        # Modern ikon (emoji və ya PNG/SVG)
        icon_label = QLabel()
        icon_label.setText("🚪")
        icon_label.setStyleSheet(f"font-size: 54px; padding: 0 8px;")
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        content_layout.addWidget(icon_label, 0)
        
        # Mesaj
        message_label = QLabel("Azer AI Səsli Asistandan çıxmaq istədiyinizə əminsiniz?")
        message_label.setWordWrap(True)
        message_label.setStyleSheet(f"""
            color: {self.colors['text_secondary']};
            font-size: 15px;
            font-family: 'Segoe UI', Arial, sans-serif;
            line-height: 1.5;
        """)
        message_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        content_layout.addWidget(message_label, 1)
        
        layout.addLayout(content_layout)
        
        # Düymələr üçün konteyner
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(0, 10, 0, 0)
        button_layout.setSpacing(22)
        
        # İmtina düyməsi (X simvolu ilə)
        cancel_button = QPushButton("❌ İmtina")
        cancel_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.colors['bg_tertiary']};
                color: {self.colors['text']};
                border: 1.5px solid {self.colors['border']};
                border-radius: 8px;
                padding: 10px 28px;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 15px;
                font-weight: 500;
            }}
            QPushButton:hover {{
                background-color: {self.colors['bg_secondary']};
                border-color: {self.colors['primary']};
                color: {self.colors['text']};
            }}
            QPushButton:pressed {{
                background-color: {self.colors['primary']};
                color: white;
            }}
        """)
        cancel_button.clicked.connect(dialog.reject)
        button_layout.addWidget(cancel_button)
        
        # Çıxış düyməsi (check simvolu ilə)
        exit_button = QPushButton("✅ Çıxış")
        exit_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.colors['error']};
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 28px;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 15px;
                font-weight: 500;
            }}
            QPushButton:hover {{
                background-color: #D32F2F;
            }}
            QPushButton:pressed {{
                background-color: #B71C1C;
            }}
        """)
        exit_button.clicked.connect(self.exit_program)
        button_layout.addWidget(exit_button)
        
        layout.addLayout(button_layout)
        
        # Dialoqu mərkəzləşdir və göstər
        dialog.setWindowFlags(dialog.windowFlags() & ~Qt.WindowType.WindowContextHelpButtonHint)
        dialog.setModal(True)
        dialog.exec()
        
    def exit_program(self):
        """Proqramı bağla"""
        import sys
        sys.exit() 