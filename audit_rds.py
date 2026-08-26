import boto3

rds = boto3.client('rds', region_name='us-east-2')

def audit_rds_instances():
    print("=== RUNNING RDS SECURITY & COMPLIANCE AUDIT ===")
    response = rds.describe_db_instances()
    
    if not response['DBInstances']:
        print("[INFO] No RDS instances found in region us-east-2.")
        return

    for db in response['DBInstances']:
        db_id = db['DBInstanceIdentifier']
        engine = db['Engine']
        storage_encrypted = db.get('StorageEncrypted', False)
        publicly_accessible = db.get('PubliclyAccessible', False)
        multi_az = db.get('MultiAZ', False)
        
        print(f"\nEvaluating Instance: {db_id} (Engine: {engine})")
        
        # 1. Storage Encryption Audit
        if storage_encrypted:
            print(f"  [PASS] Storage Encryption is ENABLED (KMS).")
        else:
            print(f"  [FAIL - CRITICAL] Storage Encryption is DISABLED.")
            
        # 2. Public Accessibility Audit
        if not publicly_accessible:
            print(f"  [PASS] Public Access is BLOCKED (Private Subnet Bound).")
        else:
            print(f"  [FAIL - HIGH] Database is PUBLICLY ACCESSIBLE to the Internet.")
            
        # 3. High Availability Status
        print(f"  [INFO] Multi-AZ Deployment: {multi_az}")

if __name__ == '__main__':
    audit_rds_instances()