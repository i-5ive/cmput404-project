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

    # Kind of a dangerous function
    @staticmethod
    def get_auth_tuple_for_host(host):
        try:
            if host.endswith("/"): host = host[:-1] # we store it without the ending slash
            server = Server.objects.get(base_url=host)
            auth = (server.fetching_username, server.fetching_password)
            return auth
        except:
            print("Auth not found for", host, "has a server user been created?")
            return ("", "")

    # Only necessary if a local user is friending an external one
    @staticmethod
    def notify_server_of_friendship(body):
        try:
            url = body["friend"]["host"]
            if not url.endswith("/"):
                url += "/"
            auth = ServerUtil.get_auth_tuple_for_host(url)
            url += "friendrequest"
            print("body:", body)
            headers={"Content-type": "application/json"}
            resp = requests.post(url, data=json.dumps(body), auth=auth, headers=headers)
            return resp.status_code == 200
        except Exception as e:
            print(e)
            return False
