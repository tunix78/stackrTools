# stackrTools
Represents the stackr tools required to glue everything together for stackr

## Useful links
[Python venv](https://code.visualstudio.com/docs/python/environments)
[Python Azure library](https://learn.microsoft.com/en-us/azure/storage/blobs/storage-quickstart-blobs-python?tabs=managed-identity%2Croles-azure-cli%2Csign-in-azure-cli)

## Build Instructions for the tools

- After you created a venv as described in the link above
- Create requirements.txt and install packages

    `pip freeze > requirements.txt`
    
    - Add `pymongo==4.3.3` to requirements.txt
    `pip install -r requirements.txt`

    - Run this command to add the azure python client libraries
    `pip install azure-storage-blob azure-identity`

## Add Storage Blob Data Contributor to the storage account

- Assumption is that storage account and containers have been created through Terraform appServices module/repo
`az storage account show --resource-group 'SvensTest' --name 'svensappstorage' --query id`
`az role assignment create --assignee "svengauggel_gmail.com#EXT#@svengauggelgmail.onmicrosoft.com" --role "Storage Blob Data Contributor" --scope "/subscriptions/f1d4db25-a121-4a93-a8a7-3329ab216466/resourceGroups/SvensTest/providers/Microsoft.Storage/storageAccounts/svensappstorage"`