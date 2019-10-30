import setuptools

from sphinx.setup_command import BuildDoc

cmdclass = {"build_sphinx": BuildDoc}

BUILD_DEPENDENCIES = [
    "nose",
    "sphinx",

]



setuptools.setup(
    name='SwissKnife',
    version='0.1',
    description='Utils and common libraries for Python',
    author='UDARealState Data engineering Team',
    url='https://bitbucket.org/udanalytics/swissknife',
    cmdclass={"build_sphinx": BuildDoc},
    setup_requires=BUILD_DEPENDENCIES,
    packages=setuptools.find_packages(),
    test_suite="nose.collector"
)