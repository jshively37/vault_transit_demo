from pydantic import BaseModel
from pymongo import MongoClient
from fastapi import FastAPI, status
from typing import Optional

app = FastAPI()
# client = MongoClient()
DB = "network_devices"
MSG_COLLECTION = "common"


class UpdateCommon(BaseModel):
    snmp_string: Optional[str]
    class Config:
        schema_extra = {
            "example": {
                "snmp_string": "abcdefg"
            }
        }

@app.get("/status")
def get_status():
    """Get status of messaging server."""
    return {"status": "running"}


@app.post("/common", status_code=status.HTTP_201_CREATED)
def post_common():
    with MongoClient as client:
        msg_collection = client[DB][MSG_COLLECTION]
        result = msg_collection.insert_one({"test": "test"})
        ack = result.acknowledged
        return {"insertion": ack}

@app.get("/common")
def get_common():
    with MongoClient as client:
        msg_collection = client[DB][MSG_COLLECTION]
        return msg_collection.distinct("channel")
