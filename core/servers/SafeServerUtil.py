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
