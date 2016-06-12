import os
import datetime

import webapp2
import jinja2

from hashing import SHA256Hashing
from hashing import HMACHashing
from validator import FieldValidator
from domainModels import User
from domainModels import DBUtility

template_dir = os.path.join(os.path.dirname(__file__), 'template')
jinja_env = jinja2.Environment (loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

class SignUpPage(webapp2.RequestHandler):
  def get(self):
    page = jinja_env.get_template('signup.html')
    self.response.out.write(page.render())

  def post(self):
    u_firstname = FieldValidator(self.request.get('firstname'), "First Name")
    u_firstname.isNotEmpty()

    u_lastname = FieldValidator(self.request.get('lastname'), "Last Name")
    u_lastname.isNotEmpty()

    u_emailaddr = FieldValidator(self.request.get('emailaddr'), "Email address")
    u_emailaddr.isNotEmpty()
    u_emailaddr.isValidEmail()
    dbHandle = DBUtility()
    users = dbHandle.getUser(u_emailaddr.value)
    emailExist = False
    for user in users:
      if user.emailaddr == u_emailaddr.value:
        emailExist = True
    if emailExist:
      if u_emailaddr.errormsg == None:
        u_emailaddr.errormsg = "This Email Address is already Registered!"


    u_password = FieldValidator(self.request.get('password'), "Password")
    u_password.isNotEmpty()
    u_password.isMinLen(8)

    c_password = FieldValidator(self.request.get('cpassword'), "Confirm Password")
    c_password.isNotEmpty()
    if u_password.value != c_password.value:
      if c_password.errormsg == None:
        c_password.errormsg = "Password Doesn't Match"

    if ((u_firstname.errormsg != None) |
        (u_lastname.errormsg != None) |
        (u_emailaddr.errormsg != None) |
        (u_password.errormsg != None) |
        (c_password.errormsg != None) ):
      page = jinja_env.get_template('signup.html')
      self.response.out.write(page.render(firstname=u_firstname.value,
                                          lastname=u_lastname.value,
                                          emailaddr=u_emailaddr.value,
                                          password=u_password.value,
                                          cpassword=c_password.value,
                                          firstname_error=u_firstname.errormsg,
                                          lastname_error=u_lastname.errormsg,
                                          emailaddr_error=u_emailaddr.errormsg,
                                          password_error=u_password.errormsg,
                                          cpassword_error=c_password.errormsg))
    else:
      hashobj = SHA256Hashing();
      newuser = User (firstname = u_firstname.value,
                      lastname = u_lastname.value,
                      emailaddr = u_emailaddr.value,
                      password = hashobj.make_pw_hash(u_emailaddr.value, u_password.value))
      newuser.put()
      self.redirect('/?action=successful_signup')

class SignInPage(webapp2.RequestHandler):
  def get(self):
    redirectDueTo = self.request.get('action')
    message = None
    if redirectDueTo == "signout":
      message = "You have successfully signed out..."
      page = jinja_env.get_template('homepage.html')
      self.response.delete_cookie('user')
      self.response.out.write(page.render(message=message))
    else:
      user_cookie = self.request.cookies.get('user')
      if user_cookie:
        u_emailaddr = user_cookie.split('|')[0]
        dbHandle = DBUtility()
        c_users = dbHandle.getUser(u_emailaddr)
        for c_user in c_users:
          if c_user.emailaddr == u_emailaddr:
            self.redirect('/blog')
          else:
            self.response.delete_cookie('user')
            self.redirect('/')
      else:
        if redirectDueTo == "successful_signup":
          message = "You have successfully signed Up..."
          page = jinja_env.get_template('homepage.html')
          self.response.out.write(page.render(message=message))
        else:
          page = jinja_env.get_template('homepage.html')
          self.response.out.write(page.render())


  def post(self):
    u_username = FieldValidator(self.request.get('username'), "Email address")
    u_username.isNotEmpty()
    u_username.isValidEmail()

    u_password = FieldValidator(self.request.get('password'), "Password")
    u_password.isNotEmpty()

    u_rememberMe = self.request.get('rememberme')

    if ((u_username.errormsg == None) & (u_password.errormsg == None)):
      hashed_password = None
      dbHandle = DBUtility()
      users = dbHandle.getUser(u_username.value)
      for user in users:
        if user.emailaddr == u_username.value:
          emailExist = True
          hashed_password = user.password
          break
      if not emailExist:
        if (u_username.errormsg == None & u_password.errormsg == None):
          u_username.errormsg = "Please enter a valid Email Address and Password"
          u_password.errormsg = "Please enter a valid Email Address and Password"
      else:
        hashobj = SHA256Hashing();
        if not (hashobj.valid_pw(u_username.value, u_password.value, hashed_password)):
          if ((u_username.errormsg == None) & (u_password.errormsg == None)):
            u_username.errormsg = "Please enter a valid Email Address and Password"
            u_password.errormsg = "Please enter a valid Email Address and Password"

    if ((u_username.errormsg != None) |
        (u_password.errormsg != None) ):
      page = jinja_env.get_template('homepage.html')
      self.response.out.write(page.render(username=u_username.value,
                                          password=u_password.value,
                                          username_error=u_username.errormsg,
                                          password_error=u_password.errormsg,
                                          rememberme=u_rememberMe))
    else:
      dbHandle = DBUtility()
      users = dbHandle.getUser(u_username.value)
      for user in users:
        if user.emailaddr == u_username.value:
          hashobj = HMACHashing()
          #Cookie Setup
          if u_rememberMe:
            cookie_active_until = datetime.datetime.now()+datetime.timedelta(days=30)
            self.response.set_cookie('user', hashobj.make_ck_hash(u_username.value),expires=cookie_active_until)
          else:
            self.response.set_cookie('user', hashobj.make_ck_hash(u_username.value))
          self.redirect('/blog')


class UserBlog(webapp2.RequestHandler):
  def get(self):
    cookie = self.request.cookies.get('user')
    if cookie:
      u_firstname = None
      u_emailaddr = cookie.split('|')[0]
      dbHandle = DBUtility()
      users = dbHandle.getUser(u_emailaddr)
      for user in users:
        if user.emailaddr == u_emailaddr:
          u_firstname = user.firstname
          break
      page = jinja_env.get_template('blog.html')
      self.response.out.write(page.render(firstname=u_firstname))
    else:
      self.redirect('/')


app = webapp2.WSGIApplication([
  ('/account/signup', SignUpPage),
  ('/', SignInPage),
  ('/blog', UserBlog),
], debug=True)

def main():
    application.run()

if __name__ == "__main__":
    main()
