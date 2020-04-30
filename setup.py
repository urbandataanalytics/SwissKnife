import setuptools
from os import path

DEPENDENCIES = [
    'coverage==4.5.4',
    'nose==1.3.7'
]

EXTRA_DEPENDENCIES = {
    "avro": ["fastavro==0.22.7"],
    "gcloud": ["google-cloud-storage==1.23.0"],
    "all": ["fastavro==0.22.7", "google-cloud-storage==1.23.0"]
}

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name='UDASwissKnife',
    version='0.5.0',
    description='Utils and common libraries for Python',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='UDARealState Data engineering Team',
    url='https://github.com/urbandataanalytics/SwissKnife',
    install_requires=DEPENDENCIES,
    packages=setuptools.find_packages(),
    test_suite="nose.collector",
    python_requires=">=3.6",
    extras_require=EXTRA_DEPENDENCIES,
    classifiers=[
        "License :: OSI Approved :: MIT License"
    ]
)