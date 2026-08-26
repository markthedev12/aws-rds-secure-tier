# AWS RDS Secure PostgreSQL Tier with Terraform & Python Compliance Audit

## Architecture Overview
This project provisions an isolated, encrypted PostgreSQL database tier on AWS using Terraform (IaC) and verifies cloud security posture using an automated Python (`boto3`) compliance audit.

### Key Security & Architectural Controls
* **Private Subnet Isolation:** Bound to an `aws_db_subnet_group` spanning multiple Availability Zones.
* **Least-Privilege Security Group:** Ingress restricted strictly to VPC CIDR on PostgreSQL port `5432` with zero public exposure (`0.0.0.0/0` ingress blocked).
* **Encryption at Rest:** Storage encrypted via AWS KMS.
* **Public Access Prevention:** `publicly_accessible` explicitly set to `false`.

## Project Structure
* `main.tf` - Infrastructure as Code defining RDS instance, subnet group, and security groups.
* `audit_rds.py` - Automated compliance script auditing live AWS RDS instances for encryption and exposure.

## Verification
Automated audit execution:
```bash
python audit_rds.py