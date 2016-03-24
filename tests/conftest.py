import pytest
import os
import six
from jinja2 import Environment, loaders
from tml import configure, build_context
from tml.session_vars import get_current_context
from tml.api.client import Client


@pytest.fixture
def here():
    return os.path.dirname(os.path.abspath(__file__))

@pytest.fixture
def file_loader(here):
    return loaders.FileSystemLoader(os.path.join(here, 'templates'))

@pytest.fixture
def env(file_loader):
    return Environment(
        loader=file_loader,
        autoescape=True)

@pytest.fixture
def env_with_ext(env):

    def _env_with_ext(ext):
        env.add_extension(ext)
        return env

    return _env_with_ext


def init_tml(here, locale, source):
    tml_settings = {
        'environment': 'dev',
        'application': {'key': '998ec7b63f1fb763f698fe0bd02d46f0e601af7e743ab5d46139560273704957'},
        'logger': {'path': os.path.join(here, 'logs', 'tml.log')}
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


@pytest.fixture
def tr(here):
    def _tr(label, data=None, description=None, options=None):
        context = init_tml(here, 'en', 'index')
        return context.tr(label, data, description, options)
    return _tr

@pytest.fixture
def testenv(env_with_ext, tr):
    env = env_with_ext("tml_jinja2.ext.TMLExtension")
    env.install_tr_callables(tr=tr)
    return env

@pytest.fixture
def fake_user():
    class FakeUser(object):

        first_name = 'Tom'
        last_name = 'Anderson'
        gender = 'male'

        def __init__(self, **kwargs):
            for k, v in six.iteritems(kwargs):
                setattr(self, k, v)

        def __str__(self):
            return self.first_name + " " + self.last_name
    return FakeUser