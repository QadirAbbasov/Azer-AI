import requests
import urllib.parse
import re

class WeatherManager:
    def __init__(self, Azer_AI):
        self.Azer_AI = Azer_AI
        self.base_url = "https://wttr.in/{}?format=j1&lang={}"
    
    def get_weather(self, command=None):
        """Hava vəziyyətini yoxla və səsli bildir"""
        current_lang = self.Azer_AI.voice_settings['language']
        
        # Əmrdən şəhər adını çıxar
        city = None
        if command:
            # Dilə görə regex pattern'i müəyyən et
            if current_lang == 'az-AZ':
                pattern = r'(.*?)\s*(?:şəhəri|şəhərində|şəhər|hava|durumu|məlumatı|necədir|nədir).*'
            else:  # tr-TR
                pattern = r'(.*?)\s*(?:şehri|şehrinde|şehir|hava|durumu|nasıl).*'
            
            match = re.match(pattern, command.lower())
            if match:
                potential_city = match.group(1).strip()
                if potential_city and not any(word in potential_city.lower() for word in ['hava', 'weather', 'durum']):
                    city = potential_city

        # Əgər şəhər adı tapılmadısa soruş
        if not city:
            if current_lang == 'az-AZ':
                self.Azer_AI.speak("Hansı şəhərin hava məlumatını öyrənmək istəyirsiniz?")
            else:  # tr-TR
                self.Azer_AI.speak("Hangi şehrin hava durumunu öğrenmek istiyorsunuz?")
            
            city = self.Azer_AI.listen_for_response()
            
            if not city:
                if current_lang == 'az-AZ':
                    self.Azer_AI.speak("Üzr istəyirəm, şəhər adını başa düşmədim.")
                else:  # tr-TR
                    self.Azer_AI.speak("Üzgünüm, şehir adını anlayamadım.")
                return
            
        try:
            # URL-safe şəhər adı yarat və URL'ni hazırla
            encoded_city = urllib.parse.quote(city)
            url = self.base_url.format(encoded_city, "tr" if current_lang == "tr-TR" else "az")
            
            # API'dən məlumat al
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # Bu günün hava vəziyyəti
            current = data['current_condition'][0]
            temp = current['temp_C']
            feels_like = current['FeelsLikeC']
            description = current['lang_tr'][0]['value'] if current_lang == "tr-TR" else current['lang_az'][0]['value']
            humidity = current['humidity']
            wind_speed = current['windspeedKmph']
            wind_dir = current['winddir16Point']
            
            # Dilə görə hava vəziyyəti məlumatını hazırla
            if current_lang == 'az-AZ':
                weather_info = (
                    f"{city} şəhəri üçün hazırkı hava: {description}, "
                    f"hərarət {temp} dərəcə, hiss edilən hərarət {feels_like} dərəcə, "
                    f"rütubət {humidity} faiz, "
                    f"külək sürəti saatda {wind_speed} kilometr, "
                    f"küləyin istiqaməti {wind_dir}."
                )
                self.Azer_AI.speak(weather_info)
            else:  # tr-TR
                weather_info = (
                    f"{city} şehri için mevcut hava durumu: {description}, "
                    f"sıcaklık {temp} derece, hissedilen sıcaklık {feels_like} derece, "
                    f"nem oranı yüzde {humidity}, "
                    f"rüzgar hızı saatte {wind_speed} kilometre, "
                    f"rüzgar yönü {wind_dir}."
                )
                self.Azer_AI.speak(weather_info)
            
        except Exception as e:
            
            if current_lang == 'az-AZ':
                self.Azer_AI.speak("Hava məlumatları alınarkən xəta baş verdi.")
            else:  # tr-TR
                self.Azer_AI.speak("Hava durumu bilgileri alınırken bir hata oluştu.") 