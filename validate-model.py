import onnxruntime as nxrun
import numpy as np
import PIL
from PIL import Image
import os

training_images = "./data-test"
model_path = "./model/model.onnx"

sess = nxrun.InferenceSession(model_path)

testimages = os.listdir(training_images)

for image_filepath in testimages[0:5]:
    image = PIL.Image.open(os.path.join(training_images,image_filepath)).resize([224,224])
    input_array = np.array(image, dtype=np.float32)[np.newaxis, :, :, :]
    input_array = input_array.transpose((0, 3, 1, 2))[:, (2, 1, 0), :, :]

    input_name = sess.get_inputs()[0].name
    outputs = sess.run(None, {input_name: input_array.astype(np.float32)})

    print("Image:", image_filepath)
    print("Label: " + outputs[0][0][0])
    print("Score: " + str(outputs[1][0][outputs[0][0][0]]))
    print("--")