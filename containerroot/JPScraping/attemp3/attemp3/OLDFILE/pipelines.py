from pathlib import Path
import os
import scrapy
from scrapy.pipelines.files import FilesPipeline
import re
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

class Attemp3Pipeline(FilesPipeline):

    logFile = "myLogPipeline.txt"
    pdLogFile = ""
    saveDir = ""

    abortContentTypeRule = [b"text/html", b"application/pdf"]

    mapperLongString = {}

    def log(self, toLog="", aCapo=0):
        print(toLog)
        self.pdLogFile.write(("\n" * aCapo) + toLog+"\n")

    def open_spider(self, spider):
        super().open_spider(spider)
        spider
        self.pdLogFile = open(self.logFile, "w")
        self.target_directory = spider.settings.get('FILES_STORE')

    def close_spider(self, spider):
        #super().close_spider(spider)
        self.pdLogFile.close()  


    def process_item(self, item, spider):
        self.log("")
        self.log(" ### INIZIO NUOVO FILE ### ")
        self.log("Analizzando la risorsa")
        for key in item:
            self.log("key: %s , value: %s" % (key, item[key]))

        self.log("")
        # self.log(" --- Analizzando i campi PRE-DOWNLOAD --- ")
        # for key1 in item:
        #     self.log(" -> Analizzando " + key1)
        #     for key in key1:
        #         self.log(" ---> key: %s , value: %s" % (str(key), str(key1[str(key)])))

        resp = item['response']
        tabR = item["tableRow"]
        doms = item["domains"]

        self.log(aCapo=2)
        self.log(" --- Analizzando l'header di risposta --- ")
        for x in resp.headers:
            self.log("-> " + str(x) + " _ " + str(resp.headers.get(x)))




        #Retrieve the Last-Modified header
        self.log()
        self.log(" --- prendendo il timestampUpload --- ")
        last_modified = resp.headers.get('Last-Modified')
        self.log(" " + str(last_modified))
        if last_modified:
            self.log("Eccolo! -> " + str(last_modified.decode()))
            tabR["timestampUpload"] = last_modified.decode()



        #download page
        urlCleaned = resp.url.split("//")[1]
        contentType = str(resp.headers.get('Content-Type'))
        desideredContentType = [None, "html", "pdf"]

        if contentType is None:
            contentType = "html"

        fPath = self.myFilePath(urlCleaned, tabR["IDregion"], doms)
        fName = self.myFileName(urlCleaned, contentType)
        fPN = self.getFullNamePath(urlCleaned, contentType,tabR["IDregion"], doms)

        self.log("######### " + fPN)
        if not os.path.exists(fPath):
            os.makedirs(fPath)
        
        # if any(desired_type in contentType for desired_type in desideredContentType):
            # if re
        Path(fPN).write_bytes(resp.body)
        tabR["fileDownloadedName"] = fName
        tabR["fileDownloadedDir"] = fPath
        
        
        # else:
        #     # do something else
        #     tabR["aborted"] = True
        #     tabR["abortReason"] = "Content tipe is not somethig like" + str(desideredContentType[1:])

        item["tableRow"] = tabR
        self.log("Analizzando i risultati")
        for key in item:
            self.log("key: %s , value: %s" % (key, item[key]))

        self.log(aCapo=7)
        return item


    def myFileName(self, url, contentType):
        fileName = url.split("/")[-1]
        # Replace invalid characters with "_"
        invalid_chars = r'[<>:"/\\|?*\x00-\x1F\x7F]'
        fileName = re.sub(invalid_chars, "_", fileName)

        if fileName == "":
            fileName = "index.html" # DA CONTROLLARE !!! 
        
        if "html" in contentType and not "html" in fileName:
            fileName += "." + "html"
        
        tollerance = 200
        if len(fileName) > tollerance:
            fileName = fileName[:tollerance] + "." + fileName.split(".")[-1]

        return fileName 
    
    def myFilePath(self, url, idR, toPreserve=[]):
        tmp = self.target_directory + idR
        upperbound = 10
        for x in url.split("/"):
            # if not x in toPreserve and len(x) > upperbound:
            #     if x in self.mapperLongString.keys():
            #         x = self.mapperLongString[x]
            #     else:
            #         hv = hash(x)
            #         toMod = -1 * hv if hv < 0 else hv
            #         mod = (str(toMod)*5)[:upperbound]
            #         self.log("WOW, ha oltrepassato il limite!" + x + " -> " + tmp)
            #         self.mapperLongString[x] = mod
            #         x = mod
                    
            tmp = os.path.join(tmp,x)
        
        self.log("%%%%%%%%%%%%%%%%%%%%%%%")
        self.log(str(url) + "  " + tmp)
        self.log("%%%%%%%%%%%%%%%%%%%%%%%")

        return tmp
    
    def getFullNamePath(self, url, contentType, idR, toPreserve=[]):
        return os.path.join(self.myFilePath(url,idR,toPreserve=toPreserve), self.myFileName(url, contentType))

    
    
    
    # def file_path(self, request, response=None, info=None, *, item=None):
    #     # Get the original filename
    #     #filename = super().file_path(request, response=response, info=info, item=item)
        
    #     filename = response.url.split("/")[-1] + '.html'

    #     self.log("file_path")

    #     return os.path.join(self.target_directory, filename)

    # def item_completed(self, results, item, info):
    #     # Get the file paths from the results
    #     file_paths = [x['path'] for ok, x in results if ok]
    #     self.log("item_completed") 
    #     # Update the item with the file paths
    #     item['file_paths'] = file_paths

    #     self.log("CCCCCCCCCCCCCCCCCCCCCCCCCCCCCC")
    #     self.log(item)

    #     # Perform any other necessary manipulations

    #     return item
