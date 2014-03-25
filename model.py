from google.appengine.ext import ndb

class Message(ndb.Model): #Guest
  first = ndb.StringProperty()
  last = ndb.StringProperty()
  msg = ndb.StringProperty()


def AllMessages(): #AllGuests
  return Message.query()


def CourseMessages(course_key):
  return Message.query(ancestor=course_key)

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
  courses = ndb.KeyProperty(repeated = True)

def AllUsers():
  return User.query()

def QueryUser(id):
  user_key = ndb.Key(User, id)
  return user_key.get()

def UpdateUser(id, course_key):
  user_key = ndb.Key(User, id)
  user = user_key.get()
  course_list = user.courses
  course_list.append(course_key)
  user.courses = course_list
  user.put()

def InsertUser(first, last, course):
  course_list = []
  course_list.append(course)
  user = User(first=first, last=last, courses=course_list)
  user.put()
  return user

class Course(ndb.Model):
  crn = ndb.IntegerProperty()
  name = ndb.StringProperty()
  message_list = ndb.KeyProperty(repeated = True)

def AddMessageToCourse(course_key, message):
  course = course_key.get()
  course_messages = course.message_list
  course_messages.append(message)
  course.message_list = course_messages
  course.put()

def InsertCourse(crn, name):
  course = Course(crn=int(crn), name=name, message_list=[])
  return course.put()

def QueryCourse(course_key):
  if(course_key is None):
    print('\nDoing this\n')
    course_key = AddCourseIfEmpty()

  course_list = []
  for course in course_key:
    course_list.append(course.get())
  return course_list

def AddCourseIfEmpty():
  if( Course.query() ):
    print('\nhere\n')
    course = Course()
    course.crn = 00000
    course.name = 'Wichita State'
    course_key = course.put()
  else:
    course = Course.query()
    print('\nno here\n')
    print(course)
    print('\nno here\n')
    course_key = ndb.Key(Course, course)
    #print(course_key)

  return course_key

