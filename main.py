#!/bin/python2
import time
import pprint
import sys
import urllib
import urllib2
import hashlib
import json
import webbrowser
import mechanize
import requests
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
def userAuth(auth_url, api_key, token):
    username = ''
    password = ''
    userAuthParams = {'api_key': api_key, 'token': token}
    url = auth_url + urllib.urlencode(userAuthParams)
    #print(url)
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
    #print(rootApi + urllib.urlencode(sessionParams))
    sessionReqJson = urllib2.urlopen(url)
    sessionJsonString = sessionReqJson.read()
    sessionJson = json.loads(sessionJsonString)
    return sessionJson['session']['key']

def auth():
    #f = open('auth', 'r')
    #f.close()
    #print (username + password)
    api_key = '242fedcf48db479f1584797a4e25d771'
    rootApi = 'http://ws.audioscrobbler.com/2.0/?'
    auth_url = 'http://www.last.fm/api/auth/?'
    mysecret =  'f8365bed081c880685acad58866b4939'
    api_sig = ''
    token = ''
    sessionKey = ''
     
    token = getToken(api_key, rootApi)
    userAuth(auth_url, api_key, token)
    api_sig = getApiSig(api_key, token, mysecret)
    sk = getSession(rootApi, api_key, api_sig, token)

    return {'api_key': api_key, 'api_sig': api_sig, 'sk': sk}

def main(argv):
    rootApi = 'http://ws.audioscrobbler.com/2.0/?'
    mysecret =  'f8365bed081c880685acad58866b4939'
    argList= [] 
    valueList= []
    authDict = auth()
    argCount = 1
    fout = open('cmusOup.txt', 'w')
    if len(argv) < 1:
        fout.write("Not recieving data from cmus")
    else:
        for args in argv: #can't enumerate for some reason
            if argCount > 1:
                if argCount % 2 == 0:
                    argList.append(args)
                else:
                    valueList.append(args)
            argCount += 1
        #for args in argList:
        #    print(args)
        #for args in valueList:
        #    print(args)
        fullCmusDict = dict(zip(argList, valueList))
        #for key, val, in fullCmusDict.items():
        #    fout.write(key+ ' ' + val + '\n')
        usefulCmusDict = dict({'artist': fullCmusDict['artist']})
        usefulCmusDict.update({'track': fullCmusDict['title']})
        usefulCmusDict.update({'album': fullCmusDict['album']}) 
        usefulCmusDict.update({'timestamp': str(int(time.time()))})
        #fout.write('END OF CMUS\n') 
        #for key, val, in usefulCmusDict.items():
        #    fout.write(key+ ' ' + val + '\n')
        api_sig_hash = 'album' + usefulCmusDict['album'] + \
                        'api_key' + authDict['api_key'] + \
                        'artist' + usefulCmusDict['artist'] + \
                        'method' + 'track.scrobble' + \
                        'sk' + authDict['sk'] + \
                        'timestamp' + usefulCmusDict['timestamp'] + \
                        'track' + usefulCmusDict['track'] + \
                        mysecret  
                        #'artist' + usefulCmusDict['artist'] + \
                        #'artist' + usefulCmusDict['artist'] + \ 
        
        #api_sig_hash= 'api_key' + authDict['api_key'] + \
        #'method' + 'track.updateNowPlaying' + \
        #'sk' + authDict['sk'] + \
        #mysecret  
        api_sig_hash = api_sig_hash.encode('utf-8')
        api_sig = hashlib.md5(api_sig_hash)
        api_sig = api_sig.hexdigest()
        authDict['api_sig'] = api_sig
        urlArgs = {'method': 'track.scrobble'}
        print(urlArgs['method'])
        urlArgs.update(usefulCmusDict)
        urlArgs.update(authDict)
        songUrl = urllib.urlencode(urlArgs)
     
        url = rootApi + songUrl 
        print(url)

        scrobbResponse = requests.post(url) 
        #print(scrobbResponse.read())
    #fout.close()

if __name__ == '__main__':
    sys.exit(main(sys.argv))
