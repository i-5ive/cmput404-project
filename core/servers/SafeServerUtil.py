from core.servers.models import Server
import json
import requests

class ServerUtil:
    @staticmethod
    def is_server(user):
        try:
            return user.server.is_server()
        except:
            return False

    @staticmethod
    def is_author(user):
        try:
            return not user.author.is_server()
        except:
            return False

    # function is __mangled, as it is unsafe (throws exceptions)
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
            resp = requests.post(url, data=json.dumps(body), auth=auth)
            print(resp.json())
            return resp.json()["success"] == True
        except Exception as e:
            print(e)
            return False
