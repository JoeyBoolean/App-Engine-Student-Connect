from google.appengine.ext import ndb

class Message(ndb.Model): #Guest
  first = ndb.StringProperty()
  last = ndb.StringProperty()
  userKey = ndb.KeyProperty()
  msg = ndb.StringProperty()
  time = ndb.DateTimeProperty(auto_now_add=True)

def AllMessages(): #AllGuests
  return Message.query()


def CourseMessages(course_key):
  msg = Message.query()
  print ('\n\n course_key\n')
  print(course_key)
  course = QuerySingleCourse(int(course_key))
  course = course.get()
  r = course.message_list
  print('\n Message List \n')
  print r
  return r

def UpdateMessage(id, first, last, msg): #UpdateGuest
  message = Message(id=id, first=first, last=last, msg=msg)
  message.put()
  return message


def InsertMessage(userKey, msg): #InsertGueset
  message = Message(userKey=userKey, msg=msg)
  r = message.put()
  return r


def DeleteMessage(id): #DeleteGuest
  key = ndb.Key(Message, id)
  key.delete()

class User(ndb.Model):
  username =ndb.StringProperty()
  name = ndb.StringProperty()
  password = ndb.StringProperty()
  logged_in = ndb.BooleanProperty()
  courses = ndb.KeyProperty(repeated = True)

def AllUsers():
  return User.query()

def QueryUser(id):
  user_key = ndb.Key(User, id)
  return user_key.get()

def CheckUser(username, password):
  print(username, password)
  users = User.query(User.username == username).fetch(1)
  # for user in users:
    # print(user.password)
  # user = users
  user = users.pop()
  print('Dis Shit')
  print(user)
  if user is None:
    return None
  # user = user_key.get()
  if(user.password == password):
    user.logged_in = True;
    user.put()
    return user
  return None

def UpdateUser(id, course_key):
  user_key = ndb.Key(User, id)
  user = user_key.get()
  course_list = user.courses
  course_list.append(course_key)
  user.courses = course_list
  user.put()

def InsertUser(username, name, password, course):
  course_list = []
  course_list.append(course)
  user = User(username=username, name=name, password=password, logged_in=True, courses=course_list)
  user.put()
  return user

class Course(ndb.Model):
  crn = ndb.IntegerProperty()
  name = ndb.StringProperty()
  message_list = ndb.KeyProperty(repeated = True)

def AddMessageToCourse(course_key, message_key):
  course = course_key.get()
  course_messages = course.message_list
  course_messages.append(message_key)
  course.message_list = course_messages
  course.put()

def InsertCourse(crn, name):
  course = Course(crn=int(crn), name=name, message_list=[])
  return course.put()

def QuerySingleCourse(course_key):
  course = ndb.Key(Course, course_key)
  return course

def QueryCourse(course_key):
  if(course_key is None):
    print('\nDoing this\n')
    course_key = AddCourseIfEmpty()
    # msgKey = InsertMessage()

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

