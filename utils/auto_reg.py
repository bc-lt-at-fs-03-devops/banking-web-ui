import os
import json
import random
import requests
import optparse

opts = optparse.OptionParser()
# Argument to specify the IP
opts.add_option('-i', '--ip', dest='ip_str', help='Indicate the ip address for the api connection')
# Obtain the arguments
(options, arguments) = opts.parse_args()

if options.ip_str != None:
    IP = options.ip_str
else:
    IP = '0.0.0.0'

data_dir= os.path.join(os.path.dirname(__file__), '..', 'data')
user_json = os.path.join(data_dir, 'new_us.json')
list_login = list()
with open(user_json) as f_json:
    new_users = json.load(f_json)

for user in new_users:
    # Create new users
    response = requests.post('http://' + IP + ':9000/users', json=user)
    # Load the response info for login
    login_data = json.loads(response.text)
    # Dictionary to login
    login = {"username": login_data["username"], 
             "password": login_data["password"], 
             "code": login_data["code"]}

    token = requests.post('http://' + IP + ':9000/login', json=login)
    cbu = login_data['cbu']
    login_data['cbu'] = [cbu]
    if user['type'] == 'User':
        the_token = json.loads(token.text)['access_token']
        # new account
        if random.randint(0, 1) == 1:
            new_account = requests.post('http://' + IP + ':9000/accounts', headers={'Authorization':the_token})
            account = json.loads(new_account.text)
            login_data['cbu'].append(account['cbu'])
        if random.randint(0, 1) == 1:
            new_account = requests.post('http://' + IP + ':9000/accounts', headers={'Authorization':the_token})
            account = json.loads(new_account.text)
            login_data['cbu'].append(account['cbu'])
        list_login.append(login_data)
        
    # Save the info for login
    login_data['type'] = user['type']
    with open(os.path.join(data_dir, 'new_us.txt'), "a") as f:
        f.write('\n ' + json.dumps(login_data))


for i in range(len(list_login)):
    for account in list_login[i]['cbu']:
        # Dictionary to login
        login = {"username": list_login[i]["username"], 
                "password": list_login[i]["password"], 
                "code": list_login[i]["code"]}

        token = requests.post('http://' + IP + ':9000/login', json=login)
        the_token = json.loads(token.text)['access_token']
            
        new_account = requests.get('http://' + IP + ':9000/home', headers={'Authorization':the_token})
        user_info = json.loads(new_account.text)

        deposit_info = {
                    "transaction_type": "deposit",
                    "origin_account": int(user_info['document_id']),
                    "final_account": int(account),
                    "description": "test deposit",
                    "amount": 5000.0
                }
        requests.post('http://' + IP + ':9000/transactions', json=deposit_info)
        
        copy_list = list_login.copy()
        copy_list.pop(i)

        for _ in range(50):
            choice_account = random.choice(random.choice(copy_list)['cbu'])
            
            transac_info = {
                    "transaction_type": "transaction",
                    "origin_account": int(account),
                    "final_account": int(choice_account),
                    "description": "test deposit",
                    "amount": round(25 * random.random(), 2)
                }
            #print(transac_info)
            requests.post('http://' + IP + ':9000/transactions', json=transac_info)
            
    
