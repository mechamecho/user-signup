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

# html boilerplate for the top of every page
page_header = """
<!DOCTYPE html>
<html>
<head>
    <title>FlickList</title>
</head>
<body>
    <h1>FlickList</h1>
"""

# html boilerplate for the bottom of every page
page_footer = """
</body>
</html>
"""

class Index(webapp2.RequestHandler):
    """ Handles requests coming in to '/' (the root of our site)
        e.g. www.flicklist.com/
    """

    def get(self):

        edit_header = "<h3>Sign me up</h3>"

        # a form for adding new movies
        signup_form = """
        <form action="/signup" method="post">
        <table>
        	<tr>
        		<td><label>Username</td>
                		<td><input type="text" name="username"/></td>
            		</label>
            </tr>
            	<td><label>Password</td>
                <td><input type="text" name="password"/></td>
            		</label>
        		<td><label>Verify Password</td>
                <td><input type="text" name="vpassword"/></td>
            		</label>
            	<td><label>Email</td>
                <td><input type="text" name="email"/></td>
            		</label>
        </table>           
            <input type="submit" value="Submit"/>
        </form>
        """
        page_content = edit_header + signup_form
        content = page_header + page_content + page_footer
        self.response.write(content)



class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello world!')

app = webapp2.WSGIApplication([
    ('/', Index)
], debug=True)
