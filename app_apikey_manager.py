import uuid
from infrastructure.security.apikey_manager import create_customer_credentials

'''
apikey 2d5388fd-73d9-4313-9aa0-9a4c6c1f2d66  client_secret 631b5d29-e173-4227-8774-fb9b8912e07e
'''

if __name__=='__main__':
    apikey = str(uuid.uuid4())
    secret = str(uuid.uuid4())
    create_customer_credentials(tenant='loyal_customer',apikey=apikey,client_secret=secret,rate_limit='3/minute')
    print(f'apikey {apikey}  client_secret {secret}')