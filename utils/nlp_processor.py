import json
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer
from nltk.tokenize import word_tokenize
import os
from config import Config
import googletrans
from googletrans import Translator

translator = Translator()

def load_models():
    """Load NLP models and necessary data"""
    try:
        # Load intent classification model
        intent_model = load_model(os.path.join(Config.MODEL_PATH, 'intent_classifier.h5'))
        
        # Load NER model
        ner_model = load_model(os.path.join(Config.MODEL_PATH, 'ner_model.h5'))
        
        # Load tokenizer and label encodings
        with open(os.path.join(Config.DATA_PATH, 'malayalam_dataset.json'), 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Create tokenizer
        tokenizer = Tokenizer()
        texts = [item['text'] for item in data]
        tokenizer.fit_on_texts(texts)
        
        # Create intent labels
        intents = list(set(item['intent'] for item in data))
        intent_labels = {intent: i for i, intent in enumerate(intents)}
        
        return {
            'intent_model': intent_model,
            'ner_model': ner_model,
            'tokenizer': tokenizer,
            'intent_labels': intent_labels,
            'intents': intents
        }
    
    except Exception as e:
        print(f"Error loading models: {e}")
        raise

def preprocess_text(text, tokenizer):
    """Preprocess text for model input"""
    sequence = tokenizer.texts_to_sequences([text])
    padded = pad_sequences(sequence, maxlen=Config.MAX_SEQUENCE_LENGTH)
    return padded

def process_text(text, models):
    """Process Malayalam text to extract intent and entities"""
    try:
        # If the text is not in Malayalam, try to translate it
        if not is_malayalam(text):
            translation = translator.translate(text, dest=Config.LANGUAGE_CODE)
            text = translation.text
        
        # Tokenize and preprocess text
        tokens = word_tokenize(text)
        processed_text = ' '.join(tokens)
        
        # Predict intent
        padded_text = preprocess_text(processed_text, models['tokenizer'])
        intent_pred = models['intent_model'].predict(padded_text)
        intent_idx = np.argmax(intent_pred)
        intent = models['intents'][intent_idx]
        
        # Predict named entities (simplified example)
        ner_pred = models['ner_model'].predict(padded_text)
        entities = extract_entities(tokens, ner_pred[0])
        
        return {
            'text': text,
            'intent': intent,
            'entities': entities,
            'tokens': tokens
        }
    
    except Exception as e:
        print(f"Error processing text: {e}")
        return {
            'text': text,
            'intent': 'unknown',
            'entities': [],
            'tokens': []
        }

def is_malayalam(text):
    """Check if text contains Malayalam characters"""
    malayalam_range = (0x0D00, 0x0D7F)
    return any(ord(char) >= malayalam_range[0] and ord(char) <= malayalam_range[1] for char in text)

def extract_entities(tokens, ner_pred):
    """Extract named entities from prediction"""
    entities = []
    current_entity = []
    current_tag = None
    
    for token, pred in zip(tokens, ner_pred):
        tag_idx = np.argmax(pred)
        # This is simplified - you'd need to map tag_idx to actual tags
        tag = 'O' if tag_idx == 0 else 'ENTITY'
        
        if tag == 'O':
            if current_entity:
                entities.append((' '.join(current_entity), current_tag))
                current_entity = []
                current_tag = None
        else:
            if current_tag is None:
                current_tag = tag
                current_entity.append(token)
            elif current_tag == tag:
                current_entity.append(token)
            else:
                if current_entity:
                    entities.append((' '.join(current_entity), current_tag))
                current_entity = [token]
                current_tag = tag
    
    if current_entity:
        entities.append((' '.join(current_entity), current_tag))
    
    return entities