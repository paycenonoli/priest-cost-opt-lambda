# AWS FinOps EC2 Start/Stop Scheduler (Console-Based)

## Overview
Non-production EC2 instances often run continuously, even when they are not actively used. This results in unnecessary AWS compute costs.

This project demonstrates a **basic FinOps cost-optimization solution** using **AWS Lambda and Amazon EventBridge**, created entirely through the **AWS Management Console**.

The solution automatically:
- **Stops dev EC2 instances at 7:00 PM**
- **Starts dev EC2 instances at 7:00 AM**

No servers or external scripts are required.

---

## Problem
Development EC2 instances are frequently left running outside business hours, leading to wasted cloud spend.

---

## Solution
A scheduled automation built using AWS-managed services:
- **Amazon EventBridge** triggers on a schedule
- **AWS Lambda** executes start/stop logic
- **Amazon EC2** instances are controlled based on tags

Only instances explicitly tagged for automation are affected.

---

## Architecture
EventBridge (Scheduled Rules)
↓
AWS Lambda
↓
Amazon EC2

---

## Cost Optimization Impact
Stopping non-production EC2 instances outside business hours can reduce EC2 compute costs by **40–60%**, depending on usage.

---

## Services Used
- AWS Lambda (Python)
- Amazon EventBridge
- Amazon EC2
- AWS IAM
- Amazon CloudWatch Logs

---

## Tagging Strategy
Only EC2 instances with the following tags are managed:

| Key | Value |
|---|---|
| Environment | dev |
| AutoSchedule | true |

> **Important:** Production instances should NOT have these tags.

---

## How It Works
1. Two scheduled EventBridge rules are created:
   - 7:00 AM → start EC2 instances
   - 7:00 PM → stop EC2 instances
2. Each rule invokes the same Lambda function.
3. The Lambda function:
   - Finds EC2 instances using tags
   - Starts or stops instances based on the rule input
4. Lambda execution logs are written to **Amazon CloudWatch Logs**.

---

## Setup (AWS Console)

### Step 1: Tag EC2 Instances
Add the following tags to dev EC2 instances:
- `Environment=dev`
- `AutoSchedule=true`

---

### Step 2: Create IAM Role for Lambda
Create an IAM role that allows Lambda to:
- Describe EC2 instances
- Start and stop EC2 instances
- Write logs to CloudWatch

---

### Step 3: Create Lambda Function
- Runtime: Python 3.x
- Permissions: Attach the IAM role
- Logic:
  - Start or stop EC2 instances based on input (`start` or `stop`)

---

### Step 4: Create EventBridge Schedules
- **7:00 AM rule**
  - Invokes Lambda with:
    ```json
    { "action": "start" }
    ```
- **7:00 PM rule**
  - Invokes Lambda with:
    ```json
    { "action": "stop" }
    ```

---

## Verification
- Check EC2 instance state in the **EC2 Console**
- View Lambda execution logs in:
CloudWatch → Logs → /aws/lambda/<lambda-function-name>


---

## Safety Controls
- Tag-based filtering prevents production impact
- IAM permissions are limited to required actions
- Instance state checks prevent redundant operations

---

## Lessons Learned
- Serverless automation is effective for FinOps use cases
- Tagging is critical for cost control
- CloudWatch Logs are essential for monitoring and troubleshooting

---

## Next Steps
- Convert this solution to Infrastructure as Code (Terraform)
- Add notifications (Slack or email)
- Extend scheduling to other AWS services

---

## Author
Built as a hands-on AWS FinOps learning project using the AWS Management Console.

