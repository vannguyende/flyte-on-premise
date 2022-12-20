while getopts i:r:v: flag
do
    case "${flag}" in
        i) IMAGE_NAME=${OPTARG};;
        r) REGISTRY_NAME=${OPTARG};;
        v) VERSION=${OPTARG};;
    esac
done
rm -f $FLYTE_PROJECT_PATH/flyte-package.tgz
$(pwd)/docker_build_and_tag.sh -a $IMAGE_NAME -r $REGISTRY_NAME -v $VERSION
# set tag name
TAG="${REGISTRY_NAME}/${IMAGE_NAME}:${VERSION}"
echo $TAG

pyflyte --pkgs flyte.workflows package --image $TAG -f

# make sure docker login succeeded
# example: docker login -u vannguyengalaxy -p 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 ghcr.io
docker push $TAG