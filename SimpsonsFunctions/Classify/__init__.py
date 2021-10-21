import logging
import onnxruntime as nxrun
import numpy as np
import PIL
from PIL import Image
import requests
from io import BytesIO
import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:

    ## Get the image and resize it to 244x244 pixels
    url = req.params.get('url')
    response = requests.get(url)
    image = PIL.Image.open(BytesIO(response.content)).resize([224,224])

    ## Load the model and score the image
    model_path = "model/model.onnx"
    sess = nxrun.InferenceSession(model_path)
    input_array = np.array(image, dtype=np.float32)[np.newaxis, :, :, :]
    input_array = input_array.transpose((0, 3, 1, 2))[:, (2, 1, 0), :, :]
    input_name = sess.get_inputs()[0].name
    outputs = sess.run(None, {input_name: input_array.astype(np.float32)})

    ## Find the label with the highest score
    label = outputs[0][0][0]
    score = (outputs[1][0][outputs[0][0][0]]*100)
    
    ## Return and log the response
    response = f"I'm {score:.2f}% sure I see: {label}"
    logging.info(response)
    return func.HttpResponse(response)