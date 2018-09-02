import urllib.request, json

class WebProvider:
    def get(self, url):
        response = urllib.request.urlopen(url)
        return response.read()

    def get_json(self, url):
        contents = self.get(url)
        return json.loads(contents)


class FakeProvider:
    def __init__(self, contents):
        self.contents=contents

    def get(self, url):
        return self.contents

    def get_json(self, url):
        contents = self.get(url)
        return json.loads(contents)
