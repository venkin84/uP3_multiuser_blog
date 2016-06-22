from google.appengine.ext import db

from domainModels import User
from domainModels import Blog
from domainModels import Comment
from domainModels import Like
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
      return blog.put()
    else:
      blog = Blog(author=b_author, title=b_title, blogbody=b_body)
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

  def read_blog_byKey (self, b_key):
    return db.get(b_key)

  def count_blogs(self):
    q = db.Query(Blog)
    return q.count()

  def delete_blog(self, blog):
    return blog.delete()

  def save_comment(self, u_comment, c_blog, c_user, c_id=0):
    if c_id>0:
      c_key = db.Key.from_path('Comment', long(c_id))
      comment = db.get(c_key)
      if u_comment:
        comment.comment = u_comment
      return comment.put()
    else:
      comment = Comment(user=c_user, blog=c_blog, comment=u_comment)
      return comment.put()

  def read_comments_byBlog(self, blog):
    q = db.Query(Comment)
    return q.filter('blog =', blog).order("-created").run()

  def count_comments_byBlog(self, blog):
    q = db.Query(Comment)
    return q.filter('blog =', blog).count()

  def delete_comment(self, comment):
    return comment.delete()

  def save_userLikes(self, l_blog, l_user):
    q = db.Query(Like)
    liked = q.filter('blog =', l_blog).filter('user =', l_user).count()
    if ((liked == 0) & (l_blog.author.key().id() != l_user.key().id())):
      like = Like(user=l_user, blog=l_blog)
      return like.put()
    else:
      return None

  def count_likes_byBlog(self, blog):
    q = db.Query(Like)
    return q.filter('blog =', blog).count()
