from subprocess import check_output
import traceback
import re
from .tempmail import TempMail
import random, string
from time import sleep

def signup(username, password):
	PASSWORD = password
	USERNAME = username

	tm = TempMail(login=USERNAME)

	EMAIL = tm.get_email_address()
	try:
		signup = check_output("megareg --scripted --register --email " + EMAIL + " --password " + PASSWORD + " --name John", shell=True).decode()
	except Exception as e:
		traceback.print_exc()
		response = { 'success': False }
		return response

	sleep(5)
	try:
		mail_box = tm.get_mailbox()
		mail_body = mail_box[0]['mail_text']
	except Exception as e:
		try:
			sleep(15)
			mail_box = tm.get_mailbox()
			mail_body = tm.get_mailbox()[0]['mail_text']
		except:
			traceback.print_exc()
			response = { 'success': False }
			return response

	m = re.search('(http|ftp|https)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?', mail_body)

	CONFIRM_LINK = m.group(0)
	# print(CONFIRM_LINK)
	try:
		confirm = signup.replace("@LINK@", CONFIRM_LINK)
		#print(confirm)
		check_output(confirm, shell=True).decode()[:-2]
		response = {
			'success': True,
			'email': EMAIL,
			'password': PASSWORD
		}
		return response
	except Exception as e:
		traceback.print_exc()
		#print("There was some error.")
		response = { 'success': False }
		return response

if __name__=="__main__":
	PASSWORD = input("Password: ")
	USERNAME = input("Username: ")

	tm = TempMail(login=USERNAME)

	EMAIL = tm.get_email_address()
	try:
		signup = check_output("megareg --scripted --register --email " + EMAIL + " --password " + PASSWORD + " --name John", shell=True).decode()
		print(signup)
	except Exception as e:
		traceback.print_exc()
		response = { 'success': False }
		print(response)

	sleep(10)
	try:
		mail_box = tm.get_mailbox()
		print(str(mail_box).encode("utf-8"))
		mail_body = mail_box[0]['mail_text']
	except Exception as e:
		try:
			sleep(5)
			mail_box = tm.get_mailbox()
			print(str(mail_box).encode("utf-8"))
			mail_body = tm.get_mailbox()[0]['mail_text']
		except:
			traceback.print_exc()
			response = { 'success': False }
			print(response)

	m = re.search('(http|ftp|https)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?', mail_body)

	CONFIRM_LINK = m.group(0)
	# print(CONFIRM_LINK)
	try:
		confirm = signup.replace("@LINK@", CONFIRM_LINK)
		#print(confirm)
		check_output(confirm, shell=True).decode()[:-2]
		response = {
			'success': True,
			'email': EMAIL,
			'password': PASSWORD
		}
		print(response)
	except Exception as e:
		traceback.print_exc()
		#print("There was some error.")
		response = { 'success': False }
		print(response)