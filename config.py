import os

class Config:
    # Path configurations
    DATA_PATH = os.path.join(os.path.dirname(__file__), 'data')
    MODEL_PATH = os.path.join(os.path.dirname(__file__), 'models')
    
    # NLP configurations
    MAX_SEQUENCE_LENGTH = 20
    EMBEDDING_DIM = 100
    
    # Speech configurations
    AUDIO_UPLOAD_FOLDER = 'uploads'
    ALLOWED_EXTENSIONS = {'wav', 'mp3', 'ogg'}
    
    # Malayalam language code
    LANGUAGE_CODE = 'ml'
    
    # Tourism domain specific
    TOURISM_KEYWORDS = {
        'places': ['സ്ഥലങ്ങൾ', 'പ്രധാനപ്പെട്ട സ്ഥലങ്ങൾ', 'ടൂറിസം സ്ഥലങ്ങൾ'],
        'hotels': ['ഹോട്ടലുകൾ', 'ലോജിങ്', 'സ്റ്റേ'],
        'transport': ['ഗതാഗതം', 'ബസ്', 'ട്രെയിൻ', 'ടാക്സി']
    }