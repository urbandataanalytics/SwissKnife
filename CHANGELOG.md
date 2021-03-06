# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
## [0.9.0] - 2020-08-10
### Fixed
- GCloudStreaming now uses GCloudStorage object and supports 'bucket_prefix_path'.

## [0.8.2] - 2020-08-10
### Fixed
- Fixed (another) bug on GCloudStreaming class that raises an exception.

## [0.8.1] - 2020-08-10
### Fixed
- Fixed bug on GCloudStreaming class that raises an exception.

## [0.8.0] - 2020-07-30
### Added
- Added copy_blob function to GCloudStorage class.

## [0.7.1] - 2020-07-24
### Changed
- Refactor GCloudStorage to support generic bucket path, but it is compatible with previous functionality
### Added
- Generic split bucket path to support bucket as a parameter 

## [0.7.0] - 2020-06-22
### Added
- Added download_to_file to GCloudStorage
### Changed
- Changed and improved the behaviour of split_bucket_env.
- Add Exception to GCloudStorage if BUCKET_NAME is not defined.

## [0.6.4] - 2020-06-01
### Added 
- Added support to GCloudStorage for Google Storage objects metadata

## [0.6.3] - 2020-05-29
### Changed
- Improved `GCloudStorage.get_storage_complete_file_path` using `os.path.join`.
- `file_name` is optional in `GCloudStorage.get_storage_complete_file_path`.
### Fixed
- Now `GCloudStorage.list_blobs` can use the BUCKET_PREFIX_PATH. It has an optional param "with_prefix" (True by default). <issue #11>

## [0.6.2] - 2020-05-28
#### Added
- Added a calendar function to get weeks numbers with format `2020W02`

## [0.6.0] - 2020-05-07
### Added
- Incubating AvroTransformer in SwissKnife 

## [0.5.3] - 2020-05-05
### Changed
- Modified `ExecutionEnvironment` Enum so that it is JSON serializable (Issue #8)

## [0.5.2] - 2020-04-30
### Changed
- Fixed bug which caused GCloudStreaming files to have twice the bucket prefix.

## [0.5.1] - 2020-04-30
### Added
- Add option to prepend "gs://" to storage paths
-  Modified `GCloudStreaming` to automatically detect bucket name 
### Changed
- Fixed incorrect variable name in GCloudStorage class
- Fixed wrong reference to logger
- Allow empty paths when building storage paths

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
