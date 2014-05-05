#!/bin/python2
import sys
import urllib2
import hashlib
#API Key: 242fedcf48db479f1584797a4e25d771
#Secret: is f8365bed081c880685acad58866b4939

#track.scrobble
    #artist
    #track
    #timestamp(in unix format UTC)
    #album (optional)
    #track number (optional)
    #album artist (optional)
    #durration(optional)

    #api_key required
    #api_sig required

    #need a class that holds the options and determines what objects it has (ie different versions with different optional variables)

    #need something to send this through html post
        #possibly urllib2
    #need to clean up input and add error checking



    #fetchrequest token
    #request auth from user
    #fetch a web service session
    #make authenticated web service calls
    #sign my calls
def auth():
    api_key = '242fedcf48db479f1584797a4e25d771'
    rootApi = 'http://ws.audioscrobbler.com/2.0/'

    #api_sig = md5('api_key'+api_key+'method' + 'auth.getSession' +'token')
    url = rootApi + '?method=auth.gettoken&api_key=' + api_key + '&format=json'
    #print(url)
    tokenhHTTP = urllib2.urlopen(url)#gets auth from user
    token = tokenhHTTP.read()
    #urllib2.urlopen.close()
    print(token)
    #api_sig_hash = unicode('api_key' + api_key + 'method' + 'auth.getToken', "utf-8")
    #api_sig = hashlib.md5(api_sig_hash).hexdigest()
#class user(self):
#    username = ''
#    password = ''
#    api_key = '242fedcf48db479f1584797a4e25d771'



#class curPlaying(self):
    

def main(argv):
    '''if len(argv) < 2:
        sys.stderr.write("Not recieving data from cmus")
        return 1
    else:
        fout = open('cmusOup.txt', 'w')
        for args in argv:
           fout.write(args) 
           fout.write('\n')
        fout.close()'''

    auth()

if __name__ == '__main__':
    sys.exit(main(sys.argv))
