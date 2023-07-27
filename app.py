from flask import Flask, request, jsonify, render_template
import openai
import requests

app = Flask(__name__)

openai.api_key = 'your_openai_api_key_here'

# Function to convert text to speech using ElevenLabs API
def elevenlabs_speak(text):
    voice_id = "NkCxB2DN5XwgvsnhTRql"  # Replace with the appropriate voice ID
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": "your_api_key_here",
    }

    data = {
        "text": text,
        "voice_settings": {
            "stability": 0.25,
            "similarity_boost": .6,
        },
    }
    # Send a POST request to the ElevenLabs API
    response = requests.post(url, headers=headers, json=data)

    # Retrieve the audio content from the response
    audio_content = b""
    for chunk in response.iter_content(chunk_size=5000):
        if chunk:
            audio_content += chunk

    return audio_content

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_advice', methods=['POST'])
def get_advice():
    query = request.json.get('query')
    try:
        response = openai.ChatCompletion.create(
          model="gpt-3.5-turbo",
          messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": query},
          ]
        )
        advice = response['choices'][0]['message']['content']
        advice_speech = elevenlabs_speak(advice)
        return jsonify({"advice": advice, "advice_speech": advice_speech})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
