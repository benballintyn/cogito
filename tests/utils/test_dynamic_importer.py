import pytest

from cogito.utils.dynamic_importer import (
    DynamicImporterError,
    import_attribute,
    import_module,
)


def test_import_module():
    os_module = import_module("os")
    assert os_module is not None
    assert hasattr(os_module, "path")


def test_import_attribute():
    join_function = import_attribute("os.path.join")
    assert join_function is not None
    assert callable(join_function)
    assert join_function("a", "b") == "a/b"


def test_import_nonexistent_module():
    with pytest.raises(DynamicImporterError, match="could not be imported"):
        import_module("nonexistent_module")


def test_import_nonexistent_attribute():
    with pytest.raises(DynamicImporterError, match="Attribute 'nonexistent' not found"):
        import_attribute("os.path.nonexistent")


def test_invalid_attribute_path():
    with pytest.raises(DynamicImporterError, match="Invalid attribute path"):
        import_attribute("invalidpath")
