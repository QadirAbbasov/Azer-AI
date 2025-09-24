import requests
from bs4 import BeautifulSoup
import urllib.parse
import random
import webbrowser

class SearchManager:
    def __init__(self, Azer_AI):
        self.Azer_AI = Azer_AI
        
    def get_random_user_agent(self):
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; rv:125.0) Gecko/20100101 Firefox/125.0",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Mobile/15E148 Safari/604.1"
        ]
        return random.choice(user_agents)

    def yandex_search(self, query, num_results=1):
        try:
            encoded_query = urllib.parse.quote_plus(query)
            url = f"https://yandex.com.tr/search/?text={encoded_query}&numdoc={num_results}"
            
            headers = {
                "User-Agent": self.get_random_user_agent(),
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5"
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            results = []
            for link in soup.select('a.Link[href^="http"]'):
                href = link['href']
                if not href.startswith(('https://yandex.com', 'https://ya.ru')):
                    results.append(href)
                    if len(results) >= num_results:
                        break
            
            return results[0] if results else None

        except Exception as e:
            print(f"Xəta baş verdi: {e}")
            return None

    def search(self, command=None):
        """İnternet axtarışı et"""
        current_lang = self.Azer_AI.voice_settings['language']
        
        # Əgər birbaşa axtarış məzmunu əmrlə gəldisə
        if command and not command.strip().lower() in ['ara', 'axtar', 'internet', 'internetde', 'internetdə']:
            # Əmri təmizlə (əvvəlindəki "ara" və ya "axtar" sözlərini çıxar)
            if current_lang == 'az-AZ':
                search_query = command.replace('axtar', '').replace('internetdə', '').strip()
            else:  # tr-TR
                search_query = command.replace('ara', '').replace('internetde', '').strip()
        else:
            # İstifadəçidən axtarış məzmununu soruş
            if current_lang == 'az-AZ':
                self.Azer_AI.speak("Nə axtarmaq istəyirsiniz?")
            else:  # tr-TR
                self.Azer_AI.speak("Ne aramak istiyorsunuz?")
            
            search_query = self.Azer_AI.listen_for_response()
        
        if search_query:
            try:
                result = self.yandex_search(search_query)
                if result:
                    webbrowser.open(result)
                    if current_lang == 'az-AZ':
                        self.Azer_AI.speak("Axtarış nəticəsi açılır.")
                    else:  # tr-TR
                        self.Azer_AI.speak("Arama sonucu açılıyor.")
                else:
                    if current_lang == 'az-AZ':
                        self.Azer_AI.speak("Üzr istəyirəm, axtarış nəticəsi tapılmadı.")
                    else:  # tr-TR
                        self.Azer_AI.speak("Üzgünüm, arama sonucu bulunamadı.")
            except:
                if current_lang == 'az-AZ':
                    self.Azer_AI.speak("Üzr istəyirəm, axtarış edilə bilmədi.")
                else:  # tr-TR
                    self.Azer_AI.speak("Üzgünüm, arama yapılamadı.") 