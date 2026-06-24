from _source import (_api_number,
                    _login_account)

class UNLOCK_ACCOUNT:
    
    def __init__(self):
        self.base_url_ = "https://account.live.com/API/"
        
        self.parameters_ = _login_account.login_account.json_form_proofs_
        self.refer_ = _login_account.login_account.json_form_abuse_
        
        self.api_canary_ = ""
        
        
    def get_request_sms_(self):
        form_ = self.base_url_ + "Proofs/SendOtt"
        
        headers_ = {
            "Host": "account.live.com",
            "Connection": "keep-alive",
            "correlationId": self.parameters_['client_request_id'],
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
            "client-request-id": self.parameters_['client_request_id'],
            "canary": self.parameters_['canary'].encode().decode('unicode-escape'),
            "Content-type": "application/json; charset=utf-8",
            "hpgid": self.parameters_['hpgid'],
            "Accept": "application/json",
            "hpgact": "0",
            "Referer": self.refer_['fmHF'],
            "Origin": "https://account.live.com",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br, zstd"}
        
        json_ = {
            "action": "TierRestore",
            "proofCountryIso": _api_number.api_number.iso_,
            "channel": "SMS",
            "proofId": _api_number.api_number.phone_number_,
            "uiflvr": self.parameters_['uiflvr'],
            "scid": self.parameters_['scid'],
            "uaid": self.parameters_['client_request_id'],
            "hpgid": self.parameters_['hpgid']}
        
        with _login_account.login_account.session.post(form_, 
                               headers = headers_,
                               json = json_) as response:
           
            if response.status_code == 200:
                data_from_respose_ = response.json()
                if 'apiCanary' not in data_from_respose_:
                    return False
                self.api_canary_ = data_from_respose_['apiCanary']
                print(" * SMS sent")
            
                
                
    def get_unlocking_(self):
        form_ = self.base_url_ + "ConsumeOneTimeToken"
        
        headers_ = {
            "Host": "account.live.com",
            "correlationId": self.parameters_['client_request_id'],
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
            "client-request-id": self.parameters_['client_request_id'],
            "canary": self.api_canary_,
            "Content-type": "application/json; charset=utf-8",
            "hpgid": self.parameters_['hpgid'],
            "Accept": "application/json",
            "hpgact": "0",
            "Origin": "https://account.live.com",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.9"}
        
        json_ = {"ottPurpose": "TierRestore",
                 "ott": _api_number.api_number.sms_code_,
                 "channelType": "SMS",
                 "destinationPii": f"+{_api_number.api_number.country_code_}{_api_number.api_number.phone_number_}",
                 "uiflvr": self.parameters_['uiflvr'],
                 "scid": self.parameters_['scid'],
                 "uaid": self.parameters_['client_request_id'],
                 "hpgid": self.parameters_['hpgid']}
        
        with _login_account.login_account.session.post(form_,
                               headers = headers_,
                               json = json_) as response:
            if response.status_code == 200:
                data_from_respose_ = response.json()
                
                if 'apiCanary' not in data_from_respose_:
                    return False
                print(" * Account Unlocked!")
            
        
        
        
        
unlock_account = UNLOCK_ACCOUNT()        