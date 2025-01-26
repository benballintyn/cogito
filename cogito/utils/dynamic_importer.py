"""
Utilities for dynamic importing of modules and attributes.
"""

import importlib
from typing import Any


class DynamicImporterError(Exception):
    """Custom exception for dynamic importing errors."""

    pass


def import_module(module_path: str) -> Any:
    """
    Dynamically import a module given its module path.

    Args:
        module_path (str): The dotted path of the module to import (e.g., "os.path").

    Returns:
        module: The imported module.

    Raises:
        DynamicImporterError: If the module cannot be imported.
    """
    try:
        return importlib.import_module(module_path)
    except ModuleNotFoundError as e:
        raise DynamicImporterError(f"Module '{module_path}' could not be imported: {e}")


def import_attribute(attribute_path: str) -> Any:
    """
    Dynamically import an attribute (class, function, variable) from a module.

    Args:
        attribute_path (str): The dotted path of the attribute to import
                              (e.g., "os.path.join").

    Returns:
        Any: The imported attribute.

    Raises:
        DynamicImporterError: If the module or attribute cannot be imported.
    """
    try:
        module_path, attribute_name = attribute_path.rsplit(".", 1)
        module = importlib.import_module(module_path)
        return getattr(module, attribute_name)
    except (ModuleNotFoundError, ValueError) as e:
        raise DynamicImporterError(f"Invalid attribute path '{attribute_path}': {e}")
    except AttributeError as e:
        raise DynamicImporterError(
            f"Attribute '{attribute_name}' not found in module '{module_path}': {e}"
        )
