import yaml

from yamlbridge import CfnYamlLoader


def test_minimal_s3_template():
    text = """
    AWSTemplateFormatVersion: "2010-09-09"
    Resources:
      MyBucket:
        Type: AWS::S3::Bucket
    Outputs:
      BucketName:
        Value: !Ref MyBucket
    """
    data = yaml.load(text, Loader=CfnYamlLoader)

    assert data == {
        "AWSTemplateFormatVersion": "2010-09-09",
        "Resources": {
            "MyBucket": {
                "Type": "AWS::S3::Bucket",
            }
        },
        "Outputs": {
            "BucketName": {
                "Value": {"Ref": "MyBucket"},
            }
        },
    }


def test_template_with_conditions_and_mappings():
    text = """
    Parameters:
      Env:
        Type: String
    Mappings:
      EnvMap:
        prod:
          InstanceType: m5.large
        dev:
          InstanceType: t3.micro
    Conditions:
      IsProd: !Equals [!Ref Env, prod]
    Resources:
      MyInstance:
        Type: AWS::EC2::Instance
        Properties:
          InstanceType: !FindInMap [EnvMap, !Ref Env, InstanceType]
    """
    data = yaml.load(text, Loader=CfnYamlLoader)

    assert data == {
        "Parameters": {
            "Env": {
                "Type": "String",
            }
        },
        "Mappings": {
            "EnvMap": {
                "prod": {"InstanceType": "m5.large"},
                "dev": {"InstanceType": "t3.micro"},
            }
        },
        "Conditions": {
            "IsProd": {
                "Fn::Equals": [
                    {"Ref": "Env"},
                    "prod",
                ]
            }
        },
        "Resources": {
            "MyInstance": {
                "Type": "AWS::EC2::Instance",
                "Properties": {
                    "InstanceType": {
                        "Fn::FindInMap": [
                            "EnvMap",
                            {"Ref": "Env"},
                            "InstanceType",
                        ]
                    }
                },
            }
        },
    }


def test_lambda_like_template_snippet():
    text = """
    Resources:
      MyFunction:
        Type: AWS::Lambda::Function
        Properties:
          FunctionName: !Sub "${AWS::StackName}-handler"
          Role: !GetAtt LambdaExecutionRole.Arn
          Environment:
            Variables:
              TABLE_NAME: !Ref MyTable
    """
    data = yaml.load(text, Loader=CfnYamlLoader)

    assert data == {
        "Resources": {
            "MyFunction": {
                "Type": "AWS::Lambda::Function",
                "Properties": {
                    "FunctionName": {"Fn::Sub": "${AWS::StackName}-handler"},
                    "Role": {"Fn::GetAtt": "LambdaExecutionRole.Arn"},
                    "Environment": {
                        "Variables": {
                            "TABLE_NAME": {"Ref": "MyTable"},
                        }
                    },
                },
            }
        }
    }