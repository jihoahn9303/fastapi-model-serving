import os
import json
from contextlib import asynccontextmanager
from typing import AsyncGenerator

import pandas as pd
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import FastAPI
from mlflow.pyfunc import load_model

from database.database_setting import get_db
from database.model import Metrics, ModelVersions


ML_MODELS = {}


class InferenceRequest(BaseModel):
    sentence: str = Field(min_length=1, max_length=150)


# Get URL for model which shows the highest performance
async def get_model_url(db: AsyncSession) -> str:
    result = await db.execute(
        select(ModelVersions.source)\
            .join(Metrics, ModelVersions.run_id == Metrics.run_uuid)\
            .order_by(Metrics.value.desc())\
            .limit(1)
    )
    model_url = result.scalar_one()
    
    return model_url

# Define the code that should be executed before the application starts up
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Get Database session
    db_gen: AsyncGenerator[AsyncSession] = get_db()
    db: AsyncSession = await db_gen.__anext__()
    
    # Get model URL in Google Cloud Storage
    print("Get model URL from Google Cloud SQL!")
    model_url = await get_model_url(db)
    
    # Load the model from URL
    print("Start loading model to local environment!")
    
    model = load_model(model_uri=model_url)
    unwrapped_model = model.unwrap_python_model()
    ML_MODELS["senti_model"] = unwrapped_model
    
    print("Finish loading model to local environment!")  
    yield
    
    # Clean up the ML models and release the resources
    ML_MODELS.clear()
    
    
app = FastAPI(lifespan=lifespan)


@app.post("/inference")
async def inference(request: InferenceRequest) -> dict:
    # parsing input sentence from POST method
    request_dict  = request.model_dump()
    sentence = request_dict["sentence"]
    
    df = pd.DataFrame(data=[[sentence]], columns=["review"])
    
    # predict sentiment using model
    prediction = ML_MODELS["senti_model"].custom_predict(input_df=df)
    prediction = list(map(lambda x: 'positive' if x == 0 else 'negative', prediction))
    
    return {"result": prediction}
    
    