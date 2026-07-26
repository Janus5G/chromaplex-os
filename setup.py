from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="chromaplex-os",
    version="1.0.1",
    author="ChromaPlex OS Contributors",
    description="Krystalbaseret programmeringssprog med farve- og potenskodning",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Janus5G/chromaplex-os",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.14",
        "Topic :: Scientific/Engineering :: Physics",
        "Topic :: System :: Hardware",
    ],
    python_requires=">=3.9",
    install_requires=[
        "numpy>=1.20.0",
        "Pillow>=9.0.0",
    ],
    extras_require={
        "ai": ["openai>=1.0.0"],
        "test": ["pytest>=8.0.0,<9.0.0"],
    },
    entry_points={
        "console_scripts": [
            "chromaplex-ai = chromaplex.ai_coder:main",
            "cplc = chromaplex.cpl_compiler:main_compile",
            "cpl-run = chromaplex.cpl_compiler:main_run_cpl",
            "cpa-run = chromaplex.crystal_simulator:main_run_cpa",
            "bf2cpa = chromaplex.bf_compiler:main",
        ],
    },
)
