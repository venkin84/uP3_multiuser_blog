import random
import string
import hashlib
import hmac

class SHA256Hashing():
  def make_salt(self):
    return ''.join(random.choice(string.letters) for x in xrange(5))

  def hash_password(self, username, password, salt = None):
    if not salt:
      salt = self.make_salt()
    hashed_password = hashlib.sha256(username + password + salt).hexdigest()
    return '%s,%s' % (hashed_password, salt)

  def validate_hashed_password(self, username, password, hashed_password):
    salt = hashed_password.split(',')[1]
    return (hashed_password == self.hash_password(username, password, salt))

class HMACHashing():
  SECRET_KEY = "rrb4t3bg43vhrh4903gh3hfj"

  def hash_cookie(self, arg):
    return "%s|%s" % (arg, hmac.new(self.SECRET_KEY, arg).hexdigest())

  def validate_hashed_cookie (self, hased_arg):
    arg = hased_arg.split('|')[0]
    if hased_arg == self.hash_cookie(arg):
      return arg
    else:
      return None

  def hash_urlsafe (self, arg):
    return (hmac.new(self.SECRET_KEY, arg).hexdigest())
