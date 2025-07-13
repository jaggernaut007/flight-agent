from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import date

class FlightQuery(BaseModel):
    departure_id: str = Field(..., description="Departure airport code or kgmid")
    arrival_id: str = Field(..., description="Arrival airport code or kgmid")
    departure_date: date = Field(..., description="Departure date (YYYY-MM-DD)")
    return_date: Optional[date] = Field(None, description="Return date (YYYY-MM-DD), required for round-trip")
    type: Optional[int] = Field(None, description="Flight type: 1=round-trip, 2=one-way, 3=multi-city")
    gl: Optional[str] = Field(None, description="Country code (optional)")
    hl: Optional[str] = Field(None, description="Language code (optional)")
    currency: Optional[str] = Field(None, description="Currency code (optional)")

    @validator('departure_id', 'arrival_id')
    def airport_code_or_kgmid(cls, v):
        if not v or (len(v) != 3 and not v.startswith('/m/')):
            raise ValueError('Must be a 3-letter airport code or kgmid starting with /m/')
        return v

    @validator('departure_date')
    def valid_date(cls, v):
        if v < date.today():
            raise ValueError('Date must not be in the past')
        return v

    @validator('return_date', always=True)
    def validate_return_date(cls, v, values):
        t = values.get('type')
        dep = values.get('departure_date')
        if t == 1:
            if v is None:
                raise ValueError('return_date is required for round-trip (type=1)')
            if dep and v <= dep:
                raise ValueError('return_date must be after departure_date')
        if t == 2 and v is not None:
            raise ValueError('return_date must not be set for one-way (type=2)')
        return v

