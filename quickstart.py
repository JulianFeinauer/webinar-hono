import json
import threading
from urllib.parse import urlparse

import requests
import uamqp
from paho.mqtt.publish import single
from requests.auth import HTTPBasicAuth
from uamqp import authentication

registryIp = "hono.eclipseprojects.io"
httpAdapterIp = "hono.eclipseprojects.io"
mqttAdapterIp = "hono.eclipseprojects.io"
amqpNetworkIp = "hono.eclipseprojects.io"

# Register Tenant
tenant = requests.post(f'http://{registryIp}:28080/v1/tenants').json()
tenantId = tenant["id"]

print(f'Registered tenant {tenantId}')

# Add Device to Tenant
device = requests.post(f'http://{registryIp}:28080/v1/devices/{tenantId}').json()
deviceId = device["id"]

print(f'Registered device {deviceId}')

# Set Device Password
devicePassword = "my-secret-password"

code = requests.put(f'http://{registryIp}:28080/v1/credentials/{tenantId}/{deviceId}',
                    headers={'content-type': 'application/json'},
                    data=json.dumps(
                        [{"type": "hashed-password", "auth-id": deviceId, "secrets": [{"pwd-plain": devicePassword}]}]))

if code.status_code == 204:
    print("Password is set!")
else:
    print("Unnable to set Password")

# Now we can start the client application
print("Start Hono Client now...")
print()
cmd = f'java -jar hono-cli-*-exec.jar --hono.client.host={amqpNetworkIp} ' \
    f'--hono.client.port=15672 --hono.client.username=consumer@HONO ' \
    f'--hono.client.password=verysecret --spring.profiles.active=receiver ' \
    f'--tenant.id={tenantId}'
print(cmd)
print()

# input("Press Enter to continue...")




def thread_function(name):
    while True:
        uri = "amqp://" + amqpNetworkIp + ":15672/telemetry/" + tenantId
        parsed_url = urlparse(uri)
        try:
            message = uamqp.receive_message(uri, auth=authentication.SASLPlain(parsed_url.hostname, "consumer@HONO", "verysecret"))
            print(message)
        except Exception as e:
            pass



x = threading.Thread(target=thread_function, args=(1,), daemon=True)
x.start()







# Send HTTP Message
print("Send Telemetry Message via HTTP")
response = requests.post(f'http://{httpAdapterIp}:8080/telemetry', headers={"content-type": "application/json"},
                         data=json.dumps({"temp": 5, "transport": "http"}),
                         auth=HTTPBasicAuth(f'{deviceId}@{tenantId}', f'{devicePassword}'))

if response.status_code == 202:
    print("HTTP sent successful")

# Send Message via MQTT
print("Send Telemetry Message via MQTT")
single("telemetry", payload=json.dumps({"temp": 17, "transport": "mqtt"}),
       hostname=mqttAdapterIp,
       auth={"username": f'{deviceId}@{tenantId}', "password": devicePassword})
