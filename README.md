# Description 

The Inference Platform Control Plane is a standalone, scalable component responsible for managing the lifecycle of inference services, including creation, updates, and deletion.

# Build & Publish 

## Prerequisite 

You need to install the following utility locally 
- Docker

## Help

`make help`

## Build 

`make build`

## Run locally 

To be able to run locally, you need to install redis and override your local path (SRC_DB_MOUNT) in Makefile  

`make run-local`

## Push to AWS

To be able to push image to ECR public repo, create ECR repo first 
`aws ecr-public create-repository --repository-name <name> --region <region>`
Once repo, it created, update repo name and url in makefile and run the following 

`make push`

## Test Coverage 
| File | Stmts | Miss | Cover |
| ---  | ---   | ---  | --- |
| projects/demo/controlplane/cp/__init__.py                       | 0      | 0   | 100% | 
| projects/demo/controlplane/cp/exceptions/exceptions.py          | 7      | 1    | 86% |
| projects/demo/controlplane/cp/jobs/__init__.py                  | 0      | 0   | 100% |
| projects/demo/controlplane/cp/jobs/jobs.py                     | 30     | 10    | 67% |
| projects/demo/controlplane/cp/models/__init__.py                | 0      | 0   | 100% |
| projects/demo/controlplane/cp/models/db_handler.py             | 49     | 20    | 59% |
| projects/demo/controlplane/cp/models/model_deployments.py      | 56      | 3    | 95% |
| projects/demo/controlplane/cp/resps/resps.py                   | 10      | 3    | 70% |
| projects/demo/controlplane/cp/services/__init__.py              | 0      | 0   | 100% |
| projects/demo/controlplane/cp/services/svc.py                  | 30     | 17    | 43% |
| __init__.py                                                                    | 0      | 0  | 100% |
| test_db_handler.py                                                            | 14      | 0  | 100% |
| test_svc.py                                                                   | 27     | 10  |  63% |

Total: 71% 