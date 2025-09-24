import datetime

class GreetManager:
    def __init__(self, Azer_AI):
        self.Azer_AI = Azer_AI
        
    def greet(self):
        """Salamlaşma"""
        hour = datetime.datetime.now().hour
        current_lang = self.Azer_AI.voice_settings['language']
        
        if current_lang == 'az-AZ':
            if 5 <= hour < 12:
                self.Azer_AI.speak("Sabahınız xeyir! Sizə necə kömək edə bilərəm?")
            elif 12 <= hour < 18:
                self.Azer_AI.speak("Günortanız xeyir! Sizə necə kömək edə bilərəm?")
            else:
                self.Azer_AI.speak("Axşamınız xeyir! Sizə necə kömək edə bilərəm?")
        else:  # tr-TR
            if 5 <= hour < 12:
                self.Azer_AI.speak("Günaydın! Size nasıl yardımcı olabilirim?")
            elif 12 <= hour < 18:
                self.Azer_AI.speak("Günaydın! Size nasıl yardımcı olabilirim?")
            else:
                self.Azer_AI.speak("İyi akşamlar! Size nasıl yardımcı olabilirim?")