import requests
from decouple import config
import ssl
import json
from websocket import create_connection
import uuid


class WebSocketClient:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.cookie = self.__get_cookie()
        self.websocket_url = config('WEBSOCKET_URL')
        self.websocket = None
        self.last_message = None
    
    def __get_cookie(self):
        """
        send login request to server and get cookie
        for websocket connection
        """
        
        #env e cixarilmalidir
        login_url = config('MESH_URL')+"/login"
        response = requests.post(login_url, data={"action": 'login', 'username': self.username, "password": self.password},
                                 verify=False)
        if response.status_code == 200:
            cookie = response.headers.get('Set-Cookie')
            cookie = cookie.split(';')
            cookie = cookie[0] + ';' + cookie[4].split(',')[1]
            return cookie
        else:
            print('Login request failed')
            return None

    def connect(self):
        """
        connect to websocket server
        """
        headers = {'Cookie': self.cookie}
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        self.websocket = create_connection(self.websocket_url, header = headers, sslopt={"cert_reqs": ssl.CERT_NONE})
        print('WebSocket connection opened')

    def __generate_correlation_id(self):
        return uuid.uuid4()
    
    def __send_mesh_info_for_create(self, desc, meshname, correlation_id):
        """
        send mesh info to server for create new mesh
        """
        company_input = {"action": "createmesh", "desc": desc, "meshname": meshname, "meshtype": 2, "correlationid": correlation_id}
        try:
            self.websocket.send(json.dumps(company_input))
        except Exception as e:
            self.last_message = str(e)
            return None
    
    def __send_user_info_for_create(self, email, username, password, correlation_id):
        user_input = {"action": "adduser", "email": email, "username": username, "pass": password,"randomPassword": False,
                     "removeEvents": True, "resetNextLogin": False, "correlationid": correlation_id}
        try:
            self.websocket.send(json.dumps(user_input))
        except Exception as e:
            self.last_message = str(e)
            return None

    def __receive_message(self, correlation_id=None):
        """
        receive message from websocket server
        until target action is received
        """
        while True:
            message = self.websocket.recv()
            print("message-----> ",message)
            if message:
                message = json.loads(message)
            else :
                continue
            print(message)
            if message.get("correlationid", None) == correlation_id:
                self.last_message = message
                return message


    def create_new_group(self, desc, company_name):
        correlation_id = self.__generate_correlation_id()
        self.__send_mesh_info_for_create(desc=desc, meshname=company_name, correlation_id=correlation_id)
        self.__receive_message(correlation_id=correlation_id)


    def create_new_user(self, email, username, password):
        correlation_id = self.__generate_correlation_id()
        self.__send_user_info_for_create(email=email, username=username, password=password, correlation_id=correlation_id)
        self.__receive_message(correlation_id=correlation_id)



    def close(self):
        """
        Method to terminate a websocket connection.
        """
        
        self.websocket.close()
        print('Websocket connection closed successfully')
