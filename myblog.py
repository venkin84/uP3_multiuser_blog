import os

import webapp2
import jinja2

template_dir = os.path.join(os.path.dirname(__file__), 'template')
jinja_env = jinja2.Environment (loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

class SignUpPage(webapp2.RequestHandler):
  def get(self):
    page = jinja_env.get_template('signup.html')
    self.response.out.write(page.render())

class SignInPage(webapp2.RequestHandler):
  def get(self):
    page = jinja_env.get_template('homepage.html')
    self.response.out.write(page.render())

  # def post(self):


app = webapp2.WSGIApplication([
  ('/account/signup', SignUpPage),
  ('/', SignInPage),
], debug=True)

def main():
    application.run()

if __name__ == "__main__":
    main()
