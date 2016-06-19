import os

import webapp2
import jinja2

from hashing import SHA256Hashing
from hashing import HMACHashing
from validator import FieldValidator
from domainModels import User
from domainModels import DBUtility

template_dir = os.path.join(os.path.dirname(__file__), 'template')
jinja_env = jinja2.Environment (loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

class BlogListPage(webapp2.RequestHandler):
  def get(self):
    u_cookie = self.request.cookies.get('user')
    if u_cookie:
      cookie_hash = HMACHashing()
      user_info = cookie_hash.validate_hashed_cookie(u_cookie)
      dbHandle = DBUtility()
      user = dbHandle.getUser(user_info)
      if user:
        u_initial = user.firstname[:1] + user.lastname[:1]
        page = jinja_env.get_template('blogs.html')
        self.response.out.write(page.render(firstname=user.firstname,
                                            emailaddr=user.emailaddr,
                                            initial=u_initial))
      else:
        self.redirect('/')
    else:
      self.redirect('/?action=signout')
