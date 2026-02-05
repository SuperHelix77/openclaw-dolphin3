"""
OpenClaw + Dolphin 3 - Railway.app with Web GUI
7/24 çalışan sansürsüz AI sunucusu
"""

from flask import Flask, request, jsonify, render_template_string
from vllm import LLM, SamplingParams
import os
import logging
from datetime import datetime

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

print("="*70)
print("Model yükleniyor...")
print("="*70)

try:
    llm = LLM(
        model="cognitivecomputations/dolphin-2.9-llama3.1-8b",
        tensor_parallel_size=1,
        gpu_memory_utilization=0.9,
        max_model_len=8192
    )
    print("✅ Model başarıyla yüklendi!")
except Exception as e:
    print(f"❌ Model yükleme hatası: {e}")
    raise

# HTML GUI Template
GUI_TEMPLATE = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OpenClaw + Dolphin 3</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .fade-in { animation: fadeIn 0.3s ease-in; }
        .message-user { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
        .message-assistant { background: #f3f4f6; }
        .typing-indicator span {
            animation: bounce 1.4s infinite;
        }
        .typing-indicator span:nth-child(2) {
            animation-delay: 0.2s;
        }
        .typing-indicator span:nth-child(3) {
            animation-delay: 0.4s;
        }
        @keyframes bounce {
            0%, 60%, 100% { transform: translateY(0); }
            30% { transform: translateY(-10px); }
        }
    </style>
</head>
<body class="bg-gradient-to-br from-slate-900 to-slate-800">
    <div class="min-h-screen flex flex-col">
        <!-- Header -->
        <header class="bg-gradient-to-r from-purple-600 to-indigo-600 text-white shadow-lg">
            <div class="max-w-6xl mx-auto px-4 py-6">
                <div class="flex items-center justify-between">
                    <div>
                        <h1 class="text-3xl font-bold">🚀 OpenClaw + Dolphin 3</h1>
                        <p class="text-purple-100 mt-1">Sansürsüz AI Asistanı</p>
                    </div>
                    <div class="text-right">
                        <p class="text-sm text-purple-100">Model: Dolphin 3 (Llama 3.1 8B)</p>
                        <p class="text-sm text-purple-100">Status: <span class="text-green-300">🟢 Çalışıyor</span></p>
                    </div>
                </div>
            </div>
        </header>

        <!-- Main Content -->
        <main class="flex-1 max-w-6xl w-full mx-auto px-4 py-8">
            <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
                <!-- Chat Area -->
                <div class="lg:col-span-2">
                    <div class="bg-white rounded-lg shadow-xl overflow-hidden flex flex-col h-[600px]">
                        <!-- Chat Messages -->
                        <div id="chatMessages" class="flex-1 overflow-y-auto p-6 space-y-4 bg-gray-50">
                            <div class="fade-in">
                                <div class="flex justify-start">
                                    <div class="bg-gray-200 text-gray-800 rounded-lg px-4 py-3 max-w-xs">
                                        <p class="text-sm">Merhaba! Ben Dolphin 3. Sana nasıl yardımcı olabilirim?</p>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- Input Area -->
                        <div class="border-t border-gray-200 p-4 bg-white">
                            <div class="flex gap-3">
                                <input 
                                    type="text" 
                                    id="messageInput" 
                                    placeholder="Mesajını yaz..." 
                                    class="flex-1 border border-gray-300 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-purple-500"
                                    onkeypress="if(event.key==='Enter') sendMessage()"
                                >
                                <button 
                                    onclick="sendMessage()" 
                                    class="bg-gradient-to-r from-purple-600 to-indigo-600 text-white px-6 py-3 rounded-lg font-semibold hover:shadow-lg transition"
                                >
                                    Gönder
                                </button>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Sidebar -->
                <div class="space-y-6">
                    <!-- Info Card -->
                    <div class="bg-white rounded-lg shadow-xl p-6">
                        <h3 class="text-lg font-bold text-gray-800 mb-4">ℹ️ Bilgi</h3>
                        <div class="space-y-3 text-sm text-gray-600">
                            <div>
                                <p class="font-semibold text-gray-800">Model</p>
                                <p>Dolphin 3 (Llama 3.1 8B)</p>
                            </div>
                            <div>
                                <p class="font-semibold text-gray-800">Özellikler</p>
                                <ul class="list-disc list-inside space-y-1">
                                    <li>Sansürsüz</li>
                                    <li>7/24 Çalışır</li>
                                    <li>OpenAI Uyumlu</li>
                                </ul>
                            </div>
                            <div>
                                <p class="font-semibold text-gray-800">API Endpoints</p>
                                <ul class="list-disc list-inside space-y-1 text-xs">
                                    <li>/v1/completions</li>
                                    <li>/v1/chat/completions</li>
                                    <li>/v1/models</li>
                                </ul>
                            </div>
                        </div>
                    </div>

                    <!-- Settings Card -->
                    <div class="bg-white rounded-lg shadow-xl p-6">
                        <h3 class="text-lg font-bold text-gray-800 mb-4">⚙️ Ayarlar</h3>
                        <div class="space-y-4">
                            <div>
                                <label class="block text-sm font-semibold text-gray-800 mb-2">
                                    Sıcaklık (Temperature)
                                </label>
                                <input 
                                    type="range" 
                                    id="temperature" 
                                    min="0" 
                                    max="1" 
                                    step="0.1" 
                                    value="0.7" 
                                    class="w-full"
                                >
                                <p class="text-xs text-gray-500 mt-1">Değer: <span id="tempValue">0.7</span></p>
                            </div>
                            <div>
                                <label class="block text-sm font-semibold text-gray-800 mb-2">
                                    Max Token
                                </label>
                                <input 
                                    type="number" 
                                    id="maxTokens" 
                                    value="512" 
                                    min="10" 
                                    max="2048" 
                                    class="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-purple-500"
                                >
                            </div>
                        </div>
                    </div>

                    <!-- Stats Card -->
                    <div class="bg-white rounded-lg shadow-xl p-6">
                        <h3 class="text-lg font-bold text-gray-800 mb-4">📊 İstatistikler</h3>
                        <div class="space-y-3 text-sm">
                            <div class="flex justify-between">
                                <span class="text-gray-600">Toplam Mesaj:</span>
                                <span class="font-bold text-gray-800" id="totalMessages">0</span>
                            </div>
                            <div class="flex justify-between">
                                <span class="text-gray-600">Oturum Süresi:</span>
                                <span class="font-bold text-gray-800" id="sessionTime">0s</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </main>

        <!-- Footer -->
        <footer class="bg-gray-900 text-gray-400 text-center py-4 mt-8">
            <p>OpenClaw + Dolphin 3 | Sansürsüz AI Sunucusu | Railway.app'da 7/24 Çalışır</p>
        </footer>
    </div>

    <script>
        let messageCount = 0;
        let startTime = Date.now();

        // Update temperature value display
        document.getElementById('temperature').addEventListener('input', (e) => {
            document.getElementById('tempValue').textContent = e.target.value;
        });

        // Update session time
        setInterval(() => {
            const elapsed = Math.floor((Date.now() - startTime) / 1000);
            const hours = Math.floor(elapsed / 3600);
            const minutes = Math.floor((elapsed % 3600) / 60);
            const seconds = elapsed % 60;
            
            if (hours > 0) {
                document.getElementById('sessionTime').textContent = `${hours}h ${minutes}m`;
            } else if (minutes > 0) {
                document.getElementById('sessionTime').textContent = `${minutes}m ${seconds}s`;
            } else {
                document.getElementById('sessionTime').textContent = `${seconds}s`;
            }
        }, 1000);

        async function sendMessage() {
            const input = document.getElementById('messageInput');
            const message = input.value.trim();
            
            if (!message) return;

            // Add user message to chat
            const chatMessages = document.getElementById('chatMessages');
            const userMessageDiv = document.createElement('div');
            userMessageDiv.className = 'fade-in flex justify-end';
            userMessageDiv.innerHTML = `
                <div class="message-user text-white rounded-lg px-4 py-3 max-w-xs">
                    <p class="text-sm">${escapeHtml(message)}</p>
                </div>
            `;
            chatMessages.appendChild(userMessageDiv);

            // Clear input
            input.value = '';

            // Add typing indicator
            const typingDiv = document.createElement('div');
            typingDiv.className = 'fade-in flex justify-start';
            typingDiv.innerHTML = `
                <div class="message-assistant rounded-lg px-4 py-3">
                    <div class="typing-indicator">
                        <span class="inline-block w-2 h-2 bg-gray-400 rounded-full"></span>
                        <span class="inline-block w-2 h-2 bg-gray-400 rounded-full ml-1"></span>
                        <span class="inline-block w-2 h-2 bg-gray-400 rounded-full ml-1"></span>
                    </div>
                </div>
            `;
            chatMessages.appendChild(typingDiv);
            chatMessages.scrollTop = chatMessages.scrollHeight;

            try {
                const response = await fetch('/api/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        message: message,
                        temperature: parseFloat(document.getElementById('temperature').value),
                        max_tokens: parseInt(document.getElementById('maxTokens').value)
                    })
                });

                const data = await response.json();
                
                // Remove typing indicator
                typingDiv.remove();

                // Add assistant response
                const assistantMessageDiv = document.createElement('div');
                assistantMessageDiv.className = 'fade-in flex justify-start';
                assistantMessageDiv.innerHTML = `
                    <div class="message-assistant text-gray-800 rounded-lg px-4 py-3 max-w-xs">
                        <p class="text-sm">${escapeHtml(data.response)}</p>
                    </div>
                `;
                chatMessages.appendChild(assistantMessageDiv);
                chatMessages.scrollTop = chatMessages.scrollHeight;

                // Update message count
                messageCount += 2;
                document.getElementById('totalMessages').textContent = messageCount;

            } catch (error) {
                typingDiv.remove();
                const errorDiv = document.createElement('div');
                errorDiv.className = 'fade-in flex justify-start';
                errorDiv.innerHTML = `
                    <div class="bg-red-100 text-red-800 rounded-lg px-4 py-3 max-w-xs">
                        <p class="text-sm">❌ Hata: ${error.message}</p>
                    </div>
                `;
                chatMessages.appendChild(errorDiv);
                chatMessages.scrollTop = chatMessages.scrollHeight;
            }
        }

        function escapeHtml(text) {
            const map = {
                '&': '&amp;',
                '<': '&lt;',
                '>': '&gt;',
                '"': '&quot;',
                "'": '&#039;'
            };
            return text.replace(/[&<>"']/g, m => map[m]);
        }

        // Focus on input when page loads
        document.getElementById('messageInput').focus();
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """GUI Ana Sayfası"""
    return render_template_string(GUI_TEMPLATE)

@app.route('/api/chat', methods=['POST'])
def api_chat():
    """Chat API Endpoint"""
    try:
        data = request.json
        message = data.get('message', '')
        temperature = data.get('temperature', 0.7)
        max_tokens = data.get('max_tokens', 512)
        
        if not message:
            return jsonify({'error': 'Mesaj boş'}), 400
        
        sampling_params = SamplingParams(
            temperature=temperature,
            top_p=0.9,
            max_tokens=max_tokens
        )
        
        outputs = llm.generate(message, sampling_params)
        response_text = outputs[0].outputs[0].text
        
        return jsonify({
            'response': response_text,
            'model': 'dolphin-2.9-llama3.1-8b'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/v1/completions', methods=['POST'])
def completions():
    """OpenAI API uyumlu completions endpoint"""
    try:
        data = request.json
        
        sampling_params = SamplingParams(
            temperature=data.get('temperature', 0.7),
            top_p=data.get('top_p', 0.9),
            max_tokens=data.get('max_tokens', 512)
        )
        
        outputs = llm.generate(
            data['prompt'],
            sampling_params
        )
        
        return jsonify({
            'id': 'openclaw-1',
            'object': 'text_completion',
            'created': 1234567890,
            'model': 'dolphin-2.9-llama3.1-8b',
            'choices': [
                {
                    'text': output.outputs[0].text,
                    'index': i,
                    'finish_reason': 'length'
                }
                for i, output in enumerate(outputs)
            ]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/v1/chat/completions', methods=['POST'])
def chat_completions():
    """OpenAI API uyumlu chat completions endpoint"""
    try:
        data = request.json
        messages = data.get('messages', [])
        
        prompt = ""
        for msg in messages:
            role = msg.get('role', 'user')
            content = msg.get('content', '')
            prompt += f"{role}: {content}\n"
        
        prompt += "assistant: "
        
        sampling_params = SamplingParams(
            temperature=data.get('temperature', 0.7),
            top_p=data.get('top_p', 0.9),
            max_tokens=data.get('max_tokens', 512)
        )
        
        outputs = llm.generate(prompt, sampling_params)
        
        return jsonify({
            'id': 'openclaw-1',
            'object': 'chat.completion',
            'created': 1234567890,
            'model': 'dolphin-2.9-llama3.1-8b',
            'choices': [
                {
                    'message': {
                        'role': 'assistant',
                        'content': output.outputs[0].text
                    },
                    'index': i,
                    'finish_reason': 'length'
                }
                for i, output in enumerate(outputs)
            ]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/v1/models', methods=['GET'])
def models():
    """Mevcut modelleri listele"""
    return jsonify({
        'object': 'list',
        'data': [
            {
                'id': 'dolphin-2.9-llama3.1-8b',
                'object': 'model',
                'owned_by': 'cognitivecomputations',
                'permission': []
            }
        ]
    })

@app.route('/health', methods=['GET'])
def health():
    """Sağlık kontrolü"""
    return jsonify({'status': 'ok', 'model': 'dolphin-2.9-llama3.1-8b'})

@app.route('/api/status', methods=['GET'])
def api_status():
    """API Durumu"""
    return jsonify({
        'status': 'online',
        'model': 'dolphin-2.9-llama3.1-8b',
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=False)
