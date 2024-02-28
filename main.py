import os
from flask import Flask, jsonify, request
import time
import psutil
import logging
import sys
from ncm import get_full_ncm, NCM_VALUE
import uuid
from firebase_utils import FireBaseConn
from flask_swagger_ui import get_swaggerui_blueprint
import re 

# Initializate Flask app
app = Flask("__name__")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./hvar-dufry-dev-46f2154886a2.json"
os.environ["DUFRY_AUTHENTICATION_KEY"] = "D857B7D2F1DE3A3257C64C53904AEE0A8FDE5F157C6BAC5C57B14B0DFBC8248E"

# Definying global variables for logging
SERVICE_NAME = "ncm_classifier"
LOGGING_AGENT = logging.getLogger(SERVICE_NAME)
LOGGING_AGENT.setLevel(logging.DEBUG) 
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format="[%(asctime)s] - [%(name)s] - [%(levelname)s] - [%(message)s]")
handler = logging.StreamHandler(sys.stdout)
LOGGING_AGENT.addHandler(handler)


@app.route("/test", methods = ['GET', 'POST'])
def test():
    LOGGING_AGENT.info("Free memory: %s ", str(psutil.virtual_memory().free / 1024.**3))
    LOGGING_AGENT.info("Used memory: %s ", str(psutil.virtual_memory().used / 1024.**3))
    LOGGING_AGENT.info("Total memory: %s ", str(psutil.virtual_memory().total / 1024.**3))
    LOGGING_AGENT.info("Input payload: %s", str(request.get_json()))

    return jsonify(success=True)

@app.route('/ncm_classifier/', methods=['POST'])  
@app.route('/ncm_classifier/<id>', methods = ['GET', 'PATCH'])
def dcm_classifier(id=None):
    """Main function to call model and store database metrics
    Parameters:
    id (str): The id of register in firebase
    Returns:
    dict: Response value
   """
    func_start = time.time()

    response_payload = dict()
    print(response_payload)
    try:

        # Tries to authenticate with secret for all methods
        authenticate()

        if(request.method == 'POST'):

            id = uuid.uuid4()

            input_text = request.get_json()["input_text"] 

            ncm_code, confidence_score, result, ncm_description = get_full_ncm(input_text)
            
            firestore = FireBaseConn()

            data = {"id":str(id), "input_text":input_text, "confidence_score":confidence_score, "ncm_code":ncm_code, "ncm_description":ncm_description, "category_type":"FULL_NCM", "result":"RIGHT", "updated_by":"ML_MODEL"}
            save = firestore.save_to_firestore(str(id), data)

            response_payload['ID'] = id
            response_payload['data'] = data


        elif(request.method == 'GET'):
            """Receive an id through url and return the entire payload.
            """

            if id != None:
                firestore = FireBaseConn()

                data = firestore.get_doc_by_id(id)
                response_payload['data'] = data
            else:
                raise NotImplementedError("Id is required.")

        elif(request.method == 'PATCH'):
            """Receive an id through url and a payload with fields result and ground_truth
            """
            if id != None:
                firestore = FireBaseConn()

                ncm = request.get_json()["NCM"] 
                ncm = re.sub('[^0-9.]', "", str(ncm))

                if len(ncm) != 8:
                    response_payload['Error'] = 'NCM must be exact 8 numbers long.'
                else:
                    data = firestore.update_doc_by_id(id, ncm)
                    response_payload['data'] = data
            else:
                raise NotImplementedError("Id is required.")
        else:
            raise NotImplementedError("This method is not supported.")

    except Exception as e:
        response_payload["error"] = e
        LOGGING_AGENT.error(e)    

    finally:
        response_payload["time_elapsed"] = (time.time() - func_start)
        LOGGING_AGENT.debug("Response payload: [%s]", str(response_payload))

        return response_payload


def authenticate():
     # Gets the API_KEY env
        try:
            API_KEY = os.environ.get("DUFRY_AUTHENTICATION_KEY")
        except:
            raise Exception("Something wrong happened. Contact your administrator.")

        #Gets the API_KEY from Header
        try:
            USER_API_KEY = request.headers.get("DUFRY_AUTHENTICATION_KEY")
        except:
            raise Exception("Something wrong happened. Contact your administrator.")

        #Compare the user KEY with Secret Manager KEY
        if(API_KEY != USER_API_KEY):
            raise Exception("Something wrong happened. Contact your administrator.")

SWAGGER_URL = "/docs"
API_URL = "/static/swagger.json"
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        "app_name": "Dufry NCM Classifier"
    }
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

if __name__ == "__main__":
    app.run() #(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
