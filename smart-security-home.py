# -*- coding: utf-8 -*-

import os
import cv2
import sys
import time

import datetime

# IBM cloud modules
import ibm_boto3
import ibmiotf.device
from dotenv import load_dotenv
from ibm_botocore.client import Config, ClientError
from cloudant.client import Cloudant

# Custom modules
from commands import myCommandCallback
from config import config


def multi_part_upload(bucket_name, item_name, file_path):

    try:
        print("Starting file transfer for {0} to bucket: {1}\n".format(item_name, bucket_name))
        
        part_size = 1024 * 1024 * 5  # set 5 MB chunks
        file_threshold = 1024 * 1024 * 15  # set threshold to 15 MB

        # set the transfer threshold and chunk size
        transfer_config = ibm_boto3.s3.transfer.TransferConfig(
            multipart_threshold=file_threshold,
            multipart_chunksize=part_size
        )

        with open(file_path, "rb") as file_data:
            cos.Object(bucket_name, item_name).upload_fileobj(
                Fileobj=file_data,
                Config=transfer_config
            )
            
        print("Transfer for {0} Complete!\n".format(item_name))

    except ClientError as be:
        print("CLIENT ERROR: {0}\n".format(be))

    except Exception as e:
        print("Unable to complete multi-part upload: {0}".format(e))


def get_connections(organization, device_type, device_id, auth_method, auth_token):

    try:
        device_options = {"org": organization,
                          "type": device_type,
                          "id": device_id,
                          "auth-method": auth_method,
                          "auth-token": auth_token
                          }
        deviceCli = ibmiotf.device.Client(device_options)

    except Exception as e:
        print("Caught exception connecting device: %s" % str(e))
        sys.exit()

    client = Cloudant(os.environ['CLOUDANT_USERNAME'], os.environ['SERVICE_PASSWORD'], url=os.environ['SERVICE_URL'])
    return client, deviceCli


if __name__ == '__main__':

    load_dotenv()
    DEVICE_TYPE = os.environ['device_type']
    DEVICE_ID = os.environ['device_id']
   
    AUTH_TOKEN = os.environ['auth_token']
    AUTH_METHOD = os.environ['auth_method']
    ORGANIZATION = os.environ['organization']

    # Current list available at "https://control.cloud-object-storage.cloud.ibm.com/v2/endpoints"
    COS_ENDPOINT = os.environ['cos_endpoint']
    COS_API_KEY_ID = os.environ['cos_api_key_id']   # eg "W00YiRnLW4a3fTjMB-oiB-2ySfTrFBIQQWanc--P3byk"
    COS_AUTH_ENDPOINT = os.environ['cos_auth_endpoint']
    COS_RESOURCE_CRN = os.environ['cos_resource_crn']

    video = cv2.VideoCapture(config['video_path'])
    face_classifier = cv2.CascadeClassifier(config['model_path'])
    
    client, device_cli = get_connections(ORGANIZATION, DEVICE_TYPE, DEVICE_ID, AUTH_METHOD,  AUTH_TOKEN)

    client.connect()
    device_cli.connect()

    # Create resource
    cos = ibm_boto3.resource("s3",
                             ibm_api_key_id=COS_API_KEY_ID,
                             ibm_service_instance_id=COS_RESOURCE_CRN,
                             ibm_auth_endpoint=COS_AUTH_ENDPOINT,
                             config=Config(signature_version="oauth"),
                             endpoint_url=COS_ENDPOINT
                             )
    while True:
        check, frame = video.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_classifier.detectMultiScale(gray, 
                                                 config['face_classifier_scaleFactor'],
                                                 config['face_classifier_minNeighbors']
                                                 )

        # drawing rectangle boundaries for the detected face
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.imshow('Face detection', frame)

            pic_name = datetime.datetime.now().strftime("%y-%m-%d-%H-%M")
            pic_name = pic_name + ".jpg"

            pic = datetime.datetime.now().strftime("%y-%m-%d-%H-%M")
            cv2.imwrite(pic_name, frame)

            person = 1

            my_database = client.create_database(config['cloudant_db'])

            multi_part_upload("safetydetectors1910", pic_name, pic + ".jpg")

            if my_database.exists():
                print("'{CLOUDANT_DB}' successfully created.")

                json_document = {
                    "_id": pic,
                    "link": "https://safetydetectors1910.s3.jp-tok.cloud-object-storage.appdomain.cloud/" + pic_name
                }

                new_document = my_database.create_document(json_document)

                if new_document.exists():
                    print("Document '{new_document}' successfully created.")

            time.sleep(1)

            t = 34  # temperature
            h = 45  # humidity
            data = {"d": {'temperature': t, 'humidity': h, 'person': person}}

            def myOnPublishCallback():
                print("Published data to IBM Watson")

            success = device_cli.publishEvent("Data", "json", data, qos=0, on_publish=myOnPublishCallback)

            if not success:
                print("Not connected to IoTF")

            time.sleep(1)
            device_cli.commandCallback = myCommandCallback
            person = 0
            Key = cv2.waitKey(1)

            if Key == ord('q'):
                video.release()
                cv2.destroyAllWindows()
                break

    deviceCli.disconnect()