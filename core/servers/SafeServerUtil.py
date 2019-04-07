# Please do not remove debugging logs all of our sanity :)
from core.servers.models import Server
import json
import requests
from posixpath import join as urljoin

class ServerUtil:
    # Init function allows you pass in variables related to the server to
    # try and find its related server object
    def __init__(self, user=None, server=None, url=None, authorUrl=None, postUrl=None):
        self.__server = None
        self.__checked_validity = False
        if user and ServerUtil.is_server(user):
            self.__server = user.server
        elif server and ServerUtil.is_server(server.user):
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
        elif postUrl:
            url = postUrl.split("/posts/")[0]
            server = Server.objects.filter(base_url__contains=url)
            if (len(server) == 1):
                self.__server = server[0]
        else:
            print("ServerUtil expects a valid server, authorUrl, or url, etc variable to initialize. (But couldn't find one)")

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

    def get_author_friends(self, id):
        url = urljoin(self.get_base_url(), 'author', id, 'friends')
        try:
            response = requests.get(
                url,
                auth=self.get_server_auth()
            )
            body = response.json()
            return True, body.get('authors', None)
        except Exception as e:
            print("fetching", url, "failed. Error:", e)
            return False, None


    def get_post(self, id, requestingAuthorUrl):
        self.__throw_if_server_is_bad_or_unchecked()
        url = self.get_base_url() + "/posts/" + id
        print("fetching from external server:", url)
        try:
            # not sure if this is necessary here..
            if not self.should_fetch_posts():
                 # return nothing, as we shouldn't be fetching from this server
                raise ValueError("The admin has disabled fetching posts from this server.")
            headers = {
                "X-Request-User-ID": requestingAuthorUrl
            }
            response = requests.get(
                url,
                headers=headers,
                auth=self.get_server_auth()
            )
            postData = response.json()
            return True, postData
        except Exception as e:
            print("fetching", url, "failed. Error:", e)
            return False, None

    def should_fetch_posts(self):
        self.__throw_if_server_is_bad_or_unchecked()
        return self.__server.fetch_posts

    def should_share_posts(self):
        self.__throw_if_server_is_bad_or_unchecked()
        return self.__server.share_posts
        
    def should_share_pictures(self):
        self.__throw_if_server_is_bad_or_unchecked()
        return self.__server.share_pictures

    def get_posts(self):
        self.__throw_if_server_is_bad_or_unchecked()
        try:
            # Print debugging logs first
            url = self.get_base_url() + "/posts" # we don't store ending slash, attach it
            print("Fetching posts from:", url)
            if not self.should_fetch_posts():
                 # return nothing, as we shouldn't be fetching from this server
                raise ValueError("The admin has disabled fetching posts from this server.")
            response = requests.get(url, auth=self.get_server_auth())
            postsData = response.json()
            print("Fetched posts!")
            return True, postsData
        except Exception as e:
            print("Failed fetching posts, error:", e)
            return False, {}
    
    def create_comment(self, id, requestingAuthorUrl, comment, origin):
        self.__throw_if_server_is_bad_or_unchecked()
        url = self.get_base_url() + "/posts/" + id + "/comments"
        print("posting comment to external server:", url)
        try:
            # not sure if this is necessary here..
            if not self.should_fetch_posts():
                 # return nothing, as we shouldn't be fetching from this server
                raise ValueError("The admin has disabled fetching posts from this server.")
            response = requests.post(
                url,
                auth=self.get_server_auth(),
                json={
                    "query": "addComment",
                    "post": origin,
                    "comment": comment
                }
            )
            if (response.status_code >= 400):
                raise Exception(response.json())
            postData = response.json()
            print(postData)
            return True, postData
        except Exception as e:
            print("posting comment", url, "failed. Error:", e)
            return False, None
    
    def get_posts_by_author(self, authorId, requesterUrl):
        self.__throw_if_server_is_bad_or_unchecked()
        try:
            # Print debugging logs first
            url = self.get_base_url() + "/author/" + authorId + "/posts" # we don't store ending slash, attach it
            print("Fetching posts by author from:", url)
            if not self.should_fetch_posts():
                 # return nothing, as we shouldn't be fetching from this server
                raise ValueError("The admin has disabled fetching posts from this server.")
            
            headers = {
                "X-Request-User-ID": requesterUrl
            }
            response = requests.get(url, auth=self.get_server_auth(), headers=headers)
            postsData = response.json()
            print("Fetched posts!")
            return True, postsData
        except Exception as e:
            print("Failed fetching posts, error:", e)
            return False, {}
    
    # Only necessary if a local user is friending an external one
    # body is the same body given to us by the post method
    def notify_server_of_friendship(self, body):
        self.__throw_if_server_is_bad_or_unchecked()
        try:
            url = self.get_base_url() + "/friendrequest"
            auth = self.get_server_auth()
            print("Sending friend request to:", url, auth, body)
            headers={"Content-type": "application/json"}
            resp = requests.post(url, data=json.dumps(body), auth=auth, headers=headers)
            print("Response received", resp.status_code, resp.content)
            return resp.status_code == 200
        except Exception as e:
            print("Failed sending friendship", e)
            return False

    def notify_of_unfriendship(self, requesterUrl, authorUrl):
        self.__throw_if_server_is_bad_or_unchecked()
        try:
            url = self.get_base_url() + "/unfollow"
            auth = self.get_server_auth()
            body = {
                "query": "unfollow",
                "author": {
                    "id": requesterUrl
                },
                "friend": {
                    "id": authorUrl
                }
            }
            print("Sending unfollow notification to:", url, auth, body)
            resp = requests.post(url, data=json.dumps(body), auth=auth, headers=headers)
            print("Response received", resp.status_code, resp.content)
            return resp.status_code == 200
        except Exception as e:
            print("Failed sending notification", e)
            return False

    # Success, friendship status
    def check_direct_friendship(self, remote_author, local_author):
        self.__throw_if_server_is_bad_or_unchecked()
        return self.check_at_least_one_friend(remote_author, [local_author])

    # Success, friendship status
    def check_at_least_one_friend(self, remote_author, authorUrls):
        self.__throw_if_server_is_bad_or_unchecked()
        try:
            url = self.get_base_url() + "/author/" + remote_author.split("author/")[1] + "/friends"
            auth = self.get_server_auth()
            print("Checking friend status of: "+ url)
            data = {
                "query":"friends",
                "author": remote_author,
                "authors": authorUrls
            }
            resp = requests.post(url, data=json.dumps(data), auth=auth)
            resp = resp.json()
            print("friendship response:", resp)
            # TODO: It would be cool to clean up our local friends based on this...
            return True, len(resp["authors"]) >= 1
        except Exception as e:
            print("Failed to check friendship", e)
            return False, False

    def author_from_this_server(self, authorUrl):
        sUtil = ServerUtil(authorUrl=authorUrl)
        return sUtil.is_valid() and sUtil.get_base_url() == self.get_base_url()

    def get_friends_of(self, authorId):
        url = self.get_base_url() + "/author/" + authorId + "/friends"
        try:
            print("Fetching friends from:", url)
            resp = requests.get(url, auth=self.get_server_auth())
            print("Fetched friends:", resp.content)
            print("Fetched friends:", resp.json())
            return resp.json()["authors"]
        except Exception as e:
            print("Failed to fetch friends for:", url, "error:", e)
            return []

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

    @staticmethod
    def get_external_posts_aggregate():
        posts = []
        servers = Server.objects.all()
        for server in servers:
            server = ServerUtil(server=server)
            if not server.is_valid():
                continue
            success, postsData = server.get_posts()
            if not success:
                continue
            if "posts" not in postsData:
                print("Couldn't find posts in response data:", postsData)
                continue
            for post in postsData.get("posts", []): # prevent KeyError
                posts.append(post)
        def key(post):
            return post["published"]
        posts.sort(key=key, reverse=True)
        return posts
            
