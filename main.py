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
import re

USER_RE  = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

PASS_RE  = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
def valid_email(email):
    return not email or EMAIL_RE.match(email)

header="""
<!DOCTYPE html>
<html>
    <head>
        <title>Signup</title>
            <style type="text/css">
                .error{
                    color:red;
                }
            </style>
    </head>
    <body>
        <h1>Signup</h1>
    """
footer="""
    </body>
    </html>
    """

form = """
        <form method="post">
            <table>
                <tbody>
                    <tr>
                        <td>
                            <label for="username">Username</label>
                        </td>
                        <td>
                            <input name="username" type="text" required>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <label for="password">Password</label>
                        </td>
                        <td>
                            <input name="password" type="password" value required>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <label for="verify">Verify Password</label>
                        </td>
                        <td>
                            <input name="verify" type="password" value required>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <label for="email">Email (optional)</label>
                        </td>
                        <td>
                            <input name="email" type="email" value>
                        </td>
                    </tr>
                </tbody>
            </table>
            <input type="submit">
        </form>
                    """



class MainHandler(webapp2.RequestHandler):
    def get(self):

        content = header + form + footer
        self.response.write(content)

    def post(self):
        username  = self.request.get("username")
        password  = self.request.get("password")
        verify    = self.request.get("verify")
        email     = self.request.get("email")
        is_error = False

        if not valid_username(username):
            error = "<p> Please choose a valid username </p>"
            is_error = True

        if not valid_password(password):
            error = "<p> Please choose a valid password</p>"
            is_error = True
        elif password != verify:
            error = "<p> Passwords do not match. </p>"
            is_error = True

        if not valid_email(email):
            error = '<p> Please enter a valid email address </p>'
            is_error = True

        if is_error:
            content = header + form + error + footer
            self.response.out.write(error)
        else:
            self.redirect('/welcome?username=' + username)

class Welcome(webapp2.RequestHandler):
    def get(self):
        username = self.request.get("username")
        new_header='''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Signup</title>
            <style type="text/css">
                .error{
                    color:red;
                }
            </style>
        </head>
        <body>
            <h1>Welcome,
        ''' + username + '</h1>'

        new_footer= """
        </body>
        </html>
        """
        content = new_header + new_footer
        self.response.write(content)



app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/welcome', Welcome),
], debug=True)
