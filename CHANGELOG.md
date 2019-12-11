# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.3.0] - 2019-12-11
### Added
- Added AvroWriter class.
- Added GCloudStreaming class.
- Added **extras** requirements to install some dependencies.

## [0.2.0] - 2019-11-05
### Added
- Added **test** as execution environment.

## [0.1.1] - 2019-11-04
### Added
- Specific version of the project dependencies.
  
### Changed
- `ExecutionEnvironment` default value set to **DEV**.
- Fixed some typos in the code.
- Change package name to *UDASwissKnife* to avoid conflicts in pipy repository.
  

## [0.1.0] - 2019-10-31
### Added
- ExecutionEnvironment object.
- CURRENT_ENVIRONMENT variable (located in SwissKnife.info.CURRENT_ENVIRONMENT) that return a ExecutionEnvironment with the current environment setted.