import os, uuid
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, ContentSettings

from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("-m", "--module", type=str, required=True,
                    help="the name of the root module to upload")
parser.add_argument("-s", "--submodule", type=str, required=False,
                    help="the name of the sub module to upload")

args = parser.parse_args()

#Location of the stackr Cucumber test result html: resourceGroup/results/cucumber.html
#Location of the stackr Cucumber test result json: resourceGroup/results/cucumber.json

account_url = "https://svensappstorage.blob.core.windows.net"
default_credential = DefaultAzureCredential()
contentSettings = ContentSettings(content_type="text/html")

# Create the BlobServiceClient object
blob_service_client = BlobServiceClient(account_url, credential=default_credential)

# FIXME Assumption is that the other modules are 2 levels up
local_path = "../../{}/test/{}/results/".format(args.module, args.submodule)
print("The local path is: " + local_path)

# Create a blob client using the local file name as the name for the blob
# And upload the created file
blob_json_file_name = "{}_{}_cucumber.json".format(args.module, args.submodule)
json_blob_client = blob_service_client.get_blob_client(container="$web", blob=blob_json_file_name)
print("\nUploading to Azure Storage as blob:\n\t" + blob_json_file_name)

json_file_name = "cucumber.json".format(args.module, args.submodule)
upload_file_path = os.path.join(local_path, json_file_name)
with open(file=upload_file_path, mode="rb") as data:
    json_blob_client.upload_blob(data, overwrite=True, content_settings=contentSettings)

# And repeat for the html side
blob_html_file_name = "{}_{}_cucumber.html".format(args.module, args.submodule)
html_blob_client = blob_service_client.get_blob_client(container="$web", blob=blob_html_file_name)
print("\nUploading to Azure Storage as blob:\n\t" + blob_html_file_name)

html_file_name = "cucumber.html".format(args.module, args.submodule)
html_upload_file_path = os.path.join(local_path, html_file_name)
with open(file=html_upload_file_path, mode="rb") as data:
    html_blob_client.upload_blob(data, overwrite=True, content_settings=contentSettings)

