# creating the neural net
import nltk
from nltk.stem.lancaster import LancasterStemmer
import tensorflow as tf
from tensorflow import keras
import numpy
import json


invalid_responses = ["Please rephrase that.", "That is weird, I do not recognize that.", "Try again later.", "Could not come up with a response, try again."]

commandIntents = ["SMS", "EMAIL", "MUSIC", "NEWS", "FINDPHONE"]

with open("Intent.json") as file:
    data = json.load(file)

stemmer = LancasterStemmer()

words = []
labels = []
docs_x = []
docs_y = []

for intent in data["intents"]:
    for pattern in intent["patterns"]:
        wrds = nltk.word_tokenize(pattern)
        words.extend(wrds)
        docs_x.append(wrds)
        docs_y.append(intent["intent"])

    if intent["intent"] not in labels:
        labels.append(intent["intent"])

words = [stemmer.stem(w.lower()) for w in words if w != ("?" or "!")]
words = sorted(list(set(words)))
labels = sorted(labels)

training = []
output = []

out_empty = [0 for _ in range(len(labels))]

for x, doc in enumerate(docs_x):
    bag = []
    wrds = [stemmer.stem(w.lower()) for w in doc]

    for w in words:
        if w in wrds:
            bag.append(1)
        else:
            bag.append(0)

    output_row = out_empty[:]
    output_row[labels.index(docs_y[x])] = 1

    training.append(bag)
    output.append(output_row)


training = numpy.array(training)
output = numpy.array(output)
# #epoch = 1000  batch size = 100 optimiser = "adam" learning_rate = 0.001
def train(model_name, num_epochs, batch_size_val, learning_rate_val):
    # Valid model check, does it exist?
    model = loadModel(model_name)
    if (type(model) is str): return model

    #sets the learning rate for the adam optimizer
    opt = keras.optimizers.Adam(learning_rate = learning_rate_val)
    model.compile(optimizer=opt,
                  loss="categorical_crossentropy", metrics=["accuracy"])
    model.fit(training, output, epochs=num_epochs, batch_size=batch_size_val, verbose=0)
    model.save('KerasModels\\' + model_name + '.h5')
    return "Model was trained successfully..."

def trainNew(model, model_name, num_epochs, batch_size_val, learning_rate_val):
    #sets the learning rate for the adam optimizer
    opt = keras.optimizers.Adam(learning_rate = learning_rate_val)
    model.compile(optimizer=opt,
                  loss="categorical_crossentropy", metrics=["accuracy"])
    model.fit(training, output, epochs=num_epochs, batch_size=batch_size_val, verbose=0)
    model.save('KerasModels\\' + model_name + '.h5')
    return "New model trained and saved successfully..."

def loadModel(model_name):
    try:
        model = keras.models.load_model('../KerasModels/' + model_name + '.h5')
        return model
    except:
        #model not found exception
        print("model: " + model_name + " could not be found")
        return "model: " + model_name + " could not be found"

def createNewModel(model_name, num_epochs, batch_size_val, learning_rate_val, hidden_layers):
    # Check if model already exists
    model = loadModel(model_name)
    if (type(model) is not str): return f"Model with name {model_name} already exists"

    model = tf.keras.Sequential()
    model.add(tf.keras.layers.InputLayer(input_shape=(len(training[0]),)))
    if (len(hidden_layers) > 0):
        # Passed in layers
        for layer in hidden_layers:
            if layer[0] == "dense":
                model.add(tf.keras.layers.Dense(layer[1]))
            elif layer[0] == "flatten":
                model.add(tf.keras.layers.Flatten(layer[1]))
    else:
        # Default layers
        model.add(tf.keras.layers.Dense(15))
        model.add(tf.keras.layers.Dense(15))
        model.add(tf.keras.layers.Dense(15))
        model.add(tf.keras.layers.Dense(15))
        model.add(tf.keras.layers.Dense(15))
        model.add(tf.keras.layers.Dense(15))
    model.add(tf.keras.layers.Dense(len(output[0]), activation="softmax"))

    trainNew(model, model_name, num_epochs, batch_size_val, learning_rate_val)
    # run this command to get the summary of the model
    model.summary()


hiddenlayers = [("dense", 8), ("dense", 8),("dense", 8)]
createNewModel("auxilium", 250, 50, 0.001, hiddenlayers)
#The current active model (pass in the name from the UI)