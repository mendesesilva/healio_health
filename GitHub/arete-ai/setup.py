from setuptools import setup, find_packages

setup(
    name='arete-ai',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'google-cloud-speech==2.10.0',
        'google-cloud-language==2.0.0',
        'google-cloud-storage==2.6.0',
        'google-cloud-functions==1.4.0',
        'google-cloud-pubsub==2.10.0',
        'google-cloud-firestore==2.5.0',
        'google-cloud-scheduler==1.6.0',
        'google-cloud-logging==3.0.0',
        'google-cloud-monitoring==2.9.0',
        'spacy==3.5.0',
        'medcat==1.1.0',
        'textblob==0.17.1',
        'networkx==2.6.3',
        'umap-learn==0.5.2',
        'scikit-learn==1.1.2',
        'pandas==1.5.3',
        'numpy==1.23.5',
        'requests==2.28.2',
        'python-dotenv==0.21.1',
        'sqlalchemy==1.4.46',
        'pytest==7.1.3',
        'flake8==5.0.4',
        'click==8.1.3',
        'openai==0.5.0'
    ],
    entry_points={
        'console_scripts': [
            'arete-ai=src.main:main',
        ],
    },
)
