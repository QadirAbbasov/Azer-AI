import re
import subprocess
import os
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL

class VolumeManager:
    def __init__(self, Azer_AI):
        self.Azer_AI = Azer_AI
        
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
        
    def set_volume(self, command=None):
        """Windows sistem səs səviyyəsini tənzimlə"""
        current_lang = self.Azer_AI.voice_settings['language']
        
        if not command or (command.strip().lower() in ['ses', 'səs']):
            if current_lang == 'az-AZ':
                self.Azer_AI.speak("Hansı səs səviyyəsini istəyirsiniz? 0-dan 100-ə qədər bir rəqəm və ya söz deyin.")
            else:
                self.Azer_AI.speak("Hangi ses seviyesini istiyorsunuz? 0'dan 100'e kadar bir rakam veya kelime söyleyin.")
                
            command = self.Azer_AI.listen_for_response()
            
            if not command:
                if current_lang == 'az-AZ':
                    self.Azer_AI.speak("Səsinizi eşitmədim.")
                else:
                    self.Azer_AI.speak("Sesinizi duyamadım.")
                return
        
        volume_level = self._extract_number_from_command(command, current_lang)
        
        if volume_level is not None:
            volume_level = max(0, min(100, volume_level))
            success = self._set_windows_volume(volume_level)
            
            if success:
                if current_lang == 'az-AZ':
                    self.Azer_AI.speak(f"Səs səviyyəsi {volume_level} faizə ayarlandı.")
                else:
                    self.Azer_AI.speak(f"Ses seviyesi yüzde {volume_level} olarak ayarlandı.")
            else:
                if current_lang == 'az-AZ':
                    self.Azer_AI.speak("Səs səviyyəsini dəyişdirərkən xəta baş verdi.")
                else:
                    self.Azer_AI.speak("Ses seviyesini değiştirirken bir hata oluştu.")
        else:
            default_volume = 50
            success = self._set_windows_volume(default_volume)
            
            if success:
                if current_lang == 'az-AZ':
                    self.Azer_AI.speak(f"Səs səviyyəsini başa düşmədim. Səs səviyyəsi {default_volume} faizə ayarlandı.")
                else:
                    self.Azer_AI.speak(f"Ses seviyesini anlayamadım. Ses seviyesi yüzde {default_volume} olarak ayarlandı.")
            else:
                if current_lang == 'az-AZ':
                    self.Azer_AI.speak("Səs səviyyəsini dəyişdirərkən xəta baş verdi.")
                else:
                    self.Azer_AI.speak("Ses seviyesini değiştirirken bir hata oluştu.")
    
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
    
    def _set_windows_volume(self, volume_level):
        """Windows'ta səs səviyyəsini tənzimlə (pycaw kitabxanası istifadə edərək)"""
        try:
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(
                IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = cast(interface, POINTER(IAudioEndpointVolume))
            
            # Mərhələli səs tənzimləməsi üçün mövcud səviyyəni al
            current_volume = volume.GetMasterVolumeLevelScalar() * 100
            step = 2 if volume_level > current_volume else -2
            
            # Mərhələli olaraq səsi tənzimlə (daha yumşaq keçid üçün)
            for level in range(int(current_volume), int(volume_level), step):
                volume.SetMasterVolumeLevelScalar(level / 100.0, None)
            
            # Son dəyəri tənzimlə
            volume.SetMasterVolumeLevelScalar(volume_level / 100.0, None)
            return True
            
        except Exception as e:
            # Pycaw işləməsə alternativ üsul (nircmd)
            try:
                nircmd_path = os.path.join(os.path.dirname(__file__), "nircmd.exe")
                if os.path.exists(nircmd_path):
                    subprocess.run([nircmd_path, "setsysvolume", str(volume_level * 655)], check=True)
                    return True
            except:
                return False