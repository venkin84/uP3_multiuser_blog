import os

import webapp2
import jinja2

from hashing import HMACHashing
from validator import FieldValidator
#from domainModels import User
from dbUtils import DBUtility

template_dir = os.path.join(os.path.dirname(__file__), 'template')
jinja_env = jinja2.Environment (loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

dbHandle = DBUtility()

class BlogsListPage(webapp2.RequestHandler):
  def get(self):
    u_cookie = self.request.cookies.get('user')
    if u_cookie:
      cookie_hash = HMACHashing()
      user_info = cookie_hash.validate_hashed_cookie(u_cookie)
      user = dbHandle.read_User(user_info)
      if user:
        u_initial = user.firstname[:1] + user.lastname[:1]
        page = jinja_env.get_template('blogs.html')
        self.response.out.write(page.render(user=user))
      else:
        self.redirect('/')
    else:
      self.redirect('/?action=signout')


class BlogInPage(webapp2.RequestHandler):
  def get (self):
    u_cookie = self.request.cookies.get('user')
    if u_cookie:
      cookie_hash = HMACHashing()
      user_info = cookie_hash.validate_hashed_cookie(u_cookie)
      user = dbHandle.read_User(user_info)
      if user:
        page = jinja_env.get_template('blogin.html')
        self.response.out.write(page.render(user=user))
      else:
        self.redirect('/')
    else:
      self.redirect('/?action=signout')

  def post (self):
    u_cookie = self.request.cookies.get('user')
    if u_cookie:
      cookie_hash = HMACHashing()
      user_info = cookie_hash.validate_hashed_cookie(u_cookie)
      user = dbHandle.read_User(user_info)
      if user:
        b_title = FieldValidator(self.request.get('blogtitle'), "Blog title")
        b_title.isNotEmpty()
        blog = dbHandle.read_blog(b_title.value)
        if blog != None:
          b_title.errormsg = "A Blog with the same title is present already... Nice Conincidence!"

        b_blogbody = FieldValidator(self.request.get('blogbody'), "Blog Body")
        b_blogbody.isNotEmpty()

        if ((b_title.errormsg != None) |
            (b_blogbody.errormsg != None)):
          #template_values = {'user' :user}
          page = jinja_env.get_template('blogin.html')
          self.response.out.write(page.render(user=user,
                                              blogtitle=b_title.value,
                                              #blogbody=b_blogbody.value,
                                              blogtitle_error=b_title.errormsg,
                                              blogbody_error=b_blogbody.errormsg
                                              ))
        else:
          b_key = dbHandle.save_Blog(b_title.value, b_blogbody.value, user)
          if b_key:
            self.redirect('/blogs?action=successfully_submission')
          else:
            self.redirect('/blogs/blogin?action=unsuccessful_submission')
      else:
        self.redirect('/')
    else:
      self.redirect('/?action=signout')
