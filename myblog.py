import webapp2

from authentication import SignUpPage
from authentication import SignInPage
from blogs import BlogListPage

app = webapp2.WSGIApplication([
  ('/account/signup', SignUpPage),
  ('/', SignInPage),
  ('/blogs', BlogListPage),
  #('/blogs/blog', BlogPage),
], debug=True)

def main():
    application.run()

if __name__ == "__main__":
    main()
