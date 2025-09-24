import pyautogui

class MusicManager:
    def __init__(self, Azer_AI):
        self.Azer_AI = Azer_AI

    def control_music(self, command=None):
        """Musiqi idarə əmrlərini emal edir"""
        if not command or (command.strip().lower() in ['musiqi', 'müzik']):
            current_lang = self.Azer_AI.voice_settings['language']
            if current_lang == 'az-AZ':
                self.Azer_AI.speak("Hansı musiqi əmrini icra etmək istəyirsiniz?")
            else:
                self.Azer_AI.speak("Hangi müzik komutunu uygulamak istiyorsunuz?")
            command = self.Azer_AI.listen_for_response()
            
            if not command:
                if current_lang == 'az-AZ':
                    self.Azer_AI.speak("Səs əmri alınmadı")
                else:
                    self.Azer_AI.speak("Ses komutu alınamadı")
                return

        current_lang = self.Azer_AI.voice_settings['language']
        command = command.lower()
        
        if current_lang == 'az-AZ':
            # Oynat/Dayandır əmrləri
            if any(word in command for word in ["oxu", "başla", "davam et", "play"]):
                pyautogui.press("playpause")
                self.Azer_AI.speak("Musiqi başladıldı")
            # Dayandır əmrləri
            elif any(word in command for word in ["pauza", "dayan", "dayandır", "saxla"]):
                pyautogui.press("playpause")
                self.Azer_AI.speak("Musiqi dayandırıldı")
            # Növbəti əmrləri
            elif any(word in command for word in ["növbəti", "sonrakı", "irəli"]):
                pyautogui.press("nexttrack")
                self.Azer_AI.speak("Növbəti mahnıya keçildi")
            # Əvvəlki əmrləri
            elif any(word in command for word in ["əvvəlki", "geri", "öncəki"]):
                pyautogui.press("prevtrack")
                self.Azer_AI.speak("Əvvəlki mahnıya keçildi")
            else:
                self.Azer_AI.speak("Musiqi əmri başa düşülmədi")
        else:  # tr-TR
            # Oynat/Dayandır əmrləri
            if any(word in command for word in ["çal", "başlat", "devam et", "oynat"]):
                pyautogui.press("playpause")
                self.Azer_AI.speak("Müzik başlatıldı")
            # Dayandır əmrləri
            elif any(word in command for word in ["duraklat", "dur", "durdur", "stop"]):
                pyautogui.press("playpause")
                self.Azer_AI.speak("Müzik duraklatıldı")
            # Növbəti əmrləri
            elif any(word in command for word in ["sonraki", "ileri", "sıradaki"]):
                pyautogui.press("nexttrack")
                self.Azer_AI.speak("Sonraki şarkıya geçildi")
            # Əvvəlki əmrləri
            elif any(word in command for word in ["önceki", "geri", "önceki şarkı"]):
                pyautogui.press("prevtrack")
                self.Azer_AI.speak("Önceki şarkıya geçildi")
            else:
                self.Azer_AI.speak("Müzik komutu anlaşılamadı")