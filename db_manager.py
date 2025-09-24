import pymysql
from datetime import datetime
import bcrypt

class DBManager:
    """MySQL verilənlər bazası idarəçi sinifi"""
    
    def __init__(self):
        # Verilənlər bazası bağlantı məlumatları
        self.db_config = {
            'host': 'localhost',
            'user': 'azer_user',
            'password': 'azer_password',
            'database': 'azer_ai',
            'port': 3306,
            'charset': 'utf8mb4',
            'cursorclass': pymysql.cursors.DictCursor
        }
    
    def connect(self):
        """Verilənlər bazasına bağlantı qurar və cursor qaytarır"""
        try:
            self.conn = pymysql.connect(**self.db_config)
            self.cursor = self.conn.cursor()
            return True
        except pymysql.Error as err:
            print(f"Verilənlər bazası bağlantı xətası: {err}")
            return False
    
    def close(self):
        """Verilənlər bazası bağlantısını bağlayır"""
        if hasattr(self, 'cursor') and self.cursor:
            self.cursor.close()
        if hasattr(self, 'conn') and self.conn:
            self.conn.close()
    
    def create_required_tables(self):
        """Lazımi cədvəlləri yaradır"""
        try:
            self.connect()
            
            # İstifadəçilər cədvəli
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    name VARCHAR(100) NOT NULL,
                    role ENUM('user', 'admin') DEFAULT 'user',
                    license_status ENUM('free', 'pro') DEFAULT 'free',
                    pro_expiry DATETIME NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    last_login DATETIME NULL
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            ''')
            
            # Səs parametrləri cədvəli
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS voice_settings (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    tts_engine VARCHAR(20) DEFAULT 'edge',
                    language VARCHAR(10) DEFAULT 'az-AZ',
                    voice_gender VARCHAR(10) DEFAULT 'male',
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            ''')
            
            # Oyanış sözü parametrləri cədvəli
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS wake_word_settings (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    az_word VARCHAR(50) DEFAULT 'azər',
                    tr_word VARCHAR(50) DEFAULT 'azer',
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            ''')
            
            # Pro açarı cədvəli
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS pro_keys (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    key_code VARCHAR(50) UNIQUE NOT NULL,
                    duration INT DEFAULT 30,
                    is_used BOOLEAN DEFAULT FALSE,
                    used_by INT NULL,
                    used_at DATETIME NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (used_by) REFERENCES users(id) ON DELETE SET NULL
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            ''')
            
            # Xüsusi əmrlər cədvəli
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS custom_commands (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    name VARCHAR(100) NOT NULL,
                    action VARCHAR(50) NOT NULL,
                    target VARCHAR(255) NOT NULL,
                    triggers_az TEXT,
                    triggers_tr TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            ''')
            
            self.conn.commit()
            
        except Exception as e:
            # Cədvəllər yaradılarkən xəta:
            print(f"Cədvəllər yaradılarkən xəta: {e}")
        finally:
            self.close()
    
    def execute_query(self, query, params=None, commit=False):
        """SQL sorğusunu işlədir və nəticəni qaytarır"""
        try:
            self.connect()
            self.cursor.execute(query, params or ())
            
            if commit:
                self.conn.commit()
                last_id = self.cursor.lastrowid
                self.close()
                return last_id
            else:
                result = self.cursor.fetchall()
                self.close()
                return result  # DictCursor ilə artıq lüğət formatında qaytaracaq
        except pymysql.Error as err:
            # Sorğu xətası:
            if hasattr(self, 'conn') and self.conn:
                self.conn.rollback()
            self.close()
            return None
    
    # İstifadəçi əməliyyatları
    
    def get_user_by_username(self, username):
        """İstifadəçi adına görə istifadəçini qaytarır"""
        query = """
        SELECT u.*, v.tts_engine, v.language, v.voice_gender
        FROM users u
        LEFT JOIN voice_settings v ON u.id = v.user_id
        WHERE u.username = %s
        """
        users = self.execute_query(query, (username,))
        if users and len(users) > 0:
            return users[0]
        return None
    
    def authenticate_user(self, username, password):
        """İstifadəçini doğrulayır və istifadəçi məlumatlarını qaytarır"""
        user = self.get_user_by_username(username)
        
        try:
            if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
                # Son giriş tarixini yenilə
                self.update_last_login(user['id'])
                
                # Pro müddəti yoxlaması
                expired_pro = False
                if user['pro_expiry'] is not None:
                    pro_expiry = datetime.strptime(user['pro_expiry'], "%Y-%m-%d %H:%M:%S") if isinstance(user['pro_expiry'], str) else user['pro_expiry']
                    if pro_expiry < datetime.now():
                        # Pro müddəti bitmiş, free et
                        self.update_license_status(user['id'], 'free')
                        user['license_status'] = 'free'
                        expired_pro = True
                
                # Səs parametrləri məlumatlarını lüğət içində topla
                voice_settings = {}
                if 'tts_engine' in user and user['tts_engine'] is not None:
                    voice_settings = {
                        'tts_engine': user['tts_engine'],
                        'language': user['language'],
                        'voice_gender': user['voice_gender']
                    }
                
                # İstifadəçi obyektini düzənlə
                user_obj = {
                    'id': user['id'],
                    'username': user['username'],
                    'name': user['name'],
                    'role': user['role'],
                    'license_status': user['license_status'],
                    'voice_settings': voice_settings
                }
                
                # Pro müddətini əlavə et
                if user['pro_expiry'] is not None:
                    user_obj['pro_expiry'] = user['pro_expiry'] if isinstance(user['pro_expiry'], str) else user['pro_expiry'].strftime("%Y-%m-%d %H:%M:%S")
                    
                return user_obj, expired_pro
            else:
                return None, False
        except ValueError:
            # Şifrə yoxlanışı zamanı xəta baş verərsə
            return None, False
        
    
    def update_last_login(self, user_id):
        """İstifadəçinin son giriş tarixini yeniləyir"""
        query = """
        UPDATE users
        SET last_login = NOW()
        WHERE id = %s
        """
        self.execute_query(query, (user_id,), commit=True)
    
    def update_license_status(self, user_id, status):
        """İstifadəçinin lisenziya vəziyyətini yeniləyir"""
        query = """
        UPDATE users
        SET license_status = %s
        WHERE id = %s
        """
        self.execute_query(query, (status, user_id), commit=True)
    
    # Pro açarı əməliyyatları
    
    def get_pro_keys(self):
        """Bütün pro açarını qaytarır"""
        query = """
        SELECT k.*, u.username as used_by_username
        FROM pro_keys k
        LEFT JOIN users u ON k.used_by = u.id
        ORDER BY k.created_at DESC
        """
        return self.execute_query(query)
    
    def get_pro_key(self, key_code):
        """Key koduna görə pro açarı məlumatını qaytarır"""
        query = """
        SELECT *
        FROM pro_keys
        WHERE key_code = %s
        """
        keys = self.execute_query(query, (key_code,))
        if keys and len(keys) > 0:
            return keys[0]
        return None
    
    def activate_pro_key(self, key_code, user_id, duration=30):
        """Pro açarını aktivləşdirir və istifadəçini pro edir"""
        # Açarı yoxla
        key = self.get_pro_key(key_code)
        
        if not key:
            return False, "Yanlış pro açarı"
        
        if key['status'] == 'used':
            return False, "Bu pro açarı əvvəlcədən istifadə edilmiş"
        
        try:
            self.connect()
            
            # Açarı istifadə edilmiş kimi işarələ
            update_key_query = """
            UPDATE pro_keys
            SET status = 'used', 
                activation_date = NOW(),
                used_by = %s
            WHERE key_code = %s
            """
            self.cursor.execute(update_key_query, (user_id, key_code))
            
            # Pro müddətini hesabla
            expiry_query = """
            UPDATE users
            SET license_status = 'pro',
                pro_expiry = DATE_ADD(NOW(), INTERVAL %s DAY)
            WHERE id = %s
            """
            self.cursor.execute(expiry_query, (key['duration'], user_id))
            
            # Əməliyyatı tamamla
            self.conn.commit()
            self.close()
            
            return True, "Pro açarı uğurla aktivləşdirildi"
        except pymysql.Error as err:
            # Xəta halında geri al
            if hasattr(self, 'conn') and self.conn:
                self.conn.rollback()
            self.close()
            return False, f"Əməliyyat zamanı xəta: {err}"
    
    def add_pro_key(self, key_code, duration):
        """Yeni pro açarı əlavə edir"""
        query = """
        INSERT INTO pro_keys (key_code, duration)
        VALUES (%s, %s)
        """
        return self.execute_query(query, (key_code, duration), commit=True)
    
    # Səs parametrləri əməliyyatları
    
    def get_voice_settings(self, user_id):
        """İstifadəçinin səs parametrlərini qaytarır"""
        query = """
        SELECT *
        FROM voice_settings
        WHERE user_id = %s
        """
        settings = self.execute_query(query, (user_id,))
        if settings and len(settings) > 0:
            return settings[0]
        return None
    
    def update_voice_settings(self, user_id, tts_engine, language, voice_gender):
        """İstifadəçinin səs parametrlərini yeniləyir"""
        # Əvvəlcə parametrin mövcud olub-olmadığını yoxla
        settings = self.get_voice_settings(user_id)
        
        if settings:
            # Yenilə
            query = """
            UPDATE voice_settings
            SET tts_engine = %s,
                language = %s,
                voice_gender = %s
            WHERE user_id = %s
            """
            params = (tts_engine, language, voice_gender, user_id)
        else:
            # Yeni əlavə et
            query = """
            INSERT INTO voice_settings (user_id, tts_engine, language, voice_gender)
            VALUES (%s, %s, %s, %s)
            """
            params = (user_id, tts_engine, language, voice_gender)
        
        return self.execute_query(query, params, commit=True)
    
    # Oyanış sözü parametrləri əməliyyatları
    
    def get_wake_word_settings(self, user_id):
        """İstifadəçinin oyanış sözü parametrlərini qaytarır"""
        query = """
        SELECT *
        FROM wake_word_settings
        WHERE user_id = %s
        """
        settings = self.execute_query(query, (user_id,))
        if settings and len(settings) > 0:
            return settings[0]
        return None
    
    def update_wake_word_settings(self, user_id, az_word, tr_word):
        """İstifadəçinin oyanış sözü parametrlərini yeniləyir"""
        # Əvvəlcə parametrin mövcud olub-olmadığını yoxla
        settings = self.get_wake_word_settings(user_id)
        
        if settings:
            # Yenilə
            query = """
            UPDATE wake_word_settings
            SET az_word = %s,
                tr_word = %s
            WHERE user_id = %s
            """
            params = (az_word, tr_word, user_id)
        else:
            # Yeni əlavə et
            query = """
            INSERT INTO wake_word_settings (user_id, az_word, tr_word)
            VALUES (%s, %s, %s)
            """
            params = (user_id, az_word, tr_word)
        
        return self.execute_query(query, params, commit=True)
    
    # Xüsusi əmrlər əməliyyatları
    
    def get_custom_commands(self, user_id):
        """İstifadəçinin xüsusi əmrlərini qaytarır"""
        query = """
        SELECT *
        FROM custom_commands
        WHERE user_id = %s
        """
        return self.execute_query(query, (user_id,))
    
    def add_custom_command(self, user_id, name, action, target, triggers_az, triggers_tr):
        """Yeni xüsusi əmr əlavə edir"""
        query = """
        INSERT INTO custom_commands 
        (user_id, name, action, target, triggers_az, triggers_tr)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        return self.execute_query(
            query, 
            (user_id, name, action, target, ",".join(triggers_az), ",".join(triggers_tr)), 
            commit=True
        )
    
    def update_custom_command(self, cmd_id, name, action, target, triggers_az, triggers_tr):
        """Xüsusi əmri yeniləyir"""
        query = """
        UPDATE custom_commands
        SET name = %s, 
            action = %s, 
            target = %s, 
            triggers_az = %s, 
            triggers_tr = %s
        WHERE id = %s
        """
        return self.execute_query(
            query, 
            (name, action, target, ",".join(triggers_az), ",".join(triggers_tr), cmd_id), 
            commit=True
        )
    
    def delete_custom_command(self, cmd_id):
        """Xüsusi əmri silir"""
        query = """
        DELETE FROM custom_commands
        WHERE id = %s
        """
        return self.execute_query(query, (cmd_id,), commit=True)
    
    # Admin əməliyyatları
    
    def get_all_users(self):
        """Bütün istifadəçiləri qaytarır"""
        query = """
        SELECT u.*, v.tts_engine, v.language, v.voice_gender
        FROM users u
        LEFT JOIN voice_settings v ON u.id = v.user_id
        ORDER BY u.created_at DESC
        """
        return self.execute_query(query)
    
    def user_exists(self, username):
        """İstifadəçi adının verilənlər bazasında olub-olmadığını yoxlayır"""
        query = """
        SELECT COUNT(*) as count
        FROM users
        WHERE username = %s
        """
        result = self.execute_query(query, (username,))
        return result[0]['count'] > 0

    def create_user(self, user_data):
        """Yeni istifadəçi yaradır"""
        try:
            # Lazımi cədvəlləri yarat
            self.create_required_tables()
            
            # Şifrəni hash'lə
            hashed_password = bcrypt.hashpw(user_data['password'].encode('utf-8'), bcrypt.gensalt())
            
            query = """
            INSERT INTO users (username, password, name, role, license_status, created_at)
            VALUES (%s, %s, %s, %s, %s, NOW())
            """
            user_id = self.execute_query(
                query, 
                (user_data['username'], 
                 hashed_password.decode('utf-8'), 
                 user_data['name'], 
                 user_data.get('role', 'user'), 
                 user_data.get('license_status', 'free')), 
                commit=True
            )
            
            if user_id:
                try:
                    # Varsayılan səs parametrlərini əlavə et
                    self.update_voice_settings(user_id, 'edge', 'az-AZ', 'male')
                except Exception as voice_error:
                    # Səs parametrləri əlavə edilərkən xəta:
                    print(f"Səs parametrləri əlavə edilərkən xəta: {voice_error}")
                
                try:
                    # Varsayılan oyanış sözü parametrlərini əlavə et
                    self.update_wake_word_settings(user_id, 'azər', 'azer')
                except Exception as wake_error:
                    # Oyanış sözü parametrləri əlavə edilərkən xəta:
                    print(f"Oyanış sözü parametrləri əlavə edilərkən xəta: {wake_error}")
                
                return True
            return False
            
        except Exception as e:
            # İstifadəçi yaratma xətası:
            print(f"İstifadəçi yaratma xətası: {e}")
            return False
    
    def delete_user(self, user_id):
        """İstifadəçini silir"""
        query = """
        DELETE FROM users
        WHERE id = %s
        """
        return self.execute_query(query, (user_id,), commit=True)
    
    def make_user_pro(self, user_id, duration=30):
        """İstifadəçini pro edir"""
        query = """
        UPDATE users
        SET license_status = 'pro',
            pro_expiry = DATE_ADD(NOW(), INTERVAL %s DAY)
        WHERE id = %s
        """
        return self.execute_query(query, (duration, user_id), commit=True)
        

    def get_version(self):
        """Verilənlər bazasından mövcud versiyanı al"""
        try:
            self.connect()
            
            # Versiya cədvəlini yarat (əgər yoxdursa)
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS version (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    version VARCHAR(10) NOT NULL,
                    web_url VARCHAR(255),
                    google_drive_id VARCHAR(255),
                    info TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            ''')
            
            # Versiya məlumatını al (created_at daxil)
            self.cursor.execute('SELECT version, web_url, google_drive_id, info, created_at FROM version ORDER BY id DESC LIMIT 1')
            result = self.cursor.fetchone()
            
            if result:
                return result
            else:
                # Varsayılan versiyanı əlavə et
                default_version = "Xəta"
                self.cursor.execute('INSERT INTO version (version, web_url, google_drive_id, info) VALUES (%s, %s, %s, %s)', 
                                  (default_version, 'https://github.com/QadirAbbasov/Azer-AI', '10itm_jMGqRTuX_YYbA1Ekk0ES3r5vIzy', 'Yeni versiyada aşağıdakı yeniliklər var:\n- Performans yaxşılaşdırmaları\n- Yeni xüsusiyyətlər\n- Xətaların düzəldilməsi\n- NLP dual dil işləmə sistemi'))
                self.conn.commit()
                return {'version': default_version, 'web_url': 'https://github.com/QadirAbbasov/Azer-AI', 'google_drive_id': '10itm_jMGqRTuX_YYbA1Ekk0ES3r5vIzy', 'info': 'Yeni versiyada aşağıdakı yeniliklər var:\n- Performans yaxşılaşdırmaları\n- Yeni xüsusiyyətlər\n- Xətaların düzəldilməsi', 'created_at': '2024-01-01 00:00:00'}
                
        except Exception as e:
            # Versiya məlumatı alınarkən xəta:
            return {'version': "Xəta", 'web_url': 'https://github.com/QadirAbbasov/Azer-AI', 'google_drive_id': '10itm_jMGqRTuX_YYbA1Ekk0ES3r5vIzy', 'info': 'Bu İlk Versiondur:\n- Azer AI\n- Səsli\n- Köməkçi', 'created_at': '2024-01-01 00:00:00'}
        finally:
            self.close()

    def update_version(self, new_version, web_url=None, google_drive_id=None, info=None, release_date=None):
        """Verilənlər bazasındakı versiyanı yenilə"""
        try:
            self.connect()
            
            # Əgər release_date verilmişsə, o tarixi istifadə et, yoxdursa indiki tarixi istifadə et
            if release_date:
                # Tarix formatını yoxla və MySQL formatına çevir
                try:
                    from datetime import datetime
                    parsed_date = datetime.strptime(release_date, '%Y-%m-%d')
                    mysql_date = parsed_date.strftime('%Y-%m-%d %H:%M:%S')
                except:
                    mysql_date = None
            else:
                mysql_date = None
            
            if mysql_date:
                # Xüsusi tarix ilə əlavə et
                self.cursor.execute('INSERT INTO version (version, web_url, google_drive_id, info, created_at) VALUES (%s, %s, %s, %s, %s)', 
                                  (new_version, web_url or 'https://github.com/QadirAbbasov/Azer-AI', google_drive_id or '10itm_jMGqRTuX_YYbA1Ekk0ES3r5vIzy', info or 'Yeni versiyada aşağıdakı yeniliklər var:\n- Performans yaxşılaşdırmaları\n- Yeni xüsusiyyətlər\n- Xətaların düzəldilməsi', mysql_date))
            else:
                # Varsayılan tarix ilə əlavə et (indiki zaman)
                self.cursor.execute('INSERT INTO version (version, web_url, google_drive_id, info) VALUES (%s, %s, %s, %s)', 
                                  (new_version, web_url or 'https://github.com/QadirAbbasov/Azer-AI', google_drive_id or '10itm_jMGqRTuX_YYbA1Ekk0ES3r5vIzy', info or 'Yeni versiyada aşağıdakı yeniliklər var:\n- Performans yaxşılaşdırmaları\n- Yeni xüsusiyyətlər\n- Xətaların düzəldilməsi'))
            
            self.conn.commit()
            return True
        except Exception as e:
            # Versiya yenilənərkən xəta:
            return False
        finally:
            self.close()

# Singleton verilənlər bazası idarəçisi
db_manager = DBManager()