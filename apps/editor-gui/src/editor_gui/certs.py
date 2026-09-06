"""Make TLS trust work in the packaged desktop app.

PyInstaller bundles the OpenSSL that Python was built against, and that OpenSSL carries the *build
machine's* trust-store location compiled in — for the macOS build,
``/Library/Frameworks/Python.framework/Versions/3.13/etc/openssl/cert.pem``. That path does not
exist on a user's machine, so ``ssl.create_default_context()`` loads zero CA certificates and every
``urllib`` HTTPS request fails with::

    [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate

``httpx`` call sites (the documentation downloader) are unaffected because httpx uses :mod:`certifi`
explicitly, which is why only the ``urllib`` ones broke: the MyKnx login, the update check and the
online catalog.

The app already ships a ``certifi`` bundle, so the fix is to point OpenSSL at it when — and only
when — it has nothing else to work with.
"""

from __future__ import annotations

import os
import ssl
from pathlib import Path


def ensure_ca_bundle() -> str | None:
    """Point OpenSSL at ``certifi`` when it has no usable trust store of its own.

    Returns the path installed into ``SSL_CERT_FILE``, or ``None`` when nothing needed changing
    (the normal case when running from source on a machine with system certificates).

    Call once, before the first HTTPS request. Cheap and safe to call unconditionally.
    """
    # `cafile`/`capath` are None unless the location actually exists on disk, and both already
    # account for the SSL_CERT_FILE / SSL_CERT_DIR overrides — so this one check covers a working
    # system store *and* an explicit override the user or a distro packager set deliberately.
    paths = ssl.get_default_verify_paths()
    if paths.cafile or paths.capath:
        return None

    try:
        import certifi
    except ImportError:  # not installed (source checkout without the GUI extras)
        return None

    bundle = certifi.where()
    if not Path(bundle).is_file():
        return None

    os.environ["SSL_CERT_FILE"] = bundle
    return bundle
