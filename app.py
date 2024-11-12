import google.generativeai as genai
from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # Mengizinkan CORS

genai.configure(api_key=os.getenv("AIzaSyDysEhFfxFcrV0cfWKfQnjiqq74CHdyzvM"))

generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-pro",
  generation_config=generation_config,
)

@app.route('/send_message', methods=['POST'])
def send_message():
    user_input = request.json.get('message')

    chat_session = model.start_chat(
      history=[
        {
          "role": "user",
          "parts": [
            "SAAT SAYA BERTANYA TOLONG BUATKAN LAPORAN PRAKTIKUM YANG harus mengikuti format laporan praktikum yang mencakup bagian berikut:\n\nSampul dengan judul 'LAPORAN PRAKTIKUM', nama praktikum, nomor pertemuan, nama pengguna, NIM, kelas, nama dosen pengampu, serta nama institusi dan jurusan.\n\nDaftar Isi dan Daftar Gambar (jika ada).\n\nBab 1 (Pendahuluan) berisi tujuan percobaan(minimal 3) dan dasar teori(minimal 3 paragraf).\n\nBab 2 (Pembahasan) berisi langkah-langkah praktikum dengan gambar atau diagram yang relevan serta penjelasan detail dan berikan sitasi per kutipan dari sumbernya dengan format APA style (minimal 5 paragraf dengan penjelasan).\n\nBab 3 (Kesimpulan) merangkum hasil praktikum(minimal 3 paragraf).\n\nDaftar Pustaka dengan format kutipan yang relevan yang berasal dari internet(minimal 5 daftar pustaka).",
          ],
        },
      ]
    )

    response = chat_session.send_message(f"{user_input}")

    return jsonify({'response': response.text})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Railway menyediakan port dinamis melalui environment variable PORT
    app.run(host="0.0.0.0", port=port)
