
from _source import (_api_number,
                    _login_account,
                    _unlock_account,
                    _selector)

class MAIN:
    
    def __init__(self):
        self.account_ = [_.strip() for _ in open("account.txt", encoding = "utf-8").readlines() if _]
        
    def _init_(self):
        for account in self.account_:
            print()
            
            _login_account.login_account.get_request_abuse_paramerts_(account.split("|")[0],
                                                                      account.split("|")[1])
            
            if not _login_account.login_account.json_form_proofs_['canary']:
                print(" * Something went wrong on login...")
                return False
            
            _api_number.api_number.get_balance_()
            
            _api_number.api_number.get_request_number_()
            
            if _api_number.api_number.phone_number_ == "" or _api_number.api_number.phone_number_ == None:
                print(" * Something went wrong finding phone...")
                return False
            
            _unlock_account.unlock_account.get_request_sms_()
            
            if _unlock_account.unlock_account.api_canary_ == "" or _unlock_account.unlock_account.api_canary_ == None:
                print(""" 
* Something wrong requesting canarys...
  caused by one of this:
  error_status_1208: "Phone number flagged as spam or invalidated",
  error_status_1346": "Service temporarily offline""")
                return False
            
            _api_number.api_number.get_sms_code_()
            
            if _api_number.api_number.sms_code_ == "" or _api_number.api_number.sms_code_ == None:
                print(" * Something went wrong requesting sms...")
                return False
            
            _unlock_account.unlock_account.get_unlocking_()
            
            
            
        
main = MAIN()
main.decode_auth_()
INFORMATION = """ 
[ This program is used to phone unlock Microsoft Accounts (study only)
  Phone API used is sms-activate.org 
  
  For a better performance residential proxies are recommended
  Proxy format user:password@host:port
  
  Make sure proxy is on phone location aswell
  
  Option 1 - Use Proxy
  Option 2 - Proxyless
  
  To cancel process press CTRL + C ]
"""
print(INFORMATION)

_selector.selector.selection_()

main._init_()
