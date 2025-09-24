import datetime
import random

class TimeManager:
    def __init__(self, Azer_AI):
        self.Azer_AI = Azer_AI
        
    def tell_time(self):
        """Saat məlumatını söylə"""
        # Mövcud dil tənzimini yoxla
        current_lang = self.Azer_AI.voice_settings['language']
        
        now = datetime.datetime.now()
        hour_24 = now.hour
        minute = now.minute
        
        # 12 saatlıq formata çevir
        hour_12 = hour_24 % 12
        if hour_12 == 0:
            hour_12 = 12
        
        # Növbəti saatı hesabla
        next_hour_12 = (hour_12 % 12) + 1
        
        # Günün hansı vaxtı olduğunu müəyyən et
        if current_lang == 'az-AZ':
            if 5 <= hour_24 < 12:
                time_of_day = "Səhər"
            elif 12 <= hour_24 < 17:
                time_of_day = "Günorta"
            elif 17 <= hour_24 < 22:
                time_of_day = "Axşam"
            else:
                time_of_day = "Gecə"
            
            # Ev vaxtı formatı
            if minute == 0:
                home_time = f"Saat tam {hour_12}"
            elif minute == 30:
                home_time = f"Saat {next_hour_12}-ün yarısı"
            elif minute < 30:
                home_time = f"Saat {next_hour_12}-ə işləyir {minute} dəqiqə"
            else:
                remaining = 60 - minute
                home_time = f"Saat {next_hour_12}-ə qalıb {remaining} dəqiqə"
            
            responses = [
                f"{time_of_day} vaxtıdır. {home_time}.",
                f"İndi {time_of_day} vaxtıdır. {home_time}.",
                f"Hazırki vaxt: {time_of_day}. {home_time}."
            ]
        else:  # tr-TR
            if 5 <= hour_24 < 12:
                time_of_day = "Sabah"
            elif 12 <= hour_24 < 17:
                time_of_day = "Öğle"
            elif 17 <= hour_24 < 22:
                time_of_day = "Akşam"
            else:
                time_of_day = "Gece"
            
            # Ev vaxtı formatı
            if minute == 0:
                home_time = f"Saat tam {hour_12}"
            elif minute == 30:
                home_time = f"Saat {next_hour_12}'ün yarısı"
            elif minute < 30:
                home_time = f"Saat {next_hour_12}'e işliyor {minute} dakika"
            else:
                remaining = 60 - minute
                home_time = f"Saat {next_hour_12}'e kaldı {remaining} dakika"
            
            responses = [
                f"{time_of_day} vakti. {home_time}.",
                f"Şu an {time_of_day} vakti. {home_time}.",
                f"Şu anki zaman: {time_of_day}. {home_time}."
            ]
        
        self.Azer_AI.speak(random.choice(responses))