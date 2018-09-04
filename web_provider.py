import urllib.request, urllib.error, json, time


class WebProvider:
    def get(self, url):
        failures = 0
        while True:
            try:
                response = urllib.request.urlopen(url)
                return response.read()
            except urllib.error.HTTPError as e:
                failures += 1
                if failures >= 5:
                    raise e
                time.sleep(0.5)


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
