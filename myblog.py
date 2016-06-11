import os

import webapp2
import jinja2

from validator import FieldValidator

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
      self.redirect('/?action=successful_signup')

class SignInPage(webapp2.RequestHandler):
  def get(self):
    page = jinja_env.get_template('homepage.html')
    self.response.out.write(page.render())

app = webapp2.WSGIApplication([
  ('/account/signup', SignUpPage),
  ('/', SignInPage),
], debug=True)

def main():
    application.run()

if __name__ == "__main__":
    main()
