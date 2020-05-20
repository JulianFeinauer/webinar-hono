# Eclispe Hono Quickstart tutorial

Note: This tutorial follows the Tutorial from the official homepage https://www.eclipse.org/hono/getting-started/.

## Preparations

Download the Eclipse Hono CLI from the Homepage: https://www.eclipse.org/hono/downloads/.

## Tutorial

First, start the script `quickstart.py`.

Then, the Script will do all HTTP calls to setup a tenant in the Public Hono Sandbox. After that it will print out the command to start the java CLI with appropriate url parameters.
This should look like

```
java -jar hono-cli-*-exec.jar --hono.client.host=hono.eclipseprojects.io --hono.client.port=15672 --hono.client.username=consumer@HONO --hono.client.password=verysecret --spring.profiles.active=receiver --tenant.id=6ff207e0-e638-44ea-acb7-ea6fc4950cd3
``` 

*Important*: Please do not use above command but copy the one from your terminal!

Go to the folder where you stored the java CLI and execute the command via terminal.

Then, go back to the Terminal running the quickstart script and press enter.

This should now

* Send a Telemetry message via HTTP API
* Send a Telemetry message via MQTT API

Both should be visible in the java CLI which receives the messages via AMQP.
The output from the java CLI should look something like

```
13:15:07.513 [vert.x-eventloop-thread-0] INFO  org.eclipse.hono.cli.app.Receiver - received telemetry message [device: c8974e16-2400-4fcf-aa60-d8adc53039b4, content-type: application/json]: {"temp": 5, "transport": "http"}
13:15:07.513 [vert.x-eventloop-thread-0] INFO  org.eclipse.hono.cli.app.Receiver - ... with application properties: {orig_adapter=hono-http, device_id=c8974e16-2400-4fcf-aa60-d8adc53039b4, orig_address=/telemetry, JMS_AMQP_CONTENT_TYPE=application/json}
13:15:08.056 [vert.x-eventloop-thread-0] INFO  org.eclipse.hono.cli.app.Receiver - received telemetry message [device: c8974e16-2400-4fcf-aa60-d8adc53039b4, content-type: application/octet-stream]: {"temp": 17, "transport": "mqtt"}
13:15:08.056 [vert.x-eventloop-thread-0] INFO  org.eclipse.hono.cli.app.Receiver - ... with application properties: {orig_adapter=hono-mqtt, device_id=c8974e16-2400-4fcf-aa60-d8adc53039b4, orig_address=telemetry, JMS_AMQP_CONTENT_TYPE=application/octet-stream}
```
