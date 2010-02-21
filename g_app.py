from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
import render

class MainPage(webapp.RequestHandler):
    def get(self, test):
        self.response.headers['Content-Type'] = 'text/plain'
        #self.response.set_cookie('key', 'value', max_age=360, path='/')
        self.response.out.write('Hello, webapp World!\n')
        self.request.GET[u'foo'] = u'bar'
        self.response.out.write(test)


application = webapp.WSGIApplication([('/', render.MainPage), 
                                      ('/page/(\d+)/', render.MainPage), 
                                      ('/d/(\w+)/\w+/', render.Single), 
                                      ('/feed/', render.Feed), 
                                      ('/signin/', render.SignIn),
                                      ('/signout/', render.SignOut),
                                      ('/delete/(\w+)/(\d+)/', render.Delete),
                                      ('/like/', render.Like),
                                      ('/add-dedication/', render.AddDedication)], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
