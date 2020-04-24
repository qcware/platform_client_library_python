from qcware.config import qcware_api_key, qcware_host, set_api_key, set_host, is_valid_host_url, ConfigurationError
from decouple import config, UndefinedValueError
import pytest
import os

@pytest.fixture(autouse = True)
def wrap_tests():
    old_key = os.environ.pop('QCWARE_API_KEY', None)
    old_host = os.environ.pop('QCWARE_HOST', None)

    yield

    if old_key is not None:
        os.environ['QCWARE_API_KEY'] = old_key
    if old_host is not None:
        os.environ['QCWARE_HOST'] = old_host

# these tests should be run with no configuration; this doesn't check
# for a config file at the moment
def test_undefined_config():
    with pytest.raises(UndefinedValueError):
        config('QCWARE_API_KEY')
        config('QCWARE_HOST')
        

def test_qcware_host():
    assert qcware_host() == "https://api.forge.qcware.com"
    assert qcware_host('https://api.hammer.qcware.com') == "https://api.hammer.qcware.com"

    # test setting host via environment variable
    os.environ['QCWARE_HOST'] = 'https://api.anvil.qcware.com'
    assert qcware_host() == 'https://api.anvil.qcware.com'

    # test host resets to default when environment variable cleared
    del os.environ['QCWARE_HOST']
    assert qcware_host() == "https://api.forge.qcware.com"

    # test for configuration errors on invalid urls
    with pytest.raises(ConfigurationError):
        qcware_host('api.forge.qcware.com')
    with pytest.raises(ConfigurationError):
        qcware_host('https://api.forge.qcware.com/')


def test_qcware_api_key():
    with pytest.raises(ConfigurationError):
        assert qcware_api_key() == "bob"
    assert qcware_api_key("test") == "test"

    # test setting host via environment variable
    os.environ['QCWARE_API_KEY'] = 'test_key'
    assert qcware_api_key() == 'test_key'

    # test host resets to default (empty) when environment variable cleared
    del os.environ['QCWARE_API_KEY']
    with pytest.raises(ConfigurationError):
        assert qcware_api_key() == "bob"

    
