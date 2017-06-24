#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import os
from google.appengine.ext import db
from google.appengine.ext.webapp import template


class Name(db.Model):
    first_name = db.StringProperty(required=True)
    last_name = db.StringProperty(required=True)


class MainHandler(webapp2.RequestHandler):

    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'templates/index.html')
        self.response.out.write(template.render(path, {}))

    def post(self):
        path = os.path.join(os.path.dirname(__file__), 'templates/form.html')
        self.response.out.write(template.render(path, {}))


class FormHandler(webapp2.RedirectHandler):

    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'templates/form.html')
        self.response.out.write(template.render(path, {}))

    def post(self):
        self.response.out.write('sent')

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/form.html', FormHandler)
], debug=True)


def main():
    app.run()

if __name__ == '__main__':
    main()