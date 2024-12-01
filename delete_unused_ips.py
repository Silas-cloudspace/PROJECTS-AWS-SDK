import boto3

# Add your AWS access Key ID and Secret Access Key here
AWS_ACCESS_KEY = "replace with access key"
AWS_SECRET_KEY = "replace with secret access key"

def get_unused_elastic_ips():
    unused_elastic_ips = {}

    # Get the list of all AWS regions
    ec2_client = boto3.client("ec2", aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)
    regions = ec2_client.describe_regions()["Regions"]

    # Iterate over each region
    for region in regions:
        current_region_name = region["RegionName"]
        print(f"Checking region: {current_region_name}")

        try:
            # Establish a connection to EC2 in the current region
            ec2_client = boto3.client(
                "ec2",
                region_name=current_region_name,
                aws_access_key_id=AWS_ACCESS_KEY,
                aws_secret_access_key=AWS_SECRET_KEY
            )

            # Find Elastic IPs in the VPC domain
            addresses = ec2_client.describe_addresses(Filters=[{"Name": "domain", "Values": ["vpc"]}])["Addresses"]
            for address in addresses:
                if "AssociationId" not in address:  # Unused IPs have no AssociationId
                    allocation_id = address["AllocationId"]
                    public_ip = address["PublicIp"]

                    # Avoid duplicates and add to the unused IPs dictionary
                    if allocation_id not in unused_elastic_ips:
                        unused_elastic_ips[allocation_id] = current_region_name

                        # Release the unused Elastic IP
                        ec2_client.release_address(AllocationId=allocation_id)
                        print(f"Released unused Elastic IP {public_ip} in region {current_region_name}")

        except Exception as e:
            print(f"Error accessing region {current_region_name}: {e}")

    return unused_elastic_ips


if __name__ == "__main__":
    # Run the function and display the results
    unused_ips = get_unused_elastic_ips()
    print(f"Found and released {len(unused_ips)} unused Elastic IPs across all regions.")
    print("Details of released IPs:", unused_ips)
