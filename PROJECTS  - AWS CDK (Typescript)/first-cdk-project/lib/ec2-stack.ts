import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as ec2 from "aws-cdk-lib/aws-ec2"

// Create an interface to acept the VPC form our VPC stack:
interface EC2StackProps extends cdk.StackProps {
    vpc: ec2.Vpc;
}

export class EC2Stack extends cdk.Stack {
    constructor(scope: Construct, id: string, props: EC2StackProps) {
        super(scope, id, props);

    // EC2 Instance 1 in AZ1
    const instance1 = new ec2.Instance(this, "MyPrivateEC2-AZ1", {
        vpc: props.vpc,
        vpcSubnets: {
            subnetType: ec2.SubnetType.PRIVATE_ISOLATED,
            availabilityZones: [props.vpc.availabilityZones[0]]
        },
        machineImage: new ec2.AmazonLinuxImage({
            generation: ec2.AmazonLinuxGeneration.AMAZON_LINUX_2
        }),
        instanceType: ec2.InstanceType.of(ec2.InstanceClass.T2, ec2.InstanceSize.MICRO)
    })

    cdk.Tags.of(instance1).add("Name", "MyPrivateEC2-AZ1")

    // EC2 Instance 2 in AZ2
    const instance2 = new ec2.Instance(this, "MyPrivateEC2-AZ2", {
        vpc: props.vpc,
        vpcSubnets: {
            subnetType: ec2.SubnetType.PRIVATE_ISOLATED,
            availabilityZones: [props.vpc.availabilityZones[1]]
        },
        machineImage: new ec2.AmazonLinuxImage({
            generation: ec2.AmazonLinuxGeneration.AMAZON_LINUX_2
        }),
        instanceType: ec2.InstanceType.of(ec2.InstanceClass.T2, ec2.InstanceSize.MICRO)
    })

    cdk.Tags.of(instance2).add("Name", "MyPrivateEC2-AZ2")
    }
}