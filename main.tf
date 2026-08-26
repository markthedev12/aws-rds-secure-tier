terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "us-east-2"
}

# 1. Look up Default VPC and its subnets across AZs
data "aws_vpc" "default" {
  default = true
}

data "aws_subnets" "default" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }
}

# 2. Section 9 Requirement: DB Subnet Group across multiple AZs
resource "aws_db_subnet_group" "rds_subnet_group" {
  name       = "secure-db-subnet-group"
  subnet_ids = data.aws_subnets.default.ids

  tags = {
    Name = "Secure-RDS-Subnet-Group"
  }
}

# 3. Security Group: Restrict PostgreSQL port 5432 to VPC internal traffic only
resource "aws_security_group" "rds_sg" {
  name        = "secure-rds-sg"
  description = "Isolated database tier - zero public access"
  vpc_id      = data.aws_vpc.default.id

  ingress {
    description = "PostgreSQL from internal VPC"
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = [data.aws_vpc.default.cidr_block]
  }

  egress {
    description = "Outbound egress"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "Secure-RDS-SG"
  }
}

# 4. PostgreSQL RDS Instance
resource "aws_db_instance" "postgres_db" {
  identifier             = "dev-secure-postgres-db"
  allocated_storage      = 20
  max_allocated_storage  = 20
  engine                 = "postgres"
  engine_version         = "16"
  instance_class         = "db.t4g.micro"
  db_name                = "appdb"
  username               = "dbadmin"
  password               = "SecureDevPass2026!"
  db_subnet_group_name   = aws_db_subnet_group.rds_subnet_group.name
  vpc_security_group_ids = [aws_security_group.rds_sg.id]

  # Core Architectural Best Practices
  publicly_accessible = false
  storage_encrypted   = true
  skip_final_snapshot = true

  tags = {
    Environment = "DevSecOps-Lab"
    ManagedBy   = "Terraform"
  }
}

output "rds_endpoint" {
  description = "Database Endpoint Address"
  value       = aws_db_instance.postgres_db.address
}