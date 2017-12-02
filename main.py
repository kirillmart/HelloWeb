from pprint import pprint
from urllib.parse import parse_qs
from http.cookies import SimpleCookie
from shelve_utils import write_to_shelve, read_from_shelve


def square(a):
    return a * a


def to_int(n, default=0):
    try:
        return int(n)
    except ValueError:
        return default


def index(environ, start_response):
    params = parse_qs(environ.get("QUERY_STRING", ''))
    num = params.get("num")
    pprint(num)
    if not len(num):
        start_response('400 Bad Request', [('Content-Type', 'text/html')])
        return [b"error"]
    num = num[0]
    if not to_int(num):
        start_response('400 Bad Request', [('Content-Type', 'text/html')])
        return ["Invalid number: {}".format(num).encode()]
    response = "PARAMS: {}".format(square(to_int(num))).encode()
    start_response('200 OK', [('Content-Type', 'text/html')])
    return [response]


def set_cookie_test(environ, start_response):
    params = parse_qs(environ.get("QUERY_STRING", ''))
    name = params.get("name", ["no_name"])[0]
    age = params.get("age", ["no_age"])[0]
    # create a cookie object
    cookies = environ.get('HTTP_COOKIE', '')
    cookies = SimpleCookie(cookies)
    session_id = cookies["sessionid"].value
    data = {
        "name": name,
        "age": age,
    }
    write_to_shelve(session_id, data)
    headers = [('content-type', 'text/html')]
    start_response("200 OK", headers)
    return [b"COOKIE EXAMPLE"]


def read_cookie(environ, start_response):
    # create a cookie object
    cookies = environ.get('HTTP_COOKIE', '')
    parsed_cookies = SimpleCookie(cookies)
    session_id = parsed_cookies["sessionid"].value
    result = read_from_shelve(session_id)
    start_response("200 OK", [('content-type', 'text/html')])
    return [str(result).encode()]


def hello(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    return [b"NEW FUNCTION"]


def not_found(environ, start_response):
    start_response('404 Not Found', [('Content-Type', 'text/html')])
    response = b"Not Found, Invalid PATH_INFO"
    return [response]


def application(environ, start_response):
    path = environ.get('PATH_INFO', '').strip('/')
    urls = {
        "index": index,
        "hello": hello,
        "set-cookie": set_cookie_test,
        "read-cookie": read_cookie,
    }
    # import ipdb
    # ipdb.set_trace()
    return urls.get(path, not_found)(environ, start_response)


if __name__ == '__main__':
    print("starting server...")
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8081, application)
    srv.serve_forever()