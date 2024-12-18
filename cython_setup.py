from setuptools import setup
from Cython.Build import cythonize

setup(
    ext_modules=cythonize(
        "mod_installer.py",
        nthreads=4,
        compiler_directives={
            "language_level": "3",       # Уровень языка Python
            "boundscheck": True,         # Проверка границ массивов
            "wraparound": False,         # Отключить поддержку отрицательных индексов
            "cdivision": True            # Использовать целочисленное деление C
        },
        annotate=True                    # Создать HTML-аннотации производительности
    )
)
