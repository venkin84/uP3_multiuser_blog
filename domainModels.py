from google.appengine.ext import db

class User(db.Model):
  firstname = db.StringProperty (required = True)
  lastname = db.StringProperty (required = True)
  emailaddr = db.StringProperty (required = True)
  password = db.StringProperty (required = True)
  created = db.DateTimeProperty (auto_now_add = True)

class DBUtility():
  def getUser (self, emailaddr):
    return db.GqlQuery("SELECT * FROM User WHERE emailaddr = :email", email=emailaddr)
