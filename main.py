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
import string

edit_header ="""
<!DOCTYPE html>
<html>
<head>
    <title>%(title)s</title>
</head>
<body>
    <h3>%(header)s %(sechead)s</h3>
"""

# html boilerplate for the bottom of every page
page_footer = """
</body>
</html>
"""

signup_form = """
<form action="/" method="post">
<table>
    <tr>
        <td><label>Username</td>
                <td><input type="text" name="username" value=%(username)s></td>
        </label>
        <td><div style="color:red">%(username_err)s</div><td>
    </tr>
    <tr>    
        <td><label>Password</td>
            <td><input type="password" name="password"/></td>
        </label>
        <td><div style="color:red">%(password_err)s</div><td>
    </tr>
    <tr>
        <td><label>Verify</td>
            <td><input type="password" name="vpassword"/></td>
        </label>
        <td><div style="color:red">%(vpassword_err)s</div><td>
    </tr>
    <tr>
        <td><label>Email (not required)</td>
            <td><input type="text" name="email" value="%(email)s"/></td>
        </label>
        <td><div style="color:red">%(email_err)s</div><td>
    </tr>
</table>      
    <input type="submit" value="Submit"/>
</form>
"""
class Index(webapp2.RequestHandler):
    """ Handles requests coming in to '/' (the root of our site)
        e.g. www.flicklist.com/
    """
    def write_form(self,
                    title="Sign me up!",
                    header="Sign me up",
                    sechead="",
                    username="",
                    email="",
                    username_err="",
                    password_err="", 
                    vpassword_err="",
                    email_err=""):
        edited_header=edit_header%{"title":title,
                                    "header":header,
                                    "sechead":sechead 
                                    }
        signup_form_w_var=signup_form%{
                                    "username":username,
                                    "email":email, 
                                    "username_err":username_err, 
                                    "password_err":password_err, 
                                    "vpassword_err":vpassword_err,
                                    "email_err":email_err}
        whole_page=edited_header+signup_form_w_var+page_footer
        whole_page_written=self.response.write(whole_page)
        return whole_page
        

    def get(self):
        self.write_form()
        
        
   
    def post(self):
        user_name=cgi.escape(self.request.get('username'), quote=True)
        user_pass=cgi.escape(self.request.get('password'), quote=True)
        user_vpass=cgi.escape(self.request.get('vpassword'), quote=True)
        user_email=cgi.escape(self.request.get('email'), quote=True)
        username_err=""
        password_err=""
        vpassword_err=""
        email_err=""
     
        if not (valid_username(user_name) and
                valid_password(user_pass) and
                valid_vpassword(user_pass, user_vpass) and
                valid_email(user_email)):
            if len(user_name)==0:
                username_err="please type in a username"
            elif not valid_username(user_name):
                username_err="invalid username"
            if not valid_password(user_pass):
                password_err="invalid password"
            if not valid_vpassword(user_pass, user_vpass):
                vpassword_err="the passwords don't match"
            if not valid_email(user_email):
                email_err="invalid email address"
            self.write_form("Sign me up!","sign me up","",user_name, user_email,
                            username_err, password_err, vpassword_err, email_err )   

        else:
            self.redirect("/welcome?user_name=" + user_name)
        
            
            

class WelcomeHandler(webapp2.RequestHandler):
    def get(self):
        user_name=self.request.get("user_name")
        self.response.write(edit_header%{"title":"Congratulations!",
                                        "header":"Welcome", "sechead":user_name +"!"})

            

app = webapp2.WSGIApplication([
    ('/', Index),
    ('/welcome', WelcomeHandler)
], debug=True)