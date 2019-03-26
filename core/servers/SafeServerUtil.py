from core.servers.models import Server
import json
import requests

class ServerUtil:
    # Ensure you use a USER object, or it will probably return incorrectly
    @staticmethod
    def is_server(user):
        try:
            return user.server.is_server
        except:
            return False

    # Ensure you use a USER object, or it will probably return incorrectly
    @staticmethod
    def is_author(user):
        try:
            return not user.server.is_server
        except:
            return True

    @staticmethod
    def get_base_url_from_user(user):
        try:
            return user.server.base_url
        except:
            print("Server URL not found, check user:", user)
            return ""

    # Kind of a dangerous function
    @staticmethod
    def get_server_auth_from_user(user):
        try:
            return (user.server.fetching_username, user.server.fetching_password)
        except:
            print("Server auth not found, check user:", user)
            return ("", "")

    # Only necessary if a local user is friending an external one
    # User is required to get the host from the server object
    @staticmethod
    def notify_server_of_friendship(user, body):
        try:
            url = ServerUtil.get_base_url_from_user(user) + "/friendrequest"
            auth = ServerUtil.get_server_auth_from_user(user)
            print(url, auth, body)
            headers={"Content-type": "application/json"}
            resp = requests.post(url, data=json.dumps(body), auth=auth, headers=headers)
            return resp.status_code == 200
        except Exception as e:
            print(e)
            return False
