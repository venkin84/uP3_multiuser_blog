from google.appengine.ext import db

class User(db.Model):
  firstname = db.StringProperty (required = True)
  lastname = db.StringProperty (required = True)
  emailaddr = db.EmailProperty (required = True)
  password = db.StringProperty (required = True)
  created = db.DateTimeProperty (auto_now_add = True)

class Blog(db.Model):
  author = db.ReferenceProperty (User, required = True, collection_name = 'blogs')
  title = db.StringProperty (required = True)
  blogbody = db.TextProperty (required = True)
