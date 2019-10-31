import setuptools

DEPENDENCIES = [
    'coverage',
    'nose'
]

setuptools.setup(
    name='SwissKnife',
    version='0.1',
    description='Utils and common libraries for Python',
    author='UDARealState Data engineering Team',
    url='https://bitbucket.org/udanalytics/swissknife',
    install_requires=DEPENDENCIES,
    packages=setuptools.find_packages(),
    test_suite="nose.collector"
)