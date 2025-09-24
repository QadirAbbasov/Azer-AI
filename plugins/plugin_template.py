class TemplatePlugin:
    """
    Bu bir Python plugin şablonudur. Öz plugininizi yaratmaq üçün bu faylı kopyalayın
    və lazımi sahələri doldurun. Tətikleyicilər (triggers) manifest.json içindən oxunur.
    """
    
    @property
    def name(self) -> str:
        """Plugin adı - Bu sahə məcburidir"""
        return "Plugin Adı"
        
    @property
    def version(self) -> str:
        """Plugin versiyası - Bu sahə məcburidir"""
        return "1.0.0"
        
    @property
    def description(self) -> str:
        """Plugin təsviri - Bu sahə məcburidir"""
        return "Plugin təsviri buraya yazılır"
        
    @property
    def author(self) -> str:
        """Plugin müəllifi - Bu sahə məcburidir"""
        return "Müəllif Adı"
        
    @property
    def license_type(self) -> str:
        """
        Plugin lisenziya növü - Bu sahə məcburidir
        "free" - Pulsuz plugin (bütün istifadəçilər istifadə edə bilər)
        "pro" - Pro plugin (yalnız Pro istifadəçilər istifadə edə bilər)
        """
        return "free"  # və ya "pro"
        
    @property
    def logo(self) -> str:
        """
        Plugin loqosunun nisbi fayl yolu və ya URL'si - Bu sahə məcburi deyil amma tövsiyə olunur
        Nümunə: 'logo.png' (manifest.json ilə eyni qovluqda)
        """
        return "logo.png"
        
    def execute(self, Azer_AI, command: str) -> None:
        """
        Plugin əmrini işlə - Bu sahə məcburidir
        
        Args:
            Azer_AI: Əsas tətbiq nümunəsi (ModernAzer_AI sinifi)
            command: İstifadəçinin dediyi əmr (string)
        """
        # Dil yoxlaması
        current_language = Azer_AI.voice_settings['language']
        
        if current_language == 'az-AZ':
            # Azərbaycan cavabı
            Azer_AI.speak("Azərbaycan dilində cavab")
        elif current_language == 'tr-TR':
            # Türk cavabı
            Azer_AI.speak("Türk cavabı")
        else:
            # Varsayılan cavab
            Azer_AI.speak("Varsayılan cavab")
            
        # Plugin kodunuzu buraya yazın
        # Nümunə: Fayl əməliyyatları, API çağırışları, hesablamalar və s.
        
        # Xəta idarəetməsi
        try:
            # Plugin əməliyyatları
            pass
        except Exception as e:
            Azer_AI.speak(f"Plugin işlədilərkən xəta baş verdi: {str(e)}")


# Plugin yaratma təlimatı (PYTHON):
"""
1. Bu faylı kopyalayın və yeni adla saxlayın (məsələn: my_plugin.py)
2. Sinif adını dəyişdirin (məsələn: TemplatePlugin -> MyPlugin)
3. Aşağıdakı property'ləri öz plugininizə görə təşkil edin: name, version, description, author, license_type (logo opsiyonel)
4. execute metodunu öz funksionallığınıza görə yazın
5. Eyni qovluqda bir manifest.json yaradın və aşağıdakı sahələri doldurun:
   {
     "name": "MyPlugin",
     "version": "1.0.0",
     "main_file": "my_plugin.py",
     "description": "Plugin təsviri",
     "author": "Sizin adınız",
     "license_type": "free",
     "logo": "logo.png",
     "triggers": {
       "az-AZ": ["tetikleyici1", "tetikleyici2"],
       "tr-TR": ["tetikleyici1", "tetikleyici2"]
     }
   }
6. Plugin qovluğunu zip faylı halına gətirin (manifest.json və ana .py faylı daxil olmalıdır)
7. Tətbiqdə "Plugin Yüklə" düyməsini istifadə edərək yükləyin

Vacib Qeydlər:
- Yalnız .py pluginləri dəstəklənir
- Plugin adı unikal olmalıdır
- Lisenziya növü düzgün olmalıdır (free/pro)
- Tətikleyicilər manifest.json içində verilməlidir
- Xəta idarəetməsi edilməlidir
- Dil dəstəyi təmin edilməlidir (az-AZ və tr-TR)
""" 