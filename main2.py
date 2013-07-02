
import webapp2

from index import Index
from signup import SignUp, Welcome, LogIn, LogOut
from rot13 import Rot13
from blog import BlogForm, BlogFront, BlogPerma, BlogFlush 
        
app = webapp2.WSGIApplication([('/', Index),
                               ('/secret', Rot13),
                               ('/blog/signup', SignUp),
                               ('/blog/welcome', Welcome),
                               ('/blog/?(?:\.json)?', BlogFront),
                               ('/blog/newpost', BlogForm),
                               ('/blog/([0-9]+)(?:\.json)?', BlogPerma),
                               ('/blog/flush', BlogFlush),
                               ('/blog/login', LogIn),
                               ('/blog/logout', LogOut)], 
                              debug=True)
