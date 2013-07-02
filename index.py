from base import BaseHandler

###############################################
### Urls and Title for Index Page
###############################################

handlers = [('/secret', 'ROT13'),
                               ('blog/signup', 'SignUp!'),
                               ('/blog', 'Blog Front Page!'),
                               ('/blog/newpost', 'Blog Form!'),
                               ('blog/login', 'Log In!'),
                               ('blog/logout', 'Log Out :('),
                               ('http://google.com', 'Google Something!')]

###############################################
### Super simple Index Handler
###############################################

class Index(BaseHandler):
    def get(self):
        self.render('index.html', handlers=handlers)