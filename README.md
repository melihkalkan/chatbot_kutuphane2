# Kütüphane Chatbot

Kütüphane hizmetleri ve politikaları hakkında sık sorulan sorulara hızlı erişim sağlayan PyQt5 tabanlı etkileşimli chatbot uygulaması.

## Özellikler

- Modern sohbet arayüzü
- Kategori bazlı soru-cevap sistemi
- Doğal dil işleme desteği
- Gerçek zamanlı yanıt sistemi

## Teknik Mimari

Uygulama üç ana bileşenden oluşur:

- `chatbot_window.py`: GUI ve kullanıcı etkileşimlerini yönetir
- `chatbot_logic.py`: Temel chatbot işlevselliği ve soru işleme
- `faq.json`: Kategorize edilmiş soru ve cevapları saklar

## Chatbot Mantığı

Chatbot, kullanıcı sorgularını işlemek için dizi eşleştirme algoritmaları kullanır:
- 0.6 benzerlik eşiği ile bulanık eşleştirme
- Hem doğrudan eşleşmeleri hem de benzer soru önerilerini destekler
- Hiyerarşik kategori-soru yapısı
- Kategori bilgisi ile bağlam duyarlı yanıtlar

## Kullanıcı Arayüzü

PyQt5 ile inşa edilmiş:
- Kullanıcı ve bot mesajları için farklı stiller
- Kategoriler ve sorular için dinamik buton oluşturma
- Yeni mesajlar için otomatik kaydırma
- Buton ve Enter tuşu desteği ile giriş alanı
- İçeriğe göre uyarlanan duyarlı düzen

## Kurulum

1. Gerekli bağımlılıkları yükleyin:
```bash
pip install PyQt5
```

2. Depoyu klonlayın:
```bash
git clone [repository-url]
cd library-chatbot
```

3. Uygulamayı çalıştırın:
```bash
python chatbot_window.py
```

## Kullanım

1. Uygulamayı başlatın
2. Ana menüden bir kategori seçin
3. Belirli bir soru seçin veya sorgunuzu yazın
4. Yanıtı görüntüleyin ve takip seçeneklerini kullanın
5. Farklı kategorilerde gezinin veya ek sorular sorun

## Bağımlılıklar

- Python 3.6+
- PyQt5
- json
- difflib

![image](https://github.com/user-attachments/assets/1538de33-46f7-4f96-a451-479940820ea5)
