#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
import jinja2
import os
import random
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext.webapp import template


jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__) + "/templates"))

ghost_name_list = ['Betelgeuse', 'Bhoot', 'Bloody Mary', 'Bogle', 'Casper', 'Chindi', 'Cihuateteo', 'Clytemnestra',
                   'Draugr', 'Dybbuk', 'Gjenganger', u'Guĭ', 'Ibbur', 'Jima', 'Jinn', 'La Llorona',
                   'Moaning Myrtle', 'Mr. Boogedy', 'Nachzehrer', 'Blinky', 'Pinky', 'Inky', 'Clyde',
                   'Patrick Swayze', 'Phi Tai Hong', 'Pishacha', 'Poltergeist', 'Revenant', 'Ringwraith',
                   'Slender Man', 'Slimer', 'Space Ghost', 'Strigoi', 'Candyman', 'The Crypt Keeper',
                   'Headless Horseman', u'Tomás', 'Vetala', u'Wiedergänger', 'Xunantunich', u'Yūrei', 'Zhong Kui',
                   'Zuul']


class Name(db.Model):
    firstname = db.StringProperty()
    lastname = db.StringProperty()


class MainHandler(webapp2.RequestHandler):

    def get(self):
        user = users.get_current_user()

        if user:
            template_values = {
                'user': user,
                'is_admin': users.is_current_user_admin(),
                'logout_url': users.create_logout_url('/'),
                'names': ghost_name_list,
            }
            template = jinja_environment.get_template('index.html')
            self.response.out.write(template.render(template_values))

        else:
            template_values = {
                'login_url': users.create_login_url(self.request.url),
                'names': ghost_name_list
            }
            template = jinja_environment.get_template('index.html')
            self.response.out.write(template.render(template_values))

    def post(self):
        path = os.path.join(os.path.dirname(__file__), 'templates/form.html')
        self.response.out.write(template.render(path, {}))


class FormHandler(webapp2.RedirectHandler):

    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'templates/form.html')
        self.response.out.write(template.render(path, {}))

    def post(self):
        name = Name(firstname=self.request.get('first-name'), lastname=self.request.get('last-name'))
        name.put()
        path = os.path.join(os.path.dirname(__file__), 'templates/select-name.html')
        self.response.out.write(template.render(path, {}))


class NameSelect(webapp2.RedirectHandler):

    def get(self):
        name = db.GqlQuery('SELECT * FROM Name')
        template_values = {
            'firstname': name.firstname,
            'ghostname': random.choice(ghost_name_list),
            'lastname': name.lastname
        }
        template = jinja_environment.get_template('select-name.html')
        self.response.out.write(template.render(template_values))

    def post(self):
        pass


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/form.html', FormHandler)
], debug=True)


def main():
    app.run()

if __name__ == '__main__':
    main()
