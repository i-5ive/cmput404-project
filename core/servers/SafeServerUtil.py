from core.servers.models import Server
import json
import requests

class ServerUtil:
    # Init function allows you pass in variables related to the server to
    # try and find its related server object
    def __init__(self, server=None, url=None, authorUrl=None):
        self.__server = None
        self.__checked_validity = False
        if server and ServerUtil.is_server(server):
            self.__server = server
        elif url:
            server = Server.objects.filter(base_url__contains=url)
            if (len(server) == 1):
                self.__server = server[0]
        elif authorUrl:
            url = authorUrl.split("/author/")[0]
            server = Server.objects.filter(base_url__contains=url)
            if (len(server) == 1):
                self.__server = server[0]
        else:
            raise ValueError("ServerUtil expects a server, authorUrl, or url variable to initialize.")

    def __throw_if_server_is_bad_or_unchecked(self):
        if not self.__checked_validity:
            raise RuntimeError("You are trying to run ServerUtil with a bad server, or did not check validity using valid_server().")

    def valid_server(self):
        if self.__server != None:
            self.__checked_validity = True
        return self.__checked_validity
    
    # same as valid_server but with a special kind of laziness
    def is_valid(self):
        return self.valid_server()

    def get_base_url(self):
        self.__throw_if_server_is_bad_or_unchecked()
        return self.__server.base_url

    def get_server_auth(self):
        self.__throw_if_server_is_bad_or_unchecked()
        server = self.__server
        return (server.fetching_username, server.fetching_password)

    # returns True, {dict of author info}
    def get_author_info(self, id):
        self.__throw_if_server_is_bad_or_unchecked()
        url = self.get_base_url() + "/author/" + id
        print("fetching from external server:", url)
        try:
            response = requests.get(
                url,
                auth=self.get_server_auth()
            )
            authorInfo = response.json()
            return True, authorInfo
        except Exception as e:
            print("fetching", url, "failed. Error:", e)
            return False, None
    
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

    # Will try to find a similar name, try not to call this with "https://" as
    # that will be useless...
    @staticmethod
    def get_base_url_from_similar_name(url):
        server = Server.objects.filter(base_url__contains=url)
        if (len(server) == 1):
            return server[0].base_url
        return "" # if we match more than one, or 0, we return an empty string