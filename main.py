#!/bin/python2
import sys
import urllib
import urllib2
import hashlib
import json
import webbrowser
import mechanize
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
#fix url encodes for url
def getToken(api_key, rootApi): # needs api key and rootapi url 
    inJson = '&format=json'
    tokenParams = {'method': 'auth.gettoken', 'api_key': api_key}
    url = rootApi + urllib.urlencode(tokenParams) + inJson
    tokenReqJson = urllib2.urlopen(url)#gets auth from user
    tokenJsonString = tokenReqJson.read()
    tokenJson = json.loads(tokenJsonString)
    return tokenJson['token']
def userAuth(auth_url):
    username = ''
    password = ''
    userAuthParams = {'api_key': api_key, 'token': token}
    url = auth_url + urllib.urlencode(userAuthParams)
    br = mechanize.Browser(factory=mechanize.RobustFactory())
    br.set_handle_robots(False)
    br.open(url)
    br.select_form(nr=1)
    br['username'] = username
    br['password'] = password
    res = br.submit()
    br.select_form(nr=2) 
    res = br.submit()
def getApiSig(api_key, token, mysecret):
    api_sig_hash = 'api_key' + api_key + 'method' + 'auth.getSession' + 'token'+ token + mysecret
    api_sig_hash = api_sig_hash.encode('utf-8')
    api_sig = hashlib.md5(api_sig_hash)
    return api_sig.hexdigest()
def getSession(rootApi, api_key, api_sig, token):
    inJson = '&format=json'
    sessionParams = {'method': 'auth.getSession', 'api_key': api_key, 'api_sig': api_sig, 'token': token}
    url = rootApi + urllib.urlencode(sessionParams) + inJson
    sessionReqJson = urllib2.urlopen(url)
    sessionJsonString = sessionReqJson.read()
    sessionJson = json.loads(sessionJsonString)
    return sessionJson['session']['key']

def auth():
    #f = open('auth', 'r')
    #f.close()
    #print (username + password)
    api_key = '242fedcf48db479f1584797a4e25d771'
    rootApi = 'http://ws.audioscrobbler.com/2.0/'
    auth_url = 'http://www.last.fm/api/auth/'
    mysecret =  'f8365bed081c880685acad58866b4939'
    api_sig = ''
    token = ''
    sessionKey = ''
     
    token = getToken(api_key, rootApi)
    userAuth(auth_url)
    api_sig = getApiSig(api_key, token, mysecret)
    sessionKey = getSession(rootApi, api_key, api_sig, token)

    return {'api_key': api_key, 'api_sig': api_sig, 'sessionKey': sessionKey}

def main(argv):
#    auth_List = []
    titleList = [] 
    infoList = []
    argCount = 1
    fout = open('cmusOup.txt', 'w')
    if len(argv) < 2:
        fout.write("Not recieving data from cmus")
    else:
        for args in argv: #can't enumerate for some reason
            if argCount >= 2:
                if argCount % 2 == 0: 
                    titleList.append(args)
                else:
                    infoList.append(args)
            argCount += 1
        albumDict = dict(zip(titleList, infoList))
        songUrl = urllib.urlencode(albumDict)
        fout.write(songUrl)
        #for things in fullList:
        #    fout.write(things[0])
        #    fout.write(' ')
        #    fout.write(things[1])
        #    fout.write('\n')
        '''for word,definition in albumDict.items():
            fout.write(word)
            fout.write(' ')
            fout.write(definition)
            fout.write('\n')'''
        #for things in infoList:
        #    fout.write(things)
    fout.close()
    #auth_List = auth()

#track.scrobble requires api_key api_sig and sk in addition to the other stuff
#    auth()

if __name__ == '__main__':
    sys.exit(main(sys.argv))
