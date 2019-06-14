
class Domain(list):
    def set_url(self, url):
        self.append(url)

    def get_url(self):
        return self

    def join_url(self):
        url = "".join(self)
        return url