#!/bin/python
# flask est un serveur web 
from flask import Flask, request, redirect, jsonify
import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
 
labels_path = 'labels.txt'
model_path = 'model'
 
model = tf.keras.Sequential([
    hub.KerasLayer(model_path)
])
model.build([None, 224, 224, 3])  # Batch input shape.
 
imagenet_labels = np.array(open(labels_path).read().splitlines())
 
 
def preprocess_image(raw_image):
    image = tf.image.decode_jpeg(raw_image)
    image = tf.image.resize(image, (224, 224))
    image = image / 255.0  # Normalize to [0,1]
    return tf.expand_dims(image, axis=0)  # Add batch dimension
 
 
def predict(raw_image):
    input_image = preprocess_image(raw_image)
    predictions = model(input_image) # (nb_imgs, 224, 224, 3) -> (nb_imgs, nb_labels)
    predicted_label_index = tf.argmax(predictions, axis=-1).numpy()[0]
    return imagenet_labels[predicted_label_index]
 
 # Create Flask app
app = Flask(__name__)

@app.route('/predict',methods=['POST'])
def run_predict():
    raw_image_data = request.data
    return jsonify({'prediction': predict(raw_image_data)})


@app.route('/predict',methods=['GET'])
def run_predict2():
    raw_image_data = tf.io.read_file('shared/test.jpg')
    return jsonify({'prediction': predict(raw_image_data)})

app.run(host='0.0.0.0', debug=True)