import yaml

from yamlbridge import CfnYamlLoader


def test_ref_scalar_becomes_ref_mapping():
    text = "Value: !Ref MyBucket"
    data = yaml.load(text, Loader=CfnYamlLoader)

    assert data == {"Value": {"Ref": "MyBucket"}}


def test_condition_scalar_becomes_condition_mapping():
    text = "Condition: !Condition IsProd"
    data = yaml.load(text, Loader=CfnYamlLoader)

    assert data == {"Condition": {"Condition": "IsProd"}}


def test_sub_scalar_becomes_fn_sub_mapping():
    text = 'Value: !Sub "${AWS::StackName}-bucket"'
    data = yaml.load(text, Loader=CfnYamlLoader)

    assert data == {"Value": {"Fn::Sub": "${AWS::StackName}-bucket"}}


def test_getatt_scalar_becomes_fn_getatt_mapping():
    text = "Value: !GetAtt MyBucket.Arn"
    data = yaml.load(text, Loader=CfnYamlLoader)

    assert data == {"Value": {"Fn::GetAtt": "MyBucket.Arn"}}


def test_importvalue_scalar_becomes_fn_importvalue_mapping():
    text = "Value: !ImportValue SharedVpcId"
    data = yaml.load(text, Loader=CfnYamlLoader)

    assert data == {"Value": {"Fn::ImportValue": "SharedVpcId"}}


def test_base64_scalar_becomes_fn_base64_mapping():
    text = "UserData: !Base64 hello"
    data = yaml.load(text, Loader=CfnYamlLoader)

    assert data == {"UserData": {"Fn::Base64": "hello"}}


def test_getazs_empty_string_scalar():
    text = "Value: !GetAZs ''"
    data = yaml.load(text, Loader=CfnYamlLoader)

    assert data == {"Value": {"Fn::GetAZs": ""}}


def test_transform_scalar_becomes_fn_transform_mapping():
    text = "Value: !Transform AWS::Include"
    data = yaml.load(text, Loader=CfnYamlLoader)

    assert data == {"Value": {"Fn::Transform": "AWS::Include"}}