import tensorflow as tf

from tensorflow.keras.preprocessing.image import (
    ImageDataGenerator
)

IMG_SIZE = (128,128)

gen = ImageDataGenerator(
    rescale=1./255
)

test = gen.flow_from_directory(
    "logmel",
    target_size=IMG_SIZE,
    batch_size=32,
    shuffle=False,
    class_mode="binary"
)

model = tf.keras.models.load_model(
    "cnn_model.keras"
)

loss, acc = model.evaluate(
    test
)

print("Accuracy:", acc)
