# Product category (NCM) classifier

This is a model that receives the text description of a given product and predicts its NCM code. NCM is a classification of imported goods in Brazil for taxation purposes. It includes both an endpoint for API usage and a visual interface for demonstration and/or small scale usage.

It was developed on Google Cloud Vertex AI, based on data extracted from airport shops (not available in this repository). It was then containerized using Docker and served on Google Cloud App Engine.

### API use

Example curl
```
curl --location --request POST "https://us-central1-ncm-dev.cloudfunctions.net/ncm-classifier" \
--header "AUTHENTICATION_KEY: " \
--header "Content-Type: application/json" \
--data-raw '{
  "input-text": "Men's Black Genuine Lambskin Leather Biker Jacket VINTAGE REAL BROWN MOTORCYCLE JACKETS FOR MEN" 
}'
```

Example response
```
{
  "input_text": {STRING},
  "confidence_score": {FLOAT},
  "ncm_code": {INT},
  "category_type": {STRING},
  "time_elapsed": {FLOAT}
}
```

### Graphic interface

![image](https://github.com/victorvsanchez/ncm-product-type-classifier/assets/43478066/8c9c97a1-a78a-4730-b154-6995014ac9ce)

![image](https://github.com/victorvsanchez/ncm-product-type-classifier/assets/43478066/e4f0b579-f36d-48c6-ab8b-b504dcf9f1db)

![image](https://github.com/victorvsanchez/ncm-product-type-classifier/assets/43478066/ac93482a-99b7-4e6b-bf66-d5c35f3590a7)

### Metrics reached

![image](https://github.com/victorvsanchez/ncm-product-type-classifier/assets/43478066/f5ec9076-340f-4c2f-a40d-a6c9017a458b)
