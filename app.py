from flask import Flask, render_template, request, jsonify
from utils.nlp_processor import process_text, load_models
from utils.speech_processor import process_audio
from utils.response_generator import generate_response
import os

app = Flask(__name__)
app.config.from_object('config.Config')

# Load models at startup
nlp_models = load_models()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        # Check if the request contains text or audio
        if 'audio' in request.files:
            audio_file = request.files['audio']
            if audio_file.filename != '':
                # Process audio file
                text_input = process_audio(audio_file)
                if not text_input:
                    return jsonify({'error': 'Audio processing failed'}), 400
        else:
            text_input = request.json.get('text', '').strip()
        
        if not text_input:
            return jsonify({'error': 'No input provided'}), 400
        
        # Process text with NLP
        processed_data = process_text(text_input, nlp_models)
        
        # Generate appropriate response
        response = generate_response(processed_data)
        
        return jsonify({
            'input': text_input,
            'response': response,
            'intent': processed_data.get('intent'),
            'entities': processed_data.get('entities')
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    os.makedirs(app.config['AUDIO_UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)