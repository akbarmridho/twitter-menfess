from .encryption import Encryption, generate_decoded_hmac_hash, compare_digest
from .filters import filter_messages
from .dates import utc_now, from_time, to_local
from os import path

chiper = Encryption()


def project_path(name: str) -> str:
    """Convert path relative to project folder to absolute path

    Args:
        name: file/directory name relative to project path.

    Returns:
        str: absolute path
    """
    """
    
    """
    basepath = path.dirname(__file__)
    return path.join(basepath, '../../{}'.format(name))
