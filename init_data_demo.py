# ------------ init brokers data only once -----------

import requests

baseURL: str = 'http://127.0.0.1:8000'  # broker-manager


# initdata
def brokers_initdata(data):
    response = requests.post(f'{baseURL}/init-brokers-data', json=data)
    print(response.json())


data = {
    "broker_data": [
        {
            "broker_address": "http://127.0.0.1:9000",
            "hostname": "broker1"
        },
        {
            "broker_address": "http://127.0.0.1:9001",
            "hostname": "broker2"
        },
        {
            "broker_address": "http://127.0.0.1:9002",
            "hostname": "broker3"
        },
        {
            "broker_address": "http://127.0.0.1:9003",
            "hostname": "broker4"
        }
    ]
}


brokers_initdata(data)
