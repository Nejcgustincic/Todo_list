#!/usr/bin/env python
import os
import jinja2
import webapp2

from models import Task
template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        return self.render_template("hello.html")

class DodajHandler(BaseHandler):
    def get(self):
        return self.render_template("dodaj_task.html")
    
    def post(self):
        sporocilo = self.request.get("sporocilo")
        task = Task(sporocilo=sporocilo)
        task.put()
        return self.redirect_to("seznam")

class SeznamHandler(BaseHandler):
    def get(self):
        taski = Task.query(Task.je_izbrisan == False).fetch()

        params = {"taski":taski}

        return self.render_template("seznam.html", params=params)

class PosameznoHandler(BaseHandler):
    def get(self,task_id):
        task = Task.get_by_id(int(task_id))
        params = {"task":task}
        return self.render_template("task.html", params=params)
    def post(self,task_id):
        task = Task.get_by_id(int(task_id))
        if task.dokoncan == True:
            task.dokoncan = False
        else:
            task.dokoncan = True

        task.put()
        return self.redirect_to("seznam")

class EditHandler(BaseHandler):
    def get(self,task_id):
        task = Task.get_by_id(int(task_id))
        params = {"task":task}
        return self.render_template("uredi.html", params=params)

    def post(self,task_id):
        task = Task.get_by_id(int(task_id))
        task.sporocilo = self.request.get
        task.put()
        return self.redirect_to("seznam")
class DeleteHandler(BaseHandler):
    def get(self,task_id):
        task = Task.get_by_id(int(task_id))
        params = {"task": task}
        return self.render_template("izbrisi.html", params=params)
    def post(self,task_id):
        task = Task.get_by_id(int(task_id))
        task.je_izbrisan = True
        task.put()
        return self.redirect_to("seznam")

class OpravljeniHandler(BaseHandler):
    def get(self):
        taski = Task.query().fetch()

        params = {"taski":taski}

        return self.render_template("opravljeno.html", params=params)

class IzbrisanoHandler(BaseHandler):
    def get(self):
        task = Task.query(Task.je_izbrisan == True).fetch()
        params = {"task": task}
        return self.render_template("izbrisano.html", params=params)
    def post(self,task_id):
        task = Task.get_by_id(int(task_id))
        task.je_izbrisan = False
        task.put()
        return self.redirect_to("seznam")




app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler, name="glavna_stran"),
    webapp2.Route('/add_task', DodajHandler),
    webapp2.Route('/seznam', SeznamHandler, name="seznam"),
    webapp2.Route('/opravljeno',OpravljeniHandler),
    webapp2.Route('/seznam/<task_id:\d+>', PosameznoHandler),
    webapp2.Route('/seznam/<task_id:\d+>/edit', EditHandler),
    webapp2.Route('/seznam/<task_id:\d+>/delete', DeleteHandler),
    webapp2.Route('/izbrisano', IzbrisanoHandler),
], debug=True)
