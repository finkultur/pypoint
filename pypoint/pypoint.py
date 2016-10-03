import requests
import json
import ConfigParser

CRED_FILE = 'credentials.txt'
API_URL = 'https://api.minut.com/draft1/'

# Parses cred_file for credentials
def get_credentials(cred_file):
    config = ConfigParser.RawConfigParser()
    config.read(cred_file)

    client_id = config.get('API_KEY', 'client_id') 
    client_secret = config.get('API_KEY', 'client_secret') 
    username = config.get('API_KEY', 'username') 
    password = config.get('API_KEY', 'password') 
    return (client_id, client_secret, username, password)

# Sends client_id/username/passowrd and returns access token
def get_token(client_id, username, password):
    url = API_URL + ('auth/token?&grant_type=password' +
                     '&client_id=' + client_id +
                     '&username=' + username +
                     '&password=' + password)
    res = requests.get(url)
    return check_response(res, 200)['access_token']

def check_response(res, *valid_responses):
    if res.status_code in valid_responses:
        return json.loads(res.content.decode('UTF-8'), 'UTF-8')
    else:
        raise Exception('Error: ' +
                        str(res.status_code) + ' ' +
                        str(res.content))

class Point(object):
    def __init__(self, cred_file):
        client_id, client_secret, username, password = get_credentials(cred_file)
        self.token = get_token(client_id, username, password)
        self.header = {'Authorization': 'Bearer ' + self.token}

        self.points = []
        for dev in self.get_devices()['devices']:
            self.points.append(dev['device_id'])
        if len(self.points) > 0:
            self.default_id = self.points[0]

    def _get(self, params, *valid_response):
        url = API_URL + params
        res = requests.get(url, headers=self.header)
        return check_response(res, *valid_response)

    ### Endpoint /devices

    def get_devices(self):
        return self._get('devices', 200)

    def get_device(self, device_id=None):
        if not device_id: device_id = self.default_id
        self._get('devices/' + str(device_id), 200)

    def update_device(self, new_conf, device_id=None):
        if not device_id: device_id = self.default_id
        url = API_URL + 'devices/' + str(device_id)
        res = requests.put(url, headers=self.header, json=new_conf)
        return check_response(res, 200)

    def get_device_id(self, device_num=0):
        if len(self.points) >= device_num and len(self.points) > 0:
            return self.default_id
        else:
            return -1

    def get_temperature(self, device_id=None):
        if not device_id: device_id = self.default_id
        return self._get('devices/' + str(device_id) + '/temperature', 200)

    def get_latest_temperature(self, device_id=None):
        """ Returns the latest reported temperature. """
        return self.get_temperature(device_id)['values'][-1]

    def get_humidity(self, device_id=None):
        if not device_id: device_id = self.default_id
        return self._get('devices/' + str(device_id) + '/humidity', 200)

    def get_latest_humidity(self, device_id=None):
        """ Returns the latest reported humidity. """
        return self.get_humidity(device_id)['values'][-1]

    def get_pressure(self, device_id=None):
        if not device_id: device_id = self.default_id
        return self._get('devices/' + str(device_id) + '/pressure', 200)

    def get_latest_pressure(self, device_id=None):
        """ Returns the latest reported pressure. """
        return self.get_pressure(device_id)['values'][-1]

    def get_sound_peak_levels(self, device_id=None):
        if not device_id: device_id = self.default_id
        return self._get('devices/' + str(device_id) + '/sound_peak_levels', 200)

    def get_sound_avg_levels(self, device_id=None):
        if not device_id: device_id = self.default_id
        return self._get('devices/' + str(device_id) + '/sound_avg_levels', 200)

    def get_events(self, device_id=None):
        if not device_id: device_id = self.default_id
        return self._get('devices/' + str(device_id) + '/events', 200)

    ### Endpoint /homes

    def get_homes(self):
        """ Get current home. """
        return self._get('homes', 200)

    def create_home(self, json_data):
        """ Create home. """
        url = API_URL + 'homes'
        res = requests.post(url, data=None, json=json_data)
        return check_response(res, 200, 201, 202)

    def get_home(self, home_id):
        """ Get home by home_id. """
        return self._get('homes/' + str(home_id), 200)

    def update_home(self, home_id, json_data):
        " Update home, accepts same data as when creating a home. """
        url = API_URL + 'homes/' + str(home_id)
        res = requests.put(url, headers=self.header, json=json_data)
        return check_response(res, 200, 201)

    def add_home_member(self, home_id, user_id):
        """ Add user to home. """
        url = API_URL + 'homes/' + str(home_id) + '/members'
        json_data = json.JSONEncoder().encode(
            {'user_id': user_id,
             'scopes': ['family']})
        res = requests.post(url, data=None, json=json_data)
        return check_response(res, 200, 201, 202)

    def delete_home_member(self, home_id, user_id):
        """ Delete a user from a home. """
        url = API_URL + 'homes/' + home_id + '/members' + user_id
        res = requests.delete(url, headers=self.header)
        return check_response(res, 200, 202, 204)

    ### Endpoint /timelines

    def get_timeline_events(self, user_id, params=None):
        """
        Retrieve a list of timeline events.
        Arguments:
            user_id (set to 'me' for current user)
        Optional parameters:
            start_at: UTC Time (e.g. 2014-12-20T09:00:00.000Z)
            end_at:   UTC Time (e.g. 2016-12-20T09:00:00.000Z)
            limit:    Number of events to retrieve
            offset:   Define which offset
        """
        url = API_URL + 'timelines/' + str(user_id) + '/'
        res = requests.get(url, headers=self.header, params=params)
        return check_response(res, 200)

    def register_web_hook(self, url, subscriptions, token=None, user_id='me'):
        """ Register new web hook.
        Arguments:
            url: Address which minut will post to, e.g. 
                 https://your.domain.com/my_hook
            subscriptions: list of events to subscribe to, e.g.
                           ["home:activity:detected", home:sound:high].
            token: Optional token  
        """
        data['url'] = url
        data['subscriptions'] = subscriptions
        if token is not None: data['token'] = token
        json_data = json.dumps(data)
        url = API_URL + 'timelines/' + str(user_id) + '/hooks'
        res = requests.post(url, data=None, json=json_data)
        return check_response(res, 200, 201, 202)

    def get_web_hooks(self, user_id='me'):
        """ Retrieve a list of registered web hooks. """
        return self._get('timelines/' + str(user_id) + '/hooks' , 200)

    def delete_web_hook(self, hook_id, user_id='me'):
        """ Delete web hook """
        url = API_URL + 'timelines/' + str(user_id) + '/hooks/' + hook_id
        res = requests.delete(url, headers=self.header)
        return check_response(res, 200, 202, 204)

    def trigger_test_event(self, hook_id, user_id='me'):
        """ Trigger test event. 
            Missing documentation so not sure if/how this works.
        """
        url = API_URL + 'timelines/' + str(user_id) + 'hooks/' + hook_id + '/ping'
        res = request.post(url, data=None, json=None)
        return check_response(res, 200, 201, 202)

    ### Endpoint /users

    def create_new_user(self, fullname, email, password, subscribe):
        """ Create new user. Args self-explained, subscribe is a bool. """
        data['fullname'] = fullname
        data['email'] = email
        data['password'] = password
        data['subscribe'] = subscribe
        json_data = json.dumps(data)
        url = API_URL + 'users'
        res = requests.post(url, data=None, json=json_data)
        return check_response(res, 200, 201, 202)

    def get_user(self, user_id='me'):
        """ Get current user. """
        return self._get('/users/' + str(user_id), 200)

    def get_user_id(self):
        """ Get user_id of user associated with the current access token. """
        return self.get_user()['user_id']

    def update_user(self, user_id='me', **kwargs):
        """ Update user information. Arguments are pretty straightforward. """
        data = {}
        if 'name' in kwargs: data['name'] = kwargs['name']
        if 'nick' in kwargs: data['nick'] = kwargs['nick']
        if 'email' in kwargs: data['email'] = kwargs['email']
        if 'old_pw' in kwargs and 'new_pw' in kwargs:
            data['password'] = {}
            data['password']['old'] = kwargs['old_pw']
            data['password']['new'] = kwargs['new_pw']
        new_conf = json.dumps(data)
        url = API_URL + 'users/' + str(user_id)
        res = requests.put(url, headers=self.header, json=new_conf)
        return check_response(res, 200)

    def get_devices_by_user(self, user_id='me'):
        return self._get('/users/' + str(user_id) + '/devices', 200)

