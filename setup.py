import setuptools

DEPENDENCIES = [
    'coverage==4.5.4',
    'nose==1.3.7'
]

EXTRA_DEPENDENCIES = {
    "avro": ["fastavro==0.22.7"],
    "gcloud": ["google-cloud-storage==1.23.0"],
    "all": ["fastavro==0.22.7", "google-cloud-storage==1.23.0"]
}

setuptools.setup(
    name='UDASwissKnife',
    version='0.3.0',
    description='Utils and common libraries for Python',
    author='UDARealState Data engineering Team',
    url='https://bitbucket.org/udanalytics/swissknife',
    install_requires=DEPENDENCIES,
    packages=setuptools.find_packages(),
    test_suite="nose.collector",
    python_requires=">=3.6",
    extras_require=EXTRA_DEPENDENCIES,
    classifiers=[
        "License :: OSI Approved :: MIT License"
    ]
)