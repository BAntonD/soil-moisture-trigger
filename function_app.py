import azure.functions as func
import datetime
import json
import logging

import json
import os
from azure.iot.hub import IoTHubRegistryManager
from azure.iot.hub.models import CloudToDeviceMethod

app = func.FunctionApp()

@app.event_hub_message_trigger(arg_name="azeventhub", event_hub_name="eventhubname",
                               connection="EventHubConnectionString") 
def eventhub_trigger(azeventhub: func.EventHubEvent):
    # Парсимо повідомлення з тіла події
    body = json.loads(azeventhub.get_body().decode('utf-8'))
    device_id = azeventhub.iothub_metadata['connection-device-id']
    logging.info(f'Received message: {body} from {device_id}')
    
    # Отримуємо значення вологості ґрунту
    soil_moisture = body.get('soil_moisture')

    # Перевіряємо значення вологості і формуємо метод для пристрою
    if soil_moisture is not None:
        if soil_moisture > 162:
            direct_method = CloudToDeviceMethod(method_name='relay_on', payload='{}')
        else:
            direct_method = CloudToDeviceMethod(method_name='relay_off', payload='{}')

        logging.info(f'Sending direct method request for {direct_method.method_name} for device {device_id}')

        # Підключення до IoT Hub і виклик методу для пристрою
        registry_manager_connection_string = os.environ['REGISTRY_MANAGER_CONNECTION_STRING']
        registry_manager = IoTHubRegistryManager(registry_manager_connection_string)

        # Виклик методу для пристрою
        registry_manager.invoke_device_method(device_id, direct_method)
        logging.info('Direct method request sent!')
    else:
        logging.error('Soil moisture value is missing in the message.')

"""
@app.event_hub_message_trigger(arg_name="azeventhub", event_hub_name="eventhubname",
                               connection="EventHubConnectionString") 
def eventhub_trigger(azeventhub: func.EventHubEvent):
    body = json.loads(azeventhub.get_body().decode('utf-8'))
    device_id = azeventhub.iothub_metadata['connection-device-id']
    logging.info(f'Received message: {body} from {device_id}')

    soil_moisture = body['soil_moisture']
    if soil_moisture > 162:
        direct_method = CloudToDeviceMethod(method_name='relay_on',
        payload='{}')
    else:
        direct_method = CloudToDeviceMethod(method_name='relay_off',
        payload='{}')

    logging.info(f'Sending direct method request for {direct_method.method_name} for device {device_id}')
    registry_manager_connection_string = os.environ['REGISTRY_MANAGER_CONNECTION_STRING']
    registry_manager = IoTHubRegistryManager(registry_manager_connection_string)

    registry_manager.invoke_device_method(device_id, direct_method)
    logging.info('Direct method request sent!')
"""