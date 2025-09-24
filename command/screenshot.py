import os
import datetime
import pyautogui
import webbrowser
from pydub import AudioSegment
from pydub.playback import play

class ScreenshotManager:
    def __init__(self, Azer_AI):
        self.Azer_AI = Azer_AI
        
    def take_screenshot(self):
        """Ekran şəkli"""
        current_lang = self.Azer_AI.voice_settings['language']
        
        try:
            # Screenshots qovluğunu yarat
            screenshots_dir = "screenshots"
            if not os.path.exists(screenshots_dir):
                os.makedirs(screenshots_dir)
            
            # Unikal fayl adı yarat
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"
            filepath = os.path.join(screenshots_dir, filename)
            
            # Ekran görüntüsü al
            if current_lang == 'az-AZ':
                self.Azer_AI.speak("Skrinşot çəkilir...")
            else:  # tr-TR
                self.Azer_AI.speak("Ekran görüntüsü alınıyor...")

            screenshot = pyautogui.screenshot()
            screenshot.save(filepath)

            song = AudioSegment.from_wav("wav/camera.wav")
            play(song)
            
            # Ekran görüntüsünü göstər
            try:
                webbrowser.open(filepath)  # Varsayılan şəkil görüntüləyici ilə aç
                if current_lang == 'az-AZ':
                    self.Azer_AI.speak("Skrinşot uğurla çəkildi, saxlanıldı və göstərilir")
                else:  # tr-TR
                    self.Azer_AI.speak("Ekran görüntüsü başarıyla alındı, kaydedildi ve gösteriliyor")
            except Exception as e:
                self.speak(f"Ekran görüntüsü göstərmə xətası: {e}")
                if current_lang == 'az-AZ':
                    self.Azer_AI.speak("Skrinşot çəkildi və saxlanıldı, amma göstərilə bilmədi")
                else:  # tr-TR
                    self.Azer_AI.speak("Ekran görüntüsü alındı ve kaydedildi, ancak gösterilemedi")
            
        except Exception as e:
            self.speak(f"Ekran görüntüsü xətası: {e}")
            if current_lang == 'az-AZ':
                self.Azer_AI.speak("Skrinşot çəkilərkən xəta baş verdi")
            else:  # tr-TR
                self.Azer_AI.speak("Ekran görüntüsü alınırken hata oluştu")