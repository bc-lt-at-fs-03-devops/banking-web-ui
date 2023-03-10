#from contextvars import copy_context
#from dash._callback_context import context_value
#from dash._utils import AttributeDic
import os
import json
from dash import no_update

# Import the callbacks of login
from pages.login import login_auth

def test_Noclicks_login_callback():
    assert login_auth(0, '', '', '') == (no_update, no_update)
    
    
def test_login_callback():
    data_users = list()
    data_dir= os.path.join(os.path.dirname(__file__), '..', 'data')
    with open(os.path.join(data_dir, 'new_us.txt'), "r") as f:
        for line in f.readlines():
            if len(line) > 3:
                data_users.append(json.loads(line))
    for user in data_users:
        if user['type'] == 'Employee':
            view =  ('/register', '')
        else:
            view = ('/home','')
        assert login_auth(1, user['username'], user['password'], user['code'], test=True) == view
