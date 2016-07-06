# Scrape a user from HackerRank

# gap to load the HackerRank page completely
pollTime = 2

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

def completeScrape(sess,username,debug=False):
	'''
	Scrapes everything, all the challenges user has completed
	'''
	user = scrape(sess,username)
	q = sess.at_xpath('//*[@data-analytics="ProfileChallengesLoadMore"]')
	last = sess.body()
	cnt = 0
	import time
	while(q != None):
		q.click()
		if(debug):
			print "LoadMore clicked"
			sess.render(str(cnt)+'.jpg')
			cnt += 1
		time.sleep(pollTime)
		sessBody = sess.body()
		if(last == sessBody):
			break
		last = sessBody
		q = sess.at_xpath('//*[@data-analytics="ProfileChallengesLoadMore"]')
	
	findCompletedChallenges(sessBody)
	from bs4 import BeautifulSoup
	renderer = BeautifulSoup(sessBody)
	user.setLastSeen(renderer.find('span','time-ago').getText())
	return user

def findCompletedChallenges(markup):
	try:
		from bs4 import BeautifulSoup
	except:
		raise Exception('BeautifulSoup not found')

	renderer = BeautifulSoup(markup)
	renderer = renderer.find(id ='profile-tab-challenges')
	renderer = renderer.find_all('a','prob_link')
	for i in renderer:
		print str(i.getText().encode('ascii','ignore'))+'\t'+'https://www.hackerrank.com' + str(i['href'])
	#print renderer

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

	# If list of users, call it one by one
	if type(username) == type([]):
		flag = True

	# we don't need images
	sess.set_attribute('auto_load_images', False)

	if(flag):
		dictionary = dict()

		for uname in username:
			dictionary[uname]=scrape(sess,uname)

		return dictionary		
	else:
		import user
		myUser = user.User(username)
		sess.visit('https://www.hackerrank.com/' + username+'/')

		sessionBody = sess.body()

		renderer = BeautifulSoup(sessionBody,'lxml')

		lastSeen = None
		while lastSeen == None:
			sleep(pollTime)
			sessBody = sess.body()
			if(sessBody != None):
				renderer=BeautifulSoup(sessBody,"lxml")
				lastSeen = renderer.find('span','time-ago')

		#print 'username'+'\t'+'Last Successful submission'
		#print username+'\t'+lastSeen
		myUser.setLastSeen(lastSeen.getText())
		
		z = renderer.find(id='hacker-contest-score')
		if(z != None):
			myUser.setContestScore(z.getText())
		
		z = renderer.find(id='hacker-archive-score')
		if(z != None):
			myUser.setArchiveScore(z.getText())

		z = renderer.find(id='hacker-percentile')
		if(z != None):
			myUser.setPercentile(z.getText())

		z = renderer.find(id='hacker-competitions')
		if(z != None):
			myUser.setCompetitions(z.getText())

		# If you want to see completed questions, too
		#findCompletedChallenges(sessBody)

		return myUser

def main():
	scrape('hasitpbhatt')

if __name__ == "__main__":
	main()