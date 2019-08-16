import requests
from flask import jsonify
import json
from datetime import datetime


class PodioIntegration(object):

    auth_url = "https://podio.com/oauth/token"
    access_token = ""
    client_id = "smart-meeting-assistance"
    client_secret = "OYj6QD6F8KP7P0Z7eGPTiWeaym9SnwHIBqf6Pvi4jE6ZtZur51gz2RBvNm1WYyuq"
    create_task_url = "https://api.podio.com/task/"

    def __init__(self, username, password):
        PARAMS = {
            "grant_type": "password",
            "client_id": self.client_id,
            "redirect_uri": "01feef49.ngrok.io",
            "client_secret": self.client_secret,
            "Content - Type": "application/x-www-form-urlencoded",
            "username": username,
            "password": password
        }
        r = requests.post(url=self.auth_url, params=PARAMS)
        data = r.json()
        PodioIntegration.access_token = data["access_token"]
        print("Acess token::: ", PodioIntegration.access_token)

    def add_task_to_podio(self,task_list):
        headers = {
            "Content-Type":"application/json",
            "Authorization": "OAuth2 " + PodioIntegration.access_token
        }
        tasks = []
        for task in task_list:
            body = {
                "text": task,
                "description": "Created By SAM"
            }
            print(headers)
            print(body)
            response = requests.post(url=self.create_task_url, headers=headers , data= json.dumps(body))
            if response.status_code == 200:
                task = response.json()
                print(task)
                tasks.append({
                    "task_name": task["text"],
                    "description": "Created By SAM",
                    "link": task["link"]
                })
            #print("Task created:: ", response.content)
        print("Tasks created::" , tasks)
        return tasks


class CWSIntegration:
    notification_ws_url = "https://api.analytics-staging.cloud.com/casvc/broadcasts/ctxana/v1/cas/broadcasts/IWS.MicroApps/broadcasts/dsconfigdata"
    authorization_header = "CWSAuth service=RE9zTnZyZVNKd2hyL2szdDM0UXFRUHROaTBXZTZvYkcwb1MycXFLZ1NVWUUrM0MzSFY0WWRpQkVRWXVGOWNWcGxDQjVoR2xpNHhOZUg1bm9IS2hPZkZ3QUhwWUNFQURMbmZUOENPN2RSelRjaElpUzlaa05uV3dUR2VuRWFaZWI5blM1RHpQaDlDMFE2aUpzV1hRcXFqK3hCN2Fmb201L2tycWdhMU9saHUvVHFQcklEd3o0SmpkNy8zQ1pCMlRtRE5pMzE4cnBiNUNTZVp4MkVlcHlxN2R3ODV5aEdSSWN6cXpubnMxZTJQclRHM3VQTFFaMTl1eVl1czdlaVU1RzZGT3hHQlV5ajVhYWhwZ3dpRExJSGsxeDdUWjBxVXBwbFNXaFFNWkpPR3NZTVFpNXpVM0tWQmJsNVpoSWJYMEJ5U1RXbmpLaXVoaDdsYi8za0NkT1JRPT07c2FtcGxlLXNlcnZpY2U="
    event_hub_endpoint = ""
    event_hub_token = ""

    def __init__(self):
        res = requests.post(CWSIntegration.notification_ws_url, headers = {"Authorization": CWSIntegration.authorization_header})
        print(res.content)
        data = res.json()
        CWSIntegration.event_hub_endpoint = data["eventHubEndpoint"]
        CWSIntegration.event_hub_token = data["eventHubToken"]

    def push_notification(self,tasks, summary):
        print("Tasks:: ", tasks)
        for task in tasks:
            print("Printing title:", task["task_name"]+ " $$ " + task["link"])
            body = {
              "ver": 1,
              "id": "a5c6c589-ce2c-4c34-9415-87bc9888c540",
              "st": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
              "prod": "IWS.MicroApps",
              "prodVer": "0.4.0",
              "type": "NOTIFICATION",
              "tenant": {
                "id": "broadcasts"
              },
              "$schema": "https://cas.citrix.com/schemas/event.json",
              "payload": {
                "title": {
                  "en": task["task_name"]+ " $$ " + task["link"]
                },
                "body": {
                  "en": json.dumps(summary)
                },
                "iconUrl": "https://cdn.iconscout.com/icon/free/png-256/podio-1-569562.png",
                "source": {
                  "origin": "BROADCAST",
                  "notification": {
                    "id": "1",
                    "label": {
                      "en": "title"
                    }
                  },
                  "app": {
                    "id": "1",
                    "title": {
                      "en": "SAM"
                    },
                    "iconUrl": "https://sf-region.sharefilestaging.com/assets/broadcast/images/citrix-workspace.png"
                  }
                },
                "detail": {
                  "appId": "1",
                  "pageId": "12",
                  "recordId": "5d30115a69d6ca0001176f73",
                  "url": "https://sf-region.sharefilestaging.com/assets/broadcast/mobile-view/index.html?RecordId=5d30115a69d6ca0001176f73"
                },
                "media": [],
                "actions": [],
                "sendTo": [
                  {
                    "channel": "FEED",
                    "recipients": [
                      {
                        "oid": "OID:/ad/broadcasts:610ea094-5263-427c-bdc6-1124da1ee513",
                        "type": "USER"
                      }
                    ]
                  }
                ]
              }
            }
            print(">>>>>>>>>>>>PRAT>>>>>>>>>>")
            print(json.dumps(body))
            res = requests.post(CWSIntegration.event_hub_endpoint, headers = {"Authorization": CWSIntegration.event_hub_token},
                      data= json.dumps(body))
            print(res)