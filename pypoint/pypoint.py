import requests
import json
import re

CRED_FILE = 'credentials.txt'
API_URL = 'https://api.minut.com/draft1/'

# Parses cred_file for credentials
def get_credentials(cred_file):
  try: lines = open(cred_file, 'r').readlines()
  except IOError:
    print('Unable to read credential file \'' + cred_file + '\'')
    return -1
  if len(lines) < 2:
    print("Invalid credentials file")
    return -1
  # Search credential file for id
  match = re.compile(r'CLIENT_ID = (\w+)').search(lines[0])
  if match: client_id = match.group(1)
  else: print('None or invalid CLIENT_ID in ' + cred_file)
  # Search credential file for secret
  match = re.compile(r'CLIENT_SECRET = (\w+)').search(lines[1])
  if match: client_secret = match.group(1)
  else: print('None or invalid CLIENT_SECRET in ' + cred_file)
  # Search credential file for username
  match = re.compile(r'USERNAME = (\w.+)').search(lines[2])
  if match: username = match.group(1)
  else: print('None or invalid USERNAME in ' + cred_file)
  # Search credential file for password
  match = re.compile(r'PASSWORD = (\w+)').search(lines[3])
  if match: password = match.group(1)
  else: print('None or invalid PASSWORD in ' + cred_file)
  print (client_id, client_secret, username, password)
  return (client_id, client_secret, username, password)

# Sends client_id/username/passowrd and returns access token
def get_token(client_id, username, password):
  url = API_URL + 'auth/token?&grant_type=password' + \
                  '&client_id=' + client_id + \
                  '&username=' + username + \
                  '&password=' + password
  res = requests.get(url)
  obj = json.loads(res.content.decode('UTF-8'))
  return obj['access_token']

# Build request.
# Appends given parameters and header with token to API_URL and returns the
# returned data.
def build_request(token, params):
  headers = { 'Authorization': 'Bearer ' + token }
  url = API_URL + params
  print("request url: " + url)
  res = requests.get(url, headers=headers)
  if res.status_code == 200:
    return json.loads(res.content.decode('UTF-8'), 'UTF-8')
  else:
    print("Error: Server response " + str(res.status_code))
    return []

class Point:
  def __init__(self, cred_file):
    client_id, client_secret, username, password = get_credentials(cred_file)
    self.token = get_token(client_id, username, password)
    self.init_devices()

  def init_devices(self):
    self.points = []
    data = self.get_devices()
    for dev in data['devices']:
      self.points.append(dev['device_id'])
    if len(self.points) > 0:
      self.default_id = self.points[0]

  ### Endpoint /devices
  
  def get_devices(self):
    return build_request(self.token, 'devices')

  def get_device(self, device_id=None):
    if not device_id: device_id = self.default_id
    params = 'devices' + device_id
    return build_request(self.token, params)

  def update_device(self, device_id=None, data):
    if not device_id: device_id = self.default_id
    url = API_URL + 'devices' + device_id
    headers = { 'Authorization': 'Bearer ' + token }
    requests.put(url, headers=headers, data=data)
  
  def get_device_id(self, device_num=0):
    if len(self.points) >= device_num and len(self.points) > 0:
      return self.default_id
    else:
      return -1 

  def get_temperature(self, device_id=None):
    if not device_id: device_id = self.default_id
    return self.get_temperature_history(device_id)['values'][-1]

  def get_temperature_history(self, device_id=None):
    if not device_id: device_id = self.default_id
    params = 'devices/' + device_id + '/temperature'
    return build_request(self.token, params)

  def get_humidity(self, device_id=None):
    if not device_id: device_id = self.default_id
    params = 'devices/' + device_id + '/humidity'
    return build_request(self.token, params)

  def get_pressure(self, device_id=None):
    if not device_id: device_id = self.default_id
    params = 'devices/' + device_id + '/pressure'
    return build_request(self.token, params)

  def get_sound_peak_levels(self, device_id=None):
    if not device_id: device_id = self.default_id
    params = 'devices/' + device_id + '/sound_peak_levels'
    return build_request(self.token, params)

  def get_sound_avg_levels(self, device_id=None):
    if not device_id: device_id = self.default_id
    params = 'devices/' + device_id + '/sound_avg_levels'
    return build_request(self.token, params)

  def get_events(self, device_id=None):
    params = 'devices/' + device_id + '/events'
    return build_request(self.token, params)

  ### Endpoint /homes

  def get_homes(self):
    params = 'homes'
    return build_request(self.token, params)

  def create_home(self, json_data):
    pass # TODO

  def get_home(self, home_id):
    pass # TODO

  def update_home(self, home_id):
    pass # TODO

  def add_home_member(self, home_id, user_id):
    pass # TODO

  def delete_home_member(self, home_id, user_id):
    pass # TODO

  ### Endpoint /timelines

  def get_timeline_events(self, user_id, start_at, end_at, limit, offset):
    pass # TODO

  def register_web_hook(self):
    pass # TODO

  def get_web_hooks(self):
    pass # TODO

  def delete_web_hook(self):
    pass # TODO

  def trigger_test_event(self):
    pass # TODO

  ### Endpoint /users

  def create_new_user(self, fullname, email, password, subscribe):
    pass # TODO

  def get_user(self, user_id):
    pass # TODO

  def update_user(self, fullname=None, nick=None, email=None, old_pw=None, new_pw=None):
    pass # TODO

  def get_devices_by_user(self, user_id):
    pass # TODO

