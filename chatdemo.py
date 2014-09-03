#!/usr/bin/env python
## -*- coding: utf-8 -*-
# Copyright 2009 Facebook
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
"""Simplified chat demo for websockets.

Authentication, error handling, etc are left as an exercise for the reader :)
"""

import logging
import tornado.escape
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.websocket
import os.path
import time
import uuid

from tornado.options import define, options

define("port", default=8880, help="run on the given port", type=int)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/chat", ChatHandler),
            (r"/chatsocket", ChatSocketHandler),
            #(r"/new", MainNewHandler),
            #(r"/chat", MainHandlerLogin),
            #(r"/login", LoginHandler),
        ]
        settings = dict(
            cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=True,
        )
        tornado.web.Application.__init__(self, handlers, **settings)

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")

# class MainHandlerLogin(BaseHandler):
#     def get(self):
#         if not self.current_user:
#             self.redirect("/login")
#             return
#         name = tornado.escape.xhtml_escape(self.current_user)
#         self.write("Hello, " + name)

# class LoginHandler(BaseHandler):
#     def get(self):
#         self.write('<html><body><form action="/login" method="post">'
#                    'Name: <input type="text" name="name">'
#                    '<input type="submit" value="Sign in">'
#                    '</form></body></html>')
#
#     def post(self):
#         self.set_secure_cookie("user", self.get_argument("name"))
#         self.redirect("/chat")

class MainHandler(BaseHandler):

    data_page = {'validator_name':False}
    timer = time.time()

    def get(self):
            self.render("index.html",data_page={'validator_name':False})

    def post(self):

        user_name = self.get_argument("name")
        #self.argument
        # if self.get_secure_cookie("user")==user_name:
        #     self.render("chat.html")
        #     return True

        #print filter(self.validate_user_name(self.get_argument("name")), ChatSocketHandler.user_list)
        if self.validate_user_name(user_name):
            self.set_secure_cookie("user", user_name)
            self.redirect("/chat")
            self.redirect("/chat")
        else:
            self.clear_cookie("user")
            self.render("index.html",data_page={'validator_name':"Имя уже занято",'post_name':user_name})
        #ChatSocketHandler.user_list.append({'user_name': self.get_argument("name")})
        #print ChatSocketHandler.user_list
        #print ChatSocketHandler.user_list1vxcvfd
        #self.render("chat.html")

    def validate_user_name(self,validate_user):
        for user in ChatSocketHandler.user_list:
            if validate_user in user["user"]:
                return False
        return True
        # def _validate_user_name(user_list):
        #     if validte_user in user_list['user']:
        #         return True
        # return _validate_user_name

class ChatHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        if not self.current_user:
            self.redirect("/")
        else:
            self.render("chat.html")


# class ChatHandler():
#     def get(self):
#         self.render("chat.html")

#class MainHandler(tornado.web.RequestHandler):
#    def get(self):
#        self.render("index.html", messages=ChatSocketHandler.cache)

# class MainNewHandler(BaseHandler):
#     def get(self):
#         self.render("index_new.html", messages=ChatSocketHandler.cache)

class ChatSocketHandler(tornado.websocket.WebSocketHandler):
     waiters = set()
     cache = []
     cache_size = 200
     user_list = [{'user':'fr1'},{'user':'ft1'}]

     user_list1 = [{'socket':10,
              'groups': ['all', 'some group']},
             {'socket': 20,
              'groups': ['other group']}]


# class ChatSocketHandler(tornado.websocket.WebSocketHandler):
#     waiters = set()
#     cache = []
#     cache_size = 200
#
#     def open(self):
#         logging.info("got message %r", self)
#         ChatSocketHandler.waiters.add(self)
#
#     def on_close(self):
#         ChatSocketHandler.waiters.remove(self)
#
#     @classmethod
#     def update_cache(cls, chat):
#         cls.cache.append(chat)
#         if len(cls.cache) > cls.cache_size:
#             cls.cache = cls.cache[-cls.cache_size:]
#
#     @classmethod
#     def send_updates(cls, chat):
#         logging.info("sending message to %d waiters", len(cls.waiters))
#         for waiter in cls.waiters:
#             try:
#                 waiter.write_message(chat)
#             except:
#                 logging.error("Error sending message", exc_info=True)
#
#     def on_message(self, message):
#         logging.info("got message %r", self)
#         parsed = tornado.escape.json_decode(message)
#
#         logging.info("message chat %r", parsed["body"])
#         chat = {
#             "id": str(uuid.uuid4()),
#             "body": parsed["body"],
#             }
#         chat["html"] = tornado.escape.to_basestring(
#             self.render_string("message.html", message=chat))
#
#         ChatSocketHandler.update_cache(chat)
#         ChatSocketHandler.send_updates(chat)


def main():
    tornado.options.parse_command_line()
    app = Application()
    app.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
