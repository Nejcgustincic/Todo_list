#!/usr/bin/env python
import os
import jinja2
import webapp2
from google.appengine.api import users

from models import Task
from models import Mail
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
        user = users.get_current_user()
        if user:
            logout_url = users.create_login_url("/")
            params= {"user":user, "logout_url":logout_url}
            return self.render_template("hello.html",params=params)
        else:
            return self.redirect_to("login")

class OsnovaHandler(BaseHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            logout_url = users.create_login_url("/")
            params = {"user": user, "logout_url": logout_url}
            return self.render_template("base.html",params=params)
        else:
            return self.redirect_to("login")




class DodajHandler(BaseHandler):
    def get(self):
        user = users.get_current_user()
        logout_url = users.create_login_url("/")
        if user:
            params = {"user":user,"logout_url":logout_url}
            return self.render_template("dodaj_task.html",params=params)
        else:
            return self.redirect_to("login")
    
    def post(self):
        user = users.get_current_user()
        if user:

            ime = user.nickname()
            sporocilo = self.request.get("sporocilo")
            task = Task(sporocilo=sporocilo, avtor= ime)
            task.put()
            return self.redirect_to("seznam")
        else:
            return self.redirect_to("login")

class SeznamHandler(BaseHandler):
    def get(self):
        user = users.get_current_user()
        logout_url = users.create_login_url("/")
        if user:
            taski = Task.query(Task.je_izbrisan == False).fetch()

            params = {"taski":taski,"user":user,"logout_url":logout_url}

            return self.render_template("seznam.html", params=params)
        else:
            return self.redirect_to("login")

class PosameznoHandler(BaseHandler):
    def get(self,task_id):
        user = users.get_current_user()
        logout_url = users.create_login_url("/")
        task = Task.get_by_id(int(task_id))
        params = {"task":task,"user":user,"logout_url":logout_url}
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
        user = users.get_current_user()
        logout_url = users.create_login_url("/")
        task = Task.get_by_id(int(task_id))
        params = {"task":task,"user":user,"logout_url":logout_url}
        return self.render_template("uredi.html", params=params)

    def post(self,task_id):
        task = Task.get_by_id(int(task_id))
        task.sporocilo = self.request.get("text_taska")
        task.put()
        return self.redirect_to("seznam")
class DeleteHandler(BaseHandler):
    def get(self,task_id):
        user = users.get_current_user()
        logout_url = users.create_login_url("/")
        task = Task.get_by_id(int(task_id))
        params = {"task": task,"user":user,"logout_url":logout_url}
        return self.render_template("izbrisi.html", params=params)
    def post(self,task_id):
        task = Task.get_by_id(int(task_id))
        task.je_izbrisan = True
        task.put()
        return self.redirect_to("seznam")

class OpravljeniHandler(BaseHandler):
    def get(self):
        user = users.get_current_user()
        logout_url = users.create_login_url("/")
        if user:
            taski = Task.query().fetch()

            params = {"taski":taski,"user":user,"logout_url":logout_url}

            return self.render_template("opravljeno.html", params=params)
        else:
            return self.redirect_to("login")

class IzbrisanoHandler(BaseHandler):
    def get(self):
        user = users.get_current_user()
        logout_url = users.create_login_url("/")
        if user:
            task = Task.query(Task.je_izbrisan == True).fetch()
            params = {"task": task,"user":user,"logout_url":logout_url}
            return self.render_template("izbrisano.html", params=params)
        else:
            return self.redirect_to("login")

class ObnoviHandler(BaseHandler):
    def get(self, task_id):
        task = Task.get_by_id(int(task_id))
        params = {"task": task}
        return self.render_template("obnovi.html", params=params)
    def post(self,task_id):
        task = Task.get_by_id(int(task_id))
        task.je_izbrisan = False
        task.put()
        return self.redirect_to("seznam")

class TrajnoIzbrisi(BaseHandler):
    def get(self, task_id):
        task = Task.get_by_id(int(task_id))
        params = {"task": task}
        return self.render_template("trajno.html", params=params)
    def post(self,task_id):
        task = Task.get_by_id(int(task_id))
        task.key.delete()
        return self.redirect_to("izbrisano")


class LoginHandler(BaseHandler):
    def get(self):
        login_url = users.create_login_url("/")
        params = {"login_url": login_url}
        return self.render_template("login.html", params=params)
class MailHandler(BaseHandler):
    def get(self):
        user = users.get_current_user()
        logout_url = users.create_login_url("/")
        if user:
            params={"user":user,"logout_url":logout_url}
            return self.render_template("poslji-sporocilo.html",params=params)
        else:
            return self.redirect_to("login")

    def post(self):
        user = str(users.get_current_user())
        besedilo = self.request.get("sporocilo")
        naslovnik = self.request.get("naslovnik")
        sporocilo= Mail(besedilo=besedilo, avtor=user,naslovnik=naslovnik)
        sporocilo.put()
        return self.redirect_to("poslji")
class PrejetoHandler(BaseHandler):
    def get(self):
        logout_url = users.create_login_url("/")
        user = users.get_current_user()
        mail= Mail.query(Mail.naslovnik == user.email()).fetch()
        params = {"mail":mail,"user":user,"logout_url":logout_url}
        return self.render_template("prejeta-sporocila.html",params=params)

class PoslanoHandler(BaseHandler):
    def get(self):
        logout_url = users.create_login_url("/")
        user = users.get_current_user()
        mail= Mail.query(Mail.avtor == str(user)).fetch()
        params = {"mail":mail,"user":user,"logout_url":logout_url}
        return self.render_template("poslana-sporocila.html",params=params)


app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler, name="glavna_stran"),
    webapp2.Route('/login', LoginHandler, name="login"),
    webapp2.Route('/base', OsnovaHandler),
    webapp2.Route('/add_task', DodajHandler),
    webapp2.Route('/seznam', SeznamHandler, name="seznam"),
    webapp2.Route('/opravljeno',OpravljeniHandler),
    webapp2.Route('/seznam/<task_id:\d+>', PosameznoHandler),
    webapp2.Route('/seznam/<task_id:\d+>/edit', EditHandler),
    webapp2.Route('/seznam/<task_id:\d+>/delete', DeleteHandler),
    webapp2.Route('/izbrisano',IzbrisanoHandler, name ="izbrisano"),
    webapp2.Route('/izbrisano/<task_id:\d+>/obnovi', ObnoviHandler),
    webapp2.Route('/izbrisano/<task_id:\d+>/izbrisi', TrajnoIzbrisi),
    webapp2.Route('/poslji-sporocilo',MailHandler, name= "poslji"),
    webapp2.Route('/prejeto',PrejetoHandler),
    webapp2.Route('/poslano',PoslanoHandler),


], debug=True)
