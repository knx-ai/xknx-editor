def test_import():
    from xknxmono.product import __version__

    assert __version__ is not None


def test_models_dependency():
    from xknxmono.models import __version__

    assert __version__ is not None
