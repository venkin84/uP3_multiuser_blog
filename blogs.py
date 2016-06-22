import os

import webapp2
import jinja2

from hashing import HMACHashing
from validator import FieldValidator
from dbUtils import DBUtility

template_dir = os.path.join(os.path.dirname(__file__), 'template')
jinja_env = jinja2.Environment (loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

dbHandle = DBUtility()

class PageLoader():
  offset = 0
  limit = 5

  def getOffset(self):
    return self.offset

  def setOffset(self, arg):
    self.offset = arg

  def getLimit(self):
    return self.limit

loader = PageLoader()

class BlogsListPage(webapp2.RequestHandler):
  def get(self):
    u_cookie = self.request.cookies.get('user')
    if u_cookie:
      cookie_hash = HMACHashing()
      user_info = cookie_hash.validate_hashed_cookie(u_cookie)
      user = dbHandle.read_User(user_info)
      if user:
        page = self.request.get('page')
        if not page:
          loader.setOffset(0)
        elif page == "next":
          if (loader.getOffset() + loader.getLimit()) <= dbHandle.count_blogs():
            loader.setOffset(loader.getOffset()+loader.getLimit())
        elif page == "previous":
          if (loader.getOffset() - loader.getLimit()) >= 0:
            loader.setOffset(loader.getOffset()-loader.getLimit())
        blogs = dbHandle.read_blogs(None,loader.getOffset(),loader.getLimit(),"created","desc")
        page = jinja_env.get_template('blogs.html')
        self.response.out.write(page.render(user=user,
                                            recentBlogs=blogs,
                                            dbHandle=dbHandle))
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
        b_key = self.request.get('id')
        blog = dbHandle.read_blog_byKey(b_key)
        page = jinja_env.get_template('blogin.html')
        self.response.out.write(page.render(user=user, blog=blog))
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

        b_blogbody = FieldValidator(self.request.get('blogbody'), "Blog Body")
        b_blogbody.isNotEmpty()

        b_key = self.request.get('id')
        if b_key != "":
          blog = dbHandle.read_blog_byKey(b_key)
          if blog!=None:
            if b_title.value:
              blog.title = b_title.value
            if b_blogbody.value:
              blog.blogbody = b_blogbody.value
        else:
          b_blog = dbHandle.read_blog(b_title.value)
          if b_blog != None:
            b_title.errormsg = "A Blog with the same title is present already... Nice Conincidence!"

        if ((b_title.errormsg != None) |
            (b_blogbody.errormsg != None)):
          page = jinja_env.get_template('blogin.html')
          if blog != None:
            self.response.out.write(page.render(user=user,
                                                blog=blog,
                                                blogtitle_error=b_title.errormsg,
                                                blogbody_error=b_blogbody.errormsg
                                                ))
          else:
            self.response.out.write(page.render(user=user,
                                                blogtitle=b_title.value,
                                                blogbody=b_blogbody.value,
                                                blogtitle_error=b_title.errormsg,
                                                blogbody_error=b_blogbody.errormsg
                                                ))
        else:
          if blog == None:
            blog_key = dbHandle.save_Blog(b_title.value, b_blogbody.value, user)
          else:
            blog_key = dbHandle.save_Blog(b_title.value, b_blogbody.value, user, blog.key().id())
          if blog_key:
            self.redirect('/blogs?action=successfully_submission')
          else:
            self.redirect('/blogs/blogin?action=unsuccessful_submission')
      else:
        self.redirect('/')
    else:
      self.redirect('/?action=signout')


class BlogPage(webapp2.RequestHandler):
  def get (self):
    u_cookie = self.request.cookies.get('user')
    if u_cookie:
      cookie_hash = HMACHashing()
      user_info = cookie_hash.validate_hashed_cookie(u_cookie)
      user = dbHandle.read_User(user_info)
      if user:
        action = self.request.get('action')
        if action == "deleteblog":
          b_key = self.request.get('b_id')
          blog = dbHandle.read_blog_byKey(b_key)
          if (blog.author.key().id() == user.key().id()):
            dbHandle.delete_blog(blog)
            self.redirect('/blogs?action=successfully_deleted')
          else:
            self.redirect('/blogs')
        b_key = self.request.get('id')
        if b_key:
          blog = dbHandle.read_blog_byKey(b_key)
          comments = dbHandle.read_comments_byBlog(blog)
          page = jinja_env.get_template('blog.html')
          self.response.out.write(page.render(user=user,
                                              blog=blog,
                                              comments=comments,
                                              dbHandle=dbHandle))
        else:
          self.redirect('/blogs')
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
        u_comment = FieldValidator(self.request.get('comment'), "Comment")
        u_comment.isNotEmpty()
        b_key = self.request.get('blog')
        blog = dbHandle.read_blog_byKey(b_key)
        if u_comment.errormsg == None:
          c_key = dbHandle.save_comment(u_comment.value, blog, user)
          self.redirect('/blogs/blog?id='+ str(blog.key()))
        else:
          self.redirect('/blogs/blog?id='+ str(blog.key()))
      else:
        self.redirect('/')
    else:
      self.redirect('/?action=signout')

class LikeABlog(webapp2.RequestHandler):
  def get(self):
    u_cookie = self.request.cookies.get('user')
    if u_cookie:
      cookie_hash = HMACHashing()
      user_info = cookie_hash.validate_hashed_cookie(u_cookie)
      user = dbHandle.read_User(user_info)
      if user:
        b_key = self.request.get('id')
        blog = dbHandle.read_blog_byKey(b_key)
        l_key = dbHandle.save_userLikes(blog, user)
        self.redirect('/blogs/blog?id='+ str(blog.key()))
      else:
        self.redirect('/')
    else:
      self.redirect('/?action=signout')
