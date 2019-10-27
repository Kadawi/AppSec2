import unittest
from bs4 import BeautifulSoup
import requests
import string
import random


server_address = "http://127.0.0.1:5000"

def randomString(stringLength=10):
	#Generate a random string of fixed length
		letters = string.ascii_lowercase
		return ''.join(random.choice(letters) for i in range(stringLength))
	
#Prevents duplicate registration errors when running tests in succession.
randomUser = randomString()

def getElementByID(text, eid):
	soup = BeautifulSoup(text, "html.parser")
	result = soup.find(id=eid)
	return result

def login(uname, pword, twofactor, session=None):
	addr = server_address + "/login"
	if session is None:
		s = requests.session()                                                         
	response = s.get(addr)                                                                                       
	soup = BeautifulSoup(response.text, "html.parser")
	for n in soup('input'):                                                        
		if n['name'] == 'csrf_token':                                             
			token = n['value']                                                     
			break
	test_creds = {"uname": uname, "pword":pword, "2fa": twofactor, "csrf_token": token}
	r = s.post(addr, data=test_creds)
	print(r)
	success = getElementByID(r.text, "result")
	assert success != None, "Missing result in your login response"
	return "success" in success.text

def register(uname, pword, twofactor, session=None):
	addr = server_address + "/register"
	s = requests.session()                                                         
	response = s.get(addr)                                                                                       
	soup = BeautifulSoup(response.text, "html.parser")
	for n in soup('input'):                                                        
		if n['name'] == 'csrf_token':                                             
			token = n['value']                                                     
			break
	test_creds = {"uname": uname, "pword":pword, "2fa": twofactor, "csrf_token": token}
	r = s.post(addr, data=test_creds)
	print(r)
	success = getElementByID(r.text, "success")
	assert success != None, "Missing result in register response"
	return "success" in success.text

def spellcheck(spelltxt):
	addr = server_address + "/spell_check"
	s = requests.session()                                                         
	response = s.get(addr)                                                                                       
	soup = BeautifulSoup(response.text, "html.parser")
	token = ""
	for n in soup('input'):                                                        
		if n['name'] == 'csrf_token':                                             
			token = n['value']                                                     
			break
	test_text = {"csrf_token": token, "inputtext": spelltxt}
	r = s.post(addr, data=test_text)
	print(r)
	result = getElementByID(r.text, "misspelled")
	assert result != None, "Missing Spellcheck Output"
	return "floof" in result.text

class TestAppFunctionality(unittest.TestCase):
#add tests here	

#Server Alive
	def test_01_ServiceAlive(self):
		req = requests.get(server_address)
		self.assertEqual(req.status_code, 200)
#Register Loads
	def test_02_RegisterLives(self):
		req = requests.get(server_address + "/register")
		self.assertEqual(req.status_code, 200)
#Regular Register
	def test_03_SuccessfulRegister(self):
		reg_addr = server_address + "/register"
		resp = register(randomUser, "Admin", "1231231234")
		self.assertTrue(resp, "Valid Registration Failed")
#Register with no pass
	def test_04_InvalidRegister(self):
		reg_addr = server_address + "/register"
		resp = register(randomUser, "", "")
		self.assertFalse(resp, "Invalid Registration Allowed")
#Register Already taken
	def test_05_AlreadyRegistered(self):
		reg_addr = server_address + "/register"
		resp = register(randomUser, "Admin", "1231231234")
		self.assertFalse(resp, "Duplicate Registration Allowed")
#Spellcheck denies access w/out session
	def test_06_SpellcheckAccessDenial(self):
		req = requests.get(server_address + "/spell_check")
		self.assertNotEqual(req.status_code, 200)
#Login Loads
	def test_07_LoginLives(self):
		req = requests.get(server_address + "/login")
		self.assertEqual(req.status_code, 200)
#Login Incorrect User
	def test_08_IncorrectUsernameLogin(self):
		login_addr = server_address + "/login"
		resp = login("Whoops", "Admin", "1231231234")
		self.assertFalse(resp, "Login authenticated invalid credentials")
#Login Incorrect Pass
	def test_09_IncorrectPassLogin(self):
		login_addr = server_address + "/login"
		resp = login(randomUser, "Whoops", "1231231234")
		self.assertFalse(resp, "Login authenticated invalid credentials")
#Login Incorrect 2fa
	def test_10_Incorrect2faLogin(self):
		login_addr = server_address + "/login"
		resp = login(randomUser, "Admin", "1")
		self.assertFalse(resp, "Login authenticated invalid credentials")
#Login Correct
	def test_11_CorrectLogin(self):
		login_addr = server_address + "/login"
		resp = login(randomUser, "Admin", "1231231234")
		self.assertTrue(resp, "Successful Login")
#Spellcheck Loads with Session
	def test_12_SpellcheckAccessGranted(self):
		addr = server_address + "/login"
		s = requests.session()                                                         
		response = s.get(addr)                                                                                       
		soup = BeautifulSoup(response.text, "html.parser")
		for n in soup('input'):                                                        
			if n['name'] == 'csrf_token':                                             
				token = n['value']                                                     
				break
		test_creds = {"uname":randomUser, "pword":"Admin", "2fa":"1231231234", "csrf_token":token}
		r = s.post(addr, data=test_creds)
		resp= s.get(server_address + "/spell_check")
		self.assertEqual(resp.status_code, 200)
#Spellcheck correct output
	def test_13_spellcheck(self):
		addr = server_address + "/login"
		s = requests.session()                                                         
		response = s.get(addr)                                                                                       
		soup = BeautifulSoup(response.text, "html.parser")
		for n in soup('input'):                                                        
			if n['name'] == 'csrf_token':                                             
				token = n['value']                                                     
				break
		test_creds = {"uname":randomUser, "pword":"Admin", "2fa":"1231231234", "csrf_token":token}
		r = s.post(addr, data=test_creds)
		spell_addr = server_address + "/spell_check"
		spell = s.get(spell_addr)                                                                                       
		soup = BeautifulSoup(spell.text, "html.parser")
		token = ""
		for n in soup('input'):                                                        
			if n['name'] == 'csrf_token':                                             
				token = n['value']                                                     
				break
		test_text = {"csrf_token": token, "inputtext": "floof hello"}
		r = s.post(spell_addr, data=test_text)
		print(r)
		result = getElementByID(r.text, "misspelled")
		assert result != None, "Missing Spellcheck Output"
		resp = "floof" in result.text
		self.assertTrue(resp, "Spellcheck failed")
#Spellcheck no CSRF 
	def test_14_spellcheckCSRF(self):
		addr = server_address + "/login"
		s = requests.session()                                                         
		response = s.get(addr)                                                                                       
		soup = BeautifulSoup(response.text, "html.parser")
		for n in soup('input'):                                                        
			if n['name'] == 'csrf_token':                                             
				token = n['value']                                                     
				break
		test_creds = {"uname":randomUser, "pword":"Admin", "2fa":"1231231234", "csrf_token":token}
		r = s.post(addr, data=test_creds)
		spell_addr = server_address + "/spell_check"
		spell = s.get(spell_addr)                                                                                       
		soup = BeautifulSoup(spell.text, "html.parser")
		token = ""
		test_text = {"csrf_token": token, "inputtext": "floof hello"}
		r = s.post(spell_addr, data=test_text)
		print(r)
		self.assertNotEqual(r.status_code, 200, "Spellcheck failed")
#Logout removes session
	def test_15_logout(self):
		addr = server_address + "/login"
		s = requests.session()                                                         
		response = s.get(addr)                                                                                       
		soup = BeautifulSoup(response.text, "html.parser")
		for n in soup('input'):                                                        
			if n['name'] == 'csrf_token':                                             
				token = n['value']                                                     
				break
		test_creds = {"uname":randomUser, "pword":"Admin", "2fa":"1231231234", "csrf_token":token}
		r = s.post(addr, data=test_creds)
		out = s.get(server_address + "/logout")
		#if cookie successfully popped, values should not be equal
		self.assertNotEqual(s, requests.session())

if __name__ == "__main__":
	unittest.main()
	
