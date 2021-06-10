
# Python user-defined exceptions
class PlaidAdapterError(Exception):
    """Base class for other exceptions"""
    def __init__(self, error_details, message="Plaid Exception!"):
        self.error_details = error_details
        self.error_message = message

class PlaidAdapterConfigurationError(Exception):
    def __init__(self, error_details, message="Plaid Configuration missing!"):
        self.error_details = error_details
        self.error_message = message
        super().__init__(self.error_message)

class PlaidCreateLinkTokenError(PlaidAdapterError):
    def __init__(self, error_details, message="Plaid Exception while creating link token!"):
        self.error_details = error_details
        self.error_message = message
        super().__init__(self.error_message)

class PlaidExchangePublicTokenError(PlaidAdapterError):
    def __init__(self, error_details, message="Plaid Exception while exchanging public token for an access token!"):
        self.error_details = error_details
        self.error_message = message
        super().__init__(self.error_message)

class PlaidAuthError(PlaidAdapterError):
    def __init__(self, error_details, message="Plaid Exception while fetching authentication details!"):
        self.error_details = error_details
        self.error_message = message
        super().__init__(self.error_message)
    
class PlaidIdentityError(PlaidAdapterError):
    def __init__(self, error_details, message="Plaid Exception while fetching user identity details!"):
        self.error_details = error_details
        self.error_message = message
        super().__init__(self.error_message)

class PlaidApiInternalServerError(PlaidAdapterError):
    def __init__(self, error_details, message="Plaid Api Internal Error occurred!"):
        self.error_details = error_details
        self.error_message = message
        super().__init__(self.error_message)

class PlaidBankTransferSyncEventError(PlaidAdapterError):
    def __init__(self, error_details, message="Plaid Exception while exchanging public token for an access token!"):
        self.error_details = error_details
        self.error_message = message
        super().__init__(self.error_message)
