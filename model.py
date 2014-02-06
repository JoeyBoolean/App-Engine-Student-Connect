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
  guest = Message(first=first, last=last, msg=msg)
  guest.put()
  return guest


def DeleteMessage(id): #DeleteGuest
  key = ndb.Key(Message, id)
  key.delete()
