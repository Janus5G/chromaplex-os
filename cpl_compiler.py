"""Bagudkompatibel wrapper.

Den autoritative compiler ligger i :mod:`chromaplex.cpl_compiler`.
"""

from chromaplex.cpl_compiler import compile_cpl, main_compile

__all__ = ["compile_cpl", "main_compile"]


if __name__ == "__main__":
    main_compile()
