# AWS RDS Secure PostgreSQL Tier with Terraform & Python Compliance Audit

## Architecture Overview
This project automates the provisioning of a private, production-ready PostgreSQL database tier on AWS using **Terraform (Infrastructure as Code)** and programmatically validates cloud security posture using an automated **Python (`boto3`) compliance audit**.

### Key Security & Architectural Controls
* **Private Subnet Placement:** Bound to an `aws_db_subnet_group` spanning multiple Availability Zones to ensure architectural isolation.
* **Network Isolation & Least Privilege:** Security Group ingress is strictly restricted to PostgreSQL port `5432` from internal VPC CIDR ranges only; all public internet ingress (`0.0.0.0/0`) is explicitly blocked.
* **Storage Encryption at Rest:** Automated encryption enforced using AWS KMS keys (`storage_encrypted = true`).
* **Zero Public Exposure:** `publicly_accessible` is set to `false`, preventing public IP assignment.

---

## Project Structure
* `main.tf` — Terraform configuration declaring the isolated VPC subnet group, security group rules, and PostgreSQL RDS instance.
* `audit_rds.py` — Python automation script leveraging `boto3` to audit live RDS instances for encryption-at-rest and network exposure.
* `.gitignore` — Standard cloud engineering rules to prevent state files and sensitive secrets from leaking to source control.

---

## Verification & Security Audit Results

### 1. Automated Python Compliance Check
The Boto3 audit queries the AWS RDS API, confirming that storage encryption is active and public accessibility is completely disabled:

<img width="484" height="127" alt="Py Audit" src="https://github.com/user-attachments/assets/84bc88de-fe69-421b-98d9-36b0197519d5" />


### 2. Terraform State & Outputs
Infrastructure deployed and validated via Terraform state outputs:

<img width="666" height="148" alt="TF plan" src="https://github.com/user-attachments/assets/20dc1346-6fae-41c2-bf26-71e3cc3276ae" />

<img width="614" height="36" alt="T output" src="https://github.com/user-attachments/assets/77f728c8-48a0-4cbc-abc3-adbd9079df90" />



---

## How to Run

### 1. Deploy Infrastructure
```bash
terraform init
terraform apply -auto-approve
