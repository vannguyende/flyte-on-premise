## 1. Setup a project
* Prerequisites: make sure you have git and python >=3.7

Step 1: Create virtual environment

    python -m venv ~/venvs/flyte
    source ~/venvs/flyte/bin/activate
Step 2: Instal flytekit on it.

    pip install flytekit
Step 3: create project

    pyflyte  init  <project_name>
Then, the project directory will be created with a sample workflow. More instructions can be found in [this link](https://docs.flyte.org/projects/cookbook/en/stable/auto/larger_apps/larger_apps_setup.html)

## 2. Register workflow
Step 1: Build image

    ./docker_build_and_tag.sh -a <image_name> -r <docker_registry> -v <version>

*example: ./docker_build_and_tag.sh -a flyte-example-pyspark-pi -r ghcr.io/vannguyengalaxy -v v1*

Step 2: Package workflow

    pyflyte --pkgs flyte.workflows package --image "<image_name>:<version>"

*example: pyflyte --pkgs flyte.workflows package --image "ghcr.io/vannguyengalaxy/flyte-hudi-query:v1"*

Step 3: Push image to docker registry

    docker push <image_name>:<version>

step 4: Upload package to the Flyte backend *(Note: make sure the image publicly accessible)*


    flytectl register files --project <project_name> --domain <domain_name> --archive flyte-package.tgz --version <version>
  
  *example: flytectl register files --project flytesnacks --domain development --archive flyte-package.tgz --version v1*

## 3. scheduler workflow
reference: [read in more detail](https://docs.flyte.org/projects/cookbook/en/stable/auto/core/scheduled_workflows/lp_schedules.html#fixed-rate-intervals)


## 4. Troubleshooting
### 4.1. scheduler workflow on flyte sandbox on local
Scheduler pod can not be pre-installed in localy Flyte Sandbox, so we can manual install scheduler pod to run scheduler job.
Step 1: adding below config to [values-sandbox.yml](https://github.com/flyteorg/flyte/blob/master/charts/flyte-core/values-sandbox.yaml)

    workflow_scheduler:
      enabled: true
      type: native

Step 2: upgrade helm 

    helm upgrade -f values-sandbox.yaml flyte-core flyte/flyte-core --version v1.0.2 -n flyte


