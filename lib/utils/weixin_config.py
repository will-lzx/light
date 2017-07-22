
class config_weixin:
    def __init__(self, appID, timestamp, noncestr, signature):
        self.appID = appID
        self.timestamp = timestamp
        self.noncestr = noncestr
        self.signature = signature
