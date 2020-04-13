import datetime
import base64
# from flask import request,json,jsonify
import requests
import json
from requests.auth import HTTPBasicAuth

class mpesa:
    # def __init__(self, num, Amount):
    #     # self.stk_url=str(''),
    #     self.token_url='https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials',
    date = datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S'),
    access_token = mpesa.access_token(),
    coded =bs64(174379,passkey,str(date))
    #     self.num= num
    #     self.Amount=Amount.strip()
    #     self.datentime=str(self.date[0])


 
    
    def bs64(self, shortp, np, timestp):
        data = str(shortp)+np+timestp

        encodedBytes = base64.b64encode(data.encode("utf-8"))
        encodedStr = str(encodedBytes, "utf-8")
        return encodedStr

    @classmethod
    def access_token(cls):
        consumer_key = "P9viP4n9XTz96cW6RH5ALoNIchidf4Cg"
        consumer_secret = "GDVm1AjD09bkq4PU"
        api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    
        r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
        m =json.loads(r)
        return m["access_token"]
    
 


    @classmethod
    def make_stk_push(cls,num,Amount):
        Amount=str(Amount)
        num =str(num)
        
        api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        headers = { "Authorization": "Bearer %s" % access_token }
        passkey ='bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'
        
        data={ 
                    "BusinessShortCode": "174379",
                    "Password": f"{coded}",
                    "Timestamp": date,
                    "TransactionType":"CustomerPayBillOnline",
                    "Amount":Amount,
                    "PartyA":num,
                    "PartyB":"174379",
                    "PhoneNumber":num,
                    "CallBackURL":"http://485f4595.ngrok.io/.webhook/mpesa",
                    "AccountReference":"test",
                    "TransactionDesc":"test"
            }
        # coded =self.bs64(174379,'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919',self.datentime)
        # print(data["Password"])
        # print(self.datentime)
        # print(self.Amount)
        # print(data["Amount"])
        # print(self.num)

        # requests.post(api_url, json = request, headers=headers)
        response = requests.post(api_url, json = data, headers=headers)
        print(response)
        return response