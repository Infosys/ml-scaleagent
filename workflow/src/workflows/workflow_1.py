import logging
import traceback
from typing import List
import azure.functions as func
from workflow_1_code import functionone

def main(events: List[func.EventHubEvent]) -> str:
    try:
        logging.info("-------------- LOG FROM WORKFLOW 1 -----------------------")

        result = functionone(events)
        
        logging.info("------------------ LOG FROM WORKFLOW 1 EXIT  ---------------------------- ")
        logging.info(type(result))
        logging.info("-----------------------------------")
        logging.info(result)
        logging.info("-----------------------------------")
        return result
    except Exception as ex:
        logging.info("HELLO FROM EXCEPTION BLOCK--------------------------" + str(ex))
        logging.error(traceback.format_exc())
        return "testdata"
