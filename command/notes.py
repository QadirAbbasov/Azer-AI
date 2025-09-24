import datetime

class NotesManager:
    def __init__(self, Azer_AI):
        self.Azer_AI = Azer_AI
        
    def take_note(self, command=None):
        """Qeyd götürmə"""
        current_lang = self.Azer_AI.voice_settings['language']
        
        # Əgər birbaşa qeyd məzmunu əmrlə gəldisə
        if command and not command.strip().lower() in ['not', 'not al', 'qeyd', 'qeyd et']:
            # Əmri təmizlə (əvvəlindəki "not" və ya "qeyd" sözlərini çıxar)
            if current_lang == 'az-AZ':
                note = command.replace('qeyd', '').replace('et', '').strip()
            else:  # tr-TR
                note = command.replace('not', '').replace('al', '').strip()
        else:
            # İstifadəçidən qeyd məzmununu soruş
            if current_lang == 'az-AZ':
                self.Azer_AI.speak("Nə qeyd etmək istəyirsiniz?")
            else:  # tr-TR
                self.Azer_AI.speak("Ne not almak istiyorsunuz?")
            
            note = self.Azer_AI.listen_for_response()
        
        if note:
            try:
                with open("notes/notes.txt", "a", encoding="utf-8") as f:
                    f.write(f"{datetime.datetime.now()}: {note}\n")
                
                if current_lang == 'az-AZ':
                    self.Azer_AI.speak("Qeydiniz yadda saxlanıldı.")
                else:  # tr-TR
                    self.Azer_AI.speak("Notunuz kaydedildi.")
            except:
                if current_lang == 'az-AZ':
                    self.Azer_AI.speak("Üzr istəyirəm, qeydi yadda saxlaya bilmədim.")
                else:  # tr-TR
                    self.Azer_AI.speak("Üzgünüm, notu kaydedemedim.")