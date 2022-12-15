from urllib3.exceptions import InsecureRequestWarning
from urllib3 import PoolManager, disable_warnings
import json
import time
from datetime import datetime
import os
from python_emails.text_email import send_mail


PATH = os.path.dirname(os.path.abspath(__file__))

disable_warnings(InsecureRequestWarning)
requests = PoolManager(cert_reqs="CERT_NONE")


def get_info(url, wallet_id):
    headers = {
        'Content-Type': 'application/json',
    }
    json_data = {
        'jsonrpc': '2.0',
        'method': 'eth_getBalance',
        'params': [
            wallet_id,
            'latest',
        ],
        'id': 1,
    }
    api_response = requests.request("POST", url, headers=headers, body=json.dumps(json_data))
    status_code = api_response.status
    if status_code == 200:
        api_response = json.loads(api_response.data.decode())
    if status_code == 200 and "result" in api_response.keys():
        api_response = api_response['result']
        decimal = int(api_response, 16)
        return round(decimal / (10 ** 18), 3), status_code, "Success"
    elif status_code == 200 and 'error' in api_response.keys():
        return -1, api_response['error']['code'], api_response['error']['message']
    else:
        return -1, status_code, "Error While api call"


def start(**kwargs):
    wallet_flag = 1
    while True:
        url = "https://goerli.infura.io/v3/01e65d54328e4c7185f9069b66dba1d5"
        wallet_id = '0x256144a60f34288F7b03D345F8Cb256C502e0f2C'
        response = get_info(url, wallet_id)
        if response[0] == -1:
            print("Error While Fetching Data",'automationtask2022@gmail.com')
        elif response[0] <= 20.01:
            send_mail(f"Dear User,\n\nYour ETH balance is low in your Wallet.\n\nETH Balance: {response[0]}\n\nRegards,\nNotification Team.", 'automationtask2022@gmail.com')
            wallet_flag = 0
        if not os.path.isfile(f"Balance_Report_{wallet_id}.csv"):
            with open(f"Balance_Report_{wallet_id}.csv", 'a') as file:
                file.write("ETH Balance,Status Code,Status Message,Time Stamp")
        with open(f"Balance_Report_{wallet_id}.csv",'a') as file:
            file.write("\n{},{},{},{}".format(*response, datetime.now()))
        time.sleep(2)
        if wallet_flag == 0:
            break
        # break


if __name__ == '__main__':
    start()
    # wallet address, email, status code, response_time -> PT
    # wallet address, value -> os
