import requests
from bs4 import BeautifulSoup
import json
import re
import os.path
import random
class Crawler:
    def __init__(self,page):
        self.current_target_index = 0
        self.currentUrl = page
        self.jsonFile = os.path.join( "data",self.currentUrl.split("/")[2]+str(random.randint(10,1000))+".json")
        
        self.currentPageContent = None

        self.__newslist = {}
        self.__newslist["news"] = []
     
        self.httpResponse = requests.get(self.currentUrl)
        self.bs = BeautifulSoup(self.httpResponse.text)
        self.TARGETFILE = "targets"
        self.HISTORYFILENAME = "already_visited"
        #self.raw_json = self.httpResponse.json()
        try:
            print("opening json: ")
            with open(self.jsonFile,"r+") as f:
                print("reading json..")
                self.data = json.load(f)
                print(self.data)
                f.close()
        except:
            print("json not found, making from scratch!")
            self.data = [{
                "links" : [],
                "articles": [],
                "emails": [],
                "titles": [],
                "headers": [],
            }]
            with open(self.jsonFile,"w+") as f:
                print("saving json..")
                json.dump(self.data,f)
                f.close()
        
  


    def saveJson(self,data):
        with open(self.jsonFile,"w+") as f:
            print("saving json..")
            self.data = data
            json.dump(self.data,f)
            f.close()
    


    
    def getLinks(self):
    
        for a in self.bs.find_all("a" ,href=True):
           with open("targets","a+") as f:
               link = a["href"]
               if link.startswith("htt"):
                   self.data[0]["links"].append(link)
                   f.write(link+"\n")
        self.saveJson(self.data)

      
        
    
    def getArticles(self):
        for article in self.bs.find_all("article"):
            self.data[0]["articles"].append(article.text)
        self.saveJson(self.data)


    def __extractEmail(self,st):
        regex = r'([\w0-9._-]+@[\w0-9._-]+\.[\w0-9_-]+)'
        return re.findall(regex, st, re.M|re.I)
    
    def getEmailAddresses(self):
        result = []
        for line in self.bs.find_all():
            
            extracted = self.__extractEmail(line.text)
            print(extracted)
            if len(extracted) > 0:
                result.append(extracted)

        if len(result) > 0:
            self.data[0]["emails"].append(result)
            self.saveJson(self.data)
        else:
            print(self.currentUrl+" No email founds on this site.")


    def history_addCurrentURL(self):
        with open(self.HISTORYFILENAME,"a+") as f:
            f.write(self.currentUrl+"\n")

    def history_getHistory(self,url):
        f = open(self.HISTORYFILENAME,"r+")
        for line in f.readlines():
            if line == url:
                return True
            else:
                return False

    def chose_target(self):
        with open(self.TARGETFILE,"r+") as f:
            lines = f.readlines()
            self.currentUrl = lines[self.current_target_index]
            self.httpResponse = requests.get(self.currentUrl)
            self.bs = BeautifulSoup(self.httpResponse.text)
            self.jsonFile = os.path.join( "data",self.currentUrl.split("/")[2]+str(random.randint(10,1000))+".json")
            f.close()

    def crawl(self,depth):
        active = True

        while active:
            #main loop!
            self.current_target_index += 1
            print("===CURRENT URL: ("+self.currentUrl+")=====")
            #modos operandi:
            #
   
            print("Getting articles...")
            self.getArticles()
            print("getting emails...")
            self.getEmailAddresses()
            print("Getting links")
            self.getLinks()
            print("done. switching website")
            s
            self.chose_target()


#testiing
s = Crawler("https://www.estbarreiro.ips.pt/")
s.crawl(3)



