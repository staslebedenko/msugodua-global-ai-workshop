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