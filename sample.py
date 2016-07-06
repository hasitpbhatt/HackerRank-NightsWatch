# sample program for test

import scraper

def main():
	inputFile = open('input.txt')

	scraper.start()

	sess = scraper.getSession()

	usernameList = []
	for i in inputFile:
		# get username
		username = i.strip()
		print username
		usernameList.append(username)
		#print username+'\t'+scraper.scrape(sess,username)

	dictionary = scraper.scrape(sess,usernameList)
	for i in dictionary.keys():
		print i+'\t'+dictionary[i]
	inputFile.close()

if __name__ == "__main__":
	main()