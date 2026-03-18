import yamlbridge


def test_package_exposes_version():
    assert hasattr(yamlbridge, "__version__")
    assert isinstance(yamlbridge.__version__, str)
    assert yamlbridge.__version__