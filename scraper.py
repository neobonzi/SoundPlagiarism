import urllib3.contrib.pyopenssl
#import urllib
import soundcloud
import os 
import datetime

urllib3.contrib.pyopenssl.inject_into_urllib3()
CLIENT_ID = os.environ["SOUNDCLOUD_CID"]
DOWNLOAD_PATH = os.getcwd() + '/Downloads/' 
GENRES = ['piano', 'orchestra', 'opera', 'chorus', 'rock', 'country', 'pop', 'techno', 'hip-hop', 'reggae', 'jazz', 'latin']
#GENRES = ['rock']

def fetch_urls(track) :
   return track.download_url + '?client_id=' + CLIENT_ID

client = soundcloud.Client(client_id=CLIENT_ID)
page_size = 100

if not os.path.isdir(DOWNLOAD_PATH) :
   os.mkdir(DOWNLOAD_PATH)

for genre in GENRES :
   print "Scraping for genre: " + genre

   download_file = open(DOWNLOAD_PATH + genre, 'w')

   tracks = client.get('/tracks', genres=genre, order='created_at', limit=page_size, linked_partitioning=1)

   while 1 :
      print tracks.next_href
      for track in tracks.collection:
         if ( track.downloadable ) :
            download_url = fetch_urls(track)
            download_file.write(download_url + '\n')
            #filename = genre_path + 'temp.mp3'
            #urllib.urlretrieve(url=download_url, filename=filename)
      try:
         tracks = client.get(tracks.next_href, genres=genre, order='created_at', limit=page_size, linked_partitioning=1)
      except Exception, e:
         print 'Error: %s, Status Code: %d' % (e.message, e.response.status_code)
         download_file.close()
         break
