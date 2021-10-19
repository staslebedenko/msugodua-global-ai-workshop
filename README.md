# msugodua-global-ai-workshop

There are several key parts of this workshop.

1. Getting an Azure Pass and activate it on your account
2. Setting up a local environment with Visual Studio code.
3. Deploying Azure infrastructure
4. Training the model
5. Building Azure function and deploying it.
6. Running it.

Request an Azure Pass
Navigate to: https://globalai.community/checkinEnter your name and emailWatch your mailbox (maybe your spam) for the confirmation emailClick the activation link in the emailEnter the event codeYour azure pass will arrive shortly in your email.
Activate an Azure Pass
Navigate to: www.microsoftazurepass.com Click start and follow the on-screen instruction



it is build around this source
https://workshops.globalai.community/

# 1 Setting up the environment

Make sure you have Python installed(with pip) from https://www.python.org/ by running CMD and executing
```
python -V
pip --version
```
Visual Studio Code - https://code.visualstudio.com/

Find and install extensions for Python and Jupiter notebooks.
```
ms-python.python
ms-toolsai.jupyter
```

Open terminal in Visual Studio Code from Terminal menu and rund following two commands
```
mkdir globalvision
cd globalvision
```
In VSCode open File menu and click Open Folder created above

Create a new jupiter notebook file. Dont forget to save all files.
```
code newbook.ipynb 
```

Add following code to the first cell and click run(Play button on the left). You will be prompted to install needed dependencies.
```
print("hello world")
```

Create a new file dataset-download.py via terminal window
```
code dataset-download.py
```

Open file and paste following code
```
import os
import urllib.request
import zipfile

# Download the dataset from Github
data_url = "https://github.com/hnky/dataset-lego-figures/raw/master/_download/simpsons-lego-dataset.zip"
data_path = "./data-train"
download_path = os.path.join(data_path,"simpsons-lego-dataset.zip")
if not os.path.exists(data_path):
    os.mkdir(data_path);
urllib.request.urlretrieve(data_url, filename=download_path)

# Unzip the dataset
zip_ref = zipfile.ZipFile(download_path, 'r')
zip_ref.extractall(data_path)
zip_ref.close()
print("Data extracted in: {}".format(data_path))

os.remove(download_path)
print("Downloaded file removed: {}".format(download_path))
```

And run file by right clicking on a code and selecting run file or with command line
```
python C:\2\dataset-download.py
```

Wait for download to complete, then install custom vision package and create new file
```
pip install azure-cognitiveservices-vision-customvision
code custom-vision.py
```

Add following imports to file and variables with values from Azure CLI output
```
from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
from azure.cognitiveservices.vision.customvision.training.models import ImageFileCreateEntry, ImageFileCreateBatch
from msrest.authentication import ApiKeyCredentials
import time

cv_endpoint = "https://<REGION>.api.cognitive.microsoft.com"
training_key = "<INSERT KEY 1>"
training_images = "data-train"

credentials = ApiKeyCredentials(in_headers={"Training-key": training_key})
trainer = CustomVisionTrainingClient(endpoint=cv_endpoint,credentials=credentials)
```

Now you are ready to create your first project. The project takes a name and domain as input, the name can be anything. The domain is a different story. You can ask for a list of all possible domains and choose the one closest to what you are trying to accomplish. For instance if you are trying to classify food you pick the domain “Food” or “Landmarks” for landmarks. Use the code below to show all domains.

```
for domain in trainer.get_domains():
  print(domain.id, "\t", domain.name) 
```

Let’s create a new project with the domain set to “General Compact”.
And add following string to the file

```
project = trainer.create_project("Lego Simpsons",domain_id="0732100f-1a38-4e49-a514-c9b44c697ab5")
```

Now we need to tag images, so we 

```
image_list = []
directories = os.listdir(training_images)

for tagName in directories:
 	tag = trainer.create_tag(project.id, tagName)
 	images = os.listdir(os.path.join(training_images,tagName))
 	for img in images:
 		with open(os.path.join(training_images,tagName,img), "rb") as image_contents:
 			image_list.append(ImageFileCreateEntry(name=img, contents=image_contents.read(), tag_ids=[tag.id]))  
```

Now we need to create a batches to upload images

```
def chunks(l, n):
 	for i in range(0, len(l), n):
 		yield l[i:i + n]
batchedImages = chunks(image_list, 64)
```

And upload them to Azure
```
for batchOfImages in batchedImages:
    upload_result = trainer.create_images_from_files(project.id, ImageFileCreateBatch(images=batchOfImages))
    if not upload_result.is_batch_successful:
        print("Image batch upload failed.")
        for image in upload_result.images:
            print("Image status: ", image.status)
    else:
        print("Batch uploaded successfully")
print("Done uploading")
```

And finally train your model
```
print ("Training...")
iteration = trainer.train_project(project.id)
while (iteration.status != "Completed"):
    iteration = trainer.get_iteration(project.id, iteration.id)
    print ("Training status: " + iteration.status)
    print ("Waiting 25 seconds...")
    time.sleep(25)
print("Training complete")
```

Now we need to test a ONNX model, so we are adding code to export model

```
platform = "ONNX"
flavor = "ONNX12"
iteration_id = iteration.id 
project_id = project.id
export = trainer.export_iteration(project_id, iteration_id , platform, flavor, raw=False)
```

And monitoring if it is done
```
while (export.status == "Exporting"):
    print ("Waiting 10 seconds...")
    time.sleep(10)
    exports = trainer.get_exports(project.id, iteration_id)
    # Locate the export for this iteration and check its status  
    for e in exports:
        if e.platform == export.platform and e.flavor == export.flavor:
            export = e
            break
    print("Export status is: ", export.status)
print("Export: done")
```

Now we will create a new file code model-download.py
```
code model-download.py
```

With contents

```
import os
import requests
import zipfile

if export.status == "Done":
    # Success, now we can download it
    export_file = requests.get(export.download_uri)
    with open("export.zip", "wb") as file:
        file.write(export_file.content)
        
# Unzip the downloaded export
if not os.path.exists("./model"):
    os.mkdir("./model");
zip_ref = zipfile.ZipFile("export.zip", 'r')
zip_ref.extractall("./model")
zip_ref.close()
print("Data extracted in: ./model")
```

and also create auxilary file to download dataset that our model don't know
```
code test-dataset-download.py
```

With contents 
```
# Download the dataset from Github
data_url = "https://github.com/hnky/dataset-lego-figures/raw/master/_download/test-images.zip"
data_path = "./data-test"
download_path = os.path.join(data_path,"test-images.zip")
if not os.path.exists(data_path):
    os.mkdir(data_path);
urllib.request.urlretrieve(data_url, filename=download_path)

# Unzip the dataset
zip_ref = zipfile.ZipFile(download_path, 'r')
zip_ref.extractall(data_path)
zip_ref.close()
print("Data extracted in: {}".format(data_path))

os.remove(download_path)
print("Downloaded file removed: {}".format(download_path))
```

And now we need to test if our model works.
```
code validate-model.py
```

With code
```
import onnxruntime as nxrun
import numpy as np
import PIL
from PIL import Image

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
```

And now the first part of workshop is concluded.


# Creating Azure infrastructure

Go to the Azure Portal 


```
az group create --name <resource-group-name> --location <location>
az cognitiveservices account create --name <name> --kind CustomVision.Training --sku F0 --resource-group <resource-group-name> --location <location> --yes

az cognitiveservices account keys list --name <name> --resource-group <resource-group-name> 

az cognitiveservices account show --name <name> --resource-group <resource-group-name> -o json --query properties.endpoint


```

At this point you should have:
- An endpoint URL looking like this: https://<region>.api.cognitive.microsoft.com/ 
- 2 keys looking like this: 06a611d19f4f4a88a03f3b552a5d2379
  
#Train your model
 
Create a jupiter notebook from terminal in VSCode
code cv.ipynb 
  
Add your code to the first cell
print("hello world")
  
Add a new cell via + plus button and run them via Play
Each block in this workshop shoulb be added as a new cell
  
Download the dataset via
https://github.com/hnky/dataset-lego-figures/raw/master/_download/simpsons-lego-dataset.zip



