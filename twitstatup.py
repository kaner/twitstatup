#!/usr/bin/python
#
# Copyright (c) 2011, Christian Fromme <kaner@strace.org>
# All rights reserved.
#
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
# 3. All advertising materials mentioning features or use of this software
#    must display the following acknowledgement:
#    This product includes software developed by the <organization>.
# 4. Neither the name of the <organization> nor the
#    names of its contributors may be used to endorse or promote products
#    derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY <COPYRIGHT HOLDER> ''AS IS'' AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# 
# Purpose: Simply post a simple message to a Twitter account.
# 
# Note that you need to set up your Twitter account to accept 3rd party apps
# to post to it in your settings. There you will receive a consumer key and a
# consumer secret from Twitter. Use those to fill in CONSUMER_KEY and 
# CONSUMER_SECRET below.
#
# The next thing you need is your token key and token secret. The easiest way
# to get those is to follow the 'three legged oauth' here:
#
#           https://github.com/simplegeo/python-oauth2
#
# Fill them into TOKEN_KEY and TOKEN_SECRET below. Now you're all set to post
# on Twitter via this script. Have fun!
#
# Bugreports to: Christian Fromme <kaner@strace.org>

import sys
import json
import urllib
import oauth2 as oauth

# These come from Twitter by registering for 3r party API support.
CONSUMER_KEY="FILLME"
CONSUMER_SECRET="FILLME"

# These come from Twitter after successfull 3-legged authentication.
# See https://github.com/simplegeo/python-oauth2 for how to retrieve them.
TOKEN_KEY="FILLMEAFTERYOUGOTME"
TOKEN_SECRET="FILLMEAFTERYOUGOTME"

# The Twitter status update request URL
REQUEST_URL="https://api.twitter.com/1/statuses/update.json"

def do_tweet(message):
    '''Post a message to Twitter.
    '''
    
    # Create oauth consumer, token, client
    consumer = oauth.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
    token = oauth.Token(TOKEN_KEY, TOKEN_SECRET)
    client = oauth.Client(consumer, token)

    data = {'status': message}

    # Ok, fire
    response, content = client.request(REQUEST_URL, "POST", urllib.urlencode(data))
    s = response['status']
    if s != "200":
        print >>sys.stderr, "Couldn't post to Twitter. Response was: %s" % s
        return 1
    else:
        jsonblob = json.loads(content)
        username = jsonblob['user']['screen_name']
        text = jsonblob['text']
        print "Posted successfully to http://twitter.com/%s:" % username
        print "'%s'" % text
        return 0

def main():
    if len(sys.argv) < 2:
        print >>sys.stderr, "Usage: %s MESSAGE" % sys.argv[0]
        sys.exit(1)

    sys.exit(do_tweet(sys.argv[1]))

if __name__ == '__main__':
    main()
