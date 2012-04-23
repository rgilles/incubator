#!/usr/bin/env python
from web import HTTP_METHODS, HTTP_GET, uri, request

__author__ = 'Romain Gilles'
import argparse

version='${version}'


def validate_method(method):
    return method in HTTP_METHODS

def main():
    parser = argparse.ArgumentParser(description='Process uri to create request.')
    parser.add_argument('--version', action='version', version='%(prog)s {0}'.format(version))
    parser.add_argument('uri', help="the uri where the request will be sent")
    parser.add_argument('-X', '--request', help="(HTTP) Specifies a custom request method to use when communicating with the HTTP server. The specified request will be used instead of the method otherwise used (which defaults to GET). Read the HTTP 1.1 specification for details and explanations. (Common additional HTTP requests include PUT and DELETE, but related technologies like WebDAV offers PROPFIND, COPY, MOVE and more). It can be: {0}".format(", ".join(HTTP_METHODS)), default = HTTP_GET)
    parser.add_argument('-G', '--get', action='store_true', help="Activate the get method")
    parser.add_argument('--put', action='store_true', help="Activate the put method")
    parser.add_argument('--post', action='store_true', help="Activate the post method")
    parser.add_argument('--del', action='store_true', help="Activate the delete method")
    parser.add_argument('--head', action='store_true', help="Activate the head method")
    args = parser.parse_args()
    target = uri(args.uri)
    if not validate_method(args.request):
        parser.error("invalid method name: {0}".format(args.request))

    response = request(target, args.request)
    print(str(response))

if __name__ == "__main__":
    main()