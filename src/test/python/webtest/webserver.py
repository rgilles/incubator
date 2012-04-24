#
# Copyright 2012 Romain Gilles
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import argparse

DEFAULT_PORT_NUMBER = 8080

__author__ = 'Romain Gilles'


from bottle import get, run

@get('/hello/<name>')
def index(name='World'):
    return '<b>Hello %s!</b>' % name

def start(port=DEFAULT_PORT_NUMBER):
    run(host='localhost', port=port, quiet=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Launch integrassion web server.')
    parser.add_argument('-p', '--port', help="Specifies a custom port number for the HTTP server (which defaults to {0}). ".format(DEFAULT_PORT_NUMBER), default =DEFAULT_PORT_NUMBER)
    args = parser.parse_args()
    start(args.port)