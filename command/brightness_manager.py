import re
import subprocess
import time
import wmi
import screen_brightness_control as sbc

class BrightnessManager:
    def __init__(self, Azer_AI):
        self.Azer_AI = Azer_AI
        self.min_safe_brightness = 10  # Minimum təhlükəsiz parlaqlıq səviyyəsi
        
        # Türk və Azərbaycan dili rəqəm sözləri və müqabilləri
        self.number_words_tr = {
            'sıfır': 0, 'bir': 1, 'iki': 2, 'üç': 3, 'dört': 4, 'beş': 5,
            'altı': 6, 'yedi': 7, 'sekiz': 8, 'dokuz': 9, 'on': 10,
            'yirmi': 20, 'otuz': 30, 'kırk': 40, 'elli': 50,
            'altmış': 60, 'yetmiş': 70, 'seksen': 80, 'doksan': 90, 'yüz': 100
        }
        
        self.number_words_az = {
            'sıfır': 0, 'bir': 1, 'iki': 2, 'üç': 3, 'dörd': 4, 'beş': 5,
            'altı': 6, 'yeddi': 7, 'səkkiz': 8, 'doqquz': 9, 'on': 10,
            'iyirmi': 20, 'otuz': 30, 'qırx': 40, 'əlli': 50,
            'altmış': 60, 'yetmiş': 70, 'səksən': 80, 'doxsan': 90, 'yüz': 100
        }
        
    def set_brightness(self, command=None):
        """Ekran parlaqlığını tənzimlə (Windows xüsusi)"""
        current_lang = self.Azer_AI.voice_settings['language']
        
        if not command or command.strip().lower() in ['parlaklık', 'parlaqlıq']:
            if current_lang == 'az-AZ':
                self.Azer_AI.speak("Hansı parlaqlıq səviyyəsini istəyirsiniz? 10-dan 100-ə qədər bir rəqəm və ya söz deyin.")
            else:
                self.Azer_AI.speak("Hangi parlaklık seviyesini istiyorsunuz? 10'dan 100'e kadar bir rakam veya kelime söyleyin.")
                
            command = self.Azer_AI.listen_for_response()
            
            if not command:
                if current_lang == 'az-AZ':
                    self.Azer_AI.speak("Səsinizi eşitmədim.")
                else:
                    self.Azer_AI.speak("Sesinizi duyamadım.")
                return
        
        brightness_level = self._extract_number_from_command(command, current_lang)
        
        if brightness_level is not None:
            brightness_level = max(self.min_safe_brightness, min(100, brightness_level))
            success = self._set_brightness_windows(brightness_level)
            
            if success:
                if current_lang == 'az-AZ':
                    self.Azer_AI.speak(f"Ekran parlaqlığı {brightness_level} faizə ayarlandı.")
                else:
                    self.Azer_AI.speak(f"Ekran parlaklığı yüzde {brightness_level} olarak ayarlandı.")
            else:
                if current_lang == 'az-AZ':
                    self.Azer_AI.speak("Parlaqlıq səviyyəsini dəyişdirərkən xəta baş verdi.")
                else:
                    self.Azer_AI.speak("Parlaklık seviyesini değiştirirken bir hata oluştu.")
        else:
            default_brightness = 50
            success = self._set_brightness_windows(default_brightness)
            
            if success:
                if current_lang == 'az-AZ':
                    self.Azer_AI.speak(f"Parlaqlıq səviyyəsini başa düşmədim. Ekran parlaqlığı {default_brightness} faizə ayarlandı.")
                else:
                    self.Azer_AI.speak(f"Parlaklık seviyesini anlayamadım. Ekran parlaklığı yüzde {default_brightness} olarak ayarlandı.")
            else:
                if current_lang == 'az-AZ':
                    self.Azer_AI.speak("Parlaqlıq səviyyəsini dəyişdirərkən xəta baş verdi.")
                else:
                    self.Azer_AI.speak("Parlaklık seviyesini değiştirirken bir hata oluştu.")
    
    def _extract_number_from_command(self, command, language):
        """Əmrdən rəqəmi çıxarır (rəqəm və ya söz olaraq)"""
        if not command:
            return None
            
        command = command.lower()
        
        # Rəqəm olaraq axtarış
        number_match = re.search(r'(\d+)', command)
        if number_match:
            return int(number_match.group(1))
        
        # Söz olaraq rəqəmləri axtar
        number_words = self.number_words_tr if language == 'tr-TR' else self.number_words_az
        
        found_words = []
        for word, value in number_words.items():
            if word in command:
                found_words.append((word, value))
        
        if not found_words:
            return None
            
        # Birləşik rəqəmləri emal et (məsələn "iyirmi beş")
        for tens_word, tens_value in [(w, v) for w, v in found_words if v >= 10 and v <= 90 and v % 10 == 0]:
            for units_word, units_value in [(w, v) for w, v in found_words if v < 10]:
                tens_pos = command.find(tens_word)
                units_pos = command.find(units_word)
                
                if tens_pos != -1 and units_pos != -1 and abs(tens_pos - units_pos) <= len(tens_word) + 5:
                    return tens_value + units_value
        
        # Tək sözlük rəqəmləri axtar
        return max([value for _, value in found_words])
    
    def _set_brightness_windows(self, brightness_level):
        """Windows'ta parlaqlıq tənzimləməsi üçün optimallaşdırılmış üsul"""
        try:
            # Mövcud parlaqlığı al
            current_brightness = sbc.get_brightness()
            if isinstance(current_brightness, list) and current_brightness:
                current_brightness = current_brightness[0]
            elif not isinstance(current_brightness, (int, float)):
                current_brightness = 50
            
            # Mərhələli dəyişim üçün addım müəyyən et
            step = 100 if brightness_level > current_brightness else -100
            
            # Parlaqığı mərhələli olaraq dəyişdir
            for level in range(int(current_brightness), int(brightness_level), step):
                sbc.set_brightness(level)
                time.sleep(0.05)  # Daha sürətli keçid
            
            # Son dəyəri tənzimlə
            sbc.set_brightness(brightness_level)
            return True
            
        except Exception as e:
            try:
                # WMI ehtiyat üsulu
                wmi_obj = wmi.WMI(namespace='wmi')
                monitors = wmi_obj.WmiMonitorBrightnessMethods()
                
                if monitors:
                    monitors[0].WmiSetBrightness(brightness_level, 0)
                    return True
            except:
                try:
                    # PowerShell ehtiyat üsulu
                    powershell_cmd = f"(Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1,{brightness_level})"
                    subprocess.run(["powershell", "-Command", powershell_cmd], 
                                 shell=True, 
                                 capture_output=True, 
                                 text=True,
                                 check=True)
                    return True
                except:
                    return False