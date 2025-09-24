import datetime

class DateManager:
    def __init__(self, Azer_AI):
        self.Azer_AI = Azer_AI

        # Azərbaycan və Türk dili ayları
        self.months = {
            'az-AZ': {
                1: "Yanvar", 2: "Fevral", 3: "Mart", 4: "Aprel", 5: "May", 6: "İyun",
                7: "İyul", 8: "Avqust", 9: "Sentyabr", 10: "Oktyabr", 11: "Noyabr", 12: "Dekabr"
            },
            'tr-TR': {
                1: "Ocak", 2: "Şubat", 3: "Mart", 4: "Nisan", 5: "Mayıs", 6: "Haziran",
                7: "Temmuz", 8: "Ağustos", 9: "Eylül", 10: "Ekim", 11: "Kasım", 12: "Aralık"
            }
        }

        # Xüsusi günlər
        self.special_days = {
            'az-AZ': {
                # Yanvar ayı xüsusi günləri
                (1, 1): "Yeni İl Bayramı",
                (1, 2): "Dünya İntrovertlər Günü",
                (1, 3): "Beynəlxalq Ağıl-Bədən Sağlamlığı Günü",
                (1, 4): "Dünya Brayl Şrifti Günü",
                (1, 5): "Ümumdünya Köçəri Quşlar Günü",
                (1, 8): "Ümumdünya Yazma Günü",
                (1, 14): "Dünya Məntiq Günü",
                (1, 16): "Beynəlxalq İsti və Ədviyyatlı Yeməklər Günü",
                (1, 20): "Ümumxalq Hüzn Günü",
                (1, 21): "Qucaqlaşma Günü",
                (1, 24): "Beynəlxalq Təhsil Günü",
                (1, 26): "Beynəlxalq Təmiz Enerji Günü",
                (1, 28): ["Məlumat Məxfiliyi Günü", "Beynəlxalq Lego Günü"],
                (1, 30): "Gömrük İşçiləri Günü",
                
                # Fevral ayı xüsusi günləri
                (2, 2): "Azərbaycan Gəncləri Günü",
                (2, 4): "Ümumdünya Xərçənglə Mübarizə Günü",
                (2, 11): ["Vergi Xidməti İşçilərinin Peşə Bayramı", "Təhlükəsiz İnternet Günü", "Beynəlxalq Qadın və Qızların Elmdə İştırakı Günü"],
                (2, 13): "Ümumdünya Radio Günü",
                (2, 14): ["Hərbi Hava Qüvvələri Günü", "Sevgililər Günü"],
                (2, 16): "Dünya Balina Günü",
                (2, 17): "Qlobal Turizm Dayanıqlığı Günü",
                (2, 21): "Beynəlxalq Ana Dili Günü",
                (2, 22): ["Avtomobil Yol İşçilərinin Peşə Bayramı Günü", "Dünya Düşüncə Günü"],
                (2, 25): "Su Çərşənbəsi",
                (2, 26): "Xocalı Soyqırımı Günü",
                (2, 27): "Ümumdünya QHT Günü",
                
                # Mart ayı xüsusi günləri
                (3, 1): ["Beynəlxalq Sıfır Diskriminasiya Günü", "Ümumdünya Kompliment Günü"],
                (3, 3): "Ümumdünya Vəhşi Təbiət Günü",
                (3, 4): "Od Çərşənbəsi",
                (3, 5): "Bədən Tərbiyəsi və İdman Günü",
                (3, 8): "Beynəlxalq Qadınlar Günü",
                (3, 10): ["Qızıl Aypara Günü", "Azərbaycan Milli Teatr Günü", "Beynəlxalq Möhtəşəmlik Günü"],
                (3, 11): "Yel Çərşənbəsi",
                (3, 12): "Daxili Qoşunlar Günü",
                (3, 14): "Ümumdünya Yuxu Günü",
                (3, 15): "Ümumdünya İstehlakçı Hüquqları Günü",
                (3, 18): ["Torpaq Çərşənbəsi", "Ümumdünya Təkrar Emal Günü"],
                (3, 19): "Miqrasiya Orqanları İşçilərinin Peşə Bayramı Günü",
                (3, 20): "Beynəlxalq Xoşbəxtlik Günü",
                (3, 20, 21): "Novruz Bayramı",
                (3, 21): ["Dünya Poeziya Günü", "Beynəlxalq Daun Sindromu Günü"],
                (3, 22): ["Ümumdünya Su Günü", "Yer Saatı Günü"],
                (3, 23): "Ümumdünya Meteorologiya Günü",
                (3, 24): "Ümumdünya Vərəmlə Mübarizə Günü",
                (3, 25): "Beynəlxalq Vəfli Günü",
                (3, 27): ["Elm Günü", "Ümumdünya Teatr Günü"],
                (3, 28): "Milli Təhlükəsizlik Orqanları İşçilərinin Peşə Bayramı",
                (3, 30): "Beynəlxalq Sıfır Tullantı Günü",
                (3, 31): ["Azərbaycanlıların Soyqırımı Günü", "Ramazan Bayramı"],
                
                # Aprel ayı xüsusi günləri
                (4, 1): "Ümumdünya Gülüş Günü",
                (4, 2): "Ümumdünya Autizm Haqqında Maariflendirmə Günü",
                (4, 3): "Ümumdünya Parti Günü",
                (4, 6): "İnkişaf və Sülh Naminə Beynəlxalq İdman Günü",
                (4, 7): "Ümumdünya Sağlamlıq Günü",
                (4, 10): "İnşaatçılar Günü",
                (4, 12): "Dünya Aviasiya və Kosmonavtika Günü",
                (4, 15): "Dünya İncəsənət Günü",
                (4, 18): "Tarixi Abidələrin Mühafizəsi Günü",
                (4, 21): "Ümumdünya Yaradıcılıq və İnnovasiya Günü",
                (4, 22): "Beynəlxalq Yer Kürəsi Günü",
                (4, 23): "Dünya Kitab Günü",
                (4, 26): "Ümumdünya Əqli Mülkiyyət Günü",
                (4, 27): "Beynəlxalq Dizayn Günü",
                (4, 28): "Ümumdünya Əməyin Mühafizəsi Günü",
                (4, 29): ["Beynəlxalq Rəqs Günü", "Ümumdünya Arzu Günü"],
                (4, 30): "Beynəlxalq Caz Günü",
                
                # May ayı xüsusi günləri
                (5, 1): ["Beynəlxalq Əmək Günü", "Ümumdünya Şifrə Günü"],
                (5, 3): "Ümumdünya Mətbuat Azadlığı Günü",
                (5, 8): "Ümumdünya Qızıl Xaç və Qızıl Aypara Hərəkatı Günü",
                (5, 9): "Faşizm Üzərində Qələbə Günü",
                (5, 10): "Ulu Öndər Heydər Əliyevin Doğum Günü",
                (5, 12): "Ümumdünya Tibb Bacısı Günü",
                (5, 15): "Beynəlxalq Ailə Günü",
                (5, 16): ["Beynəlxalq Sülh İçində Birgə Yaşayış Günü", "Beynəlxalq İşıq Günü"],
                (5, 18): "Beynəlxalq Muzeylər Günü",
                (5, 20): "Ümumdünya Arı Günü",
                (5, 21): "Beynəlxalq Çay Günü",
                (5, 23): "Ekologiya və Təbii Sərvətlər Nazirliyi İşçilərinin Peşə Bayramı",
                (5, 25): "Dünya Futbol Günü",
                (5, 27): "Dünya Marketing Günü",
                (5, 28): ["Müstəqillik Günü", "Burger Günü"],
                (5, 31): "Ümumdünya Tütünlə Mübarizə Günü",
                
                # İyun ayı xüsusi günləri
                (6, 1): "Uşaqların Beynəlxalq Müdafiəsi Günü",
                (6, 2): "Mülki Aviasiya İşçilərinin Peşə Bayramı Günü",
                (6, 3): "Ümumdünya Velosiped Günü",
                (6, 5): ["Su Təsərrüfatı və Meliorasiya İşçiləri Günü", "Ümumdünya Ətraf Mühit Günü"],
                (6, 6, 7): "Qurban Bayramı",
                (6, 7): "Ümumdünya Qida Təhlükəsizliyi Günü",
                (6, 8): "Ümumdünya Okeanlar Günü",
                (6, 12): "Ümumdünya Uşaq Əməyinə Qarşı Mübarizə Günü",
                (6, 14): "Ümumdünya Qan Donorları Günü",
                (6, 15): ["Milli Qurtuluş Günü", "Atalar Günü"],
                (6, 17): "Azərbaycan Respublikası Tibb İşçilərinin Peşə Bayramı Günü",
                (6, 18): ["Beynəlxalq Süşi Günü", "İnsan Hüquqları Günü"],
                (6, 20): "Qaz Təsərrüfatı İşçilərinin Peşə Bayramı Günü",
                (6, 21): ["Beynəlxalq Yoqa Günü", "Dünya Musiqi Günü"],
                (6, 23): "Dövlət Qulluqçularının Peşə Bayramı Günü",
                (6, 24): ["Maşınqayırma Sənayesi İşçiləri Günü", "Diplomatiyada Qadınların Beynəlxalq Günü"],
                (6, 25): "Dənizçilərin Peşə Bayramı",
                (6, 26): ["Azərbaycan Respublikası Silahlı Qüvvələri Günü", "Narkomaniyaya və Narkobiznese Qarşı Beynəlxalq Mübarizə Günü"],
                (6, 27): "Mikro, Kiçik və Orta Müəssisələr Günü",
                (6, 30): "Ümumdünya Sosial Media Günü",
                
                # İyul ayı xüsusi günləri
                (7, 1): "Beynəlxalq Zarafat Günü",
                (7, 2): ["Azərbaycan Polisi Günü", "Ümumdünya UNO Günü"],
                (7, 5): "Beynəlxalq Kooperativlər Günü",
                (7, 6): "Ümumdünya Öpüş Günü",
                (7, 7): "Ümumdünya Şokolad Günü",
                (7, 9): "Diplomatik Xidmət Orqanları Əməkdaşlarının Peşə Bayramı Günü",
                (7, 11): "Ümumdünya Əhali Günü",
                (7, 15): "Ümumdünya Gənclərin Bacarıqları Günü",
                (7, 17): "Dünya Emoji Günü",
                (7, 18): "Ümumdünya Dinləmə Günü",
                (7, 20): "Beynəlxalq Şahmat Günü",
                (7, 22): ["Milli Mətbuat və Jurnalistika Günü", "Ümumdünya Beyin Günü"],
                (7, 30): "Beynəlxalq Dostluq Günü",
                
                # Avqust ayı xüsusi günləri
                (8, 1): ["Azərbaycan Əlifbası və Azərbaycan Dili Günü", "Beynəlxalq Pivə Günü"],
                (8, 2): "Azərbaycan Kinosu Günü",
                (8, 5): "Hərbi Donanma Günü",
                (8, 8): "Beynəlxalq Pişiklər Günü",
                (8, 12): ["Beynəlxalq Gənclər Günü", "Dünya Fil Günü"],
                (8, 13): "Ümumdünya Solaxaylar Günü",
                (8, 18): "Sərhəd Qoşunları Əməkdaşlarının Peşə Bayramı Günü",
                (8, 19): ["Ümumdünya Fotoqrafiya Günü", "Ümumdünya Humanitar Yardım Günü"],
                (8, 23): ["Azərbaycan Respublikası Prezidentinin Təhlükəsizlik Xidmətinin Peşə Bayramı Günü", "Həştəg Günü (Hashtag)"],
                (8, 26): ["Azərbaycan Respublikasının Birinci Vitse-Prezidenti Mehriban Əliyevanın Doğum Günü", "Beynəlxalq İtlər Günü"],
                
                # Sentyabr ayı xüsusi günləri
                (9, 1): "Ümumdünya Məktub Yazma Günü",
                (9, 5): "Beynəlxalq Xeyriyyəçilik Günü",
                (9, 7): "Mavi Səma üçün Təmiz Hava Günü",
                (9, 8): "Beynəlxalq Savadlılıq Günü",
                (9, 15): "Bilik Günü",
                (9, 16): "Beynəlxalq Ozon Qatının Mühafizəsi Günü",
                (9, 18): "Milli Musiqi Günü (Üzeyir Hacıbəyovun Doğum Günü)",
                (9, 20): ["Neftçilər Günü", "Ümumdünya Təmizlik Günü"],
                (9, 21): "Beynəlxalq Sülh Günü",
                (9, 23): "Beynəlxalq İşarə Dilləri Günü",
                (9, 26): "Ümumdünya Dənizçilik Günü",
                (9, 27): ["Anım Günü", "Dünya Turizm Günü"],
                (9, 29): "Turizm İşçiləri Günü",
                (9, 30): ["Beynəlxalq Tərcümə Günü", "Beynəlxalq Podkast Günü"],
                
                # Oktyabr ayı xüsusi günləri
                (10, 1): ["Prokurorluq İşçiləri Günü", "Beynəlxalq Ahıllar Günü", "Ümumdünya Vegetarian Günü", "Beynəlxalq Qəhvə Günü"],
                (10, 2): "Ümumdünya Zorakılığa Qarşı Mübarizə Günü",
                (10, 3): "Ümumdünya Təbəssüm Günü",
                (10, 4): "Ümumdünya Heyvanlar Günü",
                (10, 5): "Beynəlxalq Müəllimlər Günü",
                (10, 7): "Dünya Pambıq Günü",
                (10, 9): "Ümumdünya Görmə Günü",
                (10, 10): ["Yangınsöndürənlərin Peşə Bayramı Günü", "Ümumdünya Psixi Sağlamlıq Günü"],
                (10, 11): "Beynəlxalq Qız Uşaqları Günü",
                (10, 13): "Dəmir Yolu İşçilərinin Peşə Bayramı Günü",
                (10, 15): "Ümumdünya Əl Yuma Günü",
                (10, 16): "Ümumdünya Qida Günü",
                (10, 18): "Müstəqilliyin Bərpası Günü",
                (10, 20): ["Energetiklər Günü", "Ümumdünya Statistika Günü", "Beynəlxalq Aşpazlar Günü"],
                (10, 28): "Dünya Animasiya Günü",
                (10, 29): "Beynəlxalq Qayğı və Dəstək Günü",
                (10, 31): ["Dünya Şəhərlər Günü", "Halloween"],
                
                # Noyabr ayı xüsusi günləri
                (11, 1): ["Kənd Təsərrüfatı İşçiləri Günü", "Ümumdünya Vegan Günü"],
                (11, 6): "Azərbaycan Televiziyası və Radiosu Günü",
                (11, 8): ["Bakı Metropoliteni İşçilərinin Peşə Bayramı Günü", "Zəfər Günü"],
                (11, 9): "Dövlət Bayrağı Günü",
                (11, 10): "Sülh və İnkişaf Naminə Dünya Elm Günü",
                (11, 12): "Konstitusiya Günü",
                (11, 13): "Ümumdünya Xeyirxahlıq Günü",
                (11, 14): "Ümumdünya Diabetlə Mübarizə Günü",
                (11, 16): "Beynəlxalq Tolerantlıq Günü",
                (11, 17): "Milli Dirçəliş Günü",
                (11, 20): ["Ümumdünya Uşaqlar Günü", "Beynəlxalq Fəlsəfə Günü"],
                (11, 21): ["Ümumdünya Salam Günü", "Ümumdünya Televiziya Günü"],
                (11, 22): "Ədliyyə İşçilərinin Peşə Bayramı Günü",
                (11, 25): "Qadın Zorakılığına Qarşı Mübarizə Günü",
                (11, 26): "Ümumdünya Dayanıqlı Nəqliyyat Günü",
                (11, 28): "Möhtəşəm Cümə (Black Friday)",
                
                # Dekabr ayı xüsusi günləri
                (12, 1): ["QİÇS'ə Qarşı Beynəlxalq Mübarizə Günü", "Kiber Bazar Ertəsi"],
                (12, 3): "Beynəlxalq Əlilliyi Olan Şəxslər Günü",
                (12, 4): "Beynəlxalq Banklar Günü",
                (12, 5): ["Dünya Torpaq Günü", "Beynəlxalq Könüllülər Günü"],
                (12, 6): "Rabitə və İnformasiya Texnologiyaları Sahəsi İşçilərinin Peşə Bayramı Günü",
                (12, 7): "Beynəlxalq Mülki Aviasiya Günü",
                (12, 10): "Ümumdünya İnsan Hüquqları Günü",
                (12, 11): "Beynəlxalq Dağlar Günü",
                (12, 12): "Ümummilli Lider Heydər Əliyevin Anım Günü",
                (12, 16): "Fövqəladə Hallar Nazirliyi İşçilərinin Peşə Bayramı Günü",
                (12, 17): "Müdafiə Sənayesi Nazirliyi İşçilərinin Peşə Bayramı Günü",
                (12, 20): "Beynəlxalq İnsan Həmrəyliyi Günü",
                (12, 21): ["Ümumdünya Meditasiya Günü", "Dünya Basketbol Günü"],
                (12, 24): "Azərbaycan Respublikasının Prezidenti İlham Əliyevin Doğum Günü",
                (12, 25): "Milad Günü (Christmas)",
                (12, 28): "\"Vəkil Günü\" Peşə Bayramı",
                (12, 29): "\"Asan Xidmət\" İşçilərinin Peşə Bayramı Günü",
                (12, 31): "Dünya Azərbaycanlılarının Həmrəyliyi Günü"
            },
            'tr-TR': {
                # Ocak ayı xüsusi günləri
                (1, 1): "Yeni Yıl Bayramı",
                (1, 2): "Dünya İçe Dönükler Günü",
                (1, 3): "Uluslararası Zihin-Beden Sağlığı Günü",
                (1, 4): "Dünya Braille Yazı Sistemi Günü",
                (1, 5): "Dünya Göçmen Kuşlar Günü",
                (1, 8): "Dünya Yazma Günü",
                (1, 14): "Dünya Mantık Günü",
                (1, 16): "Uluslararası Sıcak ve Baharatlı Yemekler Günü",
                (1, 20): "Genel Yas Günü",
                (1, 21): "Sarılma Günü",
                (1, 24): "Uluslararası Eğitim Günü",
                (1, 26): "Uluslararası Temiz Enerji Günü",
                (1, 28): ["Veri Gizliliği Günü", "Uluslararası Lego Günü"],
                (1, 30): "Gümrük Çalışanları Günü",
                
                # Şubat ayı xüsusi günləri
                (2, 2): "Azerbaycan Gençlik Günü",
                (2, 4): "Dünya Kanserle Mücadele Günü",
                (2, 11): ["Vergi Çalışanları Günü", "Güvenli İnternet Günü", "Uluslararası Bilimde Kadın ve Kız Çocukları Günü"],
                (2, 13): "Dünya Radyo Günü",
                (2, 14): ["Hava Kuvvetleri Günü", "Sevgililer Günü"],
                (2, 16): "Dünya Balina Günü",
                (2, 17): "Küresel Turizm Sürdürülebilirliği Günü",
                (2, 21): "Uluslararası Anadil Günü",
                (2, 22): ["Karayolu Çalışanları Günü", "Dünya Düşünce Günü"],
                (2, 25): "Su Çarşambası",
                (2, 26): "Hocalı Soykırımı Günü",
                (2, 27): "Dünya STK Günü",
                
                # Mart ayı xüsusi günləri
                (3, 1): ["Uluslararası Sıfır Ayrımcılık Günü", "Dünya Kompliment Günü"],
                (3, 3): "Dünya Yaban Hayatı Günü",
                (3, 4): "Ateş Çarşambası",
                (3, 5): "Beden Eğitimi ve Spor Günü",
                (3, 8): "Dünya Kadınlar Günü",
                (3, 10): ["Kızılay Günü", "Azerbaycan Milli Tiyatro Günü", "Uluslararası Muhteşemlik Günü"],
                (3, 11): "Yel Çarşambası",
                (3, 12): "İç Kuvvetler Günü",
                (3, 14): "Dünya Uyku Günü",
                (3, 15): "Dünya Tüketici Hakları Günü",
                (3, 18): ["Toprak Çarşambası", "Dünya Geri Dönüşüm Günü"],
                (3, 19): "Göç İdaresi Çalışanları Günü",
                (3, 20): "Uluslararası Mutluluk Günü",
                (3, 20, 21): "Nevruz Bayramı",
                (3, 21): ["Dünya Şiir Günü", "Uluslararası Down Sendromu Günü"],
                (3, 22): ["Dünya Su Günü", "Dünya Saati"],
                (3, 23): "Dünya Meteoroloji Günü",
                (3, 24): "Dünya Tüberkülozla Mücadele Günü",
                (3, 25): "Uluslararası Waffle Günü",
                (3, 27): ["Bilim Günü", "Dünya Tiyatro Günü"],
                (3, 28): "Milli Güvenlik Teşkilatı Çalışanları Günü",
                (3, 30): "Uluslararası Sıfır Atık Günü",
                (3, 31): ["Azerbaycanlıların Soykırımı Günü", "Ramazan Bayramı"],
                
                # Nisan ayı xüsusi günləri
                (4, 1): "Dünya Gülümseme Günü",
                (4, 2): "Dünya Otizm Farkındalık Günü",
                (4, 3): "Dünya Parti Günü",
                (4, 6): "Kalkınma ve Barış için Uluslararası Spor Günü",
                (4, 7): "Dünya Sağlık Günü",
                (4, 10): "İnşaatçılar Günü",
                (4, 12): "Dünya Havacılık ve Uzay Günü",
                (4, 15): "Dünya Sanat Günü",
                (4, 18): "Tarihi Anıtları Koruma Günü",
                (4, 21): "Dünya Yaratıcılık ve İnovasyon Günü",
                (4, 22): "Uluslararası Dünya Günü",
                (4, 23): "Dünya Kitap Günü",
                (4, 26): "Dünya Fikri Mülkiyet Günü",
                (4, 27): "Uluslararası Tasarım Günü",
                (4, 28): "Dünya İş Sağlığı ve Güvenliği Günü",
                (4, 29): ["Uluslararası Dans Günü", "Dünya Dilek Günü"],
                (4, 30): "Uluslararası Caz Günü",
                
                # Mayıs ayı xüsusi günləri
                (5, 1): ["Uluslararası İşçi Bayramı", "Dünya Şifre Günü"],
                (5, 3): "Dünya Basın Özgürlüğü Günü",
                (5, 8): "Dünya Kızılhaç ve Kızılay Hareketi Günü",
                (5, 9): "Faşizm Üzerinde Zafer Günü",
                (5, 10): "Ulu Önder Haydar Aliyev'in Doğum Günü",
                (5, 12): "Dünya Hemşireler Günü",
                (5, 15): "Uluslararası Aile Günü",
                (5, 16): ["Uluslararası Barış İçinde Birlikte Yaşama Günü", "Uluslararası Işık Günü"],
                (5, 18): "Uluslararası Müzeler Günü",
                (5, 20): "Dünya Arı Günü",
                (5, 21): "Uluslararası Çay Günü",
                (5, 23): "Ekoloji ve Doğal Kaynaklar Bakanlığı Çalışanları Günü",
                (5, 25): "Dünya Futbol Günü",
                (5, 27): "Dünya Pazarlama Günü",
                (5, 28): ["Bağımsızlık Günü", "Hamburger Günü"],
                (5, 31): "Dünya Tütünsüz Günü",
                
                # Haziran ayı xüsusi günləri
                (6, 1): "Uluslararası Çocukları Koruma Günü",
                (6, 2): "Sivil Havacılık Çalışanları Günü",
                (6, 3): "Dünya Bisiklet Günü",
                (6, 5): ["Su ve Sulama İşçileri Günü", "Dünya Çevre Günü"],
                (6, 6, 7): "Kurban Bayramı",
                (6, 7): "Dünya Gıda Güvenliği Günü",
                (6, 8): "Dünya Okyanuslar Günü",
                (6, 12): "Dünya Çocuk İşçiliği ile Mücadele Günü",
                (6, 14): "Dünya Kan Bağışçıları Günü",
                (6, 15): ["Milli Kurtuluş Günü", "Babalar Günü"],
                (6, 17): "Azerbaycan Cumhuriyeti Sağlık Çalışanları Günü",
                (6, 18): ["Uluslararası Suşi Günü", "İnsan Hakları Günü"],
                (6, 20): "Doğalgaz Çalışanları Günü",
                (6, 21): ["Uluslararası Yoga Günü", "Dünya Müzik Günü"],
                (6, 23): "Devlet Memurları Günü",
                (6, 24): ["Makine Sanayi İşçileri Günü", "Diplomaside Kadınlar Günü"],
                (6, 25): "Denizciler Günü",
                (6, 26): ["Azerbaycan Cumhuriyeti Silahlı Kuvvetler Günü", "Uyuşturucu Kullanımı ve Kaçakçılığı ile Mücadele Günü"],
                (6, 27): "Mikro, Küçük ve Orta Ölçekli İşletmeler Günü",
                (6, 30): "Dünya Sosyal Medya Günü",
                
                # Temmuz ayı xüsusi günləri
                (7, 1): "Uluslararası Şaka Günü",
                (7, 2): ["Azerbaycan Polis Günü", "Dünya UFO Günü"],
                (7, 5): "Uluslararası Kooperatifler Günü",
                (7, 6): "Dünya Öpücük Günü",
                (7, 7): "Dünya Çikolata Günü",
                (7, 9): "Diplomatik Hizmet Çalışanları Günü",
                (7, 11): "Dünya Nüfus Günü",
                (7, 15): "Dünya Gençlik Becerileri Günü",
                (7, 17): "Dünya Emoji Günü",
                (7, 18): "Dünya Dinleme Günü",
                (7, 20): "Uluslararası Satranç Günü",
                (7, 22): ["Milli Basın ve Gazetecilik Günü", "Dünya Beyin Günü"],
                (7, 30): "Uluslararası Dostluk Günü",
                
                # Ağustos ayı xüsusi günləri
                (8, 1): ["Azerbaycan Alfabesi ve Azerbaycan Dili Günü", "Uluslararası Bira Günü"],
                (8, 2): "Azerbaycan Sineması Günü",
                (8, 5): "Deniz Kuvvetleri Günü",
                (8, 8): "Uluslararası Kediler Günü",
                (8, 12): ["Uluslararası Gençlik Günü", "Dünya Fil Günü"],
                (8, 13): "Dünya Solaklar Günü",
                (8, 18): "Sınır Muhafızları Günü",
                (8, 19): ["Dünya Fotoğrafçılık Günü", "Dünya İnsani Yardım Günü"],
                (8, 23): ["Azerbaycan Cumhuriyeti Cumhurbaşkanlığı Koruma Servisi Günü", "Hashtag Günü"],
                (8, 26): ["Azerbaycan Cumhuriyeti Birinci Başkan Yardımcısı Mehriban Aliyeva'nın Doğum Günü", "Uluslararası Köpekler Günü"],
                
                # Eylül ayı xüsusi günləri
                (9, 1): "Dünya Mektup Yazma Günü",
                (9, 5): "Uluslararası Hayırseverlik Günü",
                (9, 7): "Mavi Gökyüzü için Temiz Hava Günü",
                (9, 8): "Uluslararası Okur Yazarlık Günü",
                (9, 15): "Bilim Günü",
                (9, 16): "Uluslararası Ozon Tabakasının Korunması Günü",
                (9, 18): "Milli Müzik Günü (Üzeyir Hacıbeyli'nin Doğum Günü)",
                (9, 20): ["Petrol İşçileri Günü", "Dünya Temizlik Günü"],
                (9, 21): "Uluslararası Barış Günü",
                (9, 23): "Uluslararası İşaret Dilleri Günü",
                (9, 26): "Dünya Denizcilik Günü",
                (9, 27): ["Anma Günü", "Dünya Turizm Günü"],
                (9, 29): "Turizm Çalışanları Günü",
                (9, 30): ["Uluslararası Çevirmenler Günü", "Uluslararası Podcast Günü"],
                
                # Ekim ayı xüsusi günləri
                (10, 1): ["Savcılık Çalışanları Günü", "Uluslararası Yaşlılar Günü", "Dünya Vejetaryenler Günü", "Uluslararası Kahve Günü"],
                (10, 2): "Dünya Şiddete Karşı Mücadele Günü",
                (10, 3): "Dünya Gülümseme Günü",
                (10, 4): "Dünya Hayvanları Koruma Günü",
                (10, 5): "Dünya Öğretmenler Günü",
                (10, 7): "Dünya Pamuk Günü",
                (10, 9): "Dünya Görme Günü",
                (10, 10): ["İtfaiyeciler Günü", "Dünya Ruh Sağlığı Günü"],
                (10, 11): "Dünya Kız Çocukları Günü",
                (10, 13): "Demiryolu Çalışanları Günü",
                (10, 15): "Dünya El Yıkama Günü",
                (10, 16): "Dünya Gıda Günü",
                (10, 18): "Bağımsızlığın Yeniden Kazanılması Günü",
                (10, 20): ["Enerji Çalışanları Günü", "Dünya İstatistik Günü", "Uluslararası Aşçılar Günü"],
                (10, 28): "Dünya Animasyon Günü",
                (10, 29): "Uluslararası Bakım ve Destek Günü",
                (10, 31): ["Dünya Şehirler Günü", "Cadılar Bayramı"],
                
                # Kasım ayı xüsusi günləri
                (11, 1): ["Tarım Çalışanları Günü", "Dünya Vegan Günü"],
                (11, 6): "Azerbaycan Televizyon ve Radyo Günü",
                (11, 8): ["Bakü Metro Çalışanları Günü", "Zafer Günü"],
                (11, 9): "Devlet Bayrağı Günü",
                (11, 10): "Barış ve Kalkınma için Dünya Bilim Günü",
                (11, 12): "Anayasa Günü",
                (11, 13): "Dünya İyilik Günü",
                (11, 14): "Dünya Diyabet Günü",
                (11, 16): "Uluslararası Hoşgörü Günü",
                (11, 17): "Milli Diriliş Günü",
                (11, 20): ["Dünya Çocuk Hakları Günü", "Uluslararası Felsefe Günü"],
                (11, 21): ["Dünya Selam Günü", "Dünya Televizyon Günü"],
                (11, 22): "Adalet Çalışanları Günü",
                (11, 25): "Kadına Yönelik Şiddete Karşı Mücadele Günü",
                (11, 26): "Dünya Sürdürülebilir Ulaşım Günü",
                (11, 28): "Muhteşem Cuma (Black Friday)",
                
                # Aralık ayı xüsusi günləri
                (12, 1): ["AIDS'e Karşı Uluslararası Mücadele Günü", "Siber Pazartesi"],
                (12, 3): "Uluslararası Engelliler Günü",
                (12, 4): "Uluslararası Bankacılık Günü",
                (12, 5): ["Dünya Toprak Günü", "Uluslararası Gönüllüler Günü"],
                (12, 6): "Haberleşme ve Bilişim Teknolojileri Çalışanları Günü",
                (12, 7): "Uluslararası Sivil Havacılık Günü",
                (12, 10): "Dünya İnsan Hakları Günü",
                (12, 11): "Uluslararası Dağlar Günü",
                (12, 12): "Ulu Önder Haydar Aliyev'in Anma Günü",
                (12, 16): "Olağanüstü Haller Bakanlığı Çalışanları Günü",
                (12, 17): "Savunma Sanayi Bakanlığı Çalışanları Günü",
                (12, 20): "Uluslararası İnsan Dayanışması Günü",
                (12, 21): ["Dünya Meditasyon Günü", "Dünya Basketbol Günü"],
                (12, 24): "Azerbaycan Cumhuriyeti Cumhurbaşkanı İlham Aliyev'in Doğum Günü",
                (12, 25): "Noel",
                (12, 28): "\"Avukatlar Günü\" Meslek Bayramı",
                (12, 29): "\"Asan Hizmet\" Çalışanları Günü",
                (12, 31): "Dünya Azerbaycanlıları Dayanışma Günü"
            }
        }
        
    def tell_date(self):
        """Tarix məlumatı"""
        current_date = datetime.datetime.now()
        current_lang = self.Azer_AI.voice_settings['language']
        
        # Dilə görə ay adını al
        month_name = self.months[current_lang][current_date.month]
        
        # Tarix sətirini yarat
        date_str = f"{current_date.day} {month_name} {current_date.year}"
        
        # Xüsusi gün yoxlaması
        special_day = self.get_special_day(current_date.month, current_date.day, current_lang)
        
        if current_lang == 'az-AZ':
            if special_day:
                if isinstance(special_day, list):
                    special_days_str = " və ".join(special_day)
                    self.Azer_AI.speak(f"Bugün {date_str}. Bu gün {special_days_str} qeyd olunur.")
                else:
                    self.Azer_AI.speak(f"Bugün {date_str}. Bu gün {special_day} qeyd olunur.")
            else:
                self.Azer_AI.speak(f"Bugün {date_str}")
        else:  # tr-TR
            if special_day:
                if isinstance(special_day, list):
                    special_days_str = " ve ".join(special_day)
                    self.Azer_AI.speak(f"Bugün {date_str}. Bugün {special_days_str} kutlanıyor.")
                else:
                    self.Azer_AI.speak(f"Bugün {date_str}. Bugün {special_day} kutlanıyor.")
            else:
                self.Azer_AI.speak(f"Bugün {date_str}")

    def get_special_day(self, month, day, language):
        """Müəyyən bir tarixdəki xüsusi günü qaytarır"""
        return self.special_days[language].get((month, day))