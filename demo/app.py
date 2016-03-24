from __future__ import absolute_import
# encoding: UTF-8
import os
import functools
import jinja2
import six
from bottle import route, run
from tml import configure, build_context
from tml.session_vars import get_current_context
from tml.api.client import Client

path = os.path.abspath(os.path.dirname(__file__))


def init_tml(locale, source):
    tml_settings = {
        'environment': 'dev',
        'application': {'key': '998ec7b63f1fb763f698fe0bd02d46f0e601af7e743ab5d46139560273704957'},
        'logger': {'path': os.path.join(path, 'logs', 'tml.log')}
    }
    config = configure(**tml_settings)
    client = Client(key=tml_settings['application']['key'])
    context = get_current_context()
    if not context:
        context = build_context(
            locale=locale,
            source=source,  # todo:
            client=client)
    return context


def tr(label, data=None, description=None, options=None):
    context = init_tml('en', 'index')
    return context.tr(label, data, description, options)


def view(template_name):
    def decorator(view_func):
        @functools.wraps(view_func)
        def wrapper(*args, **kwargs):
            response = view_func(*args, **kwargs)

            if isinstance(response, dict):
                template = env.get_or_select_template(template_name)
                return template.render(**response)
            else:
                return response

        return wrapper

    return decorator


class FakeUser(object):

    first_name = 'Tom'
    last_name = 'Anderson'
    gender = 'male'

    def __init__(self, **kwargs):
        for k, v in six.iteritems(kwargs):
            setattr(self, k, v)

    def __str__(self):
        return self.first_name + " " + self.last_name


@route('/', name='home')
@view('home.html')
def home():
    users = {
        'michael': FakeUser(**{'gender': 'male', 'first_name': 'Michael', 'last_name': 'Berkovitch'}),
        'anna': FakeUser(**{'gender': 'female', 'first_name': 'Anna', 'last_name': 'Tusso'})
    }
    return {'title': 'Hello world', 'users': users}


env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(path, 'templates')),
    autoescape=True,)
env.add_extension('jinja2.ext.with_')
env.add_extension('tml_jinja2.ext.TMLExtension')
env.install_tr_callables(tr=tr)

if __name__ == '__main__':
    run(host='localhost', port=8000, debug=True, reloader=True)
