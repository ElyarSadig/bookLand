import uuid
import requests
from decouple import config
from .exceptions import InvalidFileFormatError, FileUploadFailedError


def generate_uuid():
    return str(uuid.uuid4())


def process_and_upload_identity_path(file_path, postfix="/identities"):
    return upload_to_file_server(file_path, postfix)


def process_and_upload_publications_image(file_path, postfix="/publications"):
    return upload_to_file_server(file_path, postfix)


def process_and_upload_book_cover_image(file_path, postfix="/book_covers"):
    return upload_to_file_server(file_path, postfix)


def process_and_upload_book(file_path, postfix="/books"):
    return upload_to_file_server(file_path, postfix)


def upload_to_file_server(file, postfix):
    file_name = generate_uuid() + '_' + file.name
    file_server_url = config('FILE_SERVER', default='http://localhost:8080')
    auth_token = config('AUTH_TOKEN')
    files = {'file': (file_name, file)}

    response = requests.post(
        file_server_url + "/upload" + postfix,
        files=files,
        headers={'Authorization': auth_token},
        timeout=10
    )

    if response.status_code == 200:
        return "http://localhost:8080" + postfix + "/" + file_name

    return ""







