[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-v2.0%20adopted-ff69b4.svg)](code_of_conduct.md)


# SwissKnife

Hey! Welcome to `SwissKnife`, a set of tools and functionalities built by the Data Engineering team at [@uDATech](https://twitter.com/uDAtech).

This library is born from an urge of having a common repo to gather some functions that are widely used accross our tools.

Suggestions and contributions are more than welcome, always respecting our [Code of Conduct](./CODE_OF_CONDUCT.md).

## Installation guide

This repo is available to download via [PyPI](https://pypi.org/project/UDASwissKnife/) and it has different sets of functionalities that can be independently installed:

- **Basic** set:
  + Packages included:
    + `info`
  ```bash
  pip install UDASwissKnife
  ```

- **Extended** set:
  + Packages included:
    + `avro`
    + `gcloud`
  ```bash
  pip install UDASwissKnife[avro,gcloud]
  ```

- **Complete** set:
  + Includes both _Basic_ and _Extended_ sets
  ```bash
  pip install UDASwissKnife[all]
  ```

## Using the modules

### `info`
The main goal of this module is to identify the environment in which we are currently working. This is done thanks to an environment variable `$ENV` which contains the name of the working environment. The accepted case insensitive values of this working environment are:

The object `SwissKnife.info.CURRENT_ENVIRONMENT`, which is of type `ExecutionEnvironment`, an enum that contains the following entries:

- `PRO`
- `PRE`
- `TEST`
- `DEV` (default)

Then, it's possible to know the working environment using a set of methods which return a boolean indicating whether we are in that environment or not:

- `is_pro()`
- `is_pre()`
- `is_test()`
- `is_dev()`

It's also possible to obtain the working environment using object `SwissKnife.info.CURRENT_ENVIRONMENT`.

## Why is there a Dockerfile?

The one and only purpose of the `Dockerfile` is to execute the tests defined in the project. By building and running the Docker image, tests results will be printed in the terminal. If it's needed to save the result in a file, run:

```bash
sudo docker run swissknife:latest > nosetests.xml
```