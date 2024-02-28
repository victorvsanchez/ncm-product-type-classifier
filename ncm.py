import pandas as pd
from model import predict_text_classification_single_label
from enum import Enum


class NCM_VALUE():
    UNKNOWN = 0
    RIGHT = 1
    WRONG = 2

def get_full_ncm(input_text):
    
    """Main function to call model and store database metrics
    Parameters:
    input_text (str): The input text
    Returns:
    ncm_code (str): ncm code
    confidence_score (float): the score of confidence
    result (str): the result string
    ncm_description (str): the description
   """
    try:
        # Prediction
        raw = predict_text_classification_single_label('211869487513', '7058622757763809280', input_text)

        # Cleaning the data
        data = []
        
        for i in raw:
            data.append(dict(i))
            
        di = dict(data[0])

        df = pd.DataFrame(di)

        result = df.iloc[df['confidences'].idxmax()]

        ncm_code = df.iloc[df['confidences'].idxmax()]['displayNames']
        
        confidence_score = df.iloc[df['confidences'].idxmax()]['confidences']

        ncm_description = _get_full_ncm_description(ncm_code)

        ncm_description = ncm_description if ncm_description else "UNKNOWN"

        return ncm_code,  round(confidence_score, 2), result, ncm_description

    except Exception as ex:
        raise ex

def _get_full_ncm_description(ncm_number):
    """Main function to call model and store database metrics
    Parameters:
    ncm_number (str): The classified NCM
    Returns:
    ncm_description (str): the description
   """
    ncm_list = pd.read_csv("list_ncm_descriptions.csv", sep=",", encoding ='utf-8')
    
    ncm_list['NCM'] = ncm_list['NCM'].astype(str)
    
    ncm_description = ncm_list.loc[ncm_list['NCM'] == str(ncm_number)]

    ncm_description = ncm_description.description.item() if hasattr(ncm_description, 'description') else None

    ncm_description = ncm_description.replace("\\n", "<br>")

    return ncm_description

