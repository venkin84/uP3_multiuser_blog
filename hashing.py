import random
import string
import hashlib

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
