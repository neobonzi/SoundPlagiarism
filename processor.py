import sys

downloadFiles = ["chorus.txt", "hip-hop.txt", "latin.txt", "orchestra.txt", "pop.txt", "rock.txt", "country.txt", "jazz.txt", "opera.txt", "piano.txt", "reggae.txt", "techno.txt"]
downloadsPath = "Downloads/"

for downloadFile in downloadFiles:
    f = open(downloadsPath + downloadFile)
    
    print(f.readline())
