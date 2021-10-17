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
Navigate to: www.microsoftazurepass.comClick start and follow the on-screen instruction



it is build around this source
https://workshops.globalai.community/

# Setting up the environment

Install.
Python latest version 
Visual Studio Code with plugins
  Select plugins and type in search
  ms-toolsai.jupyter
  ms-python.python

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



