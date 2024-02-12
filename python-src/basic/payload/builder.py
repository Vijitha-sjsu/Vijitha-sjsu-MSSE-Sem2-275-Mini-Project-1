import json

class BasicBuilder(object):
    def __init__(self):
        pass
        
    def encode(self, name, group, msg):
        if not all(isinstance(field, str) and field.strip() for field in [name, group, msg]):
            raise ValueError("Name, group, and message must be non-empty strings.")
        payload = json.dumps({"group": group, "name": name, "msg": msg})
        return f"{len(payload):04d}{payload}"

    def decode(self, raw):
        try:
            length = int(raw[:4])
        except ValueError:
            raise ValueError("Length prefix is not an integer.")
        
        payload = raw[4:]
        if len(payload) != length:
            raise ValueError("Actual message length does not match length prefix.")
        
        try:
            message = json.loads(payload)
        except json.JSONDecodeError:
            raise ValueError("Payload is not valid JSON.")
        
        if 'group' not in message or 'name' not in message or 'msg' not in message:
            raise ValueError("Missing required message fields.")
        
        return message['name'], message['group'], message['msg']
