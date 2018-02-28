class Error(Exception):
    pass

class InvalidType(Error):

    # def __init__(self,msg):
    #     self.msg=msg
    #     print(msg)
    pass

class NotCoinSelected(Error):
    pass

class FiatInvalidType(Error):
    pass

class FiatNotValid(Error):
    pass
