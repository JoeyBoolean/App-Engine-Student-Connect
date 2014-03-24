import json
import webapp2
import time

import model


def AsDict(message):
  return {'id': message.key.id(), 'first': message.first, 'last': message.last, 'msg': message.msg}

def AsDictUser(user):
  """ 
  course is a list in the user object
  """
  course_list = model.QueryCourse(user.courses)
  course_out = []
  for course in course_list:
    course_out.append({'crn': course.crn, 'name':course.name})
  return {'id': user.key.id(), 'first': user.first, 'last': user.last, 'course': course_out}

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

  def get(self, course):
    messages = model.CourseMessages(course)
    r = [ AsDict(message) for message in messages]
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
    message = model.InsertMessage(r['first'], r['last'], r['msg'])
    r = AsDict(message)
    self.SendJson(r)

class InsertUserHandler(RestHandler):

  def post(self):
    r = json.loads(self.request.body)
    course = model.AddCourseIfEmpty()
    user = model.InsertUser(r['first'], r['last'], course)
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
    ('/rest/insert_course', InsertCourseHandler),
], debug=True)


