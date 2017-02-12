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
import cgi
from helpers import valid_username, valid_password, valid_vpassword, valid_email

edit_header ="""
<!DOCTYPE html>
<html>
<head>
    <title>{}</title>
</head>
<body>
    <h3>{}{}</h3>
"""

# html boilerplate for the bottom of every page
page_footer = """
</body>
</html>
"""

signup_form = """
<form action="/welcome" method="post">
<table>
    <tr>
        <td><label>Username</td>
                <td><input type="text" name="username" value="%(username)s"/></td>
        </label>
        <td><div style="color:red">{}</div><td>
    </tr>
    <tr>    
        <td><label>Password</td>
            <td><input type="password" name="password" value="%(password)s"/></td>
        </label>
        <td><div style="color:red">{}</div><td>
    </tr>
    <tr>
        <td><label>Verify</td>
            <td><input type="password" name="vpassword" value="%(vpassword)s"/></td>
        </label>
        <td><div style="color:red">{}</div><td>
    </tr>
    <tr>
        <td><label>Email</td>
            <td><input type="text" name="email" value="%(email)s"/></td>
        </label>
        <td><div style="color:red">{}</div><td>
    </tr>
</table>      
    <input type="submit" value="Submit"/>
</form>
"""
class Index(webapp2.RequestHandler):
    """ Handles requests coming in to '/' (the root of our site)
        e.g. www.flicklist.com/
    """
    def write_form(self, error="",username="",password="",vpassword="",email=""):
        form=self.response.write(signup_form.replace("{}", "")%{
                                    "username":username,
                                    "password":password,
                                    "vpassword":vpassword,
                                    "email":email})
        return form
        

    def get(self):
        self.response.write(edit_header.format("Sign me up!", "Sign me up", ""))
        self.write_form()
        self.response.write(page_footer)

class InputHandler(webapp2.RequestHandler):   
    def post(self):
        user_name=self.request.get('username')
        user_pass=self.request.get('password')
        user_vpass=self.request.get('vpassword')
        user_email=self.request.get('email')
        username=valid_username(user_name)
        password=valid_password(user_pass)
        vpassword=valid_vpassword(user_pass, user_vpass)
        email=valid_email(user_email)
        


        if not(username and password and vpassword and email):
            if len(user_name)==0:
                username="please type in a username"
            if not username:
                username="invalid username"
            else:
                username=""
            if not password:
                password="invalid password"
            else:
                password=""
            if not vpassword:
                vpassword="the passwords don't match"
            else:
                vpassword=""
            if not email:
                email="invalid email address"
            else: 
                email=""
            #inserts errors
            error=(signup_form.format(username,password,
                                     vpassword,
                                     email))
            #returns the form as it is 
            error_final=error%{
                               "username":user_name,
                               "password":user_pass,
                               "vpassword":user_vpass,
                               "email":user_email}
            self.response.write(error_final)
        else:
            self.response.write(edit_header.format("Congratulations!","Welcome ", user_name+"!"))
            

app = webapp2.WSGIApplication([
    ('/', Index),
    ('/welcome', InputHandler)
], debug=True)
