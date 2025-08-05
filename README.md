
# Serverless Backup and Recovery System 

A cloud-native solution for automating backups and disaster recovery using serverless architecture on AWS. This project demonstrates how to build a scalable, event-driven system that securely backs up data and enables reliable restoration — without managing any servers.

## Key Features

- Fully **serverless architecture** using AWS Lambda, S3, DynamoDB, and EventBridge
- Automated **backup scheduling and execution**
- **Disaster recovery** support with one-click restore
- Real-time **monitoring and logging** (via CloudWatch)
- Lightweight **web dashboard** for triggering and managing backups

##  Architecture Overview

**AWS Services Used:**
- AWS Lambda (for backup/restore logic)
- Amazon S3 (for storing backup files)
- EventBridge (for scheduled tasks)
- CloudWatch (for monitoring and alerts)
- API Gateway (for exposing endpoints to dashboard)
- IAM (for permission control)

## Project Structure

```
Serverless_backup_and_recovery/
├── lambda/
│   ├── backup_function.py        # Lambda function to trigger backups
│   ├── restore_function.py       # Lambda function to restore data
│   └── utils.py                  # Shared helpers (S3, DynamoDB ops)
├── dashboard/
│   ├── index.html                # Simple web UI for triggering backups
│   └── script.js                 # JS for interacting with the backend API
├── cloudformation/
│   └── template.yaml             # Infra as Code (AWS SAM or CloudFormation)
├── README.md
└── requirements.txt              # Dependencies for Lambda functions
```

## How It Works

1. **User triggers** a backup from the dashboard or by schedule (EventBridge)
2. **Lambda function** compresses and uploads files to S3
3. **Metadata is logged** in DynamoDB for traceability
4. **Restore** function downloads the backup from S3 and restores it on command

## Setup Instructions

### 1. Deploy Infrastructure (via AWS SAM or manually)
```bash
sam deploy --guided
```

### 2. Setup Environment Variables

- `S3_BUCKET_NAME`
- `DYNAMODB_TABLE_NAME`

### 3. Install Python Dependencies (for Lambda)

```bash
pip install -r requirements.txt -t lambda/
```

### 4. Launch Web Dashboard

Open `dashboard/index.html` in your browser. Ensure CORS and API Gateway permissions are properly configured.

##  Security Best Practices

- Use IAM roles with least privilege
- Enable server-side encryption for S3 and DynamoDB
- Log API activity with CloudTrail

## Author

**Hemanth Kumar**  

## License

This project is licensed under the MIT License.
