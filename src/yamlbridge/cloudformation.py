from collections.abc import Hashable, Mapping, Sequence
from typing import Any, Union

import yaml


class CfnYamlLoader(yaml.SafeLoader):
    """PyYAML-compatible loader for CloudFormation YAML."""


def construct_value(
    loader: CfnYamlLoader, node: yaml.Node
) -> Union[str, Sequence[Any], Mapping[Hashable, Any]]:
    """Construct a Python value from a YAML node.

    Supports scalar, sequence, and mapping nodes. Raises a constructor error
    if the node type is not supported by the current loader.
    """
    value: Union[str, Sequence[Any], Mapping[Hashable, Any]]
    if isinstance(node, yaml.ScalarNode):
        value = loader.construct_scalar(node)
    elif isinstance(node, yaml.SequenceNode):
        value = loader.construct_sequence(node)
    elif isinstance(node, yaml.MappingNode):
        value = loader.construct_mapping(node)
    else:
        raise yaml.constructor.ConstructorError(
            problem="Unsupported YAML node type for CloudFormation intrinsic",
            problem_mark=node.start_mark,
        )
    return value


class GenericYamlConstructor:
    """Shared constructor logic for extended YAML dialects.

    Converts PyYAML nodes into standard Python objects and provides a reusable
    foundation for handling custom YAML tags. Dialect-specific loaders can
    build on this class to normalize non-standard YAML syntax into predictable
    Python representations.
    """

    def __init__(self, transformation_key: str):
        self.transformation_key = transformation_key

    def __call__(
        self, loader: CfnYamlLoader, node: yaml.Node
    ) -> Mapping[str, Union[str, Sequence[Any], Mapping[Hashable, Any]]]:
        value = construct_value(loader, node)
        return {self.transformation_key: value}


CfnYamlLoader.add_constructor("!Ref", GenericYamlConstructor("Ref"))
CfnYamlLoader.add_constructor("!Condition", GenericYamlConstructor("Condition"))

fn_tags = [
    "Transform",
    "Join",
    "Equals",
    "GetAtt",
    "Sub",
    "GetAtt",
    "ImportValue",
    "Base64",
    "GetAZs",
    "Join",
    "If",
    "FindInMap",
    "Select",
    "Split",
    "Equals",
    "And",
    "Or",
    "Not",
    "Cidr",
]

for tag in fn_tags:
    CfnYamlLoader.add_constructor(f"!{tag}", GenericYamlConstructor(f"Fn::{tag}"))
