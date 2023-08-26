import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
from flask import Flask, request, redirect, jsonify

labels_path = 'labels.txt'
model_path = 'model'


model = tf.keras.Sequential([
    hub.KerasLayer(model_path)
])
model.build([None, 224, 224, 3])  # Batch input shape.

imagenet_labels = np.array(open(labels_path).read().splitlines())


def preprocess_image(image_path):
    image = tf.image.decode_jpeg(tf.io.read_file(image_path))
    image = tf.image.resize(image, (224, 224))
    image = image / 255.0  # Normalize to [0,1]
    return tf.expand_dims(image, axis=0)  # Add batch dimension


def predict(image_path):
    input_image = preprocess_image(image_path)
    predictions = model(input_image) # (nb_imgs, 224, 224, 3) -> (nb_imgs, nb_labels)
    predicted_label_index = tf.argmax(predictions, axis=-1).numpy()[0]
    return imagenet_labels[predicted_label_index]

image_path = 'flower-test.jpg'
print("Predicted label: ", predict(image_path))


app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    # Check if a file was uploaded
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']

    # If the user does not select a file, the browser submits an empty file
    if file.filename == '':
        return redirect(request.url)

    # Read the image file
    image_data = file.read()
    
    # Open the image with PIL
    image = Image.open(io.BytesIO(image_data))

    # Preprocess the image (resize, rescale, etc.)
    image = image.resize((150, 150))  # Example resize, adjust as needed
    image_array = np.array(image) / 255.0  # Example rescale, adjust as needed
    image_array = np.expand_dims(image_array, axis=0)  # Add batch dimension

    # Predict
    prediction = model(image_array)

    # Process the prediction
    result = {
        'prediction': str(prediction)  # Adjust this as needed
    }

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
