# OpenClaw + Dolphin 3

Sansürsüz AI Sunucusu - Railway.app'da 7/24 Çalışır

## 🎨 Web GUI

Sunucuya erişim sağlandığında, tarayıcıda açarak web arayüzünü kullanabilirsiniz:

```
https://your-railway-app.railway.app
```

### GUI Özellikleri

- 💬 **Chat Interface** - Sohbet et ve cevap al
- ⚙️ **Ayarlar** - Temperature ve Max Token ayarla
- 📊 **İstatistikler** - Mesaj sayısı ve oturum süresi
- 🎨 **Modern Tasarım** - Tailwind CSS ile profesyonel görünüm
- 📱 **Responsive** - Mobil ve desktop uyumlu

## 🚀 Özellikler

- ✅ Tamamen sansürsüz Dolphin 3 modeli
- ✅ 7/24 çalışır
- ✅ OpenAI API uyumlu
- ✅ Web GUI ile kolay kullanım
- ✅ Ücretsiz
- ✅ Otomatik ölçeklendirme

## 📡 API Endpoints

### Web GUI
```
GET / - Web arayüzü
```

### Chat API
```bash
POST /api/chat
Content-Type: application/json

{
  "message": "Merhaba!",
  "temperature": 0.7,
  "max_tokens": 512
}
```

### Text Completion (OpenAI uyumlu)
```bash
curl -X POST https://your-app.railway.app/v1/completions \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Merhaba, nasılsın?",
    "max_tokens": 100
  }'
```

### Chat Completion (OpenAI uyumlu)
```bash
curl -X POST https://your-app.railway.app/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"role": "user", "content": "Merhaba!"}
    ],
    "max_tokens": 100
  }'
```

### List Models
```bash
curl https://your-app.railway.app/v1/models
```

### Health Check
```bash
curl https://your-app.railway.app/health
```

### API Status
```bash
curl https://your-app.railway.app/api/status
```

## 🔧 OpenClaw Yapılandırması

`~/.openclaw/config.yaml`:

```yaml
models:
  default:
    provider: openai
    model: dolphin-2.9-llama3.1-8b
    credentials:
      apiKey: 'ollama'
      apiBase: 'https://your-railway-app.railway.app'
```

## 💻 Yerel Kullanım

### OpenClaw Gateway
```bash
openclaw gateway --port 18789 --verbose
```

### OpenClaw Agent
```bash
openclaw agent --message 'Merhaba! Kimsin?'
```

## 📊 Model Bilgileri

- **Model**: Dolphin 3 (Llama 3.1 8B)
- **Parametreler**: 8 Milyar
- **Bellek**: ~4.5GB
- **Sansürsüz**: Evet ✅
- **Hız**: Orta (GPU'ya bağlı)

## 🌐 Deployment

### Railway.app'da Deploy

1. GitHub'da repo oluştur
2. Railway dashboard'da "Create New Project"
3. "Deploy from GitHub repo" seç
4. Repository'yi seç
5. Deploy'ı tıkla

### Bekleme Süresi

- **Build**: 10-15 dakika
- **Model indirmesi**: 10-15 dakika
- **Başlama**: 2-3 dakika
- **TOPLAM**: ~25-30 dakika

## 🐛 Sorun Giderme

### Sunucu yanıt vermiyor
- Railway dashboard'da logs'u kontrol et
- Model yüklenmesi 15-20 dakika sürebilir

### GUI açılmıyor
- Tarayıcı cache'ini temizle
- URL'nin sonunda `/` olduğundan emin ol

### API hatası alıyorum
- Railway logs'unda hata mesajını oku
- Dockerfile'ı kontrol et

## 📝 Teknoloji Stack

- **Backend**: Flask (Python)
- **LLM**: vLLM + Dolphin 3
- **Frontend**: HTML5 + Tailwind CSS + Vanilla JavaScript
- **Deployment**: Railway.app
- **Container**: Docker + CUDA

## 📄 Lisans

MIT License - Özgürce kullan ve değiştir

## 🙏 Teşekkürler

- OpenClaw - Açık kaynak AI framework
- Dolphin 3 - Sansürsüz LLM modeli
- Railway.app - Ücretsiz deployment
- vLLM - Hızlı LLM inference

---

**Yapımcı**: SuperHelix77
**Son Güncelleme**: 2026-02-05
