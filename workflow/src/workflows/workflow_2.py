from typing import List
import azure.functions as func
from workflow_2_code import functionone
import logging

def main(events: List[func.EventHubEvent]) -> str:
    try:
        logging.info("-------------- LOG FROM WORKFLOW 2 -----------------------")
        result = functionone()
        return result
    except Exception as ex:
        logging.info("HELLO FROM EXCEPTION BLOCK--------------------------" + str(ex))
