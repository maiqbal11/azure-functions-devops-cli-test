import logging
from dataclasses import dataclass
import azure.functions as func

@dataclass
class Datum:
    a: int = 3

def main(req: func.HttpRequest) -> func.HttpResponse:
    datum = Datum()
    return func.HttpResponse(f'dataclasses-trigger {datum.a}')
