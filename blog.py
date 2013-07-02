from base import BaseHandler
#import json

from google.appengine.ext import db
from google.appengine.api import memcache
import logging
import time


def top_posts(update = False):
    key = 'top'
    posts = memcache.get(key)
    if posts is None or update:
        logging.error("DB QUERY")
        posts = db.GqlQuery("SELECT * FROM BlogEntry ORDER BY created DESC LIMIT 10")
        posts = list(posts)
        memcache.set(key,(time.time(),posts))
    return memcache.get(key)

def id_post(post_id, update = False):
    post = memcache.get(post_id)
    if post is None:
        logging.error("DB QUERY")
        post = BlogEntry.get_by_id(int(post_id))
        memcache.set(post_id,(time.time(),post))
    return memcache.get(post_id)


###############################################
### Creat DB of Entries
###############################################

class BlogEntry(db.Model):
    #database of entries
    subject = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    last_modified = db.DateTimeProperty(auto_now_add = True)
    
    def as_dict(self):
        time_fmt = '%c'
        d = dict(subject = self.subject,
                content = self.content,
                created = self.created.strftime(time_fmt),
                last_modified = self.last_modified.strftime(time_fmt))
        return d 
 
###############################################
### Blog Form Handler
###############################################   
    
class BlogForm(BaseHandler):
    #form to submit entries
    def get(self):
        self.render('blog-form.html')
    def post(self):
        subject = self.request.get('subject')
        content = self.request.get('content')
        if subject and content:
            p = BlogEntry(content=content , subject=subject)
            p.put()
            top_posts(True)
            post_id = str(p.key().id())
            memcache.set(post_id,(time.time(),p))
            url = '/blog/{}'.format(post_id)
            
        
            self.redirect(url)
        else:
            error = 'oops, I need subject AND content for this!'
            self.render('blog-form.html', subject=subject, content=content, error=error )

###############################################
### Blog Front Page Handler
###############################################

class BlogFront(BaseHandler):
    #front page that displays entries
    def get(self):
        post_time = top_posts()
        entries = post_time[1]
        seconds = time.time() - post_time[0]
        if self.format == 'html':
            self.render('blog-front.html', entries=entries, seconds=int(seconds))
        else:
            return self.render_json([p.as_dict() for p in entries])


###############################################
### Blog Permalink Handler
###############################################

class BlogPerma(BaseHandler):
    #permalink to blog posts
    def get(self, post_id):
        #key = db.Key.from_path('BlogEntry', int(post_id))
        #gql = "SELECT * from BlogEntry where __key__=" + key
        #post = db.GqlQuery(gql)
        post_time = id_post(post_id)
        post = post_time[1]
        seconds = time.time() - post_time[0]
        if self.format == 'html':
            self.render('blog-posted.html', post = post, seconds = int(seconds))
        else:
            self.render_json(post.as_dict())

###############################################
### Blog Flush Handler
###############################################

class BlogFlush(BaseHandler):
    def get(self):
        
        flushed = memcache.flush_all()
        if flushed:
            self.redirect('/blog')
        else:
            self.write('oops!')

       
        
        
        
        