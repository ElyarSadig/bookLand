import os
import uuid
import requests
from decouple import config
from .exceptions import InvalidFileFormatError, FileUploadFailedError


ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'pdf', 'png'}


# def check_extension(file_path):
#     file_extension = os.path.splitext(file_path)[1][1:].lower()
#     if file_extension not in ALLOWED_EXTENSIONS:
#         raise InvalidFileFormatError()


def generate_uuid():
    return str(uuid.uuid4())


def process_and_upload_identity_path(file_path, postfix="/identities"):
    return upload_to_file_server(file_path, postfix)


def process_and_upload_publications_image(file_path, postfix="/publications"):
    return upload_to_file_server(file_path, postfix)


def upload_to_file_server(file, postfix):
    # check_extension(file_path)
    file_name = generate_uuid() + '_' + file.name
    file_server_url = config('FILE_SERVER_URL')
    auth_token = config('AUTH_TOKEN')
    files = {'file': (file_name, file)}

    response = requests.post(
        file_server_url + "/upload" + postfix,
        files=files,
        headers={'Authorization': auth_token},
        timeout=1
    )

    if response.status_code == 200:
        return file_server_url + postfix + "/" + file_name  # Adjust this based on your file server response







