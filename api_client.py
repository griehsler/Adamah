import http.client
import json

connection = http.client.HTTPSConnection("www.adamah.at")


def login(user, password):
    headers = {'Content-type': 'application/json'}
    request = {
        "username": user,
        "password": password,
        "authInfo": None,
        "systemModuleSid": 18
    }
    connection.request('POST', '/ACM/api/auth/login',
                       json.dumps(request), headers)
    response = json.loads(connection.getresponse().read().decode())
    return_code = response['returnCode']
    if return_code != 1:
        raise Exception('Login failed: {}'.format(response["msg"]))
    return response['token']


def getdeliveries(token, fromdate, todate):
    headers = {
        'Content-type': 'application/json',
        'Authorization': 'Bearer {}'.format(token)
    }
    request = {"deliveryDateFrom": int(fromdate.timestamp() * 1000),
               "deliveryDateTo": int(todate.timestamp() * 1000)}
    connection.request(
        'POST', '/ACM/api/webshop/getdeliveries', json.dumps(request), headers)
    response = json.loads(connection.getresponse().read().decode())
    return response


def store_deliveries(filename, deliveries):
    f = open(filename, "w")
    json.dump(deliveries, f, indent=2, sort_keys=True)
    f.close()
