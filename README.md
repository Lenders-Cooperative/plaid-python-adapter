# Plaid Python Adapter

This is a python adapter library for accessing Plaid APIs.

**Table of Contents** 

- [Environment](#environment)
- [1. Create Link Token](#create_link_tokenclient_user_idaccess_token)
- [2. Exchange Public Token](#exchange_public_tokenpublic_token)
- [3. Auth Request](#auth_requestaccess_tokenaccount_ids)
- [4. Identity Request](#identity_requestaccess_tokennoneaccount_ids)
- [5. Sync Bank Transfer Event](#sync_bank_transfer_eventafter_idcount)
- [6. Initialize Plaid](#initialize_plaidclient_namecountry_codeslanguage-products-account_subtypes)
- [Errors](#errors)


## _Environment:_ 
Environment Configuration parameters for this library

| Parameter Name |  Description |
|:--- |:--- |
| PLAID_CLIENT_ID | Plaid Client Id |
| PLAID_PUBLIC_KEY | Plaid Public Key |
| PLAID_SECRET | Plaid Secret Key |
| PLAID_ENV | Plaid Environment to work on. Sample values: 'sandbox','production','development'|
| PLAID_BASE_URL | The base url of plaid to connect their API. E.G. https://sandbox.plaid.com |

## Steps to generate access token
Plaid requires the user to authenticate in order to use their APIs.
So the steps for accessing the API are as below:
1. Using your UI client, make a request to create_link_token which will return the link token.
2. This link token will be sent to the UI for initializing Plaid. Once Plaid is initialized, we get the public token from plaid server.
3. Then using the public token you need to make a request to exchange_public_token to get the access token. This access token is used for all the remaining api calls.

### 1.create_link_token(client_user_id,access_token)
Use to get the plaid link token

> Mandatory field: <br>
`client_user_id` : Unique id to identify the client <br>
> Optional Field: <br>
`access_token` : If link token need to be re-initialized with the existing access token.<br>

> Response: For response, please refer to below link: <br>
https://plaid.com/docs/api/tokens/#linktokencreate

### 2.exchange_public_token(public_token)
Use to exchange public token for an access token

> Mandatory field: <br>
`public_token` : public token received from plaid client <br>

> Response: For response, please refer to below link: <br>
https://plaid.com/docs/api/tokens/#itempublic_tokenexchange

### 3.auth_request(access_token,account_ids)
Use to get account details associated with the access_token

> Mandatory field: <br>
`access_token` : Unique access token of the Plaid user <br>
> Optional Field: <br>
`account_ids` : List of account ids for which details needs to be fetched.<br>

> Response: For response, please refer to below link: <br>
https://plaid.com/docs/api/products/#authget

### 4.identity_request(access_token=None,account_ids)
Use to get identity details associated with the access_token

> Mandatory field: <br>
`access_token` : Unique access token of the Plaid user <br>
> Optional Field: <br>
`account_ids` : List of account ids for which details needs to be fetched.<br>

> Response: For response, please refer to below link: <br>
https://plaid.com/docs/api/products/#identityget

### 5.sync_bank_transfer_event(after_id,count)
Use to get bank transfer ACH details

> Mandatory field: <br>
`after_id` : The latest (largest) event_id fetched via the sync endpoint, or 0 initially.<br>
> Optional Field: <br>
`count` : The maximum number of bank transfer events to return.<br>
Default: 25 <br>
Minimum: 1 <br>
Maximum: 25 <br>


> Response: For response, please refer to below link: <br>
https://plaid.com/docs/api/products/#bank_transfereventsync

### 6.initialize_plaid(client_name,country_codes,language, products, account_subtypes)
Use to initialize plaid client for specific configuration. All the parameters are optional with the below default values.

> Optional Field: <br>
Intialization Parameters for Plaid

| Parameter name | Type | Default value | Description |
|:--- |:--- |:--- |:--- |
| client_name | `string`  | 'None' | The name of Plaid Client |
| country_codes | `list` | ['US'] | The country code of Plaid app.|
| language | `string` | 'en' | The language of Plaid app |
| products | `list` | ['auth'] | The products that are supported by Plaid app.|
| account_subtypes | `list` | ['checking', 'savings'] | The account sub-types returned by Plaid app |

### Errors
The below list of errors are expected for the API's

| Error name | API | Description |
|:--- |:--- |:--- |
| PlaidAdapterError | ALL API's | This is the base Error |
| PlaidAdapterConfigurationError | initialize_plaid | Raised when there is configuration error|
| PlaidCreateLinkTokenError | create_link_token | Raised when there is error while creating link token|
| PlaidExchangePublicTokenError | exchange_public_token | Raised when there is error while exchanging public  token for an access token|
| PlaidAuthError | auth_request | Raised when there is error while fetching auth details|
| PlaidIdentityError | identity_request | Raised when there is error while fetching identity details|
| PlaidApiInternalServerError | ALL API's | Raised when there is an internal error returned by Plaid server|
| PlaidBankTransferSyncEventError | sync_bank_transfer_event | Raised when there is an error in fetching bank transfer events|

## Examples

```python

from plaid_python_adapter.plaid_adapter import PlaidAdapter
from plaid_python_adapter.exceptions import *


def create_link_token():
    response_dict = {}
    plaid_adapter = PlaidAdapter()
    try:
        response = plaid_adapter.create_link_token(client_user_id='<Unique-Id>')
    except PlaidCreateLinkTokenError as err:
        #Handle the error
        pass
    except PlaidApiInternalServerError as err:
        #Handle the error
        pass
    response_dict = {
        'link_token': response.get('link_token'),
        'expiration': response.get('expiration'),
        'request_id': response.get('request_id')
    }
    return response_dict

def exchange_public_token(public_token):
    plaid_adapter = PlaidAdapter()
    try:
        response = plaid_adapter.exchange_public_token(public_token)
    except PlaidExchangePublicTokenError as err:
        #Handle the error
        pass
    except PlaidApiInternalServerError as err:
        #Handle the error
        pass
    access_token = response['access_token']
    return access_token

def auth_request(access_token=None, account_ids=None):
    accounts_details = {}
    plaid_adapter = PlaidAdapter()
    try:
        accounts_details = plaid_adapter.auth_request(access_token, account_ids)
    except PlaidAuthError as err:
        #Handle the error
        pass
    except PlaidApiInternalServerError as err:
        #Handle the error
        pass
    return accounts_details
```