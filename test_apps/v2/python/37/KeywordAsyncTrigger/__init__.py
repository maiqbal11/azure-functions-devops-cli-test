import logging
import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    # async keyword assignment should only work in Python 3.6
    async: int = 9
    return func.HttpResponse(
        f"async {async}",
        status_code=200
    )

    # The result should be "async 9"
