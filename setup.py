import setuptools

DEPENDENCIES = [
    'coverage==4.5.4',
    'nose==1.3.7'
]

setuptools.setup(
    name='UDASwissKnife',
    version='0.1.1',
    description='Utils and common libraries for Python',
    author='UDARealState Data engineering Team',
    url='https://bitbucket.org/udanalytics/swissknife',
    install_requires=DEPENDENCIES,
    packages=setuptools.find_packages(),
    test_suite="nose.collector",
    python_required=">=3.6"
)