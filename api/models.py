# api/models.py
from pydantic import BaseModel
from datetime import datetime

class SensorReading(BaseModel):
    ritmo: float
    oxigeno: float  # porcentaje de oxígeno en sangre
    temperatura: float
    timestamp: datetime
