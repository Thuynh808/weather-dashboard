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

## Versions

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
- **AWS Account**
   - An AWS account with proper access-key/secret-key

## Environment Setup

**Run the following commands to setup our VM:**
```bash
cd
dnf install -y git ansible-core
git clone -b feature/sns-eventbridge https://github.com/Thuynh808/weather-dashboard
cd weather-dashboard
ansible-galaxy collection install -r requirements.yaml -vv
```
  - Navigate to home directory
  - Install `Git` and `Ansible`
  - Clone repository
  - Navigate to project directory
  - Install required Ansible Collections
  
  
  
  
  <details close>
  <summary> <h4>Command breakdown</h4> </summary>
    
  - Navigate to home directory
  - Install `Git` and `Ansible`
  - Clone repository
  - Navigate to project directory
  - Install required Ansible Collections
  </details>

> Note: This project is configured and executed as `root` for simplicity and to streamline the setup process.
<br>   

## Installation

Power on Controller node and follow these steps to install necessary tools and configure the cluster.

- **Install Git, Ansible, and Clone the Project Repository:**
```bash
dnf install -y git ansible-core
git clone -b dev https://github.com/Thuynh808/HPC_CryptoCluster
cd HPC_CryptoCluster
ansible-galaxy collection install -r requirements.yaml -vv
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
