import os
import json
import zipfile
import importlib.util
import shutil
from typing import List, Dict

class PluginManager:
    def __init__(self, Azer_AI):
        self.Azer_AI = Azer_AI
        self.plugins: Dict[str, object] = {}
        self.plugin_dir = "plugins"
        self.installed_plugins_file = os.path.join(self.plugin_dir, "installed_plugins.json")
        
        # Plugin qovluğunu yarat
        os.makedirs(self.plugin_dir, exist_ok=True)
        
        # Yüklü pluginləri yüklə
        self.load_installed_plugins()
        
    def load_installed_plugins(self):
        """Yüklü pluginləri yüklə (toplu nəticə bildirişi ilə)"""
        if not os.path.exists(self.installed_plugins_file):
            return
        
        successful_plugins = []
        failed_plugins = []
        try:
            with open(self.installed_plugins_file, 'r', encoding='utf-8') as f:
                installed_plugins = json.load(f)
            
            for plugin_info in installed_plugins:
                plugin_path = os.path.join(self.plugin_dir, plugin_info['name'])
                if os.path.exists(plugin_path):
                    result = self.load_plugin(plugin_path, batch_mode=True)
                    if result:
                        successful_plugins.append(plugin_info['name'])
                    else:
                        failed_plugins.append(plugin_info['name'])
                else:
                    failed_plugins.append(plugin_info['name'])
        except Exception as e:
            current_lang = self.Azer_AI.voice_settings['language']
            if current_lang == 'az-AZ':
                self.Azer_AI.speak(f"Plugin yükləmə xətası: {e}")
            else:
                self.Azer_AI.speak(f"Plugin yükleme hatası: {e}")
            return
        
        # Yalnız xəta varsa danış
        if len(failed_plugins) > 0:
            current_lang = self.Azer_AI.voice_settings['language']
            if len(successful_plugins) > 0:
                if current_lang == 'az-AZ':
                    self.Azer_AI.speak(
                        f"{len(successful_plugins)} plugin uğurla yükləndi: {', '.join(successful_plugins)}. "
                        f"{len(failed_plugins)} plugin yüklənə bilmədi: {', '.join(failed_plugins)}."
                    )
                else:
                    self.Azer_AI.speak(
                        f"{len(successful_plugins)} plugin başarıyla yüklendi: {', '.join(successful_plugins)}. "
                        f"{len(failed_plugins)} plugin yüklenemedi: {', '.join(failed_plugins)}."
                    )
            else:
                if current_lang == 'az-AZ':
                    self.Azer_AI.speak(
                        f"Heç bir plugin yüklənə bilmədi. Xətali pluginlər: {', '.join(failed_plugins)}."
                    )
                else:
                    self.Azer_AI.speak(
                        f"Hiçbir plugin yüklenemedi. Hatalı pluginler: {', '.join(failed_plugins)}."
                    )
            
    def install_plugin(self, zip_path: str) -> bool:
        """Yeni bir plugin yüklə"""
        try:
            # Zip faylını yoxla
            if not zipfile.is_zipfile(zip_path):
                raise ValueError("Yanlış plugin faylı")
                
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                # manifest.json faylını yoxla
                if 'manifest.json' not in zip_ref.namelist():
                    raise ValueError("manifest.json tapılmadı")
                    
                # Manifest faylını oxu
                manifest_content = zip_ref.read('manifest.json').decode('utf-8')
                manifest = json.loads(manifest_content)
                
                # Lazımi sahələri yoxla
                required_fields = ['name', 'version', 'main_file']
                for field in required_fields:
                    if field not in manifest:
                        raise ValueError(f"manifest.json'da {field} sahəsi çatışmır")
                        
                plugin_name = manifest['name']
                main_file = manifest['main_file']
                
                # Əsas faylın zip içində olub-olmadığını yoxla
                if main_file not in zip_ref.namelist():
                    raise ValueError(f"Əsas fayl {main_file} tapılmadı")
                
                plugin_dir = os.path.join(self.plugin_dir, plugin_name)
                
                # Köhnə versiyanı sil
                if os.path.exists(plugin_dir):
                    shutil.rmtree(plugin_dir)
                    
                # Plugin'i qovluğa çıxar
                zip_ref.extractall(plugin_dir)
                
                # Plugin'i yüklə
                if self.load_plugin(plugin_dir):
                    # Yüklü pluginlər siyahısını yenilə
                    self.update_installed_plugins_list(manifest)
                    return True
                else:
                    # Yükləmə uğursuzdursa qovluğu təmizlə
                    if os.path.exists(plugin_dir):
                        shutil.rmtree(plugin_dir)
                    return False
                    
        except Exception as e:
            current_lang = self.Azer_AI.voice_settings['language']
            if current_lang == 'az-AZ':
                self.Azer_AI.speak(f"Plugin yükləmə xətası: {e}")
            else:
                self.Azer_AI.speak(f"Plugin yükleme hatası: {e}")
            return False
            
    def load_plugin(self, plugin_dir: str, batch_mode: bool = False) -> bool:
        """Göstərilən qovluqdakı plugin'i yüklə. batch_mode=True isə uğur mesajı vermə."""
        try:
            # manifest.json faylını oxu
            manifest_path = os.path.join(plugin_dir, 'manifest.json')
            if not os.path.exists(manifest_path):
                if not batch_mode:
                    current_lang = self.Azer_AI.voice_settings['language']
                    if current_lang == 'az-AZ':
                        self.Azer_AI.speak(f"manifest.json faylı tapılmadı: {manifest_path}")
                    else:
                        self.Azer_AI.speak(f"manifest.json dosyası bulunamadı: {manifest_path}")
                return False
                
            with open(manifest_path, 'r', encoding='utf-8') as f:
                manifest = json.load(f)
                
            # Əsas faylı yoxla
            main_file = manifest['main_file']
            main_file_path = os.path.join(plugin_dir, main_file)
            
            if not os.path.exists(main_file_path):
                if not batch_mode:
                    current_lang = self.Azer_AI.voice_settings['language']
                    if current_lang == 'az-AZ':
                        self.Azer_AI.speak(f"Əsas fayl tapılmadı: {main_file_path}")
                    else:
                        self.Azer_AI.speak(f"Ana dosya bulunamadı: {main_file_path}")
                return False
            
            # Fayl uzantısını yoxla
            file_extension = os.path.splitext(main_file)[1].lower()
            
            if file_extension == '.py':
                # Python faylı üçün normal yükləmə
                return self._load_python_plugin(plugin_dir, manifest, batch_mode)
            else:
                if not batch_mode:
                    current_lang = self.Azer_AI.voice_settings['language']
                    if current_lang == 'az-AZ':
                        self.Azer_AI.speak(f"Dəstəklənməyən fayl növü: {file_extension}. Yalnız .py faylları dəstəklənir.")
                    else:
                        self.Azer_AI.speak(f"Desteklenmeyen dosya türü: {file_extension}. Yalnız .py dosyaları desteklenir.")
                return False
            
        except Exception as e:
            if not batch_mode:
                current_lang = self.Azer_AI.voice_settings['language']
                if current_lang == 'az-AZ':
                    self.Azer_AI.speak(f"Plugin yükləmə xətası: {e}")
                else:
                    self.Azer_AI.speak(f"Plugin yükleme hatası: {e}")
                import traceback
                traceback.print_exc()
            return False
    
    def _load_python_plugin(self, plugin_dir: str, manifest: dict, batch_mode: bool = False) -> bool:
        """Python faylı üçün plugin yüklə"""
        try:
            main_file = manifest['main_file']
            module_path = os.path.join(plugin_dir, main_file)
            
            # Module adını yarat
            module_name = f"plugins.{manifest['name']}.{os.path.splitext(main_file)[0]}"
            
            # Module'ü yüklə
            spec = importlib.util.spec_from_file_location(module_name, module_path)
            if spec is None:
                if not batch_mode:
                    current_lang = self.Azer_AI.voice_settings['language']
                    if current_lang == 'az-AZ':
                        self.Azer_AI.speak(f"Module spec yaradıla bilmədi: {module_path}")
                    else:
                        self.Azer_AI.speak(f"Module spec oluşturulamadı: {module_path}")
                return False
                
            module = importlib.util.module_from_spec(spec)
            if module is None:
                if not batch_mode:
                    current_lang = self.Azer_AI.voice_settings['language']
                    if current_lang == 'az-AZ':
                        self.Azer_AI.speak(f"Module yaradıla bilmədi: {module_path}")
                    else:
                        self.Azer_AI.speak(f"Module oluşturulamadı: {module_path}")
                return False
                
            # Module'ü işlə
            spec.loader.exec_module(module)
            
            # Plugin sinifini tap və yüklə
            plugin_class = None
            for item_name in dir(module):
                item = getattr(module, item_name)
                # Sinif olub-olmadığını yoxla
                if (isinstance(item, type) and 
                    item_name.endswith('Plugin') and 
                    hasattr(item, 'name') and 
                    hasattr(item, 'execute')):
                    plugin_class = item
                    break
                    
            if not plugin_class:
                if not batch_mode:
                    current_lang = self.Azer_AI.voice_settings['language']
                    if current_lang == 'az-AZ':
                        self.Azer_AI.speak(f"Plugin sinifi tapılmadı: {module_path}")
                    else:
                        self.Azer_AI.speak(f"Plugin sınıfı bulunamadı: {module_path}")
                return False
                
            # Plugin nümunəsini yarat
            plugin_instance = plugin_class()
            
            # Plugin'in lazımi xüsusiyyətlərini yoxla
            required_properties = ['name', 'version', 'description', 'author', 'license_type']
            for prop in required_properties:
                if not hasattr(plugin_instance, prop):
                    if not batch_mode:
                        current_lang = self.Azer_AI.voice_settings['language']
                        if current_lang == 'az-AZ':
                            self.Azer_AI.speak(f"Plugin'də {prop} xüsusiyyəti çatışmır")
                        else:
                            self.Azer_AI.speak(f"Plugin'de {prop} özelliği eksik")
                    return False
            
            # Plugin dict'i yarat
            plugin = {
                'name': plugin_instance.name,
                'version': plugin_instance.version,
                'description': plugin_instance.description,
                'author': plugin_instance.author,
                'license_type': plugin_instance.license_type,
                'triggers': manifest.get('triggers', {'az-AZ': [], 'tr-TR': []}),
                'logo': getattr(plugin_instance, 'logo', manifest.get('logo', '')),
                'instance': plugin_instance,
                'type': 'python'
            }
            
            # Plugin'i saxla
            self.plugins[plugin['name']] = plugin
            if not batch_mode:
                current_lang = self.Azer_AI.voice_settings['language']
                if current_lang == 'az-AZ':
                    self.Azer_AI.speak(f"Python plugin'i uğurla yükləndi: {plugin['name']}")
                else:
                    self.Azer_AI.speak(f"Python plugin'i başarıyla yüklendi: {plugin['name']}")
            return True
            
        except Exception as e:
            if not batch_mode:
                current_lang = self.Azer_AI.voice_settings['language']
                if current_lang == 'az-AZ':
                    self.Azer_AI.speak(f"Python plugin yükləmə xətası: {e}")
                else:
                    self.Azer_AI.speak(f"Python plugin yükleme hatası: {e}")
            return False
            
    def uninstall_plugin(self, plugin_name: str) -> bool:
        """Plugin'i sil"""
        try:
            if plugin_name not in self.plugins:
                return False
                
            # Plugin'i siyahıdan sil
            del self.plugins[plugin_name]
            
            # Plugin qovluğunu sil
            plugin_dir = os.path.join(self.plugin_dir, plugin_name)
            if os.path.exists(plugin_dir):
                shutil.rmtree(plugin_dir)
                
            # Yüklü pluginlər siyahısını yenilə
            self.update_installed_plugins_list(remove_plugin_name=plugin_name)
            return True
            
        except Exception as e:
            current_lang = self.Azer_AI.voice_settings['language']
            if current_lang == 'az-AZ':
                self.Azer_AI.speak(f"Plugin silmə xətası: {e}")
            else:
                self.Azer_AI.speak(f"Plugin silme hatası: {e}")
            return False
            
    def update_installed_plugins_list(self, new_plugin=None, remove_plugin_name=None):
        """Yüklü pluginlər siyahısını yenilə"""
        try:
            installed_plugins = []
            
            if os.path.exists(self.installed_plugins_file):
                with open(self.installed_plugins_file, 'r', encoding='utf-8') as f:
                    installed_plugins = json.load(f)
                    
            if new_plugin:
                # Köhnə versiyanı sil
                installed_plugins = [p for p in installed_plugins if p.get('name') != new_plugin.get('name')]
                # Yalnız minimal məlumatları saxla
                minimal_entry = {
                    'name': new_plugin.get('name'),
                    'version': new_plugin.get('version', '1.0.0')
                }
                # Yeni versiyanı əlavə et
                installed_plugins.append(minimal_entry)
            elif remove_plugin_name:
                # Plugin'i siyahıdan sil
                installed_plugins = [p for p in installed_plugins if p.get('name') != remove_plugin_name]
            else:
                # Mövcud pluginləri yenidən yaz (silinmiş pluginləri təmizləmək üçün)
                current_plugin_names = set(self.plugins.keys())
                installed_plugins = [
                    {'name': p.get('name'), 'version': p.get('version', '1.0.0')}
                    for p in installed_plugins if p.get('name') in current_plugin_names
                ]
                
            with open(self.installed_plugins_file, 'w', encoding='utf-8') as f:
                json.dump(installed_plugins, f, indent=4, ensure_ascii=False)
                
        except Exception as e:
            current_lang = self.Azer_AI.voice_settings['language']
            if current_lang == 'az-AZ':
                self.Azer_AI.speak(f"Plugin siyahısı yeniləmə xətası: {e}")
            else:
                self.Azer_AI.speak(f"Plugin listesi güncelleme hatası: {e}")
            
    def get_plugin_info(self, plugin_name: str) -> dict:
        """Plugin məlumatlarını qaytar"""
        if plugin_name not in self.plugins:
            return None
            
        plugin = self.plugins[plugin_name]
        return {
            'name': plugin['name'],
            'version': plugin['version'],
            'description': plugin['description'],
            'author': plugin['author'],
            'license_type': plugin['license_type'],
            'triggers': plugin['triggers'],
            'logo': plugin['logo']
        }
        
    def execute_plugin(self, plugin_name: str, command: str) -> bool:
        """Plugin'i işlə"""
        if plugin_name not in self.plugins:
            return False
            
        try:
            plugin = self.plugins[plugin_name]
            
            # Lisenziya yoxlaması
            if plugin['license_type'] == 'pro' and self.Azer_AI.current_user['license_status'] != 'pro':
                current_lang = self.Azer_AI.voice_settings['language']
                if current_lang == 'az-AZ':
                    self.Azer_AI.speak("Bu plugin yalnız Pro istifadəçilər üçün mövcuddur.")
                else:
                    self.Azer_AI.speak("Bu plugin yalnızca Pro kullanıcılar için mevcuttur.")
                return False
                
            # Plugin'i işlə
            if plugin['type'] == 'python':
                plugin['instance'].execute(self.Azer_AI, command)
            return True
            
        except Exception as e:
            current_lang = self.Azer_AI.voice_settings['language']
            if current_lang == 'az-AZ':
                self.Azer_AI.speak(f"Plugin işlətmə xətası: {e}")
            else:
                self.Azer_AI.speak(f"Plugin çalıştırma hatası: {e}")
            return False
    
            
    def get_all_plugins(self) -> List[Dict]:
        """Bütün yüklü pluginlərin məlumatlarını qaytar"""
        plugins_info = []
        for plugin_name in self.plugins:
            info = self.get_plugin_info(plugin_name)
            if info:
                plugins_info.append(info)
        return plugins_info
        
    def check_plugin_trigger(self, command: str) -> tuple:
        """Əmrin hər hansı bir plugin tətikleyicisi ilə uyğun gəlib-gəlmədiyini yoxla"""
        command = command.lower().strip()
        
        for plugin_name, plugin in self.plugins.items():
            current_lang = self.Azer_AI.voice_settings['language']
            
            if current_lang in plugin['triggers']:
                for trigger in plugin['triggers'][current_lang]:
                    trigger = trigger.lower().strip()
                    
                    # Tam uyğunluq yoxlaması
                    if command == trigger:
                        return plugin_name, trigger, 1.0
                    
                    # Başlanğıc uyğunluğu yoxlaması
                    if command.startswith(trigger):
                        return plugin_name, trigger, 0.9
                    
                    # Söz əsaslı fuzzy uyğunluq
                    command_words = command.split()
                    trigger_words = trigger.split()
                    
                    # Ən azı bir söz uyğunluğu
                    common_words = set(command_words) & set(trigger_words)
                    if common_words:
                        similarity = len(common_words) / max(len(command_words), len(trigger_words))
                        if similarity >= 0.5:  # %50 uyğunluq həddi
                            return plugin_name, trigger, similarity
        
        return None, None, 0.0 