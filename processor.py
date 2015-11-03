#!/usr/bin/python
import os 
import glob
import datetime
import logging
import fpectl
import random
from granulizer import storeGrains
from granulizer import chopSound
from analyzer import analyzeAllMFCC
from analyzer import analyzeAllPitch
from analyzer import analyzeAllEnergy
from analyzer import analyzeAllSpectralShape
from analyzer import analyzeAllZeroCrossingRate
import subprocess
import synthesizer
import urllib

downloadFiles = ["chorus.txt", "hip-hop.txt", "latin.txt", "orchestra.txt", "pop.txt", "rock.txt", "country.txt", "jazz.txt", "opera.txt", "piano.txt", "reggae.txt", "techno.txt"]
downloadsPath = "Downloads/"

fpectl.turnon_sigfpe()
logging.basicConfig(filename='processingLog.log',level=logging.DEBUG)

for downloadFile in downloadFiles: 
    filename = "tmpDownload.mp3"
    
    with open(downloadsPath + downloadFile) as f: 
        for toDownload in f.xreadlines(): 
            logging.debug("downloading " + toDownload)
            urllib.urlretrieve(url=toDownload, filename=filename)
            songFile = open(filename)
            print("done downloading file")
            subprocess.call(["ffmpeg -i tmpDownload.mp3 -ac 1 tmpDownloadMono.mp3"], close_fds=True, shell=True)
            grainMongoObjects = chopSound("tmpDownloadMono.mp3", 20, "grains", downloadFile[:-4]) 
            storeGrains(grainMongoObjects)
            analyzeAllMFCC()
            logging.debug("done with mfcc for " + toDownload)
            analyzeAllPitch()
            logging.debug("done with pitch for " + toDownload)
            analyzeAllEnergy()
            logging.debug("done with energy for " + toDownload)
            #analyzeAllSpectralShape()
            analyzeAllZeroCrossingRate() 
            logging.debug("done with zcr for " + toDownload)
            subprocess.call(["rm tmpDownload.mp3"], shell=True)   
            subprocess.call(["rm tmpDownloadMono.mp3"], shell=True)   
            files = glob.glob('/home/ubuntu/SoundPlagiarism/grains/*')
            for f in files:
                os.remove(f)
            songFile.close()
            logging.debug("done removing tmp files for  " + toDownload)
            logging.debug("Done converting " + toDownload)
            print("done converting file")
            
    print("Done processing " + downloadFile)
