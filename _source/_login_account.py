import requests, re

from _source import _selector

class LOGIN_ACCOUNT:
    
    def __init__(self):
        self.session = None
        
        self.base_url_ = "https://login.live.com/"
        
        self.json_form_abuse_ = {}
        
        self.json_form_proofs_ = {}
        
        
    def get_parameters_and_redirect_(self):
        self.session = requests.Session()
        
        if _selector.selector.use_proxy_:
            self.session.proxies = {'https': f'http://{_selector.selector.rotating_proxy_}',
                                    'http': f'http://{_selector.selector.rotating_proxy_}'}
            
        else:
            pass
        
        with self.session.get(self.base_url_) as response:
            if response.status_code == 200:
                data_from_response_ = response.text
                try:
                    form_ =  re.findall("urlPost:'(.+?(?=\'))", data_from_response_)[0]
                    ppft_ = data_from_response_.split(''''<input type="hidden" name="PPFT" id="i0327" value="''')[1].split('"')[0]
                    
                except:
                    return False
                
                return form_, ppft_
            
    
    def get_login_into_account_(self, email, password):
        form_ , ppft_ = self.get_parameters_and_redirect_()

        data_ = {
            "PPFT": ppft_,
            "login": f"{email}",
            "loginfmt": f"{email}",
            "passwd": f"{password}"}
        
        with self.session.post(form_, data = data_) as response:
            if response.status_code == 200:
                data_from_response_ = response.text
                try:
                    self.json_form_abuse_.update({
                        "fmHF": data_from_response_.split('id="fmHF" action="')[1].split('"')[0],
                        "pprid": data_from_response_.split('id="pprid" value="')[1].split('"')[0],
                        "ipt": data_from_response_.split('id="ipt" value="')[1].split('"')[0],
                        "uaid": data_from_response_.split('id="uaid" value="')[1].split('"')[0]})
                    
                except:
                    return False
                
                print(" * Access granted")
                
                
    def get_request_abuse_paramerts_(self, email, password):
        print(f" * Accessing to {email}")
        
        self.get_login_into_account_(email, password)
        
        data_ = {
            "pprid": self.json_form_abuse_['pprid'],
            "ipt": self.json_form_abuse_['ipt'],
            "uaid": self.json_form_abuse_['uaid']}
        
        with self.session.post(self.json_form_abuse_['fmHF'], data = data_) as response:
            if response.status_code == 200:
                data_from_response_ = response.text
                try:
                    self.json_form_proofs_.update({
                    "canary": data_from_response_.split('"apiCanary":"')[1].split('"')[0],
                    "client_request_id": data_from_response_.split('"sUnauthSessionID":"')[1].split('"')[0],
                    "hpgid": data_from_response_.split('"hpgid":')[1].split(',')[0],
                    "scid": data_from_response_.split('"iScenarioId":')[1].split(',')[0],
                    "uiflvr": data_from_response_.split('"iUiFlavor":')[1].split(',')[0]})
                except:
                    return False
                
                print(" * Parameters obtained")
                
                
            
        
login_account = LOGIN_ACCOUNT()