import webbrowser
import wikipedia
import pyttsx3

class WikipediaManager:
    def __init__(self, Azer_AI):
        self.Azer_AI = Azer_AI
        self.engine = pyttsx3.init()
        
    def search_wikipedia(self, command=None):
        """Wikipedia'da axtarış et"""
        current_lang = self.Azer_AI.voice_settings['language']
        
        # Əgər birbaşa axtarış məzmunu əmrlə gəldisə
        if command and not command.strip().lower() in ['wikipedia', 'wikipedia ara', 'wikipedia axtar', 'wiki', 'wiki ara', 'wiki axtar']:
            # Əmri təmizlə (əvvəlindəki "wikipedia" və ya "wiki" sözlərini çıxar)
            if current_lang == 'az-AZ':
                search_query = command.replace('wikipedia', '').replace('wiki', '').replace('axtar', '').strip()
            else:  # tr-TR
                search_query = command.replace('wikipedia', '').replace('wiki', '').replace('ara', '').strip()
        else:
            # İstifadəçidən axtarış məzmununu soruş
            if current_lang == 'az-AZ':
                self.Azer_AI.speak("Wikipedia-da nə axtarmaq istəyirsiniz?")
            else:  # tr-TR
                self.Azer_AI.speak("Wikipedia'da ne aramak istiyorsunuz?")
            
            search_query = self.Azer_AI.listen_for_response()
        
        if search_query:
            try:
                # Wikipedia dilini tənzimlə
                wikipedia.set_lang('az' if current_lang == 'az-AZ' else 'tr')
                
                # Axtarış et
                search_results = wikipedia.search(search_query, results=1)
                
                if search_results:
                    # İlk nəticəni al
                    page_title = search_results[0]
                    
                    # Məqalənin xülasəsini al
                    try:
                        summary = wikipedia.summary(page_title, sentences=3)
                        
                        # Xülasəni oxu
                        if current_lang == 'az-AZ':
                            self.Azer_AI.speak(f"{page_title} haqqında qısa məlumat:")
                        else:  # tr-TR
                            self.Azer_AI.speak(f"{page_title} hakkında kısa bilgi:")
                        
                        self.Azer_AI.speak(summary)
                        
                        # Tam məqaləni açmaq istəyib istəmədiyini soruş
                        if current_lang == 'az-AZ':
                            self.Azer_AI.speak("Tam məqaləni açmaq istəyirsinizmi?")
                        else:  # tr-TR
                            self.Azer_AI.speak("Tam makaleyi açmak istiyor musunuz?")
                        
                        response = self.Azer_AI.listen_for_response()
                        
                        # İstifadəçinin cavabını yoxla
                        if any(word in response.lower() for word in ['bəli', 'əla', 'aç', 'yes', 'evet', 'aç', 'ok']):
                            url = f"https://{current_lang.split('-')[0]}.wikipedia.org/wiki/{page_title.replace(' ', '_')}"
                            webbrowser.open(url)
                            if current_lang == 'az-AZ':
                                self.Azer_AI.speak(f"{page_title} məqaləsi açılır.")
                            else:  # tr-TR
                                self.Azer_AI.speak(f"{page_title} makalesi açılıyor.")
                        else:
                            if current_lang == 'az-AZ':
                                self.Azer_AI.speak("Tamam, məqalə açılmır.")
                            else:  # tr-TR
                                self.Azer_AI.speak("Tamam, makale açılmıyor.")
                                
                    except wikipedia.exceptions.DisambiguationError as e:
                        # Əgər qeyri-müəyyən bir axtarış nəticəsi varsa
                        if current_lang == 'az-AZ':
                            self.Azer_AI.speak("Bu axtarış üçün bir neçə nəticə var. Daha spesifik olun.")
                        else:  # tr-TR
                            self.Azer_AI.speak("Bu arama için birden fazla sonuç var. Daha spesifik olun.")
                            
                else:
                    if current_lang == 'az-AZ':
                        self.Azer_AI.speak("Məqalə tapılmadı.")
                    else:  # tr-TR
                        self.Azer_AI.speak("Makale bulunamadı.")
            except Exception as e:
                if current_lang == 'az-AZ':
                    self.Azer_AI.speak("Üzr istəyirəm, axtarış edilə bilmədi.")
                else:  # tr-TR
                    self.Azer_AI.speak("Üzgünüm, arama yapılamadı.") 