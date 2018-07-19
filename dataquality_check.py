'''
Created on Jul 9, 2018

@author: Jason Zhang
'''

import pandas as pd
import os
import re
import requests
import unicodedata
import fuzzy
from fuzzywuzzy import fuzz
import fuzzywuzzy
import phonenumbers
import dns.resolver
import socket 
import smtplib
from geopy.geocoders import Nominatim
import errorlog
from docutils.nodes import reference
import json

class dataqualityTest:
	def __init__(self):
		self.base_url = 'http://127.0.0.1:5000/'
		
		#import first name Dictionary
		path = os.path.join('QualityGap_Data','Firstname.csv')
		self.Firstname = pd.read_csv(path)
		#convert non-English character
		self.Firstname = list(map(lambda x:unicodedata.normalize('NFKD',x).encode('ascii','ignore').decode("utf-8"),self.Firstname.Firstname))

		#import last name Dictionary
		path = os.path.join('QualityGap_Data','Lastname.csv')
		self.Lastname = pd.read_csv(path)
		#convert non-English character
		self.Lastname = list(map(lambda x:unicodedata.normalize('NFKD',x).encode('ascii','ignore').decode("utf-8"),self.Lastname.Lastname))  

	def reference_check(self,ref, sourceType, resourceId):
		#reference format can be found at http://hl7.org/fhir/references.html
		try:
			base = 'http://test.fhir.org/r3/'
			if 'reference' in ref.keys():
				url = ref['reference']
				if url[0:3] == 'http':
					#absolute reference
					response = requests.get(url)
				else:
					#relevant reference
					response = requests.get(base+url)
				#This condition is only for testing, since we don't know the real return for API
				if response.status_code != 200:
					source = sourceType +': ' + resourceId
					raw = ref
					etype = 'reference'
					description = 'No response from reference'
					error = errorlog.Error(source,raw,etype,description)
					return error
				else:
					response = response.content.decode('utf-8')
				#This condition is only for testing, since we don't know the real return for API
				if re.search('not exist',response, re.IGNORECASE):
					source = sourceType +':' + resourceId
					raw = ref
					etype = 'reference'
					description = 'Reference Object do not exist'
					error = errorlog.Error(source,raw,etype,description)
					return error
				# Display validation
				if 'display' in list(ref.keys()):
					value = ref['display']
					value = value.replace(',','')
					for item in value.split():
						if not re.search(item, response, re.IGNORECASE):
							source = sourceType +': ' + resourceId
							raw = ref
							etype = 'reference'
							description = 'Reference display might not correct'
							error = errorlog.Error(source, raw, etype,description)
							return error
			return None
		except:
			#Unknown Error
			source = sourceType +': ' + resourceId
			raw = ref
			etype = 'reference'
			description = 'Unknown error'
			error = errorlog.Error(source, raw, etype,description)
			return error



	def codeConcept_check(self,codeConcept,sourceType, resourceId):
		try:
			if 'coding' in codeConcept.keys():
				codes = codeConcept['coding']
				for code in codes:
					if 'system' in code.keys():
						# Case 1: SNOMED CT code concept
						if code['system'] == 'http://snomed.info/sct':
							c = code['code']
							response = requests.get(self.base_url+'codeConcept/SNOMED/'+c)
							if response.text == '[]':
								source = sourceType +':' + resourceId
								raw = codeConcept
								etype = 'codeConcept'
								description = 'Check SNOMED code'
								error = errorlog.Error(source, raw, etype,description)
								return error
	
						# Case 2: LOINC code concept
						elif code['system'] == 'http://loinc.org':
							c = code['code']
							response = requests.get(self.base_url+'codeConcept/LOINC/'+c)
							if response.text == '[]':
								source = sourceType +':' + resourceId
								raw = codeConcept
								etype = 'codeConcept'
								description = 'Check LOINC code'
								error = errorlog.Error(source, raw, etype,description)
								return error
							else:
								loinc = pd.read_json(response.text)
								terms = list(loinc['SHORTNAME']) + list(loinc['LONG_COMMON_NAME'])
								if 'display' in code.keys():
								#might have to find a better way to test display
									for term in terms:
										if code['display'].lower() in term.lower():
											return None
									source = sourceType +':' + resourceId
									raw = codeConcept
									etype = 'codeConcept'
									description = 'Check LOINC display'
									error = errorlog.Error(source, raw, etype,description)
									return error
						# Case 3: UCUM
						elif code['system'] == 'http://unitsofmeasure.org':
							c = code['code']
							response = requests.get(self.base_url+'codeConcept/UCUM/'+c)
							if response.text == '[]':
								source = sourceType +':' + resourceId
								raw = codeConcept
								etype = 'codeConcept'
								description = 'Check UCUM code'
								error = errorlog.Error(source, raw, etype,description)
								return error
						# Case 4: NDFRT
						elif code['system'] == 'http://hl7.org/fhir/ndfrt':
							c = code['code']
							response = requests.get(self.base_url+'codeConcept/NDFRT/'+c)
							if response.text == '[]':
								source = sourceType +':' + resourceId
								raw = codeConcept
								etype = 'codeConcept'
								description = 'Check NDFRT code'
								error = errorlog.Error(source, raw, etype,description)
								return error
						# Case 5: UNII
						elif code['system'] == 'http://fdasis.nlm.nih.gov':
							c = code['code']
							response = requests.get(self.base_url+'codeConcept/UNII/'+c)
							if response.text == '[]':
								source = sourceType +':' + resourceId
								raw = codeConcept
								etype = 'codeConcept'
								description = 'Check UNII code'
								error = errorlog.Error(source, raw, etype,description)
								return error
							else:
								unii = pd.read_json(response.text)
								terms = list(unii['PT']) 
								if 'display' in code.keys():
								#might have to find a better way to test display
									for term in terms:
										if code['display'].lower() in term.lower():
											return None
									source = sourceType +':' + resourceId
									raw = codeConcept
									etype = 'codeConcept'
									description = 'Check UNII display'
									error = errorlog.Error(source, raw, etype,description)
									return error
						# Case 6: NDC
						elif code['system'] == 'http://hl7.org/fhir/sid/ndc':
							c = code['code']
							response = requests.get(self.base_url+'codeConcept/NDC/'+c)
							if response.text == '[]':
								source = sourceType +':' + resourceId
								raw = codeConcept
								etype = 'codeConcept'
								description = 'Check NDC code'
								error = errorlog.Error(source, raw, etype,description)
								return error
							else:
								ndc = pd.read_json(response.text)
								terms = list(ndc['PACKAGEDESCRIPTION']) 
								if 'display' in code.keys():
								#might have to find a better way to test display
									for term in terms:
										if code['display'].lower() in term.lower():
											return None
									source = sourceType +':' + resourceId
									raw = codeConcept
									etype = 'codeConcept'
									description = 'Check NDC display'
									error = errorlog.Error(source, raw, etype,description)
									return error
						# Case 7: CVX
						elif code['system'] == 'http://hl7.org/fhir/sid/cvx':
							c = code['code']
							response = requests.get(self.base_url+'codeConcept/CVX/'+c)
							if response.text == '[]':
								source = sourceType +':' + resourceId
								raw = codeConcept
								etype = 'codeConcept'
								description = 'Check CVX code'
								error = errorlog.Error(source, raw, etype,description)
								return error
							else:
								ndc = pd.read_json(response.text)
								terms = list(ndc['CVX Short Description']) 
								if 'display' in code.keys():
								#might have to find a better way to test display
									for term in terms:
										if code['display'].lower() in term.lower():
											return None
									source = sourceType +':' + resourceId
									raw = codeConcept
									etype = 'codeConcept'
									description = 'Check CVX display'
									error = errorlog.Error(source, raw, etype,description)
									return error
						# Case 8: v2
						elif 'http://hl7.org/fhir/v2' in code['system']:
							c = code['code']
							system = code['system']
							s = system.split('/')[-1]
							cs = {}
							response = requests.get(self.base_url+'codeConcept/v2/'+s)
							if response.status_code == 200:
								obj = json.loads(response.text)
								concepts = obj['concept']
								for concept in concepts:
									cs[concept['code']] = concept['display']
								if c not in cs.keys():
									source = sourceType +':' + resourceId
									raw = codeConcept
									etype = 'codeConcept'
									description = 'Check v2/' + s + 'code'
									error = errorlog.Error(source, raw, etype,description)
									return error
								else:
									if 'display' in code.keys():
										if code['display'] != cs[c]:
											source = sourceType +':' + resourceId
											raw = codeConcept
											etype = 'codeConcept'
											description = 'Check v2/' + s + 'display'
											error = errorlog.Error(source, raw, etype,description)
											return error
							else:
								source = sourceType +':' + resourceId
								raw = codeConcept
								etype = 'codeConcept'
								description = 'Check v2/' + s + 'system'
								error = errorlog.Error(source, raw, etype,description)
								return error
						
						# Case 9: v3
						elif 'http://hl7.org/fhir/v2' in code['system']:
							c = code['code']
							system = code['system']
							s = system.split('/')[-1]
							cs = {}
							response = requests.get(self.base_url+'codeConcept/v3/'+s)
							if response.status_code == 200:
								obj = json.loads(response.text)
								concepts = obj['concept']
								for concept in concepts:
									cs[concept['code']] = concept['display']
								if c not in cs.keys():
									source = sourceType +':' + resourceId
									raw = codeConcept
									etype = 'codeConcept'
									description = 'Check v3/' + s + 'code'
									error = errorlog.Error(source, raw, etype,description)
									return error
								else:
									if 'display' in code.keys():
										if code['display'] != cs[c]:
											source = sourceType +':' + resourceId
											raw = codeConcept
											etype = 'codeConcept'
											description = 'Check v3/' + s + 'display'
											error = errorlog.Error(source, raw, etype,description)
											return error
							else:
								source = sourceType +':' + resourceId
								raw = codeConcept
								etype = 'codeConcept'
								description = 'Check v3/' + s +  'system'
								error = errorlog.Error(source, raw, etype,description)
								return error
								
						# Case 10: Internal
						else:
							if 'http://hl7.org/fhir/' in code['system']:
								c = code['code']
								system = code['system']
								s = system.split('/')[-1]
								cs = {}
								response = requests.get(self.base_url+'codeConcept/internal/'+s)
								if response.status_code == 200:
									obj = json.loads(response.text)
									concepts = obj['concept']
									for concept in concepts:
										cs[concept['code']] = concept['display']
									if c not in cs.keys():
										source = sourceType +':' + resourceId
										raw = codeConcept
										etype = 'codeConcept'
										description = 'Check internal/' + s + 'code'
										error = errorlog.Error(source, raw, etype,description)
										return error
									else:
										if 'display' in code.keys():
											if code['display'] != cs[c]:
												source = sourceType +':' + resourceId
												raw = codeConcept
												etype = 'codeConcept'
												description = 'Check internal/' + s + 'display'
												error = errorlog.Error(source, raw, etype,description)
												return error
								else:
									source = sourceType +':' + resourceId
									raw = codeConcept
									etype = 'codeConcept'
									description = 'Check internal/' + s + 'display'
									error = errorlog.Error(source, raw, etype,description)
									return error			
													
			return None
		except:
			#Unknown System Error
			source = sourceType +': ' + resourceId
			raw = codeConcept
			etype = 'codeConcept'
			description = 'Unknown error'
			error = errorlog.Error(source, raw, etype,description)
			return error


	def name_test(self,n,sourceType, resourceId):
		use = ['usual','official','temp','nickname','anonymous','old','maiden']
		#Human name use attribute testing
		if 'use' in n.keys():
			if n['use'] not in use:
				source = sourceType +':' + resourceId
				raw = n['use']
				etype = 'humanName'
				description = 'Check name use'
				error = errorlog.Error(source, raw, etype,description)
				return error
		#First Name Testing
		for fn in n['given']:
			if self.name_check(fn,self.Firstname) != None:
				source = sourceType +': ' + resourceId
				raw = n['given']
				etype = 'humanName'
				description = 'Check first name and spelling suggestions are '+ self.name_check(fn,self.Firstname)
				error = errorlog.Error(source, raw, etype,description)
				return error
		#Last Name Testing
		ln = n['family']
		if self.name_check(ln,self.Lastname) != None:
			source = sourceType +':' + resourceId
			raw = n['family']
			etype = 'humanName'
			description = 'Check last name and spelling suggestions are '+ self.name_check(ln,self.Firstname)
			error = errorlog.Error(source, raw, etype,description)
			return error


	def name_check(self,name,namelist):
		#Name is in the name dictionary
		if name in namelist:
			return None
		#Name is not in the dictionary, find the most similar using Double Metaphone and similar ratio
		else:
			dmeta = fuzzy.DMetaphone()
			result = []
			for n in namelist:
				if set(dmeta(n)) == set(dmeta(name)):
					result.append(n)
			score = {}
			for i in result:
				score[i] = fuzzywuzzy.fuzz.ratio(i,name)
			score = dict(sorted(score.items())[:3])
			suggestion = ' '.join(score.keys())
			return suggestion


	def telecom_test(self,t,sourceType, resourceId):
	#The contactPoint format can be found at http://hl7.org/fhir/datatypes.html#ContactPoint
		system = ['phone','fax','email','pager','url','sms','other']
		use = ['home','work','temp','old','mobile']
		#Format attribute test
		if 'system' in t.keys():
			if t['system'] not in system:
				source = sourceType +':' + resourceId
				raw = t['system']
				etype = 'contactPoint'
				description = 'Check contactPoint system'
				error = errorlog.Error(source, raw, etype,description)
				return error
		#Use attribute test
		if 'use' in t.keys():
			if t['use'] not in use:
				source = sourceType +':' + resourceId
				raw = t['use']
				etype = 'contactPoint'
				description = 'Check contactPoint use'
				error = errorlog.Error(source, raw, etype,description)
				return error
		#Phone number validation
		if t['system'] in ['phone','fax','sms']:
			#print(t['value'])
			if not self.phone_check(t['value']):
				source = sourceType +':' + resourceId
				raw = t['value']
				etype = 'contactPoint/phone'
				description = 'Check contactPoint phone'
				error = errorlog.Error(source, raw, etype,description)
				return error
		#Email address validation
		elif t['system'] == 'email':
			if not self.email_check(t['value']):
				source = sourceType +':' + resourceId
				raw = t['value']
				etype = 'contactPoint/email'
				description = 'Email address might not be correct'
				error = errorlog.Error(source, raw, etype,description)
				return error
		return None

	def phone_check(self,phone):
		#Try parse phone number with E164 format
		try:
			p = phonenumbers.parse(phone, None)
		except:
			try:
				#if not in E164 format, parse with US phone number format by default
				p = phonenumbers.parse(phone,'US')
			except:
				return False
		#Use successful parsing phone number to validate
		m = phonenumbers.is_valid_number(p)
		if m is None:
			return False
		else:
			return True


	def email_check(self,email):
		#Email format check
		m = re.match( "^.+@(\[?)[a-zA-Z0-9-.]+.([a-zA-Z]{2,3}|[0-9]{1,3})(]?)$",email)
		if m is None:
			#This is not a valid email address
			return False
		else:   
			domain_name = email.split('@')[1]
			#if satisfy the format, use smtp to ping email server
			#get the MX record for the domain
			records = dns.resolver.query(domain_name, 'MX')
			mxRecord = records[0].exchange
			mxRecord = str(mxRecord)

			#ping email server
			#check if the email address exists

			# Get local server hostname
			host = socket.gethostname()

			# SMTP lib setup (use debug level for full output)
			server = smtplib.SMTP()
			server.set_debuglevel(0)

			# SMTP Conversation
			server.connect(mxRecord)
			server.helo(host)
			server.mail('me@domain.com')
			code, message = server.rcpt(str(email))
			server.quit()

			# Assume 250 as Success
			if code == 250:
				#This is a valid email address
				return True
			else:
				#This might not be a valid email address, require validation email
				return False


	def address_test(self,a, sourceType, resourceId):
		# The address format can be found at  http://hl7.org/fhir/datatypes.html#Address
		use = ['home','work','temp','old']
		#check address use format
		if 'use' in a.keys():
			if a['use'] not in use:
				source = sourceType +': ' + resourceId
				raw = a['use']
				etype = 'address/use'
				description = 'Check address use'
				error = errorlog.Error(source, raw, etype,description)
				return error
		#check address existence
		address = ''
		if 'line' in a.keys():
			address = ' '.join(a['line']) 
			if not self.address_check(address):
				source = sourceType +': ' + resourceId
				raw = address
				etype = 'address'
				description = 'Check address street'
				error = errorlog.Error(source, raw, etype,description)
				return error
			if 'city' in a.keys():
				address = address + ' ' + a['city']
				if not self.address_check(address):
					source = sourceType +': ' + resourceId
					raw = address
					etype = 'address'
					description = 'Check address city'
					error = errorlog.Error(source, raw, etype,description)
					return error
				if 'state' in a.keys():
					address = address + ' ' + a['state']
					if not self.address_check(address):
						source = sourceType +': ' + resourceId
						raw = address
						etype = 'address'
						description = 'Check address state'
						error = errorlog.Error(source, raw, etype,description)
						return error
					if 'country' in a.keys():
						address = address + ' ' + a['country']
						if not self.address_check(address):
							source = sourceType +': ' + resourceId
							raw = address
							etype = 'address'
							description = 'Check address country'
							error = errorlog.Error(source, raw, etype,description)
							return error
						if 'postalCode' in a.keys():
							address = address + ' ' + a['postalCode']
							if not self.address_check(address):
								source = sourceType +': ' + resourceId
								raw = address
								etype = 'address'
								description = 'Check address post code'
								error = errorlog.Error(source, raw, etype,description)
								return error           

	def address_check(self,address):
		#Here is example of OpenStreetMap Nominatim, several other popular geocoding web service can be used
		geolocator = Nominatim()
		location = geolocator.geocode(address)
		if location is None:
				#can't find geo-coder for the given address
				return False
		else:
			if self.isSubSequence(address,str(location),len(address),len(str(location))):
				return True
			else:
				#address might not be correct, since geo-coder is significantly different from address
				return False

	def isSubSequence(self,string1, string2, m, n):
		#Check whether address is subsequence of geo-coder location i
		string1 = string1.lower()
		string2 = string2.lower()
		# Base Cases
		if m == 0:    return True
		if n == 0:    return False
		# If last characters of two strings are matching
		if string1[m-1] == string2[n-1]:
			return self.isSubSequence(string1, string2, m-1, n-1)
		# If last characters are not matching
		return self.isSubSequence(string1, string2, m, n-1)

	