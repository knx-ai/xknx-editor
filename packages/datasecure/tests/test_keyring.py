def test_import():
    from xknxeditor.datasecure import __version__

    assert __version__ is not None


def test_models_dependency():
    from xknxeditor.namespaces import __version__

    assert __version__ is not None
