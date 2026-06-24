import time, json



class SELECTOR:
    def __init__(self):
        self.settings = json.load(open('_json/settings.json'))
        self.rotating_proxy_ = self.settings['Settings']['Proxy']
        
        self.use_proxy_ = False
    
    def selection_(self):
        options_ = input(" * Your choice: ")
        
        if options_ not in ['1', '2']:
            for count_ in ['5', '4', '3', '2', '1']:
                print(f" * Choose a valid option, try after {count_} seconds", end = '\r', flush = True)
                time.sleep(1)
                
            print()
            return self.selection_()
        if options_ == '1':
            self.use_proxy_ = True
            
        else:
            self.use_proxy_ = False
    
    
selector = SELECTOR()
