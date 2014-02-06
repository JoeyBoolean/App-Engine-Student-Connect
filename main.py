import json
import webapp2
import time

import model


def AsDict(message):
  return {'id': message.key.id(), 'first': message.first, 'last': message.last, 'msg': message.msg}


class RestHandler(webapp2.RequestHandler):

  def dispatch(self):
    #time.sleep(1)
    super(RestHandler, self).dispatch()


  def SendJson(self, r):
    self.response.headers['content-type'] = 'text/plain'
    self.response.write(json.dumps(r))
    

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


class InsertHandler(RestHandler):

  def post(self):
    r = json.loads(self.request.body)
    message = model.InsertMessage(r['first'], r['last'], r['msg'])
    r = AsDict(message)
    self.SendJson(r)

class DeleteHandler(RestHandler):


  def post(self):
    r = json.loads(self.request.body)
    model.DeleteMessage(r['id'])


APP = webapp2.WSGIApplication([
    ('/rest/query', QueryHandler),
    ('/rest/insert', InsertHandler),
    ('/rest/delete', DeleteHandler),
    ('/rest/update', UpdateHandler),
], debug=True)


