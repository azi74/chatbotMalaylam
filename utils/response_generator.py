import json
import random
from config import Config

def load_responses():
    """Load predefined responses from JSON file"""
    with open(os.path.join(Config.DATA_PATH, 'responses.json'), 'r', encoding='utf-8') as f:
        return json.load(f)

def generate_response(processed_data):
    """Generate appropriate response based on intent and entities"""
    responses = load_responses()
    intent = processed_data['intent']
    entities = processed_data['entities']
    
    # Get base responses for the intent
    intent_responses = responses.get(intent, [])
    
    if not intent_responses:
        return "ക്ഷമിക്കണം, എനിക്ക് ആ ചോദ്യത്തിന് ഉത്തരം നൽകാൻ കഴിയില്ല."
    
    # Select a random response template
    response_template = random.choice(intent_responses)
    
    # Replace placeholders with entities
    for entity, tag in entities:
        response_template = response_template.replace(f'[{tag}]', entity)
    
    return response_template