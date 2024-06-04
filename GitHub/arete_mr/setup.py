from setuptools import setup, find_packages

setup(
    name='arete_mr',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'google-cloud-speech',
        'openai',
        'languagetool-python',
        'google-cloud-language',
        'google-cloud-storage',
        'google-cloud-functions',
        'pandas',
        'numpy',
        'flask',
        'requests',
        'spacy'
    ],
    entry_points={
        'console_scripts': [
            'arete_mr=src.main:main',
        ],
    },
    python_requires='>=3.7',
)
