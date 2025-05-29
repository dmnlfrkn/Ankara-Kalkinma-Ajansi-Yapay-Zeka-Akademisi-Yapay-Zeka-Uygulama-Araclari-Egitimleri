import requests



class FinanceAPICLient:
    def __init__(self,base_url='http://localhost:5005'):
        self.base_url = base_url
        self.username = None
        self.password = None


    def register(self,username,password):
        response = requests.post(f'{self.base_url}/register',json={'username':username,'password':password})
        print("Çalıştı!")
        response.raise_for_status()
        return response.json()

    def login(self,username,password):
        response = requests.post(f'{self.base_url}/login', json={'username': username, 'password': password})
        response.raise_for_status()
        self.username = username
        self.password = password
        return response.json()

    def add_transaction(self,amount,category,description, is_income):
        response = requests.post(f'{self.base_url}/transactions', json={'username': self.username, 'password': self.password,
                                 'amount':amount,'category':category,'description':description,'is_income':is_income})
        response.raise_for_status()
        return response.json()

    def get_transactions(self,category=None):
        params = {'username':self.username, 'password':self.password}
        if category:
            params['category']=category
        response = requests.get(f'{self.base_url}/transactions',params=params)
        response.raise_for_status()
        return response.json()

    def delete_transaction(self,transaction_id):
        params = {'username':self.username,'password':self.password}
        response = requests.delete(f'{self.base_url}/transactions/{transaction_id}',params=params)
        response.raise_for_status()
        return response.json()
