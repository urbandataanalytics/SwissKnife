import setuptools

BUILD_DEPENDENCIES = [
    "nose"
]



setuptools.setup(
    name='SwissKnife',
    version='0.1',
    description='Utils and common libraries for Python',
    author='UDARealState Data engineering Team',
    url='https://bitbucket.org/udanalytics/swissknife',
    setup_requires=BUILD_DEPENDENCIES,
    packages=setuptools.find_packages(),
    test_suite="nose.collector"
)