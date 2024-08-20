import nltk
import numpy as np
import json
import tensorflow as tf
from nltk.stem.lancaster import LancasterStemmer

# Initialize the stemmer
stemmer = LancasterStemmer()

# Load and process the intents file
with open('intents.json') as intents:
    data = json.load(intents)

words = []
labels = []
x_docs = []
y_docs = []

for intent in data['intents']:
    for pattern in intent['patterns']:
        wrds = nltk.word_tokenize(pattern)
        words.extend(wrds)
        x_docs.append(wrds)
        y_docs.append(intent['tag'])

        if intent['tag'] not in labels:
            labels.append(intent['tag'])

words = sorted(list(set([stemmer.stem(w.lower()) for w in words if w not in "?"])))
labels = sorted(labels)

# Prepare training data
training = []
output = []
out_empty = [0 for _ in range(len(labels))]

for x, doc in enumerate(x_docs):
    bag = []
    wrds = [stemmer.stem(w) for w in doc]
    for w in words:
        bag.append(1 if w in wrds else 0)
    output_row = out_empty[:]
    output_row[labels.index(y_docs[x])] = 1

    training.append(bag)
    output.append(output_row)

training = np.array(training)
output = np.array(output)

# Build the model
model = tf.keras.Sequential([
    tf.keras.layers.Dense(10, input_shape=(len(training[0]),), activation='relu'),
    tf.keras.layers.Dense(10, activation='relu'),
    tf.keras.layers.Dense(len(output[0]), activation='softmax')
])

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Train and save the model
model.fit(training, output, epochs=500, batch_size=8)
model.save('model.h5')
