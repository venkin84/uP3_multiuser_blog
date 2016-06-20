from google.appengine.ext import db

from domainModels import User
from domainModels import Blog
from hashing import SHA256Hashing

class DBUtility():
  def save_User (self, u_firstname, u_lastname, u_emailaddr, u_password, u_id = 0):
    if u_id > 0:
      u_key = db.Key.from_path('User', long(u_id))
      user = db.get(u_key)
      hashobj = SHA256Hashing();
      if u_firstname:
        user.firstname = u_firstname
      if u_lastname:
        user.lastname = u_lastname
      if u_emailaddr:
        user.emailaddr = u_emailaddr
      if u_password:
        user.password = hashobj.hash_password(u_emailaddr, u_password)
      return user.put()
    else:
      hashobj = SHA256Hashing();
      user = User(firstname = u_firstname,
                  lastname = u_lastname,
                  emailaddr = u_emailaddr,
                  password = hashobj.hash_password(u_emailaddr, u_password))
      return user.put()

  def read_User (self, email):
    q = db.Query(User)
    q.filter("emailaddr =", email)
    return q.get()

  def save_Blog (self, b_title, b_body, b_author, b_id = 0):
    if b_id > 0:
      b_key = db.Key.from_path('Blog', long(b_id))
      blog = db.get(b_key)
      if b_title:
        blog.title = b_title
      if b_body:
        blog.blogbody = b_body
      if b_author:
        blog.author = b_author
      return blog.put()
    else:
      blog = Blog(author=b_author, title=b_title,blogbody=b_body)
      return blog.put()

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

  def read_blog (self, b_title, author = None):
    q = db.Query(Blog)
    if author != None:
      return q.filter('title =', b_title).filter('user =', author).get()
    else:
      return q.filter('title =', b_title).get()