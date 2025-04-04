import sys
import os

import certifi
# ca = certifi.where()

from dotenv import load_dotenv
# load_dotenv()
# mongo_db_url = os.getenv("MONGODB_URL_KEY")
# print(mongo_db_url)
import pymongo
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.pipeline.training_pipeline import TrainingPipeline

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile,Request
from uvicorn import run as app_run
from fastapi.responses import Response
from starlette.responses import RedirectResponse
import pandas as pd

from networksecurity.utils.main_utils.utils import load_object

from networksecurity.utils.ml_utils.model.estimator import NetworkModel


# client = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca)

from networksecurity.constant.training_pipeline import DATA_INGESTION_COLLECTION_NAME
from networksecurity.constant.training_pipeline import DATA_INGESTION_DATABASE_NAME

# database = client[DATA_INGESTION_DATABASE_NAME]
# collection = database[DATA_INGESTION_COLLECTION_NAME]

from fastapi.templating import Jinja2Templates
templates=Jinja2Templates(directory="./templates")

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/",tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")

# @app.get("/train")
# async def train_route():
#     try:
#         train_pipeline=TrainingPipeline()
#         train_pipeline.run_pipeline()
#         # return Response("Training of model is successfull")
#         pass
#     except Exception as e :
#         raise NetworkSecurityException(e,sys)

@app.post("/predict")
async def predict_route(request: Request, file: UploadFile = File(...)):
    try:
        # Read the uploaded CSV file into a DataFrame
        df = pd.read_csv(file.file)
        
        # Load preprocessor and model
        preprocessor = load_object("D:/Work/NLP & ML/NetworkSecurity/final_model/preprocessor.pkl")
        final_model = load_object("D:/Work/NLP & ML/NetworkSecurity/final_model/model.pkl")

        # Create model instance and predict
        network_model = NetworkModel(preprocessor=preprocessor, model=final_model)
        y_pred = network_model.predict(df)
        
        # Add predictions to DataFrame
        df['predicted_column'] = y_pred
        
        # Save predictions to a CSV file
        output_path = "D:/Work/NLP & ML/NetworkSecurity/prediction_output.csv"
        df.to_csv(output_path, index=False)

        # Convert DataFrame to an HTML table
        table_html = df.to_html(classes='table table-striped')

        return templates.TemplateResponse("table.html", {"request": request, "table": table_html})

    except Exception as e:
        return {"error": str(e)}

if __name__=="__main__":
    app_run(app,host="localhost",port=8000)