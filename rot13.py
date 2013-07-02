from base import BaseHandler

###############################################
### SECRET Handler
###############################################

class Rot13(BaseHandler):
    def get(self):        
        self.render('rot13-form.html')
                               

    def post(self):
        rot13 = ''
        text = self.request.get('text')
        if text:
            rot13 = text.encode('rot13')

        self.render('rot13-form.html',text = rot13)
