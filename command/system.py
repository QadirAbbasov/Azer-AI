import psutil
from pydub import AudioSegment
from pydub.playback import play

class SystemManager:
    def __init__(self, Azer_AI):
        self.Azer_AI = Azer_AI
        
    def system_info(self):
        """Sistem məlumatları"""
        current_lang = self.Azer_AI.voice_settings['language']
        
        cpu = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory().percent

        # CPU və RAM vəziyyətini qiymətləndir
        cpu_status = self._evaluate_status(cpu)
        memory_status = self._evaluate_status(memory)

        song = AudioSegment.from_wav("wav/system.wav")
        play(song)
        
        if current_lang == 'az-AZ':
            self.Azer_AI.speak(f"Sistem məlumatları: CPU istifadəsi {cpu}% ({cpu_status}), RAM istifadəsi {memory}% ({memory_status})")
        else:  # tr-TR
            self.Azer_AI.speak(f"Sistem bilgileri: CPU kullanımı {cpu}% ({cpu_status}), RAM kullanımı {memory}% ({memory_status})")
    
    def _evaluate_status(self, percentage):
        """Faiz dəyərinə görə vəziyyət qiymətləndirməsi edir"""
        if percentage < 50:
            return "iyi" if self.Azer_AI.voice_settings['language'] == 'tr-TR' else "yaxşı"
        elif percentage < 80:
            return "normal"
        else:
            return "kötü" if self.Azer_AI.voice_settings['language'] == 'tr-TR' else "pis"