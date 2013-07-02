import os
import re
#from string import letters

import webapp2
import jinja2

#from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)
def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)




class BaseHandler(webapp2.RequestHandler):
    def render(self, template, **kw):
        self.response.out.write(render_str(template, **kw))

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

class Index(BaseHandler):
    def get(self):
        self.render('index.html')
        

class Rot13(BaseHandler):
    def get(self):        
        self.render('rot13-form.html')
                               

    def post(self):
        rot13 = ''
        text = self.request.get('text')
        if text:
            rot13 = text.encode('rot13')

        self.render('rot13-form.html',text = rot13)



USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASS_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")

def valid(username, rec):
    m = rec.match(username)
    if m:
        return m.group()
    else:
        return ''

class SignUp(BaseHandler):
    
    def get(self):
        self.render('signup.html')
    
    
    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')
        
        has_error = False
                
        valdic = dict(username=username,
                      email=email)
        if not valid(username,USER_RE):
            uname_error = "That's not a valid User Name!"
            valdic['uname_error'] = uname_error
            has_error = True
        
        if not valid(password,PASS_RE):
            passval_error = "That's not a valid Password!"
            valdic['passval_error'] = passval_error
            has_error = True
        elif password != verify:
            passmat_error = "You're passwords don't match! Did you go to typing school?"
            valdic['passmat_error'] = passmat_error
            has_error = True
        
        
        if not valid(email,EMAIL_RE):
            email_error = "That's not a valid eMail! If you're having trouble, try skipping the eMail part... it's a bitch!"
            valdic['email_error'] = email_error
            has_error = True
        
        if has_error:
            self.render('signup.html',**valdic)
        else:
            self.redirect('/welcome?username='+username)
            

class Welcome(BaseHandler):
    def get(self):
        username = self.request.get('username')
        if valid(username, USER_RE):
            self.render('welcome.html',username = username)
        else:
            self.redirect('/signup')
    
        
        
        





        
app = webapp2.WSGIApplication([('/',Index),
                               ('/secret', Rot13),
                               ('/signup' , SignUp),
                               ('/welcome',Welcome)], 
                              debug=True)
