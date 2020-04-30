# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.5.0] - 2020-04-30
### Added
- Class `GCloudStorage` inside of module `gcloud`, used to upload files and strings to a gcloud bucket.
- `Makefile` to build and push the library to our PyPI repo.
### Changed
- Moved test_utils to a higher level folder, to allow access from any test class.

## [0.4.2] - 2020-04-29
### Changed
- Environmental variable `BUCKET_PATH` now is divided into `BUCKET_NAME` and `BUCKET_PATH_PREFIX` to distinguish the bucket name from an specific path inside that bucket.

## [0.4.1] - 2020-04-28
### Changed
- Bumped version to 0.4.1 to fix a version problem in PyPI.

## [0.4.0] - 2020-04-28
### Added
- Code of Conduct document.
- Issue templates.
- Contributor Covenant badge.
- Variable `BUCKET_PATH` used to identify the value of an environmental variable.
- Revamped tests to remove duplicated code.
### Changed
- Translated to English and updated `README.md`.
- Reduced complexity in some parts of the code.

## [0.3.2] - 2020-04-02
### Changed
- Changed project location to github.
- Removed inaccessible Jenkins pill.

## [0.3.1] - 2019-12-17
### Fixed
- Remove import of `logger` and added import of `logging` in `GCloudStreaming `.

## [0.3.0] - 2019-12-11
### Added
- Added `AvroWriter` class.
- Added `GCloudStreaming` class.
- Added **extras** requirements to install some dependencies.

## [0.2.0] - 2019-11-05
### Added
- Added **test** as execution environment.

## [0.1.1] - 2019-11-04
### Added
- Specific version of the project dependencies.
### Chang ed
- `ExecutionEnvironment` default value set to **DEV**.
- Fixed some typos in the code.
- Change package name to `UDASwissKnife` to avoid conflicts in pipy repository.

## [0.1.0] - 2019-10-31
### Added
- `ExecutionEnvironment` object.
- `CURRENT_ENVIRONMENT` variable (located in `SwissKnife.info.CURRENT_ENVIRONMENT`) that return a ExecutionEnvironment with the current environment setted.