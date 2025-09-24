import keyboard
import pyttsx3

class TypingManager:
    def __init__(self, Azer_AI):
        self.Azer_AI = Azer_AI
        self.engine = pyttsx3.init()
        
    def type_text(self, command=None):
        """Ekrana mətn yazdır"""
        current_lang = self.Azer_AI.voice_settings['language']
        
        # Əgər birbaşa yazılacaq mətn əmrlə gəldisə
        if command and not command.strip().lower() in ['yaz', 'yazdir', 'yazdır', 'yaz', 'yazdır', 'type']:
            # Əmri təmizlə (əvvəlindəki "yaz" və ya "yazdır" sözlərini çıxar)
            if current_lang == 'az-AZ':
                text_to_type = command.replace('yaz', '').replace('yazdır', '').strip()
            else:  # tr-TR
                text_to_type = command.replace('yaz', '').replace('yazdır', '').strip()
        else:
            # İstifadəçidən yazılacaq mətni soruş
            if current_lang == 'az-AZ':
                self.Azer_AI.speak("Nə yazmaq istəyirsiniz?")
            else:  # tr-TR
                self.Azer_AI.speak("Ne yazmak istiyorsunuz?")
            
            text_to_type = self.Azer_AI.listen_for_response()
        
        if text_to_type:
            try:
                # Mətni yaz
                keyboard.write(text_to_type, delay=0.05)
                
                if current_lang == 'az-AZ':
                    self.Azer_AI.speak("Mətn yazıldı.")
                else:  # tr-TR
                    self.Azer_AI.speak("Metin yazıldı.")
            except Exception as e:
                if current_lang == 'az-AZ':
                    self.Azer_AI.speak("Üzr istəyirəm, mətn yazıla bilmədi.")
                else:  # tr-TR
                    self.Azer_AI.speak("Üzgünüm, metin yazılamadı.") 