# 🚀 Google Colab Kurulum Rehberi

OpenClaw + Dolphin 3'ü Google Colab'da çalıştırmak için adım adım rehber.

## 📋 Gereksinimler

- Google hesabı
- Ngrok hesabı (ücretsiz)
- 15-20 dakika

## 🎯 Adım 1: Colab Notebook'u Aç

1. Bu linke tıkla: https://colab.research.google.com/github/SuperHelix77/openclaw-dolphin3/blob/main/openclaw_colab.ipynb
2. Google hesabınla giriş yap

## ⚙️ Adım 2: GPU'yu Aktif Et

1. **Runtime** menüsüne tıkla
2. **Change runtime type** seç
3. **Hardware accelerator**: **T4 GPU** seç
4. **Save** tıkla

## 🔑 Adım 3: Ngrok Token Al

1. https://dashboard.ngrok.com/signup adresine git
2. Ücretsiz hesap oluştur
3. https://dashboard.ngrok.com/get-started/your-authtoken adresine git
4. Token'ı kopyala

## ▶️ Adım 4: Notebook'u Çalıştır

1. **Runtime → Run all** tıkla
2. Her hücre sırayla çalışacak
3. Ngrok token istendiğinde yapıştır
4. **Enter** bas

## ⏳ Adım 5: Bekle

- Paket kurulumu: 2-3 dakika
- Model indirmesi: 10-15 dakika
- Sunucu başlatma: 2-3 dakika
- **TOPLAM**: ~15-20 dakika

## 🌍 Adım 6: Public URL'yi Kopyala

Notebook'ta şöyle bir çıktı göreceksin:

```
======================================================================
✅ BAŞARILI! Sunucu hazır.
======================================================================

🌍 Public URL: https://xxxx-xx-xxx-xxx-xxx.ngrok-free.app

📝 Bu URL'yi tarayıcıda aç ve kullan!
======================================================================
```

Bu URL'yi kopyala!

## 🎨 Adım 7: Web Arayüzünü Kullan

1. Public URL'yi yeni bir tarayıcı sekmesinde aç
2. Web GUI açılacak
3. Chat et! 🎉

## 📱 OpenClaw Config (İsteğe Bağlı)

Yerel makinende OpenClaw kullanmak için:

`~/.openclaw/config.yaml`:

```yaml
models:
  default:
    provider: openai
    model: dolphin-2.9-llama3.1-8b
    credentials:
      apiKey: 'ollama'
      apiBase: 'YOUR_PUBLIC_URL_HERE'
```

Sonra:

```bash
openclaw gateway --port 18789 --verbose
```

Başka terminalde:

```bash
openclaw agent --message 'Merhaba!'
```

## ⚠️ Önemli Notlar

### ✅ Avantajlar
- Tamamen ücretsiz
- GPU desteği
- Kolay kurulum
- Web GUI

### ⚠️ Dezavantajlar
- 12 saat sonra kapanır
- Colab sekmesini açık tutmalısın
- GPU kullanımı sınırlı

### 💡 İpuçları

1. **Colab sekmesini AÇIK TUT** - Kapanırsa sunucu durur
2. **12 saat sonra yeniden başlat** - Otomatik kapanır
3. **Ngrok URL değişir** - Her başlatmada yeni URL
4. **Model cache'lenir** - İkinci çalıştırma daha hızlı

## 🐛 Sorun Giderme

### Model yüklenmiyor
- GPU seçili mi kontrol et
- Runtime'ı yeniden başlat

### Ngrok hatası
- Token'ı doğru kopyaladın mı?
- Ngrok hesabı aktif mi?

### Sunucu yanıt vermiyor
- 15-20 dakika bekle
- Logs'u kontrol et

## 🎉 Başarılar!

Artık tamamen ücretsiz, sansürsüz bir AI sunucun var! 🚀
