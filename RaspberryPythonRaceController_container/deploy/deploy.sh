#!/bin/bash

# Race Controller Deployment Script
set -e

# Configuration
REGION=${AWS_REGION:-us-east-1}
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
REPOSITORY_NAME="race-controller"
IMAGE_TAG=${IMAGE_TAG:-latest}
STACK_NAME="race-controller-stack"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}"
}

warn() {
    echo -e "${YELLOW}[$(date +'%Y-%m-%d %H:%M:%S')] WARNING: $1${NC}"
}

error() {
    echo -e "${RED}[$(date +'%Y-%m-%d %H:%M:%S')] ERROR: $1${NC}"
    exit 1
}

# Check prerequisites
check_prerequisites() {
    log "Checking prerequisites..."
    
    command -v aws >/dev/null 2>&1 || error "AWS CLI is required but not installed"
    command -v docker >/dev/null 2>&1 || error "Docker is required but not installed"
    
    aws sts get-caller-identity >/dev/null 2>&1 || error "AWS credentials not configured"
    
    log "Prerequisites check passed"
}

# Create ECR repository if it doesn't exist
create_ecr_repository() {
    log "Creating ECR repository if it doesn't exist..."
    
    aws ecr describe-repositories --repository-names $REPOSITORY_NAME --region $REGION >/dev/null 2>&1 || {
        log "Creating ECR repository: $REPOSITORY_NAME"
        aws ecr create-repository --repository-name $REPOSITORY_NAME --region $REGION
    }
    
    log "ECR repository ready"
}

# Build and push Docker image
build_and_push_image() {
    log "Building Docker image..."
    
    # Build image
    docker build -t $REPOSITORY_NAME:$IMAGE_TAG .
    
    # Tag for ECR
    ECR_URI="$ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/$REPOSITORY_NAME:$IMAGE_TAG"
    docker tag $REPOSITORY_NAME:$IMAGE_TAG $ECR_URI
    
    log "Logging into ECR..."
    aws ecr get-login-password --region $REGION | docker login --username AWS --password-stdin $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com
    
    log "Pushing image to ECR..."
    docker push $ECR_URI
    
    log "Image pushed successfully: $ECR_URI"
    echo $ECR_URI
}

# Deploy CloudFormation stack
deploy_stack() {
    local image_uri=$1
    
    log "Deploying CloudFormation stack..."
    
    # Get default VPC and subnets
    VPC_ID=$(aws ec2 describe-vpcs --filters "Name=is-default,Values=true" --query 'Vpcs[0].VpcId' --output text --region $REGION)
    SUBNET_IDS=$(aws ec2 describe-subnets --filters "Name=vpc-id,Values=$VPC_ID" --query 'Subnets[].SubnetId' --output text --region $REGION | tr '\t' ',')
    
    # Get IoT endpoint
    IOT_ENDPOINT=$(aws iot describe-endpoint --endpoint-type iot:Data-ATS --query 'endpointAddress' --output text --region $REGION)
    
    log "Using VPC: $VPC_ID"
    log "Using Subnets: $SUBNET_IDS"
    log "Using IoT Endpoint: $IOT_ENDPOINT"
    
    aws cloudformation deploy \
        --template-file deploy/cloudformation.yaml \
        --stack-name $STACK_NAME \
        --parameter-overrides \
            ImageUri=$image_uri \
            VpcId=$VPC_ID \
            SubnetIds=$SUBNET_IDS \
            AwsIotEndpoint=$IOT_ENDPOINT \
        --capabilities CAPABILITY_IAM \
        --region $REGION
    
    log "Stack deployed successfully"
}

# Get stack outputs
get_stack_outputs() {
    log "Getting stack outputs..."
    
    aws cloudformation describe-stacks \
        --stack-name $STACK_NAME \
        --query 'Stacks[0].Outputs' \
        --output table \
        --region $REGION
}

# Main deployment function
main() {
    log "Starting Race Controller deployment..."
    
    check_prerequisites
    create_ecr_repository
    
    IMAGE_URI=$(build_and_push_image)
    deploy_stack $IMAGE_URI
    
    get_stack_outputs
    
    log "Deployment completed successfully!"
    log "Monitor logs with: aws logs tail /ecs/race-controller --follow --region $REGION"
}

# Run main function
main "$@"