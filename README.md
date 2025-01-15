![HPC_CryptoCluster](https://i.imgur.com/31TiOpL.png)

## Project Overview
This project automates daily weather data collection, aggregation, and notification delivery using AWS services and Ansible. The **Weather Dashboard** fetches weather data from the OpenWeather API for four cities, uploads it to an S3 bucket, triggers a Lambda function via EventBridge, and sends the aggregated weather report to a subscribed email via SNS. This project demonstrates cloud automation, event-driven architecture, and end-to-end deployment workflows.

### Components

- **Rocky Linux VM**: Provides a stable environment for Ansible and script execution
- **Ansible**: Automates the deployment of AWS infrastructure and project setup
- **AWS Services**:
  - **S3**: Stores aggregated weather data
  - **SNS**: Sends email notifications with weather reports
  - **Lambda**: Processes S3 events and publishes reports to SNS
  - **EventBridge**: Triggers Lambda on S3 object creation
- **OpenWeather API**: Provides real-time weather data for multiple cities

### Versions

| Component        | Version  |
|------------------|----------|
| Rocky Linux      | 9.4      |
| Ansible          | 2.14     |
| AWS CLI          | Latest   |
| Python           | 3.9      |
| Boto3            | 1.28.0   |
| Requests         | 2.28.2   |

<br>

## Prerequisites

- **Rocky Linux VM**
  - Ensure a fresh installation of Rocky Linux
  - Allocate sufficient resources (2 CPUs, 4GB RAM)
- **OpenWeather API**
  - A free registered account with provided API key 
- **AWS Account**
   - An AWS account with proper access-key/secret-key

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
  The `weather_env_s2_sns.yaml` playbook will:
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
  

  

**Install Git, Ansible, and Clone the Project Repository:**
```bash
ansible-playbook weather_env_s3_sns.yaml -vv
```
- **Run the Ansible playbooks to install and configure `Warewulf` and `John the Ripper`:**
```bash
ansible-playbook warewulf.yaml -vv
ansible-playbook john.yaml -vv
```
- **In `Warewulf` container image shell, install dependencies, and configure `Slurm` for the compute nodes:**
```bash
wwctl container shell rockylinux-9
```
```bash
dnf install -y git ansible-core
git clone -b dev https://github.com/Thuynh808/HPC_CryptoCluster
cd HPC_CryptoCluster
ansible-galaxy collection install -r requirements.yaml -vv
ansible-playbook slurm-node.yaml -vv
exit #rebuild container image
```
- **Set Up `Slurm` and `Munge` on the Controller Node to manage the Slurm job scheduler and secure communication:**
```bash
ansible-playbook slurm-control.yaml -vv
```
- **`Power on` compute nodes to initialize the network boot and connect to the controller node**

<br>

## Deployment Verification

Let's verify everything is up and running!

- **Confirm `Warewulf` service is up and node overlays configured**
```bash
wwctl node list -l && wwctl node list -n
wwctl node list -a | tail -9
systemctl status warewulfd.service --no-pager
firewall-cmd --list-all
```
  <details close>
  <summary> <h4>See Images</h4> </summary>
  
  ![HPC_CryptoCluster](https://i.imgur.com/Julx1xb.png)
  ![HPC_CryptoCluster](https://i.imgur.com/82vV2aF.png)
  <br><br>
  </details>
  
- **Confirm sample password file is created and Run a benchmark test with `John`**
```bash
cd /home/slurm
ls -l
cat john_hash.txt
john --test --format=raw-sha256
```
  <details close>
  <summary> <h4>See Images</h4> </summary>
  
  ![HPC_CryptoCluster](https://i.imgur.com/UCc5IMD.png)
  <br><br>
  </details>
  
- **Confirm `Slurm` and `Munge` are operational and Munge key is valid**
```bash
systemctl status slurmctld munge --no-pager
munge -n | ssh node1 unmunge
ssh node1 systemctl status slurmd
```
  <details close>
  <summary> <h4>See Images</h4> </summary>
  
  ![HPC_CryptoCluster](https://i.imgur.com/AvlmOHC.png)
  ![HPC_CryptoCluster](https://i.imgur.com/zQkYUcj.png)
  <br><br>
  </details>
  
- **Confirm compute nodes are properly up with network boot and hosts configured**
```bash
ssh node3
```
```bash
dmesg | head
cat /etc/hosts
sinfo -l
scontrol show node
```
  <details close>
  <summary> <h4>See Images</h4> </summary>
    
  ![HPC_CryptoCluster](https://i.imgur.com/xY4asql.png)
  ![HPC_CryptoCluster](https://i.imgur.com/RHsmczr.png)
  <br><br>
  </details>
<br>   


## Testing Cluster with John the Ripper

This section demonstrates the cluster's functionality through two tests: a single-node password-cracking job and a multi-node distributed job.

<details close>
<summary> <h3>Single Node Test</h3> </summary>

- **Submit the sbatch password-cracking job on a single compute node**
```bash
cd /home/slurm
sbatch john_test.sh
```
- **Verify the job is submitted and running on single node**
```bash
sinfo -l
scontrol show job <JobId>
```
![HPC_CryptoCluster](https://i.imgur.com/MnZO0Tu.png)

- With 2 cpus, Slurm can be configured to allocate 2 processes to split the load of the job
     
![HPC_CryptoCluster](https://i.imgur.com/lk5kop8.png)  

- **Confirm finished job and view results**
```bash
scontrol show job <JobId>
cat /home/slurm/john_result.log
```

- The job ran efficiently and recovered all 10 target passwords within 16 minutes and 22 seconds, confirming the effectiveness of the single-node configuration for password cracking.
    
![HPC_CryptoCluster](https://i.imgur.com/kv4N547.png)

</details>

<details close>
<summary> <h3>Multi-Node Distributed Test</h3> </summary>
  
- **Now we'll submit the distributed job**
```bash
cd /home/slurm
sbatch john_distributed.sh
sleep 5
sinfo -l
scontrol show job <JobId>
```

- The job is allocated across three nodes (node[1-3]), with each node contributing 2 CPUs for a total of 6 CPUs.
    
![HPC_CryptoCluster](https://i.imgur.com/4Sp87TD.png)
  
- **Confirm job finished and view results**
```bash
scontrol show job <JobId>
cat /home/slurm/john_distributed_result.log
```
![HPC_CryptoCluster](https://i.imgur.com/qB3Oj56.png) 

</details>
<br>

## Conclusion

  <details close>
  <summary> <h4>images</h4> </summary>
    
![HPC_CryptoCluster](https://i.imgur.com/UCc5IMD.png)
  </details>

> Note: This project is configured and executed as `root` for simplicity and to streamline the setup process.
<br>   
