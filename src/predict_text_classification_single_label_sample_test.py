# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="C:/Users/Victor/OneDrive/Documentos/HvarConsulting/MLOps/Dufry/sandbox-ml-pipeline-be74f70fa45b.json"

import predict_text_classification_single_label_sample

ENDPOINT_ID = "4038585373658447872"  # text_classification_single_label
PROJECT_ID = "689966009866" #os.getenv("BUILD_SPECIFIC_GCLOUD_PROJECT")

content = "Lindt Choco Excellence 85 Cacao 100g"

def test_ucaip_generated_predict_text_classification_single_label_sample(capsys):

    predict_text_classification_single_label_sample.predict_text_classification_single_label_sample(
        content=content, project=PROJECT_ID, endpoint_id=ENDPOINT_ID
    )

    out, _ = capsys.readouterr()
    assert "prediction" in out



def test_model():

    predictions = predict_text_classification_single_label_sample.predict_text_classification_single_label_sample(
        content=content, project=PROJECT_ID, endpoint_id=ENDPOINT_ID
    )

    for prediction in predictions:
        print(" prediction:", dict(prediction))

if __name__ == '__main__':
    test_model()