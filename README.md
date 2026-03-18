# yamlbridge

Bridge vendor-specific YAML into standard Python objects.

`yamlbridge` provides PyYAML-compatible loaders for YAML dialects that generic YAML parsers cannot handle directly.

The primary goal is simple: let SDEs keep using familiar `yaml.load(..., Loader=...)` patterns while adding support for product-specific YAML syntax such as AWS CloudFormation intrinsic tags.

## Why yamlbridge exists

Many tools use YAML as a base format, then extend it with their own syntax.

A standard YAML loader works for plain YAML, but it often fails on real-world configuration files that contain product-specific constructs.

Examples include:

* AWS CloudFormation intrinsics such as `!Ref`, `!Sub`, and `!GetAtt`
* GitLab CI custom tags such as `!reference`
* Ansible Vault tagged values such as `!vault`
* Docker Compose merge tags such as `!override` and `!reset`

For these files, Python tooling often ends up doing one of three things:

1. failing to parse the file,
2. dropping dialect-specific meaning, or
3. reimplementing custom parsing logic in every project.

`yamlbridge` provides reusable compatibility loaders instead.

## Design goals

* Work naturally with PyYAML
* Support YAML dialects that are syntactically incompatible with generic loaders
* Normalize dialect-specific syntax into predictable Python objects
* Provide safe, reusable building blocks for developer tooling
* Stay practical for SDE workflows such as validation, analysis, migration, and code generation

## Non-goals

`yamlbridge` is not intended to replace the native behavior of products like CloudFormation or GitLab.

It is intended to make their YAML files loadable and usable inside Python applications.

## Installation

```bash
pip install yamlbridge
```

## Quick start

### CloudFormation with PyYAML

```python
import yaml
from yamlbridge import CfnYamlLoader

with open("template.yaml", "r", encoding="utf-8") as yaml_file:
    data = yaml.load(yaml_file, Loader=CfnYamlLoader)
```

This is the primary usage model for `yamlbridge`.

It is designed to fit into codebases that already use PyYAML, without forcing a new parsing API.

### Example

Input:

```yaml
Resources:
  MyBucket:
    Type: AWS::S3::Bucket
Outputs:
  BucketName:
    Value: !Ref MyBucket
  BucketArn:
    Value: !GetAtt MyBucket.Arn
```

Code:

```python
import yaml
from yamlbridge import CfnYamlLoader

text = """
Resources:
  MyBucket:
    Type: AWS::S3::Bucket
Outputs:
  BucketName:
    Value: !Ref MyBucket
  BucketArn:
    Value: !GetAtt MyBucket.Arn
"""

data = yaml.load(text, Loader=CfnYamlLoader)
print(data)
```

Output:

```python
{
    "Resources": {
        "MyBucket": {
            "Type": "AWS::S3::Bucket"
        }
    },
    "Outputs": {
        "BucketName": {
            "Value": {
                "Ref": "MyBucket"
            }
        },
        "BucketArn": {
            "Value": {
                "Fn::GetAtt": "MyBucket.Arn"
            }
        }
    }
}
```

## Core API

### Loader classes

`yamlbridge` exposes dialect-specific loader classes that can be passed directly into PyYAML.

```python
import yaml
from yamlbridge import CfnYamlLoader

with open("template.yaml", "r", encoding="utf-8") as f:
    data = yaml.load(f, Loader=CfnYamlLoader)
```

Planned loader classes include:

* `CfnYamlLoader`
* `GitlabYamlLoader`
* `AnsibleVaultYamlLoader`
* `ComposeYamlLoader`

### Optional convenience helpers

For users who want a higher-level API, `yamlbridge` may also expose helper functions such as:

```python
from yamlbridge import load, loads
```

But the main API is the PyYAML-compatible loader model.

## Normalization model

Where possible, `yamlbridge` converts dialect-specific syntax into standard Python representations.

For CloudFormation, short tags are normalized into the long-form intrinsic representation.

Examples:

* `!Ref MyResource` becomes `{"Ref": "MyResource"}`
* `!Sub "${AWS::StackName}-bucket"` becomes `{"Fn::Sub": "${AWS::StackName}-bucket"}`
* `!GetAtt MyBucket.Arn` becomes `{"Fn::GetAtt": "MyBucket.Arn"}`

This makes downstream tooling simpler because consumers can operate on one predictable object model.

## Supported and planned dialects

Initial focus is on YAML dialects that are syntactically incompatible with generic loaders.

Target dialects include:

* CloudFormation
* GitLab CI
* Ansible Vault-tagged YAML
* Docker Compose merge-tag syntax

## Who should use yamlbridge

`yamlbridge` is useful for SDEs building:

* static analysis tools
* policy validators
* linters
* migration tools
* code generators
* internal deployment platforms
* config visualization tools
* compliance scanners
* IDE and editor tooling

## Example use cases

### Build a CloudFormation linter

Parse templates containing intrinsic tags without hand-writing custom YAML constructors in every project.

### Normalize templates into JSON-compatible structures

Convert product-specific YAML syntax into plain Python dicts and lists before validation or export.

### Support multiple YAML dialects in one internal platform

Use a consistent loader-based model across repositories and teams.

### Add your company’s internal YAML dialect

Create a custom loader for internal tags or syntax without replacing your entire YAML stack.

## Extending yamlbridge

`yamlbridge` is designed to support additional dialect loaders over time.

Conceptually, each dialect defines:

* what custom syntax it accepts,
* how incompatible nodes are constructed,
* how vendor-specific features are normalized, and
* what guarantees it provides to downstream code.

A future extension API may look like this:

```python
from yamlbridge import register_loader

register_loader("mycompany", MyCompanyYamlLoader)
```

## Safety

`yamlbridge` is intended for compatibility loading, not arbitrary object deserialization.

The default design should stay suitable for developer tooling, CI systems, and automation that may need to inspect untrusted or semi-trusted YAML sources.

## Roadmap

* Stable `CfnYamlLoader`
* GitLab CI custom tag support
* Ansible Vault tag-aware loading
* Docker Compose merge-tag support
* Better errors with file and line context
* Optional convenience functions such as `load()` and `loads()`
* Extension API for custom dialect loaders
* Optional advanced representations for tooling use cases

## Status

Early-stage project.

The first priority is a clean, reliable loader API that feels natural to PyYAML users.

## Contributing

Issues and pull requests are welcome.

If you want support for a new YAML dialect, open an issue with:

* the product or ecosystem,
* a sample file that fails with a generic loader,
* the incompatible syntax involved, and
* the Python representation you would expect after loading.

## License

MIT
