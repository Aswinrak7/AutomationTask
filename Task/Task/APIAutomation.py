from urllib3.exceptions import InsecureRequestWarning
from urllib3 import PoolManager, disable_warnings
import json
import time
from datetime import datetime
import os
import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

PATH = os.path.dirname(os.path.abspath(__file__))

disable_warnings(InsecureRequestWarning)
requests = PoolManager(cert_reqs="CERT_NONE")
details = {'username': '', 'smtp_password': '', 'outgoing_mail_id': '', 'smtp_server': '', 'port': '25', 'auth_enabled': True}


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


def send_mail(smtp_details, subject, body, attach_exist, file_name, toaddr=[], ccaddr=[]):
    """ Send email with attachments """
    if smtp_details == {}:
        raise Exception("SMTP Details is empty. Kindly enable your authentication")
    else:
        auth_enabled = smtp_details.get("auth_enabled", '')
        outgoing_mail_id = smtp_details.get("outgoing_mail_id", '')
        smtp_server = smtp_details.get("smtp_server", '')
        port = smtp_details.get("port", '')
        try:
            msg = MIMEMultipart()
            msg['From'] = outgoing_mail_id
            msg['To'] = ','.join(toaddr)
            if ccaddr:
                msg['CC'] = ','.join(ccaddr)
            msg['Subject'] = subject
            body = body
            msg.attach(MIMEText(body, 'html'))
            if attach_exist == "yes":
                with open(PATH + '/../dependencies/' + file_name, 'rb') as fil:
                    part = MIMEApplication(fil.read(), Name=basename(PATH + '/../dependencies/' + file_name))
                    part['Content-Disposition'] = 'attachment; filename="%s"' % basename(
                        PATH + '/../dependencies/' + file_name)
                    msg.attach(part)
            server = smtplib.SMTP(smtp_server, port)
            server.ehlo()
            server.starttls()
            server.ehlo()
            if smtp_details.get("auth_enabled", ''):
                username = smtp_details.get("username", '')
                smtp_password = smtp_details.get("smtp_password", '')
                server.login(username, smtp_password)
            text = msg.as_string()
            server.sendmail(outgoing_mail_id, toaddr + ccaddr, text)
            if os.path.exists(file_name):
                os.remove(file_name)
            return 'Send mail successfully'
        except Exception as e:
            raise e


def start(**kwargs):
    while True:
        url = "https://goerli.infura.io/v3/01e65d54328e4c7185f9069b66dba1d5"
        wallet_id = '0x256144a60f34288F7b03D345F8Cb256C502e0f2C'
        response = get_info(url, wallet_id)
        if response[0] == -1:
            send_mail(smtp_details=details, subject="Notification", body="Error While Fetching Data",file_name="", attach_exist=False, toaddr=['abc@xyz.com'])
        elif response[0] <= 0.01:
            send_mail(smtp_details=details, subject="Notification", body=f"Wallet balance is low\nBalance: {response[0]}", file_name="", attach_exist=False,
                      toaddr=['abc@xyz.com'])
            send_mail(f"Wallet balance is low\nBalance: {response[0]}")
        if not os.path.isfile(f"Result{wallet_id}.csv"):
            with open(f"Result{wallet_id}.csv", 'a') as file:
                file.write("ETH Balance,Status Code,Status Message,Time Stamp")
        with open(f"Result{wallet_id}.csv",'a') as file:
            file.write("\n{},{},{},{}".format(*response, datetime.now()))
        time.sleep(1800)
        #break


if __name__ == '__main__':
    start()
    # wallet address, email, status code, response_time -> PT
    # wallet address, value -> os
