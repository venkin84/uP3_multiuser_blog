from google.appengine.ext import db

from domainModels import User
from domainModels import Blog
from hashing import SHA256Hashing

class DBUtility():
  def create_User (self, u_firstname, u_lastname, u_emailaddr, u_password):
    if (u_firstname & u_lastname & u_emailaddr & u_password):
      hashobj = SHA256Hashing();
      return User(firstname = u_firstname,
                  lastname = u_lastname,
                  emailaddr = u_emailaddr,
                  password = hashobj.hash_password(u_emailaddr, u_password)).put()
    else:
      return None

  def read_User (self, email):
    q = db.Query(User)
    q.filter("emailaddr =", email)
    return q.get()

  def create_Blog (self, b_title, b_body, b_author):
    if b_author:
      user = self.read_User(b_author.emailaddr)
      if user:
        return Blog(user = b_author,
                    title = b_title,
                    body = b_body).put()
    else:
      return None

  def read_blogs (self, author = None, offset_num = None, limit_num = None, orderby_property = None, orderin = "asc"):
    q = db.Query(Blog)
    if author:
      if orderby_property:
        if orderin == "desc":
          return q.filter('user =', b_author).order('-' + orderby_property).run(offset = offset_num, limit = limit_num)
        else:
          return q.filter('user =', b_author).order(orderby_property).run(offset = offset_num, limit = limit_num)
      else:
        return q.filter('user =', b_author).run(offset = offset_num, limit = limit_num)
    else:
      if orderby_property:
        if orderin == "desc":
          return q.order('-' + orderby_property).run(offset = offset_num, limit = limit_num)
        else:
          return q.order(orderby_property).run(offset = offset_num, limit = limit_num)
      else:
        return q.run(offset = offset_num, limit = limit_num)

  def read_blog (self, b_title, author):
    q = db.Query(Blog)
    return q.filter('title =', b_title).filter('user =', author).get()
