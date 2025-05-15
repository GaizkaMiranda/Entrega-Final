# api/influx.py
from influxdb_client import InfluxDBClient, Point, WritePrecision
from datetime import datetime

class InfluxDBManager:
    def __init__(self, url, token, org, bucket):
        self.client = InfluxDBClient(url=url, token=token, org=org)
        self.write_api = self.client.write_api()
        self.org = org
        self.bucket = bucket

    def write_data(self, measurement, tags, fields):
        point = Point(measurement)
        for key, value in tags.items():
            point = point.tag(key, value)
        for key, value in fields.items():
            point = point.field(key, value)
        point = point.time(datetime.utcnow(), WritePrecision.NS)
        self.write_api.write(bucket=self.bucket, org=self.org, record=point)
