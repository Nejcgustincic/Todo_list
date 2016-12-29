from google.appengine.ext import ndb

class Task(ndb.Model):
    sporocilo = ndb.StringProperty()
    dokoncan = ndb.BooleanProperty(default = False)
    cas_nastanka = ndb.DateTimeProperty(auto_now_add = True)
    je_izbrisan = ndb.BooleanProperty(default = False)
    avtor = ndb.StringProperty()

class Mail(ndb.Model):
    besedilo = ndb.StringProperty()
    avtor = ndb.StringProperty()
    naslovnik = ndb.StringProperty()