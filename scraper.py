# Scrape a user from HackerRank

pollTime = 5

def setPollTime(time):
	'''
	Sets polling time for checking webkit server
	'''
	pollTime = time

def start():
	import sys

	try:
		import dryscrape
	except:
		raise Exception('dryscrape not found')

	if 'linux' in sys.platform:
		# start xvfb in case no X is running. Make sure xvfb 
		# is installed, otherwise this won't work!
		dryscrape.start_xvfb()	

def getSession():

	try:
		import dryscrape
	except:
		raise Exception('dryscrape not found')
	
	# set up a web scraping session
	sess = dryscrape.Session()

	return sess	

def scrape(sess,username):
	'''
	Scrapes details related to given username

	'''

	from time import sleep

	try:
		from bs4 import BeautifulSoup
	except:
		raise Exception('BeautifulSoup not found')

	flag = False

	if type(username) == type([]):
		flag = True

	# we don't need images
	sess.set_attribute('auto_load_images', False)

	if(flag):
		dictionary = dict()

		for uname in username:
			sess.visit('https://www.hackerrank.com/' + uname+'/')

			lastSeen = None
			while lastSeen == None:
				sleep(pollTime)
				sessBody = sess.body()
				if(sessBody != None):
					renderer=BeautifulSoup(sessBody,"lxml")
					lastSeen = renderer.find('span','time-ago')
			dictionary[uname]=lastSeen.getText()

		return dictionary		
	else:
		sess.visit('https://www.hackerrank.com/' + username+'/')

		sessionBody = sess.body()

		renderer = BeautifulSoup(sessionBody,'lxml')

		lastSeen = None
		while lastSeen == None:
			sessBody = sess.body()
			if(sessBody != None):
				renderer=BeautifulSoup(sessBody,"lxml")
				lastSeen = renderer.find('span','time-ago')
			sleep(pollTime)
		#print 'username'+'\t'+'Last Successful submission'
		#print username+'\t'+lastSeen

		return lastSeen.getText()

def main():
	scrape('hasitpbhatt')

if __name__ == "__main__":
	main()