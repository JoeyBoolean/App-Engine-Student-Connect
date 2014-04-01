import json
import webapp2
import time

import model


def AsDict(message):
  user = model.QueryUser(message.userKey)
  r = {'id': message.key.id(), 'username': user.username, 'name': user.name, 'msg': message.msg, 'time':message.time}
  r.append({'id': 1234, 'username': 'Student Connect', 'name': 'Student Connect', 'msg': 'Hello', 'time':12323})
  return r

def AsDictUser(user):
  """ 
  course is a list in the user object
  """
  course_list = model.QueryCourse(user.courses)
  print('\n\n')
  print(course_list)
  print('\n\n')
  course_out = []
  for course in course_list:
    course_out.append({'courseKey':course.key.id(), 'crn': course.crn, 'name':course.name})
    print('\n\n')
    print(course_out)
    print('\n\n')
  return {'id': user.key.id(), 'nameCheck': True, 'username': user.username, 'name': user.name, 'courses': course_out}

def AsDictCourse(course):
  return {'courseID': course.key.id(), 'crn': course.crn, 'name': course.name}

class RestHandler(webapp2.RequestHandler):

  def dispatch(self):
    #time.sleep(1)
    super(RestHandler, self).dispatch()


  def SendJson(self, r):
    self.response.headers['content-type'] = 'text/plain'
    self.response.write(json.dumps(r))
    

class QueryCourseMessageHandler(RestHandler):

  def post(self):
    courses = json.loads(self.request.body)
    r = {'courses':[]}
    for course in courses:
      print('\n')
      print( course )
      print('\n')
      messages = model.CourseMessages(course['courseKey'])
      # if messages:
        # msg = [ AsDict(message) for message in messages]
      # else:
      msg = [{'id': 1234, 'username': 'Student Connect', 'name': 'Student Connect', 'msg': 'Hello', 'time':12323}]
      course_dict = {'course': course['courseKey'], 'messages':msg}
      r['courses'].append(course_dict)
    self.SendJson(r)

class QueryHandler(RestHandler):

  def get(self):
    messages = model.AllMessages()
    r = [ AsDict(message) for message in messages ]
    self.SendJson(r)


class UpdateHandler(RestHandler):

  def post(self):
    r = json.loads(self.request.body)
    message = model.UpdateMessage(r['id'], r['first'], r['last'], r['msg'])
    r = AsDict(message)
    self.SendJson(r)


class InsertMessageHandler(RestHandler):

  def post(self):
    r = json.loads(self.request.body)
    course = model.QueryCourse(int(r['courseKey']))
    user = model.QueryUser(int(r['userKey']))
    message = model.InsertMessage(user.key.id(), r['msg'])
    return_msg = model.AddMessageToCourse(course.key.id(), message.key.id())
    # r = AsDict(message)
    r = {'msgID': message.key.id, 'time':message.time}
    self.SendJson(r)

class InsertUserHandler(RestHandler):

  def post(self):
    r = json.loads(self.request.body)
    course = model.AddCourseIfEmpty()
    user = model.InsertUser(r['username'], r['name'], r['password'], course)
    r = AsDictUser(user)
    self.SendJson(r)

class DeleteHandler(RestHandler):

  def post(self):
    r = json.loads(self.request.body)
    model.DeleteMessage(r['id'])

class UserQueryHandler(RestHandler):

  def get(self):
    users = model.AllUsers()
    r = [ AsDictUser(user) for user in users ]
    self.SendJson(r)

class UserSigninHandler(RestHandler):

  def post(self):
    r = json.loads(self.request.body)
    print('\n\n')
    print(r)
    print('\n\n')
    check = model.CheckUser(r['username'], r['password'])
    print check
    if check is not None:
      check_key = check.key.id()
      user = model.QueryUser(check_key)
      r = AsDictUser(user)
    else:
      r = {'userCheck': False}
    self.SendJson(r)


class UserIDQueryHandler(RestHandler):

  def post(self):
    r = json.loads(self.request.body)
    print('\n\n')
    print(r['user'])
    print('\n\n')
    user = model.QueryUser(int(r['user']))
    r = AsDictUser(user)
    self.SendJson(r)

class InsertCourseHandler(RestHandler):

  def post(self):
    r = json.loads(self.request.body)
    course = model.InsertCourse(r['crn'], r['name'])
    model.UpdateUser(r['id'], course)
    r = AsDictCourse(course.get())
    self.SendJson(r)

APP = webapp2.WSGIApplication([
    ('/rest/query', QueryHandler),
    ('/rest/insert', InsertMessageHandler),
    ('/rest/delete', DeleteHandler),
    ('/rest/update', UpdateHandler),
    ('/rest/message/<course>', QueryCourseMessageHandler),
    ('/rest/insert_user', InsertUserHandler),
    ('/rest/query-user', UserQueryHandler),
    ('/rest/user-signin', UserSigninHandler),
    ('/rest/query-user-id', UserIDQueryHandler),
    ('/rest/query-course-msg', QueryCourseMessageHandler),
    ('/rest/insert_course', InsertCourseHandler),
], debug=True)


