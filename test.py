from utils.nlp_processor import load_models, process_text
import nltk
nltk.download('punkt')

models = load_models()
test = process_text("കൊച്ചിയിലെ ഹോട്ടലുകൾ", models)
print(test)