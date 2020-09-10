import requests
import json

admin_dict = {}


def get_token():
    url = "https://login.microsoftonline.com/avaemtech.onmicrosoft.com/oauth2/token"

    payload = 'resource=b42b94be-4012-4af3-95ac-f7e8c5022dfb&client_id=70a017c9-a62d-4372-a2e1-113afecf8507' \
              '&client_secret=PDL~4aaT.-eEx5pP.5kVT67Ne2b.9_1kr6&grant_type=client_credentials&scope=https' \
              '://mscblockchain-h4atns.azurewebsites.net.default'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': 'stsservicecookie=ests; fpc=AoFiR8Rd_UlBvjV1OdAQ-vu09zlXAgAAAJIFstYOAAAA; '
                  'x-ms-gateway-slice=estsfd'
    }

    raw_token_data = requests.request("POST", url, headers=headers, data=payload)

    token_data = raw_token_data.json()
    access_token = token_data['access_token']

    return access_token




