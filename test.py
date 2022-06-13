
# from run import app
import unittest2
import requests
import random
import string
import random

class FlaskTest(unittest2.TestCase):
    API_URL_LOGIN = "http://127.0.0.1:5000/login"
    API_URL_REGISTER = "http://127.0.0.1:5000/register"
    BASE = "http://127.0.0.1:5000/"

    
    def test_login(self):
        response = requests.post(FlaskTest.API_URL_LOGIN, {"login": "admin", "password": "admin"})
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    def test_register(self):
        letters = string.ascii_lowercase
        login = ''.join(random.choice(letters) for i in range(10))
        password = ''.join(random.choice(letters) for i in range(10))

        response = requests.post(FlaskTest.API_URL_REGISTER, {"login": login, "password": password})
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    def test_login_fail(self):
        letters = string.ascii_lowercase
        login = ''.join(random.choice(letters) for i in range(10))
        password = ''.join(random.choice(letters) for i in range(10))

        response = requests.post(FlaskTest.API_URL_LOGIN, {"login": login, "password": password})
        statuscode = response.status_code
        self.assertEqual(statuscode, 404)
    
    def test_register_fail(self):
        response = requests.post(FlaskTest.API_URL_REGISTER, {"login": "admin", "password": "admin"})
        statuscode = response.status_code
        self.assertEqual(statuscode, 409)

    def test_put_car(self):
        response_login = requests.post(FlaskTest.API_URL_LOGIN, {"login": "admin", "password": "admin"})
        cookie = response_login.cookies
        response = requests.put(FlaskTest.BASE + "car/{}".format(random.randint(0, 10000)), {"brand": "toyota", "version": 2, "year": 2005}, cookies=cookie)
        statuscode = response.status_code
        self.assertEqual(statuscode, 201)
    
    def test_put_car_fail(self):
        response_login = requests.post(FlaskTest.API_URL_LOGIN, {"login": "admin", "password": "admin"})
        cookie = response_login.cookies
        random_num = random.randint(0, 10000000)
        response = requests.put(FlaskTest.BASE + "car/{}".format(random_num), {"brand": "toyota", "version": 2, "year": 2005}, cookies=cookie)
        response = requests.put(FlaskTest.BASE + "car/{}".format(random_num), {"brand": "toyota", "version": 2, "year": 2005}, cookies=cookie)
        statuscode = response.status_code
        self.assertEqual(statuscode, 404)
    
    def test_get_car(self):
        response_login = requests.post(FlaskTest.API_URL_LOGIN, {"login": "admin", "password": "admin"})
        cookie = response_login.cookies
        random_num = random.randint(0, 10000000)
        response = requests.put(FlaskTest.BASE + "car/{}".format(random_num), {"brand": "toyota", "version": 2, "year": 2005}, cookies=cookie)
        response = requests.get(FlaskTest.BASE + "car/{}".format(random_num), cookies=cookie)
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
    
    def test_get_car_fail(self):
        response_login = requests.post(FlaskTest.API_URL_LOGIN, {"login": "admin", "password": "admin"})
        cookie = response_login.cookies
        random_num = random.randint(0, 10000000)
        response = requests.get(FlaskTest.BASE + "car/{}".format(random_num), cookies=cookie)
        statuscode = response.status_code
        self.assertEqual(statuscode, 404)

    def test_delete_car(self):
        response_login = requests.post(FlaskTest.API_URL_LOGIN, {"login": "admin", "password": "admin"})
        cookie = response_login.cookies
        random_num = random.randint(0, 10000000)
        response = requests.put(FlaskTest.BASE + "car/{}".format(random_num), {"brand": "toyota", "version": 2, "year": 2005}, cookies=cookie)
        response = requests.delete(FlaskTest.BASE + "car/{}".format(random_num), cookies=cookie)
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
    
    def test_delete_car_fail(self):
        response_login = requests.post(FlaskTest.API_URL_LOGIN, {"login": "admin", "password": "admin"})
        cookie = response_login.cookies
        random_num = random.randint(0, 10000000)
        response = requests.delete(FlaskTest.BASE + "car/{}".format(random_num), cookies=cookie)
        statuscode = response.status_code
        self.assertEqual(statuscode, 404)

