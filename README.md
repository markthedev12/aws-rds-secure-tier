# AWS RDS PostgreSQL Security Lab

A Terraform lab that provisions encrypted PostgreSQL with public addressing
disabled, plus a read-only Python auditor. Demonstrates infrastructure and API
inspection; it is not a production-ready database architecture.

## Architecture and boundaries

`Default VPC subnets -> RDS subnet group -> encrypted PostgreSQL`

`VPC CIDR -> security group TCP/5432 -> RDS`

RDS manages the master password in Secrets Manager. No password value belongs in
source or command history. A previous version contained a literal password: if
it was ever deployed, rotate that credential. This change neither rotates a live
database nor removes earlier Git history.

The subnet group uses discovered default-VPC subnets; this does **not** establish
private subnet routing. `publicly_accessible = false` disables public addressing
but is not a complete network isolation audit. TCP/5432 is permitted from the
whole VPC CIDR, not just one application security group. Multi-AZ and production
backup/deletion protections are not implemented.

## Local tests

Python 3.12+; no AWS account or dependencies required for tests.

```sh
python -m unittest discover -s tests -v
```

## Provision and inspect

Requires Terraform, provisioning credentials, a default VPC in us-east-2,
and permission for RDS to manage its Secrets Manager secret. RDS, storage, and
Secrets Manager may incur charges; check account eligibility and pricing first.

```sh
terraform init
terraform fmt -check
terraform validate
terraform plan -out=lab.tfplan
terraform apply lab.tfplan
python -m pip install -r requirements.txt
python audit_rds.py --region us-east-2
```

The auditor uses `rds:DescribeDBInstances` and paginates all instances in the
selected region. JSON shows encryption, public accessibility, and Multi-AZ
configuration. Exit 0 means no encrypted/public-access violations were found;
1 means at least one was found; 2 means collection failed. An empty list means
no instances were returned, not proof that the entire account is secure.

Verify the instance settings in AWS and test intended application connectivity.
Neither the auditor nor its tests prove subnet isolation, actual reachability,
least privilege, or compliance.

## Cleanup and next steps

```sh
terraform plan -destroy
terraform destroy
```

The lab sets `skip_final_snapshot = true`: destroying it deletes the database
without a final snapshot. Use fictional data. Confirm remaining snapshots and
Secrets Manager resources and charges separately after teardown.

Next: explicit private subnets, application-only security-group ingress, defined
backup retention, deletion protection, migration/restore exercises, and CI policy
scanning. Keep Terraform state/plans and live audit reports out of Git. Add
targeted tests whenever changing audit behavior.
