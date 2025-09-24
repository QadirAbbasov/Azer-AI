import time
import os
import pyautogui
import webbrowser
from pydub import AudioSegment
from pydub.playback import play
from difflib import get_close_matches
from typing import Dict, List, Tuple, Optional

# command qovluğundan modulları idxal et
from command.screenshot import ScreenshotManager
from command.notes import NotesManager
from command.system import SystemManager
from command.date import DateManager
from command.time_manager import TimeManager
from command.greet_manager import GreetManager
from command.volume_manager import VolumeManager
from command.brightness_manager import BrightnessManager
from command.weather_manager import WeatherManager
from command.music_manager import MusicManager
from command.search_manager import SearchManager
from command.youtube_manager import YouTubeManager
from command.wikipedia_manager import WikipediaManager
from command.typing_manager import TypingManager

class Azer_AICommands:
    def __init__(self, Azer_AI):
        self.Azer_AI = Azer_AI
        self.screenshot_manager = ScreenshotManager(Azer_AI)
        self.notes_manager = NotesManager(Azer_AI)
        self.system_manager = SystemManager(Azer_AI)
        self.date_manager = DateManager(Azer_AI)
        self.time_manager = TimeManager(Azer_AI)
        self.greet_manager = GreetManager(Azer_AI)
        self.volume_manager = VolumeManager(Azer_AI)
        self.brightness_manager = BrightnessManager(Azer_AI)
        self.weather_manager = WeatherManager(Azer_AI)
        self.music_manager = MusicManager(Azer_AI)
        self.search_manager = SearchManager(Azer_AI)
        self.youtube_manager = YouTubeManager(Azer_AI)
        self.wikipedia_manager = WikipediaManager(Azer_AI)
        self.typing_manager = TypingManager(Azer_AI)
        self.custom_commands = self.Azer_AI.load_custom_commands()
        self.last_command = ""  # Son əmri saxlamaq üçün
        self.command_context = {}  # Əmr kontekstini saxlamaq üçün
        
        # Əmr ləqəbləri - dilə görə dəyişəcək
        self.update_command_aliases()
        
    def update_command_aliases(self):
        """Dilə görə əmr ləqəblərini yenilə"""
        current_lang = self.Azer_AI.voice_settings['language']
        
        if current_lang == 'az-AZ':
            # Azərbaycan dili əmr ləqəbləri və təbii dil variantları
            self.free_command_aliases = {
                "selamlaşma": [
                    "salam", "salamlar", "salam əleyküm", "salamun əleyküm",
                    "sabahın xeyir", "axşamın xeyir", "günortan xeyir",
                    "necəsən", "necə", "nə var nə yox"
                ],
                "saat": [
                    "saat", "vaxt", "saat neçədir", "vaxt neçədir",
                    "saatı söylə", "vaxtı söylə", "indi saat neçədir"
                ],
                "tarix": [
                    "tarix", "gün", "ay", "bu gün", "bugün nə günüdür",
                    "hansı tarixdir", "tarix neçədir", "ayın neçəsidir"
                ],
                "qeyd": [
                    "qeyd", "qeyd et", "yadda saxla", "qeydə al",
                    "qeydiyyat", "qeyd götür", "yadda saxla bunu"
                ],
                "sistem": [
                    "sistem", "sistem məlumatı", "kompüter", "kompüter məlumatı",
                    "sistem vəziyyəti", "sistem durumu", "resurslar"
                ],
                "səs səviyyəsi": [
                    "səs", "səsi", "səs səviyyəsi", "səsi artır", "səsi azalt",
                    "səsi qaldır", "səsi endır", "səsi tənzimlə"
                ],
                "parlaqlıq": [
                    "parlaqlıq", "ekran parlaqlığı", "işıq", "ekran işığı",
                    "parlaqlığı artır", "parlaqlığı azalt", "ekranı işıqlandır"
                ],
                "hava": [
                    "hava", "hava durumu", "hava məlumatı", "hava necədir",
                    "havalar necə olacaq", "hava proqnozu", "hava şəraiti"
                ],
                "musiqi": [
                    "musiqi", "mahnı", "musiqi idarəsi", "musiqini başlat",
                    "musiqini dayandır", "mahnı qoş", "mahnını dayandır"
                ],
                "axtarış": [
                    "axtar", "axtarış", "internet", "internetdə", "axtarış et",
                    "axtarış apar", "internetdə axtar", "axtarış edək"
                ],
                "youtube": [
                    "youtube", "youtube axtar", "video", "video axtar",
                    "youtube video", "youtube video axtar", "youtube axtarış"
                ],
                "wikipedia": [
                    "wikipedia", "wikipedia axtar", "wiki", "wiki axtar",
                    "wikipedia məqaləsi", "wikipedia məqalə axtar", "wiki məqalə"
                ],
                "yazma": [
                    "yaz", "yazdir", "yazdır", "mətn yaz", "mətn yazdır",
                    "yazma", "yazmaq", "yazdırma", "yazdırmaq"
                ]
            }
            
            self.pro_command_aliases = {
                "ekran şəkli": [
                    "skrinşot", "ekran şəkli", "ekran şəkli çək",
                    "ekranın şəklini çək", "ekranı çek", "şəkil çək"
                ]
            }
        else:  # tr-TR
            # Türk dili əmr ləqəbləri və təbii dil variantları
            self.free_command_aliases = {
                "selamlama": [
                    "selam", "selamlar", "selam aleyküm", "selamun aleyküm",
                    "günaydın", "iyi akşamlar", "iyi günler", "merhaba",
                    "nasılsın", "naber", "ne haber"
                ],
                "saat": [
                    "saat", "zaman", "saat kaç", "şu an saat kaç",
                    "saati söyle", "zamanı söyle", "şimdiki saat"
                ],
                "tarih": [
                    "tarih", "gün", "ay", "bugün", "bugün günlerden ne",
                    "hangi tarih", "tarih kaç", "ayın kaçı"
                ],
                "not": [
                    "not", "not al", "kaydet", "not et",
                    "not tut", "hatırlat", "bunu kaydet"
                ],
                "sistem": [
                    "sistem", "sistem bilgisi", "bilgisayar", "pc durumu",
                    "sistem durumu", "kaynaklar", "performans"
                ],
                "ses seviyesi": [
                    "ses", "sesi", "ses seviyesi", "sesi arttır", "sesi azalt",
                    "sesi yükselt", "sesi kıs", "sesi ayarla"
                ],
                "parlaklık": [
                    "parlaklık", "ekran parlaklığı", "ışık", "ekran ışığı",
                    "parlaklığı arttır", "parlaklığı azalt", "ekranı aydınlat"
                ],
                "hava": [
                    "hava", "hava durumu", "hava nasıl", "havalar nasıl olacak",
                    "hava tahmini", "meteoroloji", "hava şartları"
                ],
                "müzik": [
                    "müzik", "şarkı", "müzik kontrolü", "müziği başlat",
                    "müziği durdur", "şarkı aç", "şarkıyı durdur"
                ],
                "arama": [
                    "ara", "arama", "internet", "internetde", "arama yap",
                    "arama yapalım", "internetde ara", "arama yapalım"
                ],
                "youtube": [
                    "youtube", "youtube ara", "video", "video ara",
                    "youtube video", "youtube video ara", "youtube arama"
                ],
                "wikipedia": [
                    "wikipedia", "wikipedia ara", "wiki", "wiki ara",
                    "wikipedia makalesi", "wikipedia makale ara", "wiki makale"
                ],
                "yazma": [
                    "yaz", "yazdir", "yazdır", "metin yaz", "metin yazdır",
                    "yazma", "yazmak", "yazdırma", "yazdırmak"
                ]
            }
            
            self.pro_command_aliases = {
                "ekran görüntüsü": [
                    "ekran görüntüsü", "screenshot", "ekran resmi çek",
                    "ekranın resmini çek", "ekranı çek", "resim çek"
                ]
            }

    def _fuzzy_match_command(self, command: str, aliases: Dict[str, List[str]]) -> Tuple[Optional[str], Optional[str], float]:
        """Əmrin əvvəlindəki ləqəbi tapıb, uyğunluq xallarını yalnız ləqəb hissəsi üçün hesablayır. Qalanını parametr kimi emal edir."""
        best_match = None
        best_score = 0
        matched_alias = None

        command = command.strip().lower()
        for cmd_name, cmd_aliases in aliases.items():
            for alias in cmd_aliases:
                alias = alias.strip().lower()
                # Əgər əmr ləqəblə başlayırsa
                if command.startswith(alias):
                    # Yalnız ləqəb hissəsi üçün xal hesabla
                    alias_words = alias.split()
                    word_scores = []
                    command_words = alias_words  # Yalnız ləqəb hissəsi üçün
                    for cmd_word in command_words:
                        best_word_score = 0
                        for alias_word in alias_words:
                            score = self._string_similarity(cmd_word, alias_word)
                            if score > best_word_score:
                                best_word_score = score
                        word_scores.append(best_word_score)
                    for alias_word in alias_words:
                        best_word_score = 0
                        for cmd_word in command_words:
                            score = self._string_similarity(alias_word, cmd_word)
                            if score > best_word_score:
                                best_word_score = score
                        word_scores.append(best_word_score)
                    score = sum(word_scores) / len(word_scores) if word_scores else 0
                    # Musiqi əmrləri üçün xüsusi yoxlama
                    if "musiqi" in cmd_name or "müzik" in cmd_name:
                        if not any(word in command for word in ["musiqi", "müzik", "mahnı", "şarkı"]):
                            score *= 0.5
                    if score > best_score:
                        best_score = score
                        best_match = cmd_name
                        matched_alias = alias
                else:
                    # Tam uyğunluq yoxlaması
                    if command == alias:
                        return cmd_name, alias, 1.0
                    # Köhnə məntiq: söz əsaslı fuzzy
                    alias_words = alias.split()
                    command_words = command.split()
                    word_scores = []
                    for cmd_word in command_words:
                        best_word_score = 0
                        for alias_word in alias_words:
                            score = self._string_similarity(cmd_word, alias_word)
                            if score > best_word_score:
                                best_word_score = score
                        word_scores.append(best_word_score)
                    for alias_word in alias_words:
                        best_word_score = 0
                        for cmd_word in command_words:
                            score = self._string_similarity(alias_word, cmd_word)
                            if score > best_word_score:
                                best_word_score = score
                        word_scores.append(best_word_score)
                    score = sum(word_scores) / len(word_scores) if word_scores else 0
                    if "musiqi" in cmd_name or "müzik" in cmd_name:
                        if not any(word in command for word in ["musiqi", "müzik", "mahnı", "şarkı"]):
                            score *= 0.5
                    if score > best_score:
                        best_score = score
                        best_match = cmd_name
                        matched_alias = alias
        return best_match, matched_alias, best_score

    def _string_similarity(self, s1: str, s2: str) -> float:
        """İki sətir arasındakı oxşarlığı hesabla"""
        # Levenshtein məsafəsindən istifadə et
        from difflib import SequenceMatcher
        return SequenceMatcher(None, s1.lower(), s2.lower()).ratio()

    def _extract_parameters(self, command: str, matched_alias: str) -> Dict[str, any]:
        """Əmrdən parametrləri çıxar"""
        params = {}
        return params

    def _fuzzy_match_custom_command(self, command: str, custom_commands: List[Dict]) -> Tuple[Optional[Dict], float, str]:
        """Əmrin əvvəlindəki trigger'ı tapıb, uyğunluq xallarını yalnız trigger hissəsi üçün hesablayır. Qalanını parametr kimi emal edir."""
        current_lang = self.Azer_AI.voice_settings['language']
        best_match = None
        best_score = 0
        matched_text = ""

        command = command.strip().lower()
        for cmd in custom_commands:
            if current_lang in cmd['triggers']:
                for trigger in cmd['triggers'][current_lang]:
                    trigger = trigger.strip().lower()
                    # Əgər əmr trigger ilə başlayırsa
                    if command.startswith(trigger):
                        trigger_words = trigger.split()
                        word_scores = []
                        command_words = trigger_words  # Yalnız trigger hissəsi üçün
                        for cmd_word in command_words:
                            best_word_score = 0
                            for trigger_word in trigger_words:
                                score = self._string_similarity(cmd_word, trigger_word)
                                if score > best_word_score:
                                    best_word_score = score
                            word_scores.append(best_word_score)
                        for trigger_word in trigger_words:
                            best_word_score = 0
                            for cmd_word in command_words:
                                score = self._string_similarity(trigger_word, cmd_word)
                                if score > best_word_score:
                                    best_word_score = score
                            word_scores.append(best_word_score)
                        score = sum(word_scores) / len(word_scores) if word_scores else 0
                        action = cmd.get('action', '').lower()
                        if action == "Veb Axtarış" and any(word in command for word in ['axtar', 'ara', 'tap', 'search']):
                            score *= 1.2
                        elif action == "Veb Sayt Aç" and any(word in command for word in ['aç', 'açıl', 'göster', 'open']):
                            score *= 1.2
                        if "pro" in cmd.get('type', '').lower():
                            score *= 0.9
                        if score > best_score:
                            best_score = score
                            best_match = cmd
                            matched_text = trigger
                    else:
                        # Tam uyğunluq yoxlaması
                        if command == trigger:
                            return cmd, 1.0, trigger
                        # Köhnə məntiq: söz əsaslı fuzzy
                        trigger_words = trigger.split()
                        command_words = command.split()
                        word_scores = []
                        for cmd_word in command_words:
                            best_word_score = 0
                            for trigger_word in trigger_words:
                                score = self._string_similarity(cmd_word, trigger_word)
                                if score > best_word_score:
                                    best_word_score = score
                            word_scores.append(best_word_score)
                        for trigger_word in trigger_words:
                            best_word_score = 0
                            for cmd_word in command_words:
                                score = self._string_similarity(trigger_word, cmd_word)
                                if score > best_word_score:
                                    best_word_score = score
                            word_scores.append(best_word_score)
                        score = sum(word_scores) / len(word_scores) if word_scores else 0
                        action = cmd.get('action', '').lower()
                        if action == "Veb Axtarış" and any(word in command for word in ['axtar', 'ara', 'tap', 'search']):
                            score *= 1.2
                        elif action == "Veb Sayt Aç" and any(word in command for word in ['aç', 'açıl', 'göster', 'open']):
                            score *= 1.2
                        if "pro" in cmd.get('type', '').lower():
                            score *= 0.9
                        if score > best_score:
                            best_score = score
                            best_match = cmd
                            matched_text = trigger
        return best_match, best_score, matched_text

    def process_command(self, command: str):
        """Əsas əmr emal metodu"""
        command = command.lower().strip()
        self.last_command = command
        
        # İstifadəçi lisenziya vəziyyəti və dil tənzimini al
        user_license_status = "Pro" if self.Azer_AI.current_user['license_status'] == "pro" else "Free"
        current_lang = self.Azer_AI.voice_settings['language']
        
        # Əmr ləqəblərini yenilə
        self.update_command_aliases()
        
        # Əmrləri "sonra" sözünə görə ayır - dilə görə
        separator = "sonra" if current_lang == 'az-AZ' else "sonra"
        commands = [cmd.strip() for cmd in command.split(separator)]
        
        # Hər əmri sırayla emal et
        for i, single_command in enumerate(commands):
            if not single_command.strip():
                continue
                
            # Əvvəlcə plugin əmrlərini yoxla
            plugin_name, matched_trigger, plugin_score = self.Azer_AI.plugin_manager.check_plugin_trigger(single_command)
            
            if plugin_name and plugin_score >= 0.5:  # %50 və yuxarı uyğunluq
                # Plugin əmrini işlə
                if self.Azer_AI.plugin_manager.execute_plugin(plugin_name, single_command):
                    # Plugin uğurla işlədildi, növbəti əmrə keç
                    if i < len(commands) - 1:  # Son əmr deyilsə qısa gözləmə
                        time.sleep(0.5)
                    continue
                # Plugin işlədilə bilmədisə normal əmr emalına davam et
            
            # Xüsusi əmrləri yoxla - təkmilləşdirilmiş uyğunlaşdırma ilə
            custom_match, custom_score, matched_text = self._fuzzy_match_custom_command(
                single_command,
                self.custom_commands
            )
            
            # matched_text'dən sonra gələn hissəni parametr kimi al
            custom_param = None
            if matched_text and matched_text in single_command:
                parts = single_command.split(matched_text, 1)
                if len(parts) > 1:
                    custom_param = parts[1].strip()
                    if custom_param == '':
                        custom_param = None

            if custom_match and custom_score >= 0.7:  # %70 və yuxarı uyğunluq
                if user_license_status != "Pro":
                    if current_lang == 'az-AZ':
                        self.Azer_AI.speak("Bu xüsusi əmr yalnız Pro versiya üçün mövcuddur.")
                    else:
                        self.Azer_AI.speak("Bu özel komut sadece Pro sürüm için mevcuttur.")
                    continue
                
                # Xüsusi əmri işlə (parametr ilə)
                self.execute_custom_command(custom_match, matched_text, single_command, custom_param)
                # Əmrlər arasında qısa bir gözləmə əlavə et
                if i < len(commands) - 1:  # Son əmr deyilsə
                    time.sleep(0.5)
                continue
            
            # Pro əmrlərini yoxla
            pro_match, pro_alias, pro_score = self._fuzzy_match_command(single_command, self.pro_command_aliases)
            pro_param = None
            if pro_alias and pro_alias in single_command:
                parts = single_command.split(pro_alias, 1)
                if len(parts) > 1:
                    pro_param = parts[1].strip()
                    if pro_param == '':
                        pro_param = None

            if pro_match and pro_score >= 0.7:
                if user_license_status != "Pro":
                    if current_lang == 'az-AZ':
                        self.Azer_AI.speak("Bu əmr yalnız Pro versiya üçün mövcuddur.")
                    else:
                        self.Azer_AI.speak("Bu komut sadece Pro sürüm için mevcuttur.")
                    continue
                
                # Pro əmrini işlə (parametr ilə)
                if "ekran" in pro_match:
                    self.screenshot()
                # Əmrlər arasında qısa bir gözləmə əlavə et
                if i < len(commands) - 1:  # Son əmr deyilsə
                    time.sleep(0.5)
                continue
            
            # Free əmrlərini yoxla
            free_match, free_alias, free_score = self._fuzzy_match_command(single_command, self.free_command_aliases)
            free_param = None
            if free_alias and free_alias in single_command:
                parts = single_command.split(free_alias, 1)
                if len(parts) > 1:
                    free_param = parts[1].strip()
                    if free_param == '':
                        free_param = None

            if free_match and free_score >= 0.6:  # Free əmrlər üçün daha aşağı hədd (%60)
                # Əmr növünə görə emal et
                if "selamlaşma" in free_match or "selamlama" in free_match:
                    self.greet()
                
                elif "saat" in free_match:
                    self.tell_time()
                
                elif "tarix" in free_match or "tarih" in free_match:
                    self.tell_date()
                
                elif "qeyd" in free_match or "not" in free_match:
                    self.take_note(free_param)
                
                elif "sistem" in free_match:
                    self.system_info()
                
                elif "səs" in free_match or "ses" in free_match:
                    self.set_volume(free_param if free_param else single_command)
                
                elif "parlaqlıq" in free_match or "parlaklık" in free_match:
                    self.set_brightness(free_param if free_param else single_command)
                
                elif "hava" in free_match:
                    self.get_weather(free_param if free_param else single_command)
                
                elif "musiqi" in free_match or "müzik" in free_match:
                    # Musiqi əmrləri üçün xüsusi yoxlama
                    if any(word in single_command.lower() for word in ["musiqi", "müzik", "mahnı", "şarkı"]):
                        self.control_music(free_param if free_param else single_command)

                elif "axtarış" in free_match or "arama" in free_match:
                    self.search(free_param)
                
                elif "youtube" in free_match:
                    self.search_youtube(free_param)
                
                elif "wikipedia" in free_match:
                    self.search_wikipedia(free_param)
                
                elif "yazma" in free_match:
                    self.type_text(free_param)
                
                # Əmrlər arasında qısa bir gözləmə əlavə et
                if i < len(commands) - 1:  # Son əmr deyilsə
                    time.sleep(0.5)
                continue
            
            # Heç bir əmr uyğun gəlmədisə
            if current_lang == 'az-AZ':
                self.Azer_AI.speak("Üzr istəyirəm, bu əmri başa düşmədim.")
            else:
                self.Azer_AI.speak("Üzgünüm, bu komutu anlamadım.")
            # Əmrlər arasında qısa bir gözləmə əlavə et
            if i < len(commands) - 1:  # Son əmr deyilsə
                time.sleep(0.5)

    def greet(self):
        """Salamlaşma"""
        self.greet_manager.greet()

    def tell_time(self):
        """Saat məlumatı"""
        self.time_manager.tell_time()

    def tell_date(self):
        """Tarix məlumatı"""
        self.date_manager.tell_date()

    def take_note(self, command=None):
        """Qeyd götürmə"""
        self.notes_manager.take_note(command)

    def system_info(self):
        """Sistem məlumatları"""
        self.system_manager.system_info()

    # Pro əmr metodları
    def screenshot(self):
        """Ekran şəkli"""
        self.screenshot_manager.take_screenshot()
    
    def set_volume(self, command=None):
        """Səs səviyyəsini tənzimlə"""
        self.volume_manager.set_volume(command)

    def set_brightness(self, command=None):
        """Ekran parlaqlığını tənzimlə"""
        self.brightness_manager.set_brightness(command)
    
    def get_weather(self, command=None):
        """Hava vəziyyətini yoxla"""
        self.weather_manager.get_weather(command)
    
    def control_music(self, command=None):
        """Musiqi idarəsi"""
        self.music_manager.control_music(command)
    
    def search(self, command=None):
        """İnternet axtarışı et"""
        self.search_manager.search(command)

    def search_youtube(self, command=None):
        """YouTube'da video axtar"""
        self.youtube_manager.search_youtube(command)
    
    def search_wikipedia(self, command=None):
        """Wikipedia'da axtarış et"""
        self.wikipedia_manager.search_wikipedia(command)
    
    def execute_custom_command(self, cmd, matched_trigger=None, current_command=None, param=None):
        """Xüsusi əmri işlə (parametr dəstəyi ilə)"""
        try:
            # Dil yoxlaması
            is_az = self.Azer_AI.voice_settings['language'] == 'az-AZ'
            
            # Mesajlar lüğəti
            messages = {
                'program_open': {
                    'az': f"{cmd['name']} proqramı açılır.",
                    'tr': f"{cmd['name']} programı açılıyor."
                },
                'program_close': {
                    'az': f"{cmd['name']} proqramı bağlandı.",
                    'tr': f"{cmd['name']} programı kapatıldı."
                },
                'program_not_found': {
                    'az': f"{cmd['name']} proqramı tapılmadı.",
                    'tr': f"{cmd['name']} programı bulunamadı."
                },
                'website_open': {
                    'az': f"{cmd['name']} saytı açılır.",
                    'tr': f"{cmd['name']} sitesi açılıyor."
                },
                'script_run': {
                    'az': f"{cmd['name']} skripti işlədilir.",
                    'tr': f"{cmd['name']} scripti çalıştırılıyor."
                },
                'web_search': {
                    'az': f"{cmd['name']} üzrə axtarış edilir.",
                    'tr': f"{cmd['name']} için arama yapılıyor."
                },
                'search_prompt': {
                    'az': "Nə axtarmaq istəyirsiniz?",
                    'tr': "Ne aramak istiyorsunuz?"
                },
                'keyboard_shortcut': {
                    'az': f"{cmd['name']} qısayolu işlədilir.",
                    'tr': f"{cmd['name']} kısayolu çalıştırılıyor."
                },
                'error': {
                    'az': "Əmr işlədilməsində xəta baş verdi.",
                    'tr': "Komut çalıştırılırken hata oluştu."
                }
            }
            
            # Mesaj seçimi üçün köməkçi funksiya
            def get_message(msg_key):
                return messages[msg_key]['az' if is_az else 'tr']
            
            if cmd['action'] == "Proqram Aç":
                os.startfile(cmd['target'])
                self.Azer_AI.speak(get_message('program_open'))
            
            elif cmd['action'] == "Proqram Bağla":
                import psutil
                target_name = os.path.basename(cmd['target']).lower()
                found = False
                
                # Bütün işləyən prosesləri yoxla
                for proc in psutil.process_iter(['name']):
                    try:
                        if proc.info['name'].lower() == target_name:
                            proc.kill()
                            found = True
                    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                        continue
                
                if found:
                    self.Azer_AI.speak(get_message('program_close'))
                else:
                    self.Azer_AI.speak(get_message('program_not_found'))
            
            elif cmd['action'] == "Veb Sayt Aç":
                webbrowser.open(cmd['target'])
                self.Azer_AI.speak(get_message('website_open'))
            
            elif cmd['action'] == "Skript İşlət":
                os.system(f"python {cmd['target']}")
                self.Azer_AI.speak(get_message('script_run'))
                
            elif cmd['action'] == "Veb Axtarış":
                search_query = param
                if not search_query:
                    self.Azer_AI.speak(get_message('search_prompt'))
                    search_query = self.Azer_AI.listen_for_response()
                if search_query:
                    search_url = cmd['target'].replace("{}", search_query)
                    webbrowser.open(search_url)
                    self.Azer_AI.speak(get_message('web_search'))
            
            elif cmd['action'] == "Klaviatura Qısayolu":
                # Klaviatura Qısayolunu işlə
                self._execute_keyboard_shortcut(cmd['target'])
                self.Azer_AI.speak(get_message('keyboard_shortcut'))
                
        except Exception as e:
            self.Azer_AI.speak(get_message('error'))
    
    def _execute_keyboard_shortcut(self, shortcut_str):
        """Klaviatura Qısayolunu işlə
        
        Nümunə formatlar:
        - "win+v" - Windows panosu
        - "ctrl+c" - Kopyala
        - "alt+tab" - Pəncərələr arası keçid
        - "ctrl+shift+esc" - Tapşırıq idarəçisi
        """
        try:
            # Dil yoxlaması
            is_az = self.Azer_AI.voice_settings['language'] == 'az-AZ'
            
            # Qısayolu hissələrə böl
            keys = shortcut_str.lower().split('+')
            
            # Bütün düymələri basılı saxla
            for key in keys:
                key = key.strip()
                pyautogui.keyDown(key)
            
            # Bütün düymələri sərbəst burax (tərs sırada)
            for key in reversed(keys):
                key = key.strip()
                pyautogui.keyUp(key)
                
            # Qısa bir gözləmə əlavə et
            time.sleep(0.1)
            
        except Exception as e:
            if is_az:
                self.Azer_AI.speak(f"Klaviatura qısayolu işlətmə xətası: {e}")
            else:
                self.Azer_AI.speak(f"Klavye kısayolu çalıştırma hatası: {e}")

    def type_text(self, command=None):
        """Ekrana mətn yazdır"""
        self.typing_manager.type_text(command)