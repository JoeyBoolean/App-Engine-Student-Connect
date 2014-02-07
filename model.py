from google.appengine.ext import ndb

class Message(ndb.Model): #Guest
  first = ndb.StringProperty()
  last = ndb.StringProperty()
  msg = ndb.StringProperty()


def AllMessages(): #AllGuests
  return Message.query()


def UpdateMessage(id, first, last, msg): #UpdateGuest
  message = Message(id=id, first=first, last=last, msg=msg)
  message.put()
  return message


def InsertMessage(first, last, msg): #InsertGueset
  message = Message(first=first, last=last, msg=msg)
  message.put()
  return message


def DeleteMessage(id): #DeleteGuest
  key = ndb.Key(Message, id)
  key.delete()

class User(ndb.Model):
  first =ndb.StringProperty()
  last = ndb.StringProperty()

def AllUsers():
  return User.query()

def InsertUser(first, last):
  user = User(first=first, last=last)
  user.put()
  return user
