import yaml

from yamlbridge import CfnYamlLoader


def test_join_sequence_becomes_fn_join_mapping():
    text = """
    Value: !Join
      - ":"
      - - a
        - b
        - c
    """
    data = yaml.load(text, Loader=CfnYamlLoader)

    assert data == {
        "Value": {
            "Fn::Join": [":", ["a", "b", "c"]],
        }
    }


def test_if_sequence_becomes_fn_if_mapping():
    text = """
    Value: !If
      - IsProd
      - prod.example.com
      - dev.example.com
    """
    data = yaml.load(text, Loader=CfnYamlLoader)

    assert data == {
        "Value": {
            "Fn::If": ["IsProd", "prod.example.com", "dev.example.com"],
        }
    }


def test_findinmap_sequence_becomes_fn_findinmap_mapping():
    text = """
    Value: !FindInMap
      - RegionMap
      - !Ref AWS::Region
      - HVM64
    """
    data = yaml.load(text, Loader=CfnYamlLoader)

    assert data == {
        "Value": {
            "Fn::FindInMap": [
                "RegionMap",
                {"Ref": "AWS::Region"},
                "HVM64",
            ]
        }
    }


def test_select_sequence_becomes_fn_select_mapping():
    text = """
    Value: !Select
      - 0
      - - subnet-1
        - subnet-2
    """
    data = yaml.load(text, Loader=CfnYamlLoader)

    assert data == {
        "Value": {
            "Fn::Select": [0, ["subnet-1", "subnet-2"]],
        }
    }


def test_split_sequence_becomes_fn_split_mapping():
    text = """
    Value: !Split
      - ","
      - "a,b,c"
    """
    data = yaml.load(text, Loader=CfnYamlLoader)

    assert data == {
        "Value": {
            "Fn::Split": [",", "a,b,c"],
        }
    }


def test_equals_sequence_becomes_fn_equals_mapping():
    text = """
    Value: !Equals
      - !Ref Env
      - prod
    """
    data = yaml.load(text, Loader=CfnYamlLoader)

    assert data == {
        "Value": {
            "Fn::Equals": [
                {"Ref": "Env"},
                "prod",
            ]
        }
    }


def test_and_sequence_becomes_fn_and_mapping():
    text = """
    Value: !And
      - !Condition IsProd
      - !Condition HasDomain
    """
    data = yaml.load(text, Loader=CfnYamlLoader)

    assert data == {
        "Value": {
            "Fn::And": [
                {"Condition": "IsProd"},
                {"Condition": "HasDomain"},
            ]
        }
    }


def test_or_sequence_becomes_fn_or_mapping():
    text = """
    Value: !Or
      - !Condition IsProd
      - !Condition IsStaging
    """
    data = yaml.load(text, Loader=CfnYamlLoader)

    assert data == {
        "Value": {
            "Fn::Or": [
                {"Condition": "IsProd"},
                {"Condition": "IsStaging"},
            ]
        }
    }


def test_not_sequence_becomes_fn_not_mapping():
    text = """
    Value: !Not
      - !Condition IsProd
    """
    data = yaml.load(text, Loader=CfnYamlLoader)

    assert data == {
        "Value": {
            "Fn::Not": [
                {"Condition": "IsProd"},
            ]
        }
    }


def test_cidr_sequence_becomes_fn_cidr_mapping():
    text = """
    Value: !Cidr
      - 10.0.0.0/16
      - 4
      - 8
    """
    data = yaml.load(text, Loader=CfnYamlLoader)

    assert data == {
        "Value": {
            "Fn::Cidr": ["10.0.0.0/16", 4, 8],
        }
    }
