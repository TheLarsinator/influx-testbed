from datetime import datetime

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# You can generate an API token from the "API Tokens Tab" in the UI
token = "74iSI77607iR7juwbeHmWLMHI5YwqixApVTVgJAgj8OyoCcSZssZrXQg1SOxk6ejq6k39WD0Attsq16KGjmRrQ=="
org = "Root"
host = "http://localhost:8086"
bucket = "ImportedTelemetry"

with InfluxDBClient(url=host, token=token, org=org) as client:
    query_api = client.query_api()

    data_frame = query_api.query_data_frame('from(bucket: "PlayBucket")'
                                            '|> range(start: 2019-08-11T14:00:00.000Z, stop: 2019-08-11T15:00:00.000Z)'
                                            '|> filter(fn: (r) => r["log"] == "FSG Endurance 2019")'
                                            '|> filter(fn: (r) => r["_measurement"] == "vcu.INS")'
                                            '|> filter(fn: (r) => r["_field"] == "vx")'
                                            '|> group(columns: ["lap"], mode: "by")'
                                            '|> mean(column: "_value")')
    
    print(data_frame.to_string())