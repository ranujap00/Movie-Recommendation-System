from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import os

# Azure Storage Account information
account_name = "irwa"
account_key = "hpkOC2DHeGg4YNewCXS+1M+uvg10MmkWCU4D7eSvKR/hCH/HlSUBFNRFLAVo/997a6e1RtkbJRCR+ASte2OnXA=="

# Blob container and .pkl file information
container_name = "irwa-container"
folder_path = "D:\\SLIIT\\Year 03 sem 02\\IRWA\\IRWA Project\\Movie-Recommendation-System\\PKL_Files\\"

file_list = []
# Iterate over files in the folder
for filename in os.listdir(folder_path):
    if os.path.isfile(os.path.join(folder_path, filename)):
        file_list.append(folder_path + filename)

for file in file_list:
    # Initialize the BlobServiceClient
    blob_service_client = BlobServiceClient(account_url=f"https://{account_name}.blob.core.windows.net", credential=account_key)

    # Create a BlobContainerClient
    container_client = blob_service_client.get_container_client(container_name)

    # Upload the .pkl file to Azure Blob Storage
    with open(file, "rb") as data:
        blob_client = container_client.get_blob_client(file)
        blob_client.upload_blob(data)

    print(f"{file} uploaded to Azure Blob Storage")
