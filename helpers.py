"""Helper classes for Google Assistant integration."""

class SmartHomeError(Exception):
    """Google Assistant Smart Home errors.
    https://developers.google.com/actions/smarthome/create-app#error_responses
    """
    def __init__(self, code, msg):
        """Log error code."""
        super().__init__(msg)
        self.code = code 

class SmartHomeErrorNoChallenge(Exception):
    def __init__(self, code, desc, msg):
        """Log error code."""
        super().__init__(msg)
        self.code = code 
        self.desc = desc
 
class AogState:
    def __init__(self):
        self.state = ''
        self.domain = ''
        self.attributes = 0
        self.name = ''
        self.entity_id = ''
        self.id = ''
        self.nicknames = None
        self.room = None
        self.level = 0
        self.temp = 0
        self.humidity = 0
        self.setpoint = ''
        self.color = ''
        self.protected = None
        self.maxdimlevel = 0
        self.seccode = ''
