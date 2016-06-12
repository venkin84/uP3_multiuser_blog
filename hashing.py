import random
import string
import hashlib
import hmac


class SHA256Hashing():
  def make_salt(self):
    return ''.join(random.choice(string.letters) for x in xrange(5))

  def make_pw_hash(self, username, password, salt = None):
    if not salt:
      salt = self.make_salt()
    hashed_password = hashlib.sha256(username + password + salt).hexdigest()
    return '%s,%s' % (hashed_password, salt)

  def valid_pw(self, username, password, hashed_password):
    salt = hashed_password.split(',')[1]
    return (hashed_password == self.make_pw_hash(username, password, salt))

class HMACHashing():
  SECRET_KEY = "rrb4t3bg43vhrh4903gh3hfj"

  def hash_str(self, arg):
    return hmac.new(self.SECRET_KEY, arg).hexdigest()

  def make_ck_hash(self, arg):
    return "%s|%s" % (arg, self.hash_str(arg))

  def valid_ck (self, hased_arg):
    arg = hased_arg.split('|')[0]
    if arg == self.make_ck_hash(arg):
      return arg
