import webbrowser
from youtube_search import YoutubeSearch
import pyttsx3

class YouTubeManager:
    def __init__(self, Azer_AI):
        self.Azer_AI = Azer_AI
        self.engine = pyttsx3.init()
        
    def search_youtube(self, command=None):
        """YouTube'da video axtar"""
        current_lang = self.Azer_AI.voice_settings['language']
        
        # Əgər birbaşa axtarış məzmunu əmrlə gəldisə
        if command and not command.strip().lower() in ['youtube', 'youtube ara', 'youtube axtar', 'video', 'video ara', 'video axtar']:
            # Əmri təmizlə (əvvəlindəki "youtube" və ya "video" sözlərini çıxar)
            if current_lang == 'az-AZ':
                search_query = command.replace('youtube', '').replace('video', '').replace('axtar', '').strip()
            else:  # tr-TR
                search_query = command.replace('youtube', '').replace('video', '').replace('ara', '').strip()
        else:
            # İstifadəçidən axtarış məzmununu soruş
            if current_lang == 'az-AZ':
                self.Azer_AI.speak("Hansı videonu axtarmaq istəyirsiniz?")
            else:  # tr-TR
                self.Azer_AI.speak("Hangi videoyu aramak istiyorsunuz?")
            
            search_query = self.Azer_AI.listen_for_response()
        
        if search_query:
            try:
                results = YoutubeSearch(search_query, max_results=1).to_dict()
                if results:
                    video_id = results[0]['id']
                    video_title = results[0]['title']
                    url = f"https://www.youtube.com/watch?v={video_id}"
                    webbrowser.open(url)
                    if current_lang == 'az-AZ':
                        self.Azer_AI.speak(f"{video_title} videosu açılır.")
                    else:  # tr-TR
                        self.Azer_AI.speak(f"{video_title} videosu açılıyor.")
                else:
                    if current_lang == 'az-AZ':
                        self.Azer_AI.speak("Video tapılmadı.")
                    else:  # tr-TR
                        self.Azer_AI.speak("Video bulunamadı.")
            except Exception as e:
                if current_lang == 'az-AZ':
                    self.Azer_AI.speak("Üzr istəyirəm, video axtarıla bilmədi.")
                else:  # tr-TR
                    self.Azer_AI.speak("Üzgünüm, video aranamadı.") 