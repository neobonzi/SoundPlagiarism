#!/usr/bin/env python
import os 
import glob
import datetime
import logging
import sys
import fpectl
import random
from pympler import summary
from pympler import muppy
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

appPath = "/home/ubuntu/SoundPlagiarism/"
downloadFiles = ["chorus.txt", "hip-hop.txt", "latin.txt", "orchestra.txt", "pop.txt", "rock.txt", "country.txt", "jazz.txt", "opera.txt", "piano.txt", "reggae.txt", "techno.txt"]
downloadsPath = appPath + "Downloads/"

fpectl.turnon_sigfpe()
logging.basicConfig(filename='processingLog.log',level=logging.DEBUG)

downloadFile = ""

for i in downloadFiles:
    num_lines = sum(1 for line in open(downloadsPath + i))
    if num_lines > 0:
        downloadFile = i
        break
    else: 
        if i == "techno.txt":
            print("Done processing all genres") 
            sys.exit()
filename = appPath + downloadFile[:-4] + "tmpDownload.mp3"
monoFilename = appPath + downloadFile[:-4] + "tmpDownloadMono.mp3"
grainsFolder = appPath + 'grains'

if os.path.exists(filename):
    print("Process in progress")
    sys.exit()

with open(downloadsPath + downloadFile) as f: 
    lines = f.readlines()
    if (len(lines) == 0):
        sys.exit()
    toDownload = lines[0]
    logging.debug("downloading " + toDownload)
    urllib.urlretrieve(url=toDownload, filename=filename)
    songFile = open(filename)
    print("done downloading file")
    subprocess.call(["ffmpeg -i " + filename +" -ac 1 " + monoFilename], close_fds=True, shell=True)
    grainMongoObjects = chopSound(monoFilename, 20, grainsFolder, downloadFile[:-4]) 
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
    subprocess.call(["rm " + filename], shell=True)   
    subprocess.call(["rm " + monoFilename], shell=True)   
    files = glob.glob(grainsFolder + '/*')
    for f in files:
        os.remove(f)
    songFile.close()
    logging.debug("done removing tmp files for  " + toDownload)
    logging.debug("Done converting " + toDownload)
    print("done converting file") 
    open(downloadsPath + downloadFile, 'w').writelines(lines[1:])
    print("Done processing " + downloadFile)
