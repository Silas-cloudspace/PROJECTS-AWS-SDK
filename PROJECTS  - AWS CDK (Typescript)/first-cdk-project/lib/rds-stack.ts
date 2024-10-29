import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as ec2 from 'aws-cdk-lib/aws-ec2';
import * as rds from 'aws-cdk-lib/aws-rds';

// Create an interface to accept the VPC from our VPC stack
interface RDSStackProps extends cdk.StackProps {
  vpc: ec2.Vpc;
}

export class RDSStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props: RDSStackProps) {
    super(scope, id, props);

    // Database1 in AZ1
    const database1 = new rds.DatabaseInstance(this, "Database1-AZ1", {
      vpc: props.vpc,
      vpcSubnets: {
        subnetType: ec2.SubnetType.PRIVATE_ISOLATED,
      },
      availabilityZone: props.vpc.availabilityZones[0],
      engine: rds.DatabaseInstanceEngine.mysql({
        version: rds.MysqlEngineVersion.VER_8_0,
      }),
      instanceType: ec2.InstanceType.of(
        ec2.InstanceClass.T3,
        ec2.InstanceSize.MICRO
      ),
      // Storage configuration
      allocatedStorage: 20,
      maxAllocatedStorage: 30,
      deletionProtection: false,
    });

    // Database2 in AZ2
    const database2 = new rds.DatabaseInstance(this, "Database2-AZ2", {
      vpc: props.vpc,
      vpcSubnets: {
        subnetType: ec2.SubnetType.PRIVATE_ISOLATED,
      },
      availabilityZone: props.vpc.availabilityZones[1],
      engine: rds.DatabaseInstanceEngine.mysql({
        version: rds.MysqlEngineVersion.VER_8_0,
      }),
      instanceType: ec2.InstanceType.of(
        ec2.InstanceClass.T3,
        ec2.InstanceSize.MICRO
      ),
      allocatedStorage: 20,
      maxAllocatedStorage: 30, 
      deletionProtection: false,
    });

    // TAGS
    cdk.Tags.of(database1).add("Name", "Database1-AZ1");
    cdk.Tags.of(database2).add("Name", "Database2-AZ2");

    // OUTPUTS
    new cdk.CfnOutput(this, "DatabaseEndpoint-AZ1", {
      value: database1.instanceEndpoint.hostname,
      description: "The endpoint of the Database1-AZ1",
      exportName: "DatabaseEndpoint-AZ1",
    });

    new cdk.CfnOutput(this, "DatabasePort-AZ1", {
      value: database1.instanceEndpoint.port.toString(),
      description: "The port of the Database1-AZ1",
      exportName: "DatabasePort-AZ1",
    });

    new cdk.CfnOutput(this, "DatabaseEndpoint-AZ2", {
      value: database2.instanceEndpoint.hostname,
      description: "The endpoint of the Database2-AZ2",
      exportName: "DatabaseEndpoint-AZ2",
    });
  
    new cdk.CfnOutput(this, "DatabasePort-AZ2", {
      value: database2.instanceEndpoint.port.toString(),
      description: "The port of the Database2-AZ2",
      exportName: "DatabasePort-AZ2",
    });
  }
}