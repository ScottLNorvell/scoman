import re
import random
import string
import hashlib
import hmac

###############################################
###These are my value checkers for Cookies
###############################################

SECRET = 'imsosecret'
def hash_str(s):
    return hmac.new(SECRET,s).hexdigest()

def make_secure_val(s):
    return "%s|%s" % (s, hash_str(s)) 

def check_secure_val(h):
    ###Your code here
    val = h.split('|')[0]
    if h == make_secure_val(val):
        return val
    
###############################################
###These are my hashers for Passwords
###############################################

def make_salt(size=5,chars=string.ascii_letters):
    #makes a random 5-letter string
    return ''.join(random.choice(chars) for x in xrange(size))



def make_pw_hash(name, pw, salt=None):
    ##makes a sweet hash of the user's password
    if not salt:
        salt = make_salt()
    hashed = hashlib.sha256(name+pw+salt).hexdigest()
    return '{},{}'.format(hashed,salt)

def valid_pw(name, pw, h):
    ##validates password
    salt = h.split(',')[1]
    
    if make_pw_hash(name,pw,salt) == h:
        return True
    else:
        return False

###############################################
###These are my validators for Signup Data!
###############################################

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASS_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")

def valid(username, rec):
    m = rec.match(username)
    if m:
        return m.group()
    else:
        return ''
  
