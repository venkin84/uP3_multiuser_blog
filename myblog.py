import webapp2

from authentication import SignUpPage
from authentication import SignInPage
from blogs import BlogsListPage
from blogs import BlogInPage
from blogs import BlogPage
from blogs import LikeABlog

app = webapp2.WSGIApplication([
  ('/account/signup', SignUpPage),
  ('/', SignInPage),
  ('/blogs', BlogsListPage),
  ('/blogs/blogin', BlogInPage),
  ('/blogs/blog', BlogPage),
  ('/blogs/blog/like', LikeABlog)
], debug=True)

def main():
    application.run()

if __name__ == "__main__":
    main()
