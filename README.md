# Malayalam Tourism Chatbot 🇮🇳

A conversational AI assistant for Malayalam-speaking tourists, providing local service information via text and voice in Malayalam.

[![Made with Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)](https://python.org)
[![NLP Framework](https://img.shields.io/badge/NLP-Transformers-orange?logo=pytorch)](https://huggingface.co/ai4bharat)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## Features ✨

- **Native Malayalam Support**

  - Text & voice input/output
  - Handles regional dialects and loanwords
- **Tourism Domain Expertise**

  - Hotel bookings
  - Transport schedules
  - Attraction information
  - FAQ responses
- **Advanced NLP Pipeline**

  - IndicBERT for intent classification
  - Custom NER for Malayalam entities
  - Sentiment-aware responses

## Tech Stack 🛠️

| Component                   | Technology Used                          |
| --------------------------- | ---------------------------------------- |
| **Backend**           | Python 3.8+, Flask                       |
| **NLP Models**        | IndicBERT, Custom BiLSTM-CRF             |
| **Speech Processing** | Google Speech-to-Text, PyDub             |
| **Frontend**          | HTML5, CSS3, JavaScript (Web Speech API) |
| **Deployment**        | Docker, Gunicorn                         |

## Dataset Structure 📂

```bash
data/
├── malayalam_dataset.json  # Training examples
├── responses.json         # Predefined bot replies
└── sentiment_data.csv     # Optional sentiment labels
```

Sample Training Data:

{
  "text": "തിരുവനന്തപുരത്ത് ഏറ്റവും നല്ല ഹോട്ടൽ ഏത്",
  "intent": "hotel_recommendation",
  "entities": [
    {"text": "തിരുവനന്തപുരം", "entity": "LOCATION"}
  ]
}

## Installation 🚀

**Clone the repository**

git clone https://github.com/azi74/malayalam-chatbot.git
cd malayalam-chatbot

**Set up Python environment**

python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate    # Windows
pip install -r requirements.txt

**Download pre-trained models**

wget https://example.com/models/indicbert-malayalam.h5 -P models/

**Run the chatbot**

flask run --host=0.0.0.0 --port=5000

## Training Custom Models 🧠

To retrain with your Malayalam dataset:

python train.py
  --data_path data/malayalam_dataset.json
  --model_type indicbert
  --epochs 10

## API Endpoints 🌐

| Endpoint       | Method | Description                  |
| -------------- | ------ | ---------------------------- |
| `/api/chat`  | POST   | Process text/voice queries   |
| `/api/train` | PUT    | Retrain models with new data |

## Screenshots 🖼️



## Contributing 🤝

We welcome Malayalam NLP contributions! Please:

1. Fork the project
2. Add your dataset to `data/`
3. Submit a pull request

**Guidelines:**

* Follow PEP 8 coding standards
* Document new Malayalam language rules in `docs/language_rules.md`
* Test changes with `pytest tests/`

## License 📜

This project is licensed under the MIT License - see the [LICENSE](https://license/) file for details.

---

Made with ❤️ for Malayalam speakers by asi.
