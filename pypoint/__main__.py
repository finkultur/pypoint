import requests
import json

CRED_FILE = '../credentials.txt'
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
  # Search credential file for key
  match = re.compile(r'CLIENT_ID = (\w+)').search(lines[0])
  if match: key = match.group(1)
  else: print('None or invalid CLIENT_ID in ' + cred_file)
  # Search credential file for secret
  match = re.compile(r'CLIENT_SECRET = (\w+)').search(lines[1])
  if match: secret = match.group(1)
  else: print('None or invalid CLIENT_SECRET in ' + cred_file)

  return (key, secret)


# Sends client_id/client_secret and returns access token
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

### Endpoint /devices

def get_temperature(device_id):
  pass

def get_humidity(device_id):
  pass

def get_pressure(device_id):
  pass

def get_sound_peak_levels(device_id):
  pass

def get_sound_avg_levels(device_id):
  pass

def get_events(device_id):
  pass

### Endpoint /homes

### Endpoint /timelines

### Endpoint /users


