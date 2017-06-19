# -*- coding: utf-8 -*-
from os.path import isfile, join, splitext
import os
import re
import datetime
import time
from collections import OrderedDict

class Reader():
    
    def __init__(self, logFile, inputDir="./"):
        self.inputDir = inputDir
        self.logFile = logFile
        self.namePatter = re.compile("\w*(\d{2})-(\d{2})-(\d{2})_(\d{2})-(\d{2})-(\d{2})-(\d{2})")
        self.imageData = []
        self.logData = OrderedDict()
        self.logTimestamps = []
        self.logTemperatures = []
        self.parseLogfile()
        self.readFiles()
    
    def readFiles(self, inputDir=None, extensionFiler=[".jpg", ".png"]):
        if inputDir is None: inputDir = self.inputDir 
        
        self.imageData = []
        for f in os.listdir(self.inputDir):
            fileName = join(self.inputDir, f)
            if not isfile(fileName): continue
            _, fileExtension = splitext(f)
            if fileExtension in extensionFiler:
                timestamp = self.parseFileName(f)
                self.imageData.append({"file":fileName, "timestamp":timestamp, "temperature": self.getTemperature(timestamp)})
        
        self.imageData.sort(key=lambda x:x['timestamp'])
        return self.imageData
    
    def parseLogfile(self, logFile=None):
        if logFile is None: logFile = self.logFile
        
        if not os.path.isfile(logFile):
            raise Exception("Log file %s does not exist!" % logFile)
        
        with open(self.logFile, 'r') as f:
            for lineNumber, line in enumerate(f.read().split("\n")):
                if line == "": continue
                try:
                    _, timestamp, _, _, temperature = line.split("\t")
                except ValueError:
                    print("Error parsing line %i" % lineNumber)
                
                self.logData[float(timestamp)] = float(temperature)
        
        self.logTimestamps = self.logData.keys()
        self.logTemperatures = self.logData.values()
        return self.logData
     
    def getTemperature(self, timestamp):
        timestamp =  min(range(len(self.logTimestamps)), key=lambda i: abs(self.logTimestamps[i]-timestamp))
        return self.logTemperatures[timestamp]
       
    def parseFileName(self, fileName):
        parsed = re.match(self.namePatter, fileName)
        dateTime = "%s/%s/%s %s:%s:%s" % (parsed.group(3), parsed.group(2), parsed.group(1), parsed.group(4), parsed.group(5), parsed.group(6))
        timestamp = time.mktime(datetime.datetime.strptime(dateTime, "%d/%m/%y %H:%M:%S").timetuple())
        
        return timestamp
    