# api/main.py
from fastapi import FastAPI
from fastapi import Request
from pydantic_settings import BaseSettings
from influx import InfluxDBManager
import paho.mqtt.client as mqtt
import json
from models import SensorReading
from notifications import notify_if_anomaly
from time import sleep
import requests

class Settings(BaseSettings):
    mqtt_broker: str
    mqtt_port: int
    mqtt_ca: str
    mqtt_cert: str
    mqtt_key: str
    influx_url: str
    influx_token: str
    influx_org: str
    influx_bucket: str
    anomaly_thresholds: dict 
    webhook_url: str

    class Config:
        env_file = ".env"

settings = Settings()
app = FastAPI()
influx = InfluxDBManager(settings.influx_url, settings.influx_token,
                         settings.influx_org, settings.influx_bucket)

def on_mqtt_message(client, userdata, msg):
    data = json.loads(msg.payload)
    lectura = SensorReading(**data)  # validación
    influx.write_data(
        measurement=msg.topic.replace("/", "_"),
        tags={"sensor": msg.topic},
        fields=lectura.dict(exclude={"timestamp"})
    )
    notify_if_anomaly(lectura, settings)

@app.on_event("startup")
def startup_event():
    client = mqtt.Client()
    client.tls_set(settings.mqtt_ca, settings.mqtt_cert, settings.mqtt_key)
    client.on_message = on_mqtt_message
    client.connect(settings.mqtt_broker, settings.mqtt_port)
    client.subscribe("salud/#")
    client.loop_start()

@app.get("/datos/")
async def get_all_data():
    # lee de Influx o de memoria, según diseño
    return {"status": "OK"}

@app.post("/datos/")
async def receive_data(lectura: SensorReading):
    influx.write_data(
        measurement="salud",
        tags={"sensor": "wearable"},
        fields=lectura.dict(exclude={"timestamp"})
    )
    notify_if_anomaly(lectura, settings)
    return {"status": "dato recibido"}