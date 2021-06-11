import os, requests, json

from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from plaid_python_adapter.exceptions import (
    PlaidAdapterError,
    PlaidCreateLinkTokenError,
    PlaidExchangePublicTokenError,
    PlaidAuthError,
    PlaidIdentityError,
    PlaidApiInternalServerError,
    PlaidBankTransferSyncEventError,
    PlaidAdapterConfigurationError,
)


class PlaidAdapter:

    def __init__(self):
        retry_strategy = Retry(
            total=5,
            backoff_factor=10,
            status_forcelist=[429, 500, 502, 503, 504],
            method_whitelist=["HEAD", "GET", "PUT", "DELETE", "OPTIONS", "TRACE"]
        )
        self.adapter = HTTPAdapter(max_retries=retry_strategy)
        self.http = requests.Session()
        self.headers = {"Content-Type": "application/json", "Accept": "application/json"}
        #http.mount("https://", adapter)

        self.initialize_plaid()
    
    def initialize_plaid(self, client_name='None', country_codes=['US'], language='en', products=['auth'], account_subtypes=["checking", "savings"]):
        self.client_name = client_name
        self.country_codes = country_codes
        self.language = language
        self.products = products
        self.account_subtypes = account_subtypes
        self.plaid_client_id = os.environ.get('PLAID_CLIENT_ID')
        self.plaid_public_key = os.environ.get('PLAID_PUBLIC_KEY')
        self.plaid_secret = os.environ.get('PLAID_SECRET')
        self.plaid_environment = os.environ.get('PLAID_ENV')
        self.plaid_base_url = os.environ.get('PLAID_BASE_URL')
        if not [x for x in (self.plaid_client_id,self.plaid_public_key,self.plaid_secret,self.plaid_environment,self.plaid_base_url) if x is None]:
            pass
        else:
            raise PlaidAdapterConfigurationError('Missing Plaid Configuration!')

    def create_link_token(self, client_user_id=None, access_token=None):
        request={}
        request['client_id'] = self.plaid_client_id
        request['secret'] = self.plaid_secret
        request['client_name'] = self.client_name
        request['country_codes'] = self.country_codes
        request['language'] = self.language
        user = {}
        user['client_user_id'] = client_user_id
        request['user'] = user
        # This is required if the user already linked his account with Plaid and needs to verify the authentication.
        if access_token:
            request['access_token'] = access_token
        else:
            request['products'] = self.products    
            account_filters = {}
            depository= {}
            depository['account_subtypes'] = self.account_subtypes
            account_filters['depository'] = depository
            request['account_filters'] = account_filters
        link_url = self.plaid_base_url + '/link/token/create'
        create_link_token_response = requests.post(link_url, data=json.dumps(request), headers=self.headers)
        res_http_code = create_link_token_response.status_code
        response_text = create_link_token_response.text
        if res_http_code != 200:
            if res_http_code == 500:
                raise PlaidApiInternalServerError(response_text)
            else:
                raise PlaidCreateLinkTokenError(response_text)
        
        return json.loads(response_text)
    
    def exchange_public_token(self, public_token=None):
        request={}
        request['client_id'] = self.plaid_client_id
        request['secret'] = self.plaid_secret
        if public_token is None:
            raise PlaidExchangePublicTokenError('Missing mandatory public token!')
        request['public_token'] = public_token
        exchange_public_token_url = self.plaid_base_url + '/item/public_token/exchange'
        exchange_public_token_response = requests.post(exchange_public_token_url, data=json.dumps(request), headers=self.headers)
        res_http_code = exchange_public_token_response.status_code
        response_text = exchange_public_token_response.text
        if res_http_code != 200:
            if res_http_code == 500:
                raise PlaidApiInternalServerError(response_text)
            else:
                raise PlaidExchangePublicTokenError(response_text)
        return json.loads(response_text)

    def auth_request(self, access_token=None, account_ids=None):
        request={}
        request['client_id'] = self.plaid_client_id
        request['secret'] = self.plaid_secret
        request['access_token'] = access_token
        if account_ids:
            options = {}
            options['account_ids'] = account_ids
            request['options'] = options
        auth_request_url = self.plaid_base_url + '/auth/get'
        auth_response = requests.post(auth_request_url, data=json.dumps(request), headers=self.headers)
        res_http_code = auth_response.status_code
        response_text = auth_response.text
        if res_http_code != 200:
            if res_http_code == 500:
                raise PlaidApiInternalServerError(response_text)
            else:
                raise PlaidAuthError(response_text)
        
        return json.loads(response_text)

    
    def identity_request(self, access_token=None, account_ids=None):
        request={}
        request['client_id'] = self.plaid_client_id
        request['secret'] = self.plaid_secret
        request['access_token'] = access_token
        if account_ids:
            options = {}
            options['account_ids'] = account_ids
            request['options'] = options
        identity_request_url = self.plaid_base_url + '/identity/get'
        identity_response = requests.post(identity_request_url, data=json.dumps(request), headers=self.headers)
        res_http_code = identity_response.status_code
        response_text = identity_response.text
        if res_http_code != 200:
            if res_http_code == 500:
                raise PlaidApiInternalServerError(response_text)
            else:
                raise PlaidIdentityError(response_text)
        
        return json.loads(response_text)

    def sync_bank_transfer_event(self, after_id=None, count=None):
        request={}
        request['client_id'] = self.plaid_client_id
        request['secret'] = self.plaid_secret
        if after_id is not None:
            request['after_id'] = after_id
        if count is not None:
            request['count'] = count
        sync_bank_transfer_url = self.plaid_base_url + '/bank_transfer/event/sync'
        bank_transfer_sync_response = requests.post(sync_bank_transfer_url, data=json.dumps(request), headers=self.headers)
        res_http_code = bank_transfer_sync_response.status_code
        response_text = bank_transfer_sync_response.text
        if res_http_code != 200:
            if res_http_code == 500:
                raise PlaidApiInternalServerError(response_text)
            else:
                raise PlaidBankTransferSyncEventError(response_text)
        return json.loads(response_text)
