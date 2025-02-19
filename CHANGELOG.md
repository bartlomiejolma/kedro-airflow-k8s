# Changelog

## [Unreleased]

## [0.5.2] - 2021-07-05

-   Support for Secrets in k8s
-   FIX: DeletePipelineStorageOperator was missing trigger rule 'all_done'

## [0.5.1] - 2021-05-17

-   Docker image added as a Mlflow run parameter (to support kedro inference pipeline)

## [0.5.0] - 2021-04-30

-   External dependencies can be added as optionals in configuration
-   Support for labels, tolerations and annotations in k8s
-   Logging added to operators

## [0.4.0] - 2021-04-20

-   Support of S3 as DAG destination
-   Operators extracted from DAG template as reusable components
-   Selection of specific pipeline by name from CLI

## [0.3.0] - 2021-04-15

-   Resources configuration added that allows describing cpu and memory resources required in k8s by pods
-   Shared persistent volume can be made optional
-   Pod startup timeout is configurable, with default to 600 seconds

## [0.2.0] - 2021-04-01

-   Command `list-pipelines` allows display of pipelines which were generated with the plugin
-   Command `ui` opens webbrowser with Apache Airflow
-   Move options to config file and restructure
-   `MLflow` enabled only if `kedro-mlflow` present in dependencies and configuration is in place 
-   Command `init` to initialize configuration for the plugin in kedro project

## [0.1.2] - 2021-03-24

-   Allow override `image` parameter from CLI for `upload_pipeline`, `run_once` and `compile`
-   Conditional SSL verification for Apache Airflow client, via AIRFLOW**CLIENT**SSL_VERIFY environment variable
-   `run-once` with `wait-for-completion` checks for task instance failure as well

## [0.1.1] - 2021-03-19

-   Inits temporary volume with data from image kedro data directory (/home/kedro/data)
-   Increased startup time for pods to 10 minutes

## [0.1.0] - 2021-03-17

-   Creates mlflow experiment on pipeline start if it does not exist
-   Temporary persistent volumes generation and removal for pipelines
-   `upload-pipeline` command that generates DAG to Airflow directory 
-   `schedule` command that generates DAG to Airflow directory with the given schedule
-   `run-once` command that uploads pipeline to Airflow and creates the DAG run

## [0.0.4] - 2021-03-10

### Fixed

-   Added DAG template to package manifest

## [0.0.3] - 2021-03-09

### Fixed

-   Drop dependency on `airflow`

## [0.0.2] - 2021-03-09

### Added

-   Initial implementation of `kedro_airflow_k8s` plugin stub. 

[Unreleased]: https://github.com/getindata/kedro-airflow-k8s/compare/0.5.2...HEAD

[0.5.2]: https://github.com/getindata/kedro-airflow-k8s/compare/0.5.1...0.5.2

[0.5.1]: https://github.com/getindata/kedro-airflow-k8s/compare/0.5.0...0.5.1

[0.5.0]: https://github.com/getindata/kedro-airflow-k8s/compare/0.4.0...0.5.0

[0.4.0]: https://github.com/getindata/kedro-airflow-k8s/compare/0.3.0...0.4.0

[0.3.0]: https://github.com/getindata/kedro-airflow-k8s/compare/0.2.0...0.3.0

[0.2.0]: https://github.com/getindata/kedro-airflow-k8s/compare/0.1.2...0.2.0

[0.1.2]: https://github.com/getindata/kedro-airflow-k8s/compare/0.1.1...0.1.2

[0.1.1]: https://github.com/getindata/kedro-airflow-k8s/compare/0.1.0...0.1.1

[0.1.0]: https://github.com/getindata/kedro-airflow-k8s/compare/0.0.4...0.1.0

[0.0.4]: https://github.com/getindata/kedro-airflow-k8s/compare/0.0.3...0.0.4

[0.0.3]: https://github.com/getindata/kedro-airflow-k8s/compare/0.0.2...0.0.3

[0.0.2]: https://github.com/getindata/kedro-airflow-k8s/compare/8f15485216cb040626b491d21e1b61eb3996be73...0.0.2
