from google.appengine.ext import db

class User(db.Model):
  firstname = db.StringProperty (required = True)
  lastname = db.StringProperty (required = True)
  emailaddr = db.EmailProperty (required = True)
  password = db.StringProperty (required = True)
  created = db.DateTimeProperty (auto_now_add = True)

class DBUtility():
  def getUser (self, email):
    q = db.Query(User)
    q.filter("emailaddr =", email)
    return q.get()
