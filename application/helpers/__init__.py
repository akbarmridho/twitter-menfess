from .encryption import Encryption
from .filters import filter_messages
from .dates import utc_now, from_time, to_local
from os import path


def project_path(name: str = '') -> str:
    """
    Convert path relative to project folder to absolute path
    """
    basepath = path.dirname(__file__)
    return path.join(basepath, '../../{}'.format(name))
