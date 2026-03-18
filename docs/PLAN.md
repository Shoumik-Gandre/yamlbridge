## Milestone 0 — Repository Foundation

### Issue: Initialize the package skeleton

* [ ] Create `src/`-based project layout
* [ ] Add `src/yamlbridge/__init__.py`
* [ ] Add `src/yamlbridge/cloudformation.py`
* [ ] Add `src/yamlbridge/exceptions.py`
* [ ] Add `tests/` directory
* [ ] Add `README.md`
* [ ] Add `LICENSE`

### Issue: Set up packaging and local development

* [ ] Add `pyproject.toml`
* [ ] Define package metadata for `yamlbridge`
* [ ] Configure build backend
* [ ] Add dependency on `PyYAML`
* [ ] Add optional dev dependencies
* [ ] Verify package installs in editable mode

### Issue: Set up code quality tooling

* [ ] Add `pytest`
* [ ] Add `ruff`
* [ ] Add `mypy` or `pyright`
* [ ] Add formatting/lint config to `pyproject.toml`
* [ ] Add a simple local developer workflow

### Issue: Set up CI

* [ ] Add GitHub Actions workflow for tests
* [ ] Run tests on push
* [ ] Run tests on pull request
* [ ] Test multiple Python versions
* [ ] Run lint checks in CI
* [ ] Run type checks in CI

---

## Milestone 1 — Public API and First Red-Green Cycle

### Issue: Define the v0.1 scope

* [ ] Document v0.1 goals
* [ ] Document non-goals
* [ ] Lock first dialect to CloudFormation
* [ ] Decide safe-loading-only policy
* [ ] Decide normalization contract for CloudFormation short tags

### Issue: Add first public API tests

* [ ] Test `from yamlbridge import CfnYamlLoader`
* [ ] Test `yaml.load(..., Loader=CfnYamlLoader)` works
* [ ] Test `CfnYamlLoader` subclasses `yaml.SafeLoader`

### Issue: Implement minimal `CfnYamlLoader`

* [ ] Create `CfnYamlLoader(yaml.SafeLoader)`
* [ ] Export `CfnYamlLoader` from `yamlbridge.__init__`
* [ ] Make import path stable for README examples

---

## Milestone 2 — CloudFormation Core Parsing

### Issue: Support `!Ref`

* [ ] Add failing test for scalar `!Ref MyBucket`
* [ ] Add failing test for nested `!Ref` inside template structure
* [ ] Verify plain YAML still loads unchanged
* [ ] Implement minimal constructor logic for `!Ref`

### Issue: Add generic CloudFormation tag construction

* [ ] Add failing tests for multiple CFN tags
* [ ] Implement a multi-constructor for `!Tag`
* [ ] Normalize `!Ref` to `{"Ref": value}`
* [ ] Normalize non-`Ref` tags to `{"Fn::Tag": value}` where appropriate

### Issue: Handle YAML node kinds correctly

* [ ] Add tests for scalar tagged nodes
* [ ] Add tests for sequence tagged nodes
* [ ] Add tests for mapping tagged nodes
* [ ] Implement scalar node construction
* [ ] Implement sequence node construction
* [ ] Implement mapping node construction

---

## Milestone 3 — CloudFormation Intrinsic Coverage

### Issue: Support common scalar-style intrinsics

* [ ] Add tests for `!Sub`
* [ ] Add tests for `!GetAtt`
* [ ] Add tests for `!ImportValue`
* [ ] Implement support for these tags

### Issue: Support common sequence-style intrinsics

* [ ] Add tests for `!Join`
* [ ] Add tests for `!If`
* [ ] Add tests for `!FindInMap`
* [ ] Add tests for `!Select`
* [ ] Add tests for `!Split`
* [ ] Implement support for these tags

### Issue: Support condition and logic intrinsics

* [ ] Add tests for `!Equals`
* [ ] Add tests for `!And`
* [ ] Add tests for `!Or`
* [ ] Add tests for `!Not`
* [ ] Add tests for `!Condition`
* [ ] Implement support for these tags

### Issue: Support additional CloudFormation intrinsics

* [ ] Add tests for `!Base64`
* [ ] Add tests for `!Cidr`
* [ ] Add tests for `!GetAZs`
* [ ] Add tests for `!Transform`
* [ ] Implement support for these tags

---

## Milestone 4 — Normalization Contract

### Issue: Formalize normalization behavior

* [ ] Document the normalization model
* [ ] Add tests for all supported short-form to long-form conversions
* [ ] Verify `!Ref X` becomes `{"Ref": "X"}`
* [ ] Verify `!Sub ...` becomes `{"Fn::Sub": ...}`
* [ ] Verify `!GetAtt X.Arn` becomes `{"Fn::GetAtt": "X.Arn"}`
* [ ] Verify sequence-based intrinsics normalize consistently

### Issue: Decide and enforce unknown tag policy

* [ ] Decide whether to allow unknown `!Tag` values
* [ ] Decide whether to raise a custom `YamlBridgeError`
* [ ] Add tests for misspelled CFN tags
* [ ] Add tests for unsupported tags
* [ ] Implement chosen behavior consistently

---

## Milestone 5 — Real Template Compatibility

### Issue: Add realistic CloudFormation fixture tests

* [ ] Add fixture for minimal S3 bucket template
* [ ] Add fixture for parameters and outputs
* [ ] Add fixture for conditions
* [ ] Add fixture for mappings
* [ ] Add fixture for nested intrinsic functions
* [ ] Add fixture for IAM example
* [ ] Add fixture for Lambda example

### Issue: Validate nested intrinsic behavior

* [ ] Add tests for nested `!Sub` usage
* [ ] Add tests for nested `!ImportValue`
* [ ] Add tests for nested `!If`
* [ ] Add tests for mixed plain YAML and CFN tags
* [ ] Confirm normalization remains predictable

---

## Milestone 6 — Robustness and Failure Modes

### Issue: Add malformed-input tests

* [ ] Add tests for invalid YAML syntax
* [ ] Add tests for malformed tagged nodes
* [ ] Add tests for invalid sequence structures
* [ ] Add tests for empty tagged values where relevant
* [ ] Ensure parser errors are understandable

### Issue: Add edge-case tests

* [ ] Add tests for `!GetAtt Resource.Attribute`
* [ ] Add tests for `!GetAZs ''`
* [ ] Add tests for booleans inside tagged values
* [ ] Add tests for numbers inside tagged values
* [ ] Add tests for anchors and aliases mixed with CFN tags
* [ ] Add tests for comments and blank lines

### Issue: Add regression-test workflow

* [ ] Create `tests/regressions/`
* [ ] Add regression test template/pattern
* [ ] Require every parser bug fix to include a regression test

---

## Milestone 7 — Optional Helper APIs

### Issue: Add convenience loading helpers

* [ ] Design `yamlbridge.load(...)`
* [ ] Design `yamlbridge.loads(...)`
* [ ] Keep helper API secondary to loader classes
* [ ] Add tests for file-path or file-like handling
* [ ] Add tests for string input handling
* [ ] Export helpers from top-level package

### Issue: Preserve PyYAML-first ergonomics

* [ ] Ensure docs still lead with `yaml.load(..., Loader=...)`
* [ ] Ensure helpers do not obscure the main loader API
* [ ] Keep naming consistent with PyYAML expectations

---

## Milestone 8 — Documentation and Release Readiness

### Issue: Align README with real behavior

* [ ] Verify every README example runs
* [ ] Make `CfnYamlLoader` the primary documented entry point
* [ ] Document normalization examples
* [ ] Document supported tags
* [ ] Document safety posture
* [ ] Document known limitations

### Issue: Add API reference and examples

* [ ] Add examples for string loading
* [ ] Add examples for file loading
* [ ] Add examples for nested CloudFormation intrinsics
* [ ] Add example for failure behavior on unsupported syntax

### Issue: Prepare v0.1 release

* [ ] Choose initial version number
* [ ] Add changelog or release notes
* [ ] Confirm CI is green
* [ ] Confirm test coverage is acceptable
* [ ] Build distribution artifacts
* [ ] Publish to PyPI

---

## Milestone 9 — Future Dialects

### Issue: Design dialect expansion model

* [ ] Decide whether each dialect gets its own loader class
* [ ] Define extension points for future loaders
* [ ] Decide how shared constructor utilities should work
* [ ] Avoid over-engineering before the CFN loader is stable

### Issue: Plan GitLab CI support

* [ ] Research `!reference` semantics
* [ ] Add parser compatibility tests
* [ ] Decide normalization behavior
* [ ] Sketch `GitlabYamlLoader`

### Issue: Plan Ansible Vault support

* [ ] Research `!vault` handling scope
* [ ] Decide parse-only vs decrypt-aware boundaries
* [ ] Sketch `AnsibleVaultYamlLoader`

### Issue: Plan Docker Compose merge-tag support

* [ ] Research `!override` and `!reset`
* [ ] Decide normalization strategy
* [ ] Sketch `ComposeYamlLoader`

---

## Nice-to-have labels

* `milestone:v0.1`
* `area:cloudformation`
* `area:public-api`
* `area:docs`
* `area:ci`
* `area:packaging`
* `type:test`
* `type:feature`
* `type:bug`
* `type:refactor`
* `good first issue`

