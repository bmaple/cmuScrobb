#!/bin/python2
import sys
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
def auth():
    api_key = '242fedcf48db479f1584797a4e25d771'
    rootApi = 'http://ws.audioscrobbler.com/2.0/'
    #api_sig = md5('api_key'+api_key+'method' + 'auth.getSession' +'token')
    
    #get token begin
    url = rootApi + '?method=auth.gettoken&api_key=' + api_key + '&format=json'
    tokenReqJson = urllib2.urlopen(url)#gets auth from user
    tokenJsonString = tokenReqJson.read()
    tokenJson = json.loads(tokenJsonString)
    token = tokenJson['token']
    #get token end
    
    #req user auth begin
    auth_url = 'http://www.last.fm/api/auth/?' + 'api_key=' + api_key + '&token=' + token
    print(auth_url)
    br = mechanize.Browser(factory=mechanize.RobustFactory())
    br.set_handle_robots(False)
    br.open(auth_url)
    br.select_form(nr=1)
    br['username'] = ''
    br['password'] = ''
    res = br.submit()
    content = res.read()
    with open('mech_results.html', 'w') as f:
        f.write(content)
    webbrowser.open('mech_results.html')

    #request = mechanize.Request(auth_url)
    #response = mechanize.urlopen(request)
    #forms = mechanize.ParseResponse(response, backwards_compat=False)
    #for f in forms:
    #    print(f)
    #req user auth end
    #fetch web service session begin
    api_sig_hash = unicode('api_key' + api_key + 'method' + 'auth.getToken', "utf-8")
    api_sig = hashlib.md5(api_sig_hash).hexdigest()
    url = rootApi + '?method=auth.getSession&api_key=' + api_key +  '&api_sig=' + api_sig + '&token=' + token

    #<input type="submit" class="button confirmButton" value="Yes, allow access">
    f = open('auth', 'r')
    username = f.readline()
    password = f.readline()
    #print(url) 
    
    
    #login stuff
    #<input type="text" id="username" name="username" class="LoginBox" style="width:98%;" value="" />
    #<input type="password" id="password" name="password" value="" class="LoginBox" style="width:98%;" />


    #<input type="submit" value="Come on in" name="login"/>
    
    #fetch web service session end
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
