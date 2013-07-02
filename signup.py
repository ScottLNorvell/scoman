
from base import BaseHandler

from signup_shit import *
from google.appengine.ext import db



###############################################
### A Class for UserInfo Database
###############################################

class UserInfo(db.Model):
    username = db.StringProperty(required = True)
    joined = db.DateTimeProperty(auto_now_add = True)
    pw_hash = db.StringProperty(required = True)
    email = db.StringProperty()
    
    @classmethod
    def by_id(cls, uid):
        return cls.get_by_id(uid)
    
    @classmethod
    def by_name(cls, name):
        u = db.GqlQuery("SELECT * FROM UserInfo WHERE username=:1", name).get()
        return u
    
    @classmethod
    def register(cls, name, pw, email = None):
        pw_hash = make_pw_hash(name,pw)
        return cls(username = name,
                   pw_hash = pw_hash,
                   email = email)
    
    @classmethod
    def ulogin(cls, name, pw):
        u = cls.by_name(name)
        if u and valid_pw(name, pw, u.pw_hash):
            return u
    
###############################################
### Main Signup Page Handler
###############################################

def already_there(un):
    u = db.GqlQuery("SELECT * FROM UserInfo WHERE username=:1", un)
    if u.get():
        return u.get()
    else:
        return False

class SignUp(BaseHandler):
    
    def get(self):
        self.render('signup.html')
    
    
    def post(self):
        ## Get all Values in Field
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')
        
        ## Keep track of errors
        has_error = False
        
        ## Dic to Store Values        
        valdic = dict(username=username,
                      email=email)
        
        ## Validate ALL Values
        
        
        
        if not valid(username,USER_RE):
            ## Add checking if Uname in db**
            uname_error = "That's not a valid User Name!"
            valdic['uname_error'] = uname_error
            has_error = True
        
        user = UserInfo.by_name(username)
        if already_there(username):
            uname_error = 'That name has been taken!'
            valdic['uname_error'] = uname_error
            valdic['username'] = ''
            has_error = True
                
        
        if not valid(password,PASS_RE):
            passval_error = "That's not a valid Password!"
            valdic['passval_error'] = passval_error
            has_error = True
        elif password != verify:
            passmat_error = "You're passwords don't match! Did you go to typing school?"
            valdic['passmat_error'] = passmat_error
            has_error = True
        
        if email:
            if not valid(email,EMAIL_RE):
                email_error = "That's not a valid eMail! If you're having trouble, try skipping the eMail part... it's a optional!"
                valdic['email_error'] = email_error
                has_error = True
            
        if has_error:
            ## Go back to Signup page
            self.render('signup.html',**valdic)
        else:
            ## Encrypt Password**
            u = UserInfo.register(username, password, email)
            u.put()
            self.login(u)
            self.redirect('/blog/welcome')

###############################################
### Login Page Handler 
###############################################

class LogIn(BaseHandler):
    def get(self):
        self.render('login.html')
    
    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')
        
        has_error = False
        
        valdic = dict(username=username)
        
        user = UserInfo.by_name(username)
        if not user:
            has_error = True
            valdic['uname_error'] = "That's not a known username!"
        
        else:
            h = user.pw_hash
            if not valid_pw(username, password, h):
                has_error = True
                valdic['passval_error'] = "That's not a valid Password"
           
        if has_error:
            ## Go back to Signup page
            self.render('login.html',**valdic)
        else:
            
            self.login(user)
            self.redirect('/blog/welcome')
 
###############################################
### Logout Page Handler
###############################################  

class LogOut(BaseHandler):     
    def get(self):
        self.logout()
        self.redirect('/blog/signup')
        
    

###############################################
### Main Welcome Page Handler 
###############################################
         
class Welcome(BaseHandler):
    #modify to check value of Cookie
    
    def get(self):
        h = self.request.cookies.get('user_id')
        user_id = check_secure_val(h)
        if user_id:
            ## Check Validity of Cookie** (or not?)
            user = UserInfo.by_id(int(user_id))
            self.render('welcome.html',username = user.username)
        else:
            self.redirect('/signup')
