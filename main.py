from typing import Annotated

import pandas as pd
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import FastAPI, Depends 
from mlflow.pyfunc import load_model

from database import get_db
from model import Metrics, ModelVersions


app = FastAPI()


class InferenceRequest(BaseModel):
    sentence: str = Field(min_length=1, max_length=150)


# @app.get("/model_url")
# async def get_model_url(db: AsyncSession = Depends(get_db)) -> str:
#     result = await db.execute(
#         select(ModelVersions.source)\
#             .join(Metrics, ModelVersions.run_id == Metrics.run_uuid)\
#             .order_by(Metrics.value.desc())\
#             .limit(1)
#     )
#     model_url = result.scalar_one()
#     return model_url


async def get_model_url(db: AsyncSession) -> str:
    result = await db.execute(
        select(ModelVersions.source)\
            .join(Metrics, ModelVersions.run_id == Metrics.run_uuid)\
            .order_by(Metrics.value.desc())\
            .limit(1)
    )
    model_url = result.scalar_one()
    
    return model_url


@app.post("/inference")
async def inference(
    request: InferenceRequest,
    db: Annotated[AsyncSession, Depends(get_db)]
) -> dict:
    request_dict  = request.model_dump()
    sentence = request_dict["sentence"]
    
    model_url = await get_model_url(db)
    
    model = load_model(model_uri=model_url)
    unwrapped_model = model.unwrap_python_model()
    
    df = pd.DataFrame(data=[[sentence]], columns=["review"])
    
    prediction = unwrapped_model.custom_predict(input_df=df)
    prediction = list(map(lambda x: 'positive' if x == 0 else 'negative', prediction))
    
    return {"result": [prediction]}
    
    