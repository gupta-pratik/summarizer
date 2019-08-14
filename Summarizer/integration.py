import requests


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
        access_token = data["access_token"]
        print("Acess token::: ", access_token)
        return access_token

    def add_task_to_podio(self,task_list):
        headers = {
            "Content-Type":"application/json",
            "Authorization": "OAuth2 " + self.access_token
        }
        for task in task_list:
            body = {
                "text": task,
                "description": task
            }
            r = requests.post(url=self.create_task_url, headers=headers , body= body)
            print("Task created:: ", r)


