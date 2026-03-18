import yaml

from yamlbridge import CfnYamlLoader


def test_yaml_anchors_and_aliases_still_work():
    text = """
    defaults: &defaults
      Type: AWS::S3::Bucket

    Resources:
      BucketA:
        <<: *defaults
      BucketB:
        <<: *defaults
    """
    data = yaml.load(text, Loader=CfnYamlLoader)

    assert data == {
        "defaults": {
            "Type": "AWS::S3::Bucket",
        },
        "Resources": {
            "BucketA": {
                "Type": "AWS::S3::Bucket",
            },
            "BucketB": {
                "Type": "AWS::S3::Bucket",
            },
        },
    }


def test_aliases_can_contain_intrinsics():
    text = """
    common: &common
      BucketName: !Sub "${AWS::StackName}-bucket"

    Resources:
      BucketA:
        Properties:
          <<: *common
    """
    data = yaml.load(text, Loader=CfnYamlLoader)

    assert data == {
        "common": {
            "BucketName": {
                "Fn::Sub": "${AWS::StackName}-bucket",
            }
        },
        "Resources": {
            "BucketA": {
                "Properties": {
                    "BucketName": {
                        "Fn::Sub": "${AWS::StackName}-bucket",
                    }
                }
            }
        },
    }