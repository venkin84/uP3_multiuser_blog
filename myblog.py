import webapp2

from authentication import SignUpPage
from authentication import SignInPage
from blogs import BlogsListPage
from blogs import BlogInPage
from blogs import BlogPage

app = webapp2.WSGIApplication([
  ('/account/signup', SignUpPage),
  ('/', SignInPage),
  ('/blogs', BlogsListPage),
  ('/blogs/blogin', BlogInPage),
  ('/blogs/blog', BlogPage),
], debug=True)

def main():
    application.run()

if __name__ == "__main__":
    main()
