import yaml

from yamlbridge import CfnYamlLoader


def test_sub_mapping_becomes_fn_sub_mapping():
    text = """
    Value: !Sub
      - "www.${Domain}"
      - Domain: !Ref RootDomainName
    """
    data = yaml.load(text, Loader=CfnYamlLoader)

    assert data == {
        "Value": {
            "Fn::Sub": [
                "www.${Domain}",
                {
                    "Domain": {"Ref": "RootDomainName"},
                },
            ]
        }
    }


def test_transform_mapping_becomes_fn_transform_mapping():
    text = """
    Value: !Transform
      Name: AWS::Include
      Parameters:
        Location: s3://bucket/snippet.yaml
    """
    data = yaml.load(text, Loader=CfnYamlLoader)

    assert data == {
        "Value": {
            "Fn::Transform": {
                "Name": "AWS::Include",
                "Parameters": {
                    "Location": "s3://bucket/snippet.yaml",
                },
            }
        }
    }


def test_nested_mapping_values_can_contain_intrinsics():
    text = """
    Metadata:
      Example: !Transform
        Name: AWS::Include
        Parameters:
          Location: !Sub "s3://${Bucket}/snippet.yaml"
    """
    data = yaml.load(text, Loader=CfnYamlLoader)

    assert data == {
        "Metadata": {
            "Example": {
                "Fn::Transform": {
                    "Name": "AWS::Include",
                    "Parameters": {"Location": {"Fn::Sub": "s3://${Bucket}/snippet.yaml"}},
                }
            }
        }
    }
