import logging
import traceback
from typing import List
import azure.functions as func
from workflow_1_code import functionone

def main(events: List[func.EventHubEvent]) -> str:
    try:
        logging.info("-------------- LOG FROM WORKFLOW 1 -----------------------")
        result = functionone(events)
        logging.info(type(result))
        logging.info(result)
        return result
    except Exception as ex:
        errordetails = "EXCEPTION FROM WORKFLOW 1 --------------------------" + str(ex)
        logging.info("EXCEPTION FROM WORKFLOW 1 --------------------------" + str(ex))
        logging.error(traceback.format_exc())
        return errordetails
