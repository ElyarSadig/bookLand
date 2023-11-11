import os
import uuid
import requests
from decouple import config
from .exceptions import InvalidFileFormatError, FileUploadFailedError


ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'pdf', 'png'}


def check_extension(file_path):
    file_extension = os.path.splitext(file_path)[1][1:].lower()
    if file_extension not in ALLOWED_EXTENSIONS:
        raise InvalidFileFormatError()


def generate_uuid(file_path):
    return f"{uuid.uuid4()}_{os.path.basename(file_path)}"


def process_and_upload_identity_path(file_path, postfix="/identities"):
    check_extension(file_path)
    return upload_to_file_server(file_path, postfix)


def process_and_upload_publications_image(file_path, postfix="/publications"):
    check_extension(file_path)
    return upload_to_file_server(file_path, postfix)


def upload_to_file_server(file_path, postfix):
    file_server_url = config('FILE_SERVER_URL')
    auth_token = config('AUTH_TOKEN')
    file_name = generate_uuid(file_path)

    with open(file_path, 'rb') as file:
        files = {'file': (file_name, file)}

        response = requests.post(file_server_url + postfix, files=files, headers={'Authorization': auth_token})

        if response.status_code == 200:
            return file_name  # Return the file name
        else:
            raise FileUploadFailedError()



