# coding-project-template
This repo is for the practice project which is to be based on Embedded AI libraries. 

## Task fulfilled

- Added SentimentAnalysis
- Altered sent_analyzer method to have standard error handling

## Alterations made

### Sentiment Analysis
- Make watson API endpoint configurable for integration testing
- Added Timeout for watson request
- Made Timeout configurable

### Server
- Moved server into own package for easier testing
- Added Unit tests for server
- Added POST response for HTML only form allowing no-js to work
- Made server port configurable
- Modified Javascript to setup events and prevent HTML submit
- Changed route for api method to have api prefix

## TODO
- Add mocked watson tests 
- Add Healthcheck
- Change Configuration setup to linux style config file & config.d folder
- Add CSRF token to form
- Change Watson usage to OpenAI compatible lib
- Add integration testing using test containers
- Add e2e testing using test containers
- Add Containerfile
- Add helm chart
- Add Knative HTTP scaler
- Add Logging integration
- Add CI/CD for code build/lint
- Add CI/CD for code dependency checks
- Add CI/CD for code unit testing
- Add CI/CD for code integration testing
- Add CI/CD for container build/lint
- Add CI/CD for container audit packages
- Add CI/CD for container integration testing
- Add CI/CD for apparmor profile generation
- Add CI/CD for seccomp profile
- Add CI/CD for helm build/lint
- Add CI/CD for helm unit testing
- Add CI/CD for minikube/kind setup

- Add CI/CD for helm integration testing
- Add CI/CD for helm unhardened e2e testing
- Add CI/CD for minikube/kind setup with hardened setup
- Add CI/CD for helm hardened e2e testing (Envoy Gateway/gvisor/networkpolicy)
- Add CI/CD for helm hardened e2e testing (Envoy Gateway/WAF/kata containers/cilium)
- Add CI/CD for helm simple load testing
- Add CI/CD for helm full load hardened testing
