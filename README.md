<h1 align="left">
  <code>🏠 Smart Home Security System</code>
</h1>
<p align="left">
    <strong>Wireless Home Security and Home Automation with SmartInternz, based on the Internet of Things.</strong>
</p>
<p align="left">
    <img style="margin: 0 0 0 60px" src="assets/images/home-security-banner.jpg" alt="home security banner"/>
</p>
<h2 align="left" style="font-weight:bold">🔒 Project Description</h2>
<p align="left">
Wireless Home security and Home automation are the dualaspects of this project. The currently built prototype of the system sends alerts to the owner over voice calls using the Internet if any sort of human movement is sensed near the entrance of his house and raises an alarm optionally upon the user’s discretion. The provision for sending alert messages to concerned security personnel in case of critical situation is also built into the system. On the other hand if the owner identiﬁes that the person may entering his house is not an intruder but an unexpected guest of his then instead of triggering the security alarm, the user/owner can make arrangements such as opening the door, switching on various appliances inside the house, which are also connected and controlled by the IBM Cloud/IBM IOT Platform in the system to welcome his guest.
</p>
<h2 align="left" style="font-weight:bold">🛠️ Skills Required</h2>
  
* **Python**
* **Python For Data Visualization**
* **IOT Open Hardware Platforms**
* **IOT Application Development**
* **IOT Cloud Platform**
* **IOT Communication Technologies**
* **IOT Communication Protocols**

<h1 align="left" style="font-weight:bold">🏗 Structure</h1>

🌟 Star the project to bookmark and appreciate the work.

## 📚 Libraries used

```py
# module supplies classes for manipulating dates and times
import datetime

# library provides complete access to the IBM® Cloud Object Storage API. Endpoints, an API key, and the instance ID must be specified during creation of a service resource or low-level client
import ibm_boto3
from ibm_botocore.client import Config, ClientError

# module import name for opencv-python
import cv2

# Python Client for IBM Watson IoT Platform
import ibmiotf.device

# Python package stands for 'Numerical Python'
import numpy as np

# Python module provides various functions and variables that are used to manipulate different parts of the Python runtime environment
import sys

# Python module provides various time-related functions
import time

# Python Client for IBM Cloud database service
from cloudant.client import Cloudant
```
## 💻 Web Preview

https://user-images.githubusercontent.com/75872316/147149737-ae534151-03c6-458d-8b33-548ef0c6aab4.mp4

## 👨‍💻 Backend Setup

```py
# Provide your IBM Watson Device Credentials
device_options = {"org": organization,
                  "type": device_type,
                  "id": device_id,
                  "auth-method": auth_method,
                  "auth-token": auth_token
                  }
```

```py
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
```

<h2 align="left" style="font-weight:bold">🌈 Contributors</h2>
<p align="left">
</p>
<p align="left">
<a href="https://github.com/SmartPracticeschool/SPS-7891-Smart-Security-System-for-Homes/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=SmartPracticeschool/SPS-7891-Smart-Security-System-for-Homes" />
</a>
</p>
<h2 align="left" style="font-weight:bold">📰 Certification</h2>

> To Visit Certificate from **SmartBridge - IBM**, <a href = "https://smartinternz.com/badge_projects/certificates/0deb1c54814305ca9ad266f53bc82511"> Click Here</a> 👈
>
> **Developed &amp; maintained by the [@amino19](https://github.com/amino19). Copyright 2021 © amino19.**
