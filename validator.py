import re

class FieldValidator():
  def __init__(self, fieldvalue, fieldname):
    self.value = fieldvalue
    self.name = fieldname
    self.errormsg = '0'

  def isNotEmpty(self):
    if not self.value:
      self.errormsg = self.name + " is Required"

  def isValidEmail (self):
    if re.match('^[_a-zA-Z0-9-]+(\.[_a-zA-Z0-9-]+)*@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*(\.[a-zA-Z]{2,4})$', self.value) == '0':
      if self.errormsg == '0':
        self.errormsg = "Enter a valid email address"

  def isMinLen (self, minlen):
    if len(self.value) < minlen:
      if self.errormsg == '0':
        self.errormsg = self.name + " should have min of " + str(minlen) + " Characters"
