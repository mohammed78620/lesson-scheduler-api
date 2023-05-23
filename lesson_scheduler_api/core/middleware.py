import json
import os

from mixpanel import Mixpanel

mixpanel_token = os.getenv("MIXPANEL_TOKEN")
mp = Mixpanel(mixpanel_token)


class SimpleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if mixpanel_token is not None:
            try:
                if request.path.startswith("/booking"):
                    r = json.loads(response.content.decode("utf-8"))
                    mp.track("api_event", request.path, r)
            except Exception as e:
                print(str(e))
        return response
