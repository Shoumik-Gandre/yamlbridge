import yaml
import pytest

from yamlbridge import CfnYamlLoader


def test_invalid_yaml_still_raises_yaml_error():
    text = """
    Resources:
      MyBucket
        Type: AWS::S3::Bucket
    """
    with pytest.raises(yaml.YAMLError):
        yaml.load(text, Loader=CfnYamlLoader)


def test_unknown_tag_raises_yaml_error():
    text = "Value: !DoesNotExist something"
    with pytest.raises(yaml.YAMLError):
        yaml.load(text, Loader=CfnYamlLoader)


def test_malformed_join_structure_still_loads_as_yaml_but_preserves_shape():
    text = """
    Value: !Join
      only-one-item
    """
    data = yaml.load(text, Loader=CfnYamlLoader)

    assert data == {
        "Value": {
            "Fn::Join": "only-one-item",
        }
    }


def test_empty_ref_value():
    text = 'Value: !Ref ""'
    data = yaml.load(text, Loader=CfnYamlLoader)

    assert data == {
        "Value": {
            "Ref": "",
        }
    }