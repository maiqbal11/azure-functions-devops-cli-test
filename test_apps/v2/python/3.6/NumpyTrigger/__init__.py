import logging
import numpy as np
import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    a = np.arange(15).reshape(3, 5)
    return func.HttpResponse(
        f"numpy-trigger {a[1][2]}",
        status_code=200
    )

    # The result should be 7
