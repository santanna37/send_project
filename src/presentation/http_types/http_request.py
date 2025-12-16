

class HttpRequest:
    def __init__(self,
                headers = None,
                body =  None,
                query_params = None,
                path_params = None,
                url = None,
                ipv4 = None
    ) -> None:
        self.headers = headers or {}
        self.body = body or {}
        self.query_params = query_params or {}
        self.path_params = path_params or {}
        self.url = url or {}
        self.ipv4 = ipv4 or {}
