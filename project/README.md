# Apache-Flyte

## Usage (running with your Flyte project )

*** **prerequisites**: 

- [Configure local kubectl to connect to EKS](https://kerneltalks.com/commands/how-to-configure-kubectl-for-aws-eks/)
- Make sure the connection with flytectl CLI and kubectl is working. Run the following command:
 
   ` export FLYTE_PROJECT_PATH=<path-to-project-directory>`

    `$FLYTE_PROJECT_PATH/flytectl_connection.sh`


- Logged into a docker registry

Step 1: 

    source $FLYTE_PROJECT_PATH/venv/bin/activate

Step 2: Package workflow.


    $FLYTE_PROJECT_PATH/package_workflow.sh -i <IMAGE_NAME> -r <DOCKER_REGISTRY> -v <VERSION>

_example: $FLYTE_PROJECT_PATH/package_workflow.sh.sh -i spark-sql -r ghcr.io/vannguyengalaxy -v v1_

Step 3: Register workflow using local tgz file. (_note: the image in the docker registry need to have public access_)


    flytectl register files --config ~/.flyte/config.yaml  --project <PROJECT_NAME> --domain <DOMAIN_NAME> --archive flyte-package.tgz --version <VERSION>
    

_example: flytectl register files --config ~/.flyte/config.yaml  --project flytesnacks --domain development --archive flyte-package.tgz --version v1_

Step 4: Open Flyte UI and launch workflow


## NOTE

1. add dependences for test in local
 "spark.jars": "/home/ec2-user/flyte-test/flyte-project/jars/hadoop-aws-3.3.1.jar,"
               "/home/ec2-user/flyte-test/flyte-project/jars/aws-java-sdk-bundle-1.11.375.jar,"
               "/home/ec2-user/flyte-test/flyte-project/jars/hudi-spark3.2-bundle_2.12-0.11.0.jar",
2. if you run in local, you must set SPARK_LOCAL_IP=127.0.0.1. this connection to get jars dependences local file
