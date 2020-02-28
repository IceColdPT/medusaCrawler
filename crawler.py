import requests
from bs4 import BeautifulSoup
import json
import re
import os.path
class Crawler:
    def __init__(self,page):
        
        self.currentUrl = page
        self.jsonFile = os.path.join( "data",self.currentUrl.split("://")[1].strip("/")+".json")
        
        self.currentPageContent = None

        self.__newslist = {}
        self.__newslist["news"] = []
     
        self.httpResponse = requests.get(self.currentUrl)
        self.bs = BeautifulSoup(self.httpResponse.text)

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
        
        
  


    def saveJson(self,data):
        with open(self.jsonFile,"w+") as f:
            print("saving json..")
            self.data = data
            json.dump(self.data,f)
            f.close()
    


    
    def getLinks(self):
    
        for a in self.bs.find_all("a" ,href=True):
            self.data[0]["links"].append(a["href"])
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
            if len(extracted) > 0:
                result.append(extracted)

        if len(result) > 0:
            self.data["email"].append(result)
            self.saveJson(self.data)
        else:
            print(self.currentUrl+" No email founds on this site.")


    def history_addCurrentURL(self):
        with open(self.HISTORYFILENAME,"a+") as f:
            f.write(self.currentUrl+"\n")
    
    def crawl(self,depth):
        active = True

        while active:
            #main loop!
            print("===CURRENT URL: ("+self.currentUrl+")=====")
            #modos operandi:
            #



#testiing
s = Crawler("https://www.sapo.pt/")



