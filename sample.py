# sample program for test

import scraper

def main():
	
	inputFile = open('input.txt')
	
	# can be changed to "input.txt" for example
	#inputFile = open('sample_input.private')

	scraper.start()

	sess = scraper.getSession()

	for i in inputFile:
		# get username
		username = i.strip()
		
		# Scrap only score, percentile
		#print str(scraper.scrape(sess,username)).strip()

		# Scrap completely
		print str(scraper.completeScrape(sess,username,debug=False)).strip()

	inputFile.close()

if __name__ == "__main__":
	main()