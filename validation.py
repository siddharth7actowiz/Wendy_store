from pydantic import BaseModel, field_validator
from typing import Optional
import json

class Store(BaseModel):
    Name:  str
    Map:   str
    StreetAddress: str
    City:  str
    State: str
    Country: str
    Pincode:  str       
    Phone_Number: str
    Restaurant_Hours:str          
    DriveThru_Hours: str          
    DeliveryOption:  str          
    CurrentlyOperating: str          
           

    @field_validator('Pincode', mode='before')
    @classmethod
    def pincode_to_str(cls, v):
        return str(v).strip() if v else ""

    @field_validator('Restaurant_Hours', 'DriveThru_Hours', 'DeliveryOption', 'CurrentlyOperating', mode='before')
    @classmethod
    def serialize_to_json(cls, v):
        if isinstance(v, (dict, list)):
            return json.dumps(v)   # ← auto converts dicts/lists to JSON string
        return v or ""

    @field_validator('*', mode='before')
    @classmethod
    def empty_str_default(cls, v):
        if isinstance(v, str):
            return v.strip() or ""
        return v