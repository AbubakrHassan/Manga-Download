#!/usr/bin/env python
import optparse
import urllib
from bs4 import BeautifulSoup
import os
def str_srch(string,B):
	if string in B:
		return True
	return False
def strings_search(string,sequence):
	l=string.split(" ")
	for i in l:
		if str_srch(i,sequence) :
			return True
	return False
def optionparser():
	parser=optparse.OptionParser("usage -M <manga name> -C <chapter Number>" )
	parser.add_option("-M",dest="manganame",type="string")
	parser.add_option("-C",dest="chapter",type="string")
	return parser
def Search(manga,chapter):
	html=BeautifulSoup(urllib.urlopen("http://www.mangatown.com/directory/"))
	for i in html.find_all("li"):
		try:
			if strings_search(manga,i.a["href"]):
				url=i.a["href"]
				break
		except:
			pass
	if strings_search(manga,i.a["href"]):
		html=BeautifulSoup(urllib.urlopen(url))
		for i in html.find_all("li"):
			try:
				if strings_search("c"+chapter,i.a["href"]):
					url=i.a["href"]
					break

			except:
				pass
		if strings_search(chapter,i.a["href"]):
			return url
	return False
def download(url,name,chapter):
  try:
    os.mkdir("manga")
  except:
    pass
	if url==False:
		print "[-] Error "
		return 0
	count= len(os.listdir("./manga"))
	os.mkdir("./manga/"+name+chapter)
	ht=".html"
	page_list=[]
	for i in range(1,23):
		page_list.append(str(i)+ht)
	for k in page_list:
		
		URL=url+"/"+k
		html=BeautifulSoup(urllib.urlopen(URL))
		for i in html.find_all("script"):
			for j in i.text.split("\n"):
				if "img.src" in j:
					print "[*] Downloading image "+k.split(".")[0]
					Download=j.split('"')[1][:-1]
					urllib.urlretrieve(Download,"./manga/"+name+chapter+"/"+k.split(".")[0])
					print "[+] Finish"
	for i in os.listdir("./manga/"+name+chapter):
		os.chmod("./manga/"+name+chapter+"/"+i,0777)
		
if __name__=="__main__":
	parser=optionparser()
	options,args=parser.parse_args()
	n=options.chapter
	while(len(n)<3):
		n="0"+n
	download(Search(options.manganame,n),options.manganame,n)
