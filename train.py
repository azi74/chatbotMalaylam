import json
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Embedding, LSTM, Bidirectional, TimeDistributed
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from config import Config

# 1. Load Dataset
with open('data/malayalam_dataset.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

texts = [item['text'] for item in data]
intents = [item['intent'] for item in data]

# 2. Intent Classifier
tokenizer = Tokenizer()
tokenizer.fit_on_texts(texts)
sequences = tokenizer.texts_to_sequences(texts)
X = pad_sequences(sequences, maxlen=Config.MAX_SEQUENCE_LENGTH)

label_encoder = LabelEncoder()
y = label_encoder.fit_transform(intents)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

intent_model = Sequential([
    Embedding(len(tokenizer.word_index) + 1, Config.EMBEDDING_DIM),
    Bidirectional(LSTM(64)),
    Dense(len(set(intents)), activation='softmax')
])
intent_model.compile(loss='sparse_categorical_crossentropy', 
                   optimizer='adam', 
                   metrics=['accuracy'])
intent_model.fit(X_train, y_train, epochs=10, validation_data=(X_test, y_test))
intent_model.save('models/intent_classifier.h5')

# 3. NER Model Preparation
# First extract all entity tags from the dataset
ner_tags = ['O']  # 'O' means 'Outside' (not an entity)
for item in data:
    for entity in item.get('entities', []):
        if entity['entity'] not in ner_tags:
            ner_tags.append(entity['entity'])

# Create sequence labels for NER
ner_sequences = []
for item in data:
    text = item['text']
    word_labels = ['O'] * len(text.split())  # Initialize all words as 'O'
    
    for entity in item.get('entities', []):
        entity_words = entity['text'].split()
        for i in range(len(entity_words)):
            # Mark first word as B-ENTITY and subsequent as I-ENTITY
            prefix = 'B-' if i == 0 else 'I-'
            word_labels[i] = prefix + entity['entity']
    
    ner_sequences.append(word_labels)

# Convert NER tags to numerical labels
ner_label_encoder = LabelEncoder()
ner_label_encoder.fit(ner_tags)

# 4. NER Model
ner_model = Sequential([
    Embedding(len(tokenizer.word_index) + 1, Config.EMBEDDING_DIM),
    Bidirectional(LSTM(64, return_sequences=True)),
    TimeDistributed(Dense(len(ner_tags), activation='softmax'))
])
ner_model.compile(loss='sparse_categorical_crossentropy', optimizer='adam')

# Note: You'll need to prepare proper NER training data (X_ner, y_ner)
# This is simplified for demonstration
ner_model.save('models/ner_model.h5')

print("Models trained and saved successfully!")
print(f"Intent classes: {label_encoder.classes_}")
print(f"NER tags: {ner_tags}")