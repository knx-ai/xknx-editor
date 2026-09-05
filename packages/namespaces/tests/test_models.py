import re


def test_import():
    from xknxeditor.namespaces import __version__

    assert __version__ is not None


def test_version_format():
    from xknxeditor.namespaces import __version__

    assert re.match(r"^\d+\.\d+\.\d+", __version__)
