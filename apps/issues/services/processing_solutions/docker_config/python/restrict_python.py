import types

safe_modules = [
    "math",
    "random",
    "datetime",
    "string",
    "collections",
    "re",
    "functools",
    "itertools",
    "usercustomize",
    "builtins",
]


def restrict_functions() -> None:
    """Wrap builtin functions in runtime.

    Implemented by using docs: https://docs.python.org/3/library/site.html

    """
    import builtins

    builtins.eval = lambda *args, **kwargs: (_ for _ in ()).throw(
        ImportError("Function 'eval' is restricted"),
    )
    builtins.exec = lambda *args, **kwargs: (_ for _ in ()).throw(
        ImportError("Function 'exec' is restricted"),
    )
    builtins.open = lambda *args, **kwargs: (_ for _ in ()).throw(
        ImportError("Function 'open' is restricted"),
    )
    builtins.compile = lambda *args, **kwargs: (_ for _ in ()).throw(
        ImportError("Function 'compile' is restricted"),
    )


def restrict_modules() -> types.ModuleType:
    """Wrap import in runtime.

    Implemented by using docs: https://docs.python.org/3/library/site.html

    """
    import builtins

    original_import = builtins.__import__

    def custom_import(module_name: str, *args: str) -> types.ModuleType:
        """Wrap import with custom logic."""
        if module_name not in safe_modules:
            raise ImportError(f"No such available module '{module_name}'.")
        return original_import(module_name, *args)

    builtins.__import__ = custom_import


restrict_modules()
restrict_functions()
