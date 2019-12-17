import azure.functions as func
import google.auth as google_auth
import azure.storage.blob as azure_storage_blob

def main(req: func.HttpRequest) -> func.HttpResponse:
    return func.HttpResponse(
        f'google_auth={google_auth.__file__},'
        f'azure_storage_blob={azure_storage_blob.__file__}'
    )
