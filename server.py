from flask import Flask, redirect, url_for, request
from flask import render_template
from storage import StorageManager
import json
from eth_api import ethAPI

server = Flask(__name__)

ip = '10.0.3.23'
port = 27017
db = 'osc_hack'
sm = StorageManager(ip, port, db)

eth = ethAPI()

@server.route('/cibc')
def cibc():
    return render_template('bank_login.html')

@server.route('/suit_yourself')
def suit_yourself_login():
    return render_template('firm_id_login.html')

@server.route('/bank_user_login', methods=['POST'])
def bank_user_login():
    print('user login')

    name = request.json['user_name']
    pwd = request.json['pwd']

    user_data = sm.find('bank_users', {'user_name': name})

    # if no user data then new user!
    if not (user_data.count()):
        return 'Not found'

    else:
        if name + pwd != user_data[0]['user_name'] + user_data[0]['password']:
            return 'Incorrect'
        else:
            return render_template('firm_id_cibc_login.html', user_data=user_data[0])


@server.route('/firm_user_login', methods=['POST'])
def firm_user_login():
    print('user login')

    name = request.json['user_name']
    pwd = request.json['pwd']

    user_data = sm.find('firm_users', {'user_name': name})
    user_data = user_data[0]

    user_data['suit_profiles'] = [{
        "profile_name": "High Risk",
        "institutions": ["TD", "CIBC"]
    }]

    # if no user data then new user!
    if not (user_data):
        return 'Not found'

    else:
        if name + pwd != user_data['user_name'] + user_data['password']:
            return 'Incorrect'
        else:
            print(user_data)
            return render_template('user_account.html', user_data=user_data)


@server.route('/firm_user_sy_login', methods=['POST'])
def firm_user_sy_login():
    print('user login')

    name = request.json['user_name']
    pwd = request.json['pwd']

    user_data = sm.find('firm_users', {'user_name': name})
    user_data = user_data[0]

    # if no user data then new user!
    if not (user_data):
        return 'Not found'

    else:
        if name + pwd != user_data['user_name'] + user_data['password']:
            return 'Incorrect'
        else:
            print(user_data)
            return render_template('user_account_sy.html', user_data=user_data)


@server.route('/bank_client_user_create', methods=['POST'])
def bank_client_user_create():

    user_name = request.json['user_name']
    pwd = request.json['pwd']
    name = request.json['name']
    address = request.json['address']
    dob = request.json['dob']
    type = request.json['type']

    user_data = sm.find('bank_users', {'user_name': user_name})

    # if no user data then new user!
    if not (user_data.count()):

        user_data = {
            'user_name': user_name,
            'password': pwd,
            'address': address,
            'name': name,
            'dob': dob,
            'type': type
        }

        print(sm.insert('bank_users', user_data))
        # return render_template('firm_id_cibc_login.html', user_data=user_data)
        return 'success'
    else:
        return 'Incorrect'


@server.route('/bank_user_create', methods=['POST'])
def bank_user_create():

    user_name = request.json['user_name']
    pwd = request.json['pwd']
    type = request.json['type']

    user_data = sm.find('bank_users', {'user_name': user_name})

    # if no user data then new user!
    if not (user_data.count()):
        # grab a new account key
        keys = sm.find('account_keys', {})

        if keys[0]:
            account_key = keys[0]
            # remove key
            sm.remove('account_keys', {'key': account_key})
        else:
            account_key = None

        user = {
            'user_name': user_name,
            'password': pwd,
            'type': type,
            'addresses': [],
            'key': account_key
        }

        print(sm.insert('bank_users', user))
        # return render_template('firm_id_cibc_login.html', user_data=user_data[0])
        return 'success'

    else:
        return 'Incorrect'


@server.route('/cibc/firm_id_cibc', methods=['GET'])
def firm_id_create():
    print('user create')
    return render_template('firm_id_cibc_login.html')


@server.route('/cibc/firm_id_cibc/profiles', methods=['GET'])
def firm_profiles():
    print('user profiles')
    return render_template('user_account.html')


@server.route('/firm_user_create', methods=['POST'])
def firm_user_create():
    print('user create')

    user_name = request.json['user_name']
    pwd = request.json['pwd']

    user_data = sm.find('firm_users', {'user_name': user_name})

    # if no user data then new user!
    if not (user_data.count()):
        # grab a new account keys
        keys = sm.find('account_keys', {})
        print(keys)

        if 0:
            pass
            # if keys and keys[0]:
            # account_key = keys[0]
            # # remove key
            # sm.remove('account_keys', {'key': account_key})
        else:
            account_key = None

        user = {
            'user_name': user_name,
            'password': pwd,
            'addresses': [],
            'key': account_key
        }

        print(sm.insert('firm_users', user))
        # return render_template('user_account.html', user_data=user_data[0])
        return 'success'

    else:
        return 'Incorrect'


@server.route('/suit_yourself/profiles', methods=['GET'])
def suit_profiles():
    print('suit')
    return render_template('user_account_sy.html')


@server.route('/deploy_contract', methods=['POST'])
def deploy_contract():

    data = {
        "knowledge": request.json['knowledge'],
        "income": request.json['income'],
        "horizon": request.json['horizon'],
        "obj": request.json['obj'],
        "risk": request.json['risk']
    }

    # eth.connect("06d3ae659a2284a04046d696cd997feea827065f")
    # eth.createSuitabilityProfile("06d3ae659a2284a04046d696cd997feea827065f", json.dumps(data))
    # eth.connect()
    # eth.createSuitabilityProfile(json.dumps(data))

    # update user account and bank
    # print(sm.update('firm_users', {'user_name': request.json['user_name']}, {"$push": {"addresses": "test"}}))
    # print(sm.update('firm_users', {'user_name': "CIBC"}, {"$push": {"addresses": "test"}}))
    # print(request.json['user_name'])

    return request.json['profile_name']

if __name__ == "__main__":
    server.run()

