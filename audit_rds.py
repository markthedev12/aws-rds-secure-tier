"""Read-only RDS encryption/public-access checks with JSON output."""
import argparse
import json

def evaluate_instance(instance):
    return {"identifier": instance["DBInstanceIdentifier"],
            "encrypted": instance.get("StorageEncrypted", False),
            "publicly_accessible": instance.get("PubliclyAccessible", False),
            "multi_az": instance.get("MultiAZ", False)}

def audit_rds_instances(client):
    return [evaluate_instance(instance)
            for page in client.get_paginator("describe_db_instances").paginate()
            for instance in page.get("DBInstances", [])]

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--region", default="us-east-2")
    args = parser.parse_args(argv)
    import boto3
    from botocore.exceptions import BotoCoreError, ClientError
    try:
        instances = audit_rds_instances(boto3.client("rds", region_name=args.region))
    except (BotoCoreError, ClientError) as error:
        parser.exit(2, f"Audit could not complete: {error}\n")
    print(json.dumps({"region": args.region, "instances": instances}, indent=2))
    return int(any(not db["encrypted"] or db["publicly_accessible"] for db in instances))

if __name__ == "__main__":
    raise SystemExit(main())
