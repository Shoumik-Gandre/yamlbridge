import yaml

from yamlbridge import CfnYamlLoader


def test_cfn_yaml_loader_is_importable():
    assert CfnYamlLoader is not None


def test_cfn_yaml_loader_is_a_safe_loader():
    assert issubclass(CfnYamlLoader, yaml.SafeLoader)


def test_yaml_load_accepts_cfn_yaml_loader():
    text = """
    Resources:
      MyBucket:
        Type: AWS::S3::Bucket
    """
    data = yaml.load(text, Loader=CfnYamlLoader)

    assert data == {
        "Resources": {
            "MyBucket": {
                "Type": "AWS::S3::Bucket",
            }
        }
    }


def test_plain_yaml_still_loads_normally():
    text = """
    name: yamlbridge
    enabled: true
    retries: 3
    items:
      - a
      - b
    """
    data = yaml.load(text, Loader=CfnYamlLoader)

    assert data == {
        "name": "yamlbridge",
        "enabled": True,
        "retries": 3,
        "items": ["a", "b"],
    }