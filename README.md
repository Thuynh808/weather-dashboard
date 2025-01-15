![HPC_CryptoCluster](https://i.imgur.com/31TiOpL.png)

## Project Overview
This project automates daily weather data collection, aggregation, and notification delivery using AWS services and Ansible. The **Weather Dashboard** fetches weather data from the OpenWeather API for four cities, uploads it to an S3 bucket, triggers a Lambda function via EventBridge, and sends the aggregated weather report to a subscribed email via SNS. This project demonstrates cloud automation, event-driven architecture, and end-to-end deployment workflows.

### Components

- **Rocky Linux VM**: Provides a RHEL-based and stable environment for Ansible and script execution
- **Ansible**: Automates the deployment of AWS infrastructure and project setup
- **AWS Services**:
  - **S3**: Stores aggregated weather data
  - **SNS**: Sends email notifications with weather reports
  - **Lambda**: Processes S3 events and publishes reports to SNS
  - **EventBridge**: Triggers Lambda on S3 object creation
- **OpenWeather API**: Provides real-time weather data for multiple cities

### Versions

| Component        | Version  | Component     | Version |
|------------------|----------|---------------|---------|
| Rocky Linux      | 9.4      | Ansible       | 2.15    |
| AWS CLI          | Latest   | Community.aws | 9.0     |
| Python           | 3.9.21   | Amazon.aws    | 9.0     |
| Botocore         | 1.31.0   | Requests      | 2.28.2  |  
| Boto3            | 1.28.0   | python-dotenv | 1.0     |

## Prerequisites

- **Rocky Linux VM**
  - Fresh installation of Rocky Linux
  - Allocate sufficient resources: **2 CPUs, 4GB RAM**
- **OpenWeather API**
  - A free registered account with provided API key 
- **AWS Account**
   - An AWS account with provisioned access-key and secret-key

## Environment Setup

**Run the following to setup our VM:**
```bash
cd
dnf install -y git ansible-core
git clone -b feature/sns-eventbridge https://github.com/Thuynh808/weather-dashboard
cd weather-dashboard
ansible-galaxy collection install -r requirements.yaml -vv
```
  Command Breakdown:
  - Navigates to home directory
  - Installs `Git` and `Ansible`
  - Clone repository
  - Navigates to project directory
  - Install required Ansible Collections

## Define Variables

**Update variables with proper values for files: `myvars.yaml` and `.env`**
```bash
vim myvars.yaml
```
```bash
accesskeyid: "<your-access-key-id>"
secretaccesskey: "<your-secret-access-key>"
defaultregion: "us-east-1"
emailendpoint: "<your-email>"
bucketname: "<your-bucket-name>"
```
```bash
vim .env
```
```bash
OPENWEATHER_API_KEY=<your-api-key>
AWS_BUCKET_NAME=<your-bucket-name>
AWS_REGION=us-east-1
```
**Set permissions to secure files**
```bash
chmod 0600 .env myvars.yaml 
```
> Note: Keep these sensitive files local. Add to `.gitignore` if uploading to GitHub
<br>  

## Execute Ansible Playbooks

**Run Playbook:**
```bash
ansible-playbook weather_env_s3_sns.yaml -vv
```
  The `weather_env_s3_sns.yaml` playbook will:
  - Install and upgrade system packages
  - Install `pip` modules with required versions
  - Download, unzip and install `AWS CLI`
  - Configure `AWS CLI`
  - Create S3 bucket
  - Create SNS topic to send notifications to email subscriber
  - Append SNS Amazon Resource Name (ARN) to `myvars.yaml` file

**Confirm Successful Execution:**
```bash
rpm -qa curl unzip python3 python3-pip
pip list | egrep "boto3|botocore|python-dotenv|requests" 
aws configure list
aws sts get-caller-identity
aws s3 ls
```
<details close>
  <summary> <h4>See images</h4> </summary>
    
![HPC_CryptoCluster](https://i.imgur.com/UCc5IMD.png)
  </details>
  
**Log in to email account and confirm subscription**
<details close>
  <summary> <h4>See images</h4> </summary>
    
![HPC_CryptoCluster](https://i.imgur.com/UCc5IMD.png)
  </details>

**Run Playbook:**
```bash
ansible-playbook weather_lambda_eventbridge.yaml -vv
```
  The `weather_lambda_eventbridge.yaml` playbook will:
  - Create IAM `lambda-execution-role` to provide permissions to execute `Lambda` function
  - Add IAM execution role ARN variable to myvars.yaml
  - Generate a custom IAM policy and attach to our `lambda-execution-role`
  - Compress the `Lambda` python script
  - Create `Lambda` function from script and attach role
  - Append `Lambda` variables to myvars.yaml
  - Enable `EventBridge` notifications on `S3` bucket
  - Generate rule in `EventBridge` for newly created objects in `S3`
  - Set `EventBridge` target to invoke the `Lambda` function when event is triggered
  - Automate a daily cron job to fetch weather data and upload it to `S3` using a Python script

**Confirm Successful Execution:**

```bash
aws sns list-topics
aws lambda list-functions
aws events list-rules 
crontab -l
```
<details close>
  <summary> <h4>See images</h4> </summary>
    
![HPC_CryptoCluster](https://i.imgur.com/UCc5IMD.png)
  </details>
  
**Excellent! Now for a demo, let's manually test our Weather Dashboard!**
```bash
python /src/weather_data_aggregator.py
```
<details close>
  <summary> <h4>See results</h4> </summary>
    
![HPC_CryptoCluster](https://i.imgur.com/UCc5IMD.png)
  </details>

## Challenges

- Versioning in Lambda ARN: Resolved by dynamically extracting the base ARN without version numbers.
- Policy Propagation Delays: Added a pause after creating IAM policies to ensure EventBridge permissions were applied.
- Dynamic Variables in Ansible: Used set_fact and lineinfile modules to dynamically update variable files.
- Conditional Task Execution: Ensured the AWS CLI installation only runs when not already present using when conditions.
- S3 Event Configuration: Properly enabled EventBridge for S3 bucket events to trigger Lambda.
- Securing Sensitive Files: Used file permissions to secure .env and myvars.yaml files.

## Conclusion

The Weather Dashboard project showcases automation of cloud services using Ansible and AWS. It emphasizes best practices for event-driven architectures, secure credential management, and efficient deployment workflows. By implementing daily cron jobs, it provides a scalable, real-world solution for automated weather notifications.


