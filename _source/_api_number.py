import requests, json, random, time

from _source import _microsoft_list

class API_NUMBER:
    
    def __init__(self):
        self.settings = json.load(open('_json/settings.json'))
        self.api_key_ = self.settings['Settings']['Api Key']
        
        self.base_url_ = f"https://api.sms-activate.org/stubs/handler_api.php?api_key={self.api_key_}&action="
        
        self.session = requests.Session()
        
        self.list_of_countrys_ = []
        self.list_of_operators_ = []
        
        self.got_country = False
        
        self.selected_country_ = ""
        self.iso_ = ""
        self.country_code_ = ""
        
        self.selected_operator_ = ""
        
        self.number_id_ = ""
        self.phone_number_ = ""
        
        self.sms_code_ = ""
        
    def get_balance_(self):
        form_ = self.base_url_ + "getBalance"
        
        with self.session.get(form_) as response:
            data_from_response_ = response.text
            
            if not "ACCESS_BALANCE" in data_from_response_:
                return
            
            value_ = data_from_response_.split(":")[1]
            
            print(f" * Balance: {value_}")
        
    def get_best_service_(self):
        form_ = self.base_url_ + "getTopCountriesByService&service=mm"
        
        with self.session.get(form_) as response:
            data_from_response_ = response.json()
            
            if not "0" in data_from_response_:
                return
            
            for _ in data_from_response_:
                current_sub_ = data_from_response_[_]

                country_ = current_sub_['country']
                price_ = current_sub_['price']
                amount_ = current_sub_['count']

                if price_ < 2.0 and amount_ > 1:
                    self.list_of_countrys_.append(f"{country_}")
                    
    def get_country_offering_service_(self):
        self.list_of_countrys_.clear()
        
        self.get_best_service_()
        
        self.selected_country_ = random.choice(self.list_of_countrys_)
                    
        form_ = self.base_url_ + "getCountries"
        
        with self.session.get(form_) as response:
            data_from_response_ = response.json()
            
            if not "0" in data_from_response_:
                return
            
            #Form for USA country ONLY
            if self.selected_country_ in data_from_response_:
                
                checking_ = data_from_response_["12"] #Name is USA (VIRTUAL) so we need change
                country_by_name_ = checking_['eng']
                country_by_name_ = "United States"

                self.selected_country_ = 12 #We need relocate USA as primordial numb if wanna change erase this line
                
                for country_info_ in _microsoft_list.microsoft_list.list_:
                    names_ = country_info_["displayValue"]
                    
                    if country_by_name_ in names_:
                        self.iso_ = country_info_["iso"]
                        self.country_code_ = country_info_["code"]
                        
                        print(f" * Country: '{country_by_name_}' | ISO: '{self.iso_}' | Code: '{self.country_code_}'")
                        self.got_country = True
                        self.get_operator_()
                        
                if not self.got_country:
                    return self.get_country_offering_service_()
                
            #Form for random country
#         if self.selected_country_ in data_from_response_:
#                checking_ = data_from_response_[self.selected_country_]
#                country_by_name_ = checking_['eng']
#                
#                for country_info_ in _microsoft_list.microsoft_list.list_:
#                    names_ = country_info_["displayValue"]
#                    
#                    if country_by_name_ in names_:
#                        self.iso_ = country_info_["iso"]
#                        self.country_code_ = country_info_["code"]
#                        print(f" * Country: '{country_by_name_}' | ISO: '{self.iso_}' | Code: '{self.country_code_}'")
#                        self.got_country = True
#                        self.get_operator_()
#                        
#                if not self.got_country:
#                    return self.get_country_offering_service_() 
                        
               
            
    def get_operator_(self):
        form_ = self.base_url_ + "getOperators&country={self.selected_country_}"
        
        with self.session.get(form_) as response:
            data_from_response_ = response.json()
            
            if not data_from_response_['status'] == 'success':
                return
            
            for sublist_ in data_from_response_["countryOperators"]:
                try:
                    for operators in sublist_:
                        self.list_of_operators_.append(operators)
                    
                    self.selected_operator_ = random.choice(self.list_of_operators_)
                    print(f" * Operator: '{self.selected_operator_}'")
                    
                except:
                    pass
                
    def get_request_number_(self):
        self.get_country_offering_service_()
        
        form_ = self.base_url_ + f"getNumber&service=mm&country={self.selected_country_}"
        
        with self.session.get(form_) as response:
            data_from_response_ = response.text
            
            if "ACCESS_NUMBER" not in data_from_response_:
                print(f" * Theres not online service for this Country/Operator")
                return
            
            self.number_id_ = data_from_response_.split(':')[1]
            phone_number_and_code_ = data_from_response_.split(':')[2]
            self.phone_number_ = phone_number_and_code_.split(self.country_code_)[1]
            
            print(f" * Phone: +{self.country_code_} {self.phone_number_}")
        
    
            
    def get_sms_code_(self):
        print(" * Searching SMS with provider")
        form_ = self.base_url_ + f"getStatus&id={self.number_id_}"
        
        for _ in range(60):
            with self.session.get(form_) as response:
                data_from_response_ = response.text
                
                if 'STATUS_WAIT_CODE' in data_from_response_:
                    time.sleep(0.3)
                else:
                    try:
                        
                        self.sms_code_ = data_from_response_.split(':')[1]
                        print(f" * Your SMS code is: {self.sms_code_}")
                        self.session.get(self.base_url_ + f"setStatus&status=6&id={self.number_id_}")
                        break
                    except:
                        return False
    
api_number = API_NUMBER()

                
            