# CHANGELOG


## v0.4.7 (2024-11-25)

### Bug Fixes

- **permissions**: Make sure to first check the base permissions
  ([`cd6979b`](https://github.com/adfinis/django-generic-api-permissions/commit/cd6979b3c55db4d9d1360249d800b28e7824209f))

Currently we first check the generic permissions and the the views actual base permission. This
  doesn't make sense as we should first check e.g. whether a user is even authenticated before
  checking more specific permissions.

### Chores

- **deps-dev**: Bump pytest-django from 4.8.0 to 4.9.0
  ([`a5ab7d0`](https://github.com/adfinis/django-generic-api-permissions/commit/a5ab7d00707e1db51d3206fce8ca61d40bc73441))

Bumps [pytest-django](https://github.com/pytest-dev/pytest-django) from 4.8.0 to 4.9.0. - [Release
  notes](https://github.com/pytest-dev/pytest-django/releases) -
  [Changelog](https://github.com/pytest-dev/pytest-django/blob/main/docs/changelog.rst) -
  [Commits](https://github.com/pytest-dev/pytest-django/compare/v4.8.0...v4.9.0)

--- updated-dependencies: - dependency-name: pytest-django dependency-type: direct:development
  update-type: version-update:semver-minor ...

Signed-off-by: dependabot[bot] <support@github.com>

- **deps**: Bump djangorestframework from 3.14.0 to 3.15.2
  ([`963cfcb`](https://github.com/adfinis/django-generic-api-permissions/commit/963cfcb6a871c5a2a56e2da9a32c1e59d67ccc29))

Bumps [djangorestframework](https://github.com/encode/django-rest-framework) from 3.14.0 to 3.15.2.
  - [Release notes](https://github.com/encode/django-rest-framework/releases) -
  [Commits](https://github.com/encode/django-rest-framework/compare/3.14.0...3.15.2)

--- updated-dependencies: - dependency-name: djangorestframework dependency-type: direct:production
  update-type: version-update:semver-minor ...

Signed-off-by: dependabot[bot] <support@github.com>

- **deps-dev**: Bump pytest from 8.3.2 to 8.3.3
  ([`3e9059d`](https://github.com/adfinis/django-generic-api-permissions/commit/3e9059d92c4cfe60d865d26f2e971f5d609cf3cd))

Bumps [pytest](https://github.com/pytest-dev/pytest) from 8.3.2 to 8.3.3. - [Release
  notes](https://github.com/pytest-dev/pytest/releases) -
  [Changelog](https://github.com/pytest-dev/pytest/blob/main/CHANGELOG.rst) -
  [Commits](https://github.com/pytest-dev/pytest/compare/8.3.2...8.3.3)

--- updated-dependencies: - dependency-name: pytest dependency-type: direct:development update-type:
  version-update:semver-patch ...

Signed-off-by: dependabot[bot] <support@github.com>

- **deps**: Bump django from 4.2.13 to 4.2.16
  ([`9054023`](https://github.com/adfinis/django-generic-api-permissions/commit/905402353e0a89c7427a1ede92416c1f0c813770))

Bumps [django](https://github.com/django/django) from 4.2.13 to 4.2.16. -
  [Commits](https://github.com/django/django/compare/4.2.13...4.2.16)

--- updated-dependencies: - dependency-name: django dependency-type: direct:production update-type:
  version-update:semver-patch ...

Signed-off-by: dependabot[bot] <support@github.com>

- **deps-dev**: Bump ruff from 0.6.3 to 0.8.0
  ([`b62d896`](https://github.com/adfinis/django-generic-api-permissions/commit/b62d896c8ae8de1513a6ab6e73ae89e1026bc9ac))

Bumps [ruff](https://github.com/astral-sh/ruff) from 0.6.3 to 0.8.0. - [Release
  notes](https://github.com/astral-sh/ruff/releases) -
  [Changelog](https://github.com/astral-sh/ruff/blob/main/CHANGELOG.md) -
  [Commits](https://github.com/astral-sh/ruff/compare/0.6.3...0.8.0)

--- updated-dependencies: - dependency-name: ruff dependency-type: direct:development update-type:
  version-update:semver-minor ...

Signed-off-by: dependabot[bot] <support@github.com>

- **deps-dev**: Bump pytest from 8.2.1 to 8.3.2
  ([`50ece89`](https://github.com/adfinis/django-generic-api-permissions/commit/50ece89b2c20670cd9c6418d0b955ff0fb099226))

Bumps [pytest](https://github.com/pytest-dev/pytest) from 8.2.1 to 8.3.2. - [Release
  notes](https://github.com/pytest-dev/pytest/releases) -
  [Changelog](https://github.com/pytest-dev/pytest/blob/main/CHANGELOG.rst) -
  [Commits](https://github.com/pytest-dev/pytest/compare/8.2.1...8.3.2)

--- updated-dependencies: - dependency-name: pytest dependency-type: direct:development update-type:
  version-update:semver-minor ...

Signed-off-by: dependabot[bot] <support@github.com>

- **deps-dev**: Bump ruff from 0.4.6 to 0.6.3
  ([`773bcd3`](https://github.com/adfinis/django-generic-api-permissions/commit/773bcd336315bbc654e7867d898b3b7a6a511720))

Bumps [ruff](https://github.com/astral-sh/ruff) from 0.4.6 to 0.6.3. - [Release
  notes](https://github.com/astral-sh/ruff/releases) -
  [Changelog](https://github.com/astral-sh/ruff/blob/main/CHANGELOG.md) -
  [Commits](https://github.com/astral-sh/ruff/compare/v0.4.6...0.6.3)

--- updated-dependencies: - dependency-name: ruff dependency-type: direct:development update-type:
  version-update:semver-minor ...

Signed-off-by: dependabot[bot] <support@github.com>

- **deps-dev**: Bump black from 23.12.1 to 24.4.2
  ([`58bf040`](https://github.com/adfinis/django-generic-api-permissions/commit/58bf040e36d6d17ffcd7ab1c0c3a63a71875671e))

Bumps [black](https://github.com/psf/black) from 23.12.1 to 24.4.2. - [Release
  notes](https://github.com/psf/black/releases) -
  [Changelog](https://github.com/psf/black/blob/main/CHANGES.md) -
  [Commits](https://github.com/psf/black/compare/23.12.1...24.4.2)

--- updated-dependencies: - dependency-name: black dependency-type: direct:development update-type:
  version-update:semver-major ...

Signed-off-by: dependabot[bot] <support@github.com>


## v0.4.6 (2024-05-29)

### Bug Fixes

- **permissions**: Extend drf permission methods
  ([`00580d8`](https://github.com/adfinis/django-generic-api-permissions/commit/00580d83c4681df17e366e54942b00b9971ef945))

instead of calling permission in each specific method (create, etc.) call super in
  check_object_permission

### Chores

- **release**: 0.4.6
  ([`04143e4`](https://github.com/adfinis/django-generic-api-permissions/commit/04143e4dcda4aac8eb59d2cb05c0d2236b8fb4a4))

Automatically generated by python-semantic-release

- **deps**: Bump python-semantic-release/python-semantic-release
  ([`d9655f1`](https://github.com/adfinis/django-generic-api-permissions/commit/d9655f17afc86e4c3d58858d639654ebf5495293))

Bumps
  [python-semantic-release/python-semantic-release](https://github.com/python-semantic-release/python-semantic-release)
  from 8.3.0 to 9.7.3. - [Release
  notes](https://github.com/python-semantic-release/python-semantic-release/releases) -
  [Changelog](https://github.com/python-semantic-release/python-semantic-release/blob/master/CHANGELOG.md)
  -
  [Commits](https://github.com/python-semantic-release/python-semantic-release/compare/v8.3.0...v9.7.3)

--- updated-dependencies: - dependency-name: python-semantic-release/python-semantic-release
  dependency-type: direct:production update-type: version-update:semver-major ...

Signed-off-by: dependabot[bot] <support@github.com>

- **deps-dev**: Bump ruff from 0.3.5 to 0.4.6
  ([`c614700`](https://github.com/adfinis/django-generic-api-permissions/commit/c6147003d33376bb06aa27b408a00ff1ad8d5894))

Bumps [ruff](https://github.com/astral-sh/ruff) from 0.3.5 to 0.4.6. - [Release
  notes](https://github.com/astral-sh/ruff/releases) -
  [Changelog](https://github.com/astral-sh/ruff/blob/main/CHANGELOG.md) -
  [Commits](https://github.com/astral-sh/ruff/compare/v0.3.5...v0.4.6)

--- updated-dependencies: - dependency-name: ruff dependency-type: direct:development update-type:
  version-update:semver-minor ...

Signed-off-by: dependabot[bot] <support@github.com>

- **deps-dev**: Bump djangorestframework-jsonapi from 6.1.0 to 7.0.0
  ([`abe4798`](https://github.com/adfinis/django-generic-api-permissions/commit/abe4798e6d81f1549d1caf6ff9e14dff5b682805))

Bumps
  [djangorestframework-jsonapi](https://github.com/django-json-api/django-rest-framework-json-api)
  from 6.1.0 to 7.0.0. - [Release
  notes](https://github.com/django-json-api/django-rest-framework-json-api/releases) -
  [Changelog](https://github.com/django-json-api/django-rest-framework-json-api/blob/main/CHANGELOG.md)
  -
  [Commits](https://github.com/django-json-api/django-rest-framework-json-api/compare/v6.1.0...v7.0.0)

--- updated-dependencies: - dependency-name: djangorestframework-jsonapi dependency-type:
  direct:development update-type: version-update:semver-major ...

Signed-off-by: dependabot[bot] <support@github.com>

- **deps**: Bump django from 4.2.11 to 4.2.13
  ([`33362de`](https://github.com/adfinis/django-generic-api-permissions/commit/33362dec0465739b5506145a8d6ba7dad7970d10))

Bumps [django](https://github.com/django/django) from 4.2.11 to 4.2.13. -
  [Commits](https://github.com/django/django/compare/4.2.11...4.2.13)

--- updated-dependencies: - dependency-name: django dependency-type: direct:production update-type:
  version-update:semver-patch ...

Signed-off-by: dependabot[bot] <support@github.com>

- **deps-dev**: Bump pytest from 8.2.0 to 8.2.1
  ([`90762a1`](https://github.com/adfinis/django-generic-api-permissions/commit/90762a161bf0de2d38c67c0e7f4882605f1b5742))

Bumps [pytest](https://github.com/pytest-dev/pytest) from 8.2.0 to 8.2.1. - [Release
  notes](https://github.com/pytest-dev/pytest/releases) -
  [Changelog](https://github.com/pytest-dev/pytest/blob/main/CHANGELOG.rst) -
  [Commits](https://github.com/pytest-dev/pytest/compare/8.2.0...8.2.1)

--- updated-dependencies: - dependency-name: pytest dependency-type: direct:development update-type:
  version-update:semver-patch ...

Signed-off-by: dependabot[bot] <support@github.com>

- **deps-dev**: Bump pytest from 8.1.1 to 8.2.0
  ([`aaae000`](https://github.com/adfinis/django-generic-api-permissions/commit/aaae0005de84ca778974d192b178705e86aee4cf))

Bumps [pytest](https://github.com/pytest-dev/pytest) from 8.1.1 to 8.2.0. - [Release
  notes](https://github.com/pytest-dev/pytest/releases) -
  [Changelog](https://github.com/pytest-dev/pytest/blob/main/CHANGELOG.rst) -
  [Commits](https://github.com/pytest-dev/pytest/compare/8.1.1...8.2.0)

--- updated-dependencies: - dependency-name: pytest dependency-type: direct:development update-type:
  version-update:semver-minor ...

Signed-off-by: dependabot[bot] <support@github.com>


## v0.4.5 (2024-04-17)

### Bug Fixes

- Don't check permissions for GET requests
  ([#51](https://github.com/adfinis/django-generic-api-permissions/pull/51),
  [`774f259`](https://github.com/adfinis/django-generic-api-permissions/commit/774f2594a56d824f1b5f9bba3d44de15b115f55c))

Permissions should only deal with POST/PATCH/DELETE - GET requests should be entirely governed by
  the visibility layer.

### Chores

- **release**: 0.4.5
  ([`dc7e8e5`](https://github.com/adfinis/django-generic-api-permissions/commit/dc7e8e540c2f1318392f984a8d77c56bd8a99f7f))

Automatically generated by python-semantic-release

- Fix maintenance docs ([#39](https://github.com/adfinis/django-generic-api-permissions/pull/39),
  [`9947377`](https://github.com/adfinis/django-generic-api-permissions/commit/99473779dca83ea5c4affe02f3625683e1b9e1c5))

- Add CONTRIBUTING.md, allow running pytest directly in dev
  ([#50](https://github.com/adfinis/django-generic-api-permissions/pull/50),
  [`4fd4a34`](https://github.com/adfinis/django-generic-api-permissions/commit/4fd4a34b2e7982048f1a4db695a598d214667dcb))

Co-authored-by: Fabio Ambauen <1833932+open-dynaMIX@users.noreply.github.com>

- **deps**: Bump django from 4.2.9 to 4.2.11
  ([`a6b445d`](https://github.com/adfinis/django-generic-api-permissions/commit/a6b445da1d2baaa304d997320ca77c87ed2f0957))

Bumps [django](https://github.com/django/django) from 4.2.9 to 4.2.11. -
  [Commits](https://github.com/django/django/compare/4.2.9...4.2.11)

--- updated-dependencies: - dependency-name: django dependency-type: direct:production update-type:
  version-update:semver-patch ...

Signed-off-by: dependabot[bot] <support@github.com>

- **deps-dev**: Bump ruff from 0.2.2 to 0.3.5
  ([`42d7930`](https://github.com/adfinis/django-generic-api-permissions/commit/42d7930176a5bec01f93159fa8395783a39c8c22))

Bumps [ruff](https://github.com/astral-sh/ruff) from 0.2.2 to 0.3.5. - [Release
  notes](https://github.com/astral-sh/ruff/releases) -
  [Changelog](https://github.com/astral-sh/ruff/blob/main/CHANGELOG.md) -
  [Commits](https://github.com/astral-sh/ruff/compare/v0.2.2...v0.3.5)

--- updated-dependencies: - dependency-name: ruff dependency-type: direct:development update-type:
  version-update:semver-minor ...

Signed-off-by: dependabot[bot] <support@github.com>


## v0.4.4 (2024-03-20)

### Bug Fixes

- Add fallback for queryset of read_only related fields
  ([#38](https://github.com/adfinis/django-generic-api-permissions/pull/38),
  [`9f6ed09`](https://github.com/adfinis/django-generic-api-permissions/commit/9f6ed09b26ee238bdccee401dce8ae4fba5332ff))

Read only fields don't have a queryset (see
  https://github.com/encode/django-rest-framework/blame/77ef27f18fc7c11e1d2e5fd4aaa8acc51cda6792/rest_framework/utils/field_mapping.py#L288),
  so we need to provide a fallback.

### Chores

- **release**: 0.4.4
  ([`d765283`](https://github.com/adfinis/django-generic-api-permissions/commit/d765283ccc338171f5cebf8837e6000cffb8cc93))

Automatically generated by python-semantic-release


## v0.4.3 (2024-03-15)

### Bug Fixes

- **validation**: Fix initialization of validator classes
  ([#37](https://github.com/adfinis/django-generic-api-permissions/pull/37),
  [`f4dae3e`](https://github.com/adfinis/django-generic-api-permissions/commit/f4dae3e457f6444e6cf8ddf4fdd706aed46bb0f4))

### Chores

- **release**: 0.4.3
  ([`f9a4687`](https://github.com/adfinis/django-generic-api-permissions/commit/f9a4687256ab602631453ad7b6aaa782ac20b12e))

Automatically generated by python-semantic-release

- **deps-dev**: Bump ruff from 0.1.11 to 0.2.2
  ([#30](https://github.com/adfinis/django-generic-api-permissions/pull/30),
  [`c40eed7`](https://github.com/adfinis/django-generic-api-permissions/commit/c40eed75567b31f71eb9a998724bd402a1582aed))

Bumps [ruff](https://github.com/astral-sh/ruff) from 0.1.11 to 0.2.2. - [Release
  notes](https://github.com/astral-sh/ruff/releases) -
  [Changelog](https://github.com/astral-sh/ruff/blob/main/CHANGELOG.md) -
  [Commits](https://github.com/astral-sh/ruff/compare/v0.1.11...v0.2.2)

--- updated-dependencies: - dependency-name: ruff dependency-type: direct:development update-type:
  version-update:semver-minor ...

Signed-off-by: dependabot[bot] <support@github.com> Co-authored-by: dependabot[bot]
  <49699333+dependabot[bot]@users.noreply.github.com>

### Documentation

- **readme**: Fix typo in readme
  ([`3a76b16`](https://github.com/adfinis/django-generic-api-permissions/commit/3a76b167e018a9ed2b172431f08a386b1a9edf2c))


## v0.4.2 (2024-01-08)

### Bug Fixes

- Pass correct request param for relationships
  ([`0609f64`](https://github.com/adfinis/django-generic-api-permissions/commit/0609f648a386ff4fe615d21aa120a7a3e9b50acd))

### Chores

- **release**: 0.4.2
  ([`0b7bcc0`](https://github.com/adfinis/django-generic-api-permissions/commit/0b7bcc078b0ea745cab063ee344f5f580d90c382))

Automatically generated by python-semantic-release

- **deps**: Revert semantic release to 8.3.0
  ([`9855045`](https://github.com/adfinis/django-generic-api-permissions/commit/985504522a059fefe2a2aeb44f6b1494bde905a2))

- **deps**: Bump python-semantic-release/python-semantic-release
  ([#16](https://github.com/adfinis/django-generic-api-permissions/pull/16),
  [`25eed91`](https://github.com/adfinis/django-generic-api-permissions/commit/25eed919efaad041353070d35f87795cb9a474fa))

Bumps
  [python-semantic-release/python-semantic-release](https://github.com/python-semantic-release/python-semantic-release)
  from 8.7.0 to 8.7.2. - [Release
  notes](https://github.com/python-semantic-release/python-semantic-release/releases) -
  [Changelog](https://github.com/python-semantic-release/python-semantic-release/blob/master/CHANGELOG.md)
  -
  [Commits](https://github.com/python-semantic-release/python-semantic-release/compare/v8.7.0...v8.7.2)

--- updated-dependencies: - dependency-name: python-semantic-release/python-semantic-release
  dependency-type: direct:production update-type: version-update:semver-patch ...

Signed-off-by: dependabot[bot] <support@github.com> Co-authored-by: dependabot[bot]
  <49699333+dependabot[bot]@users.noreply.github.com>

- **deps**: Bump django from 4.2.8 to 4.2.9
  ([#15](https://github.com/adfinis/django-generic-api-permissions/pull/15),
  [`5410af0`](https://github.com/adfinis/django-generic-api-permissions/commit/5410af0b6c1fce1fc4a08d583953e6298f5c20aa))

Bumps [django](https://github.com/django/django) from 4.2.8 to 4.2.9. -
  [Commits](https://github.com/django/django/compare/4.2.8...4.2.9)

--- updated-dependencies: - dependency-name: django dependency-type: direct:production update-type:
  version-update:semver-patch ...

Signed-off-by: dependabot[bot] <support@github.com> Co-authored-by: dependabot[bot]
  <49699333+dependabot[bot]@users.noreply.github.com>

- **deps-dev**: Bump ruff from 0.1.9 to 0.1.11
  ([#14](https://github.com/adfinis/django-generic-api-permissions/pull/14),
  [`4f80c4f`](https://github.com/adfinis/django-generic-api-permissions/commit/4f80c4f0461149ee5982b884e0a98419b0cea9f3))

Bumps [ruff](https://github.com/astral-sh/ruff) from 0.1.9 to 0.1.11. - [Release
  notes](https://github.com/astral-sh/ruff/releases) -
  [Changelog](https://github.com/astral-sh/ruff/blob/main/CHANGELOG.md) -
  [Commits](https://github.com/astral-sh/ruff/compare/v0.1.9...v0.1.11)

--- updated-dependencies: - dependency-name: ruff dependency-type: direct:development update-type:
  version-update:semver-patch ...

Signed-off-by: dependabot[bot] <support@github.com> Co-authored-by: dependabot[bot]
  <49699333+dependabot[bot]@users.noreply.github.com>

- Change semantic release commit message
  ([`6d39527`](https://github.com/adfinis/django-generic-api-permissions/commit/6d395276bbba71647d87cbc09f71ce29eac64e7c))


## v0.4.1 (2024-01-03)

### Bug Fixes

- Increase min python for flake8
  ([`393b930`](https://github.com/adfinis/django-generic-api-permissions/commit/393b93054371477b73f998ea61ffed29c247de53))

### Chores

- Add python to release action
  ([`9c16fa4`](https://github.com/adfinis/django-generic-api-permissions/commit/9c16fa4eed2402aa4e99f3ae6de522522ec73f01))

- Add poetry to release action
  ([`d76b9d9`](https://github.com/adfinis/django-generic-api-permissions/commit/d76b9d963cb3a77b15f789b28480b1015eb292b7))

- Add build command
  ([`67e2529`](https://github.com/adfinis/django-generic-api-permissions/commit/67e2529ec1a824debc0a706cc642b033f28cd3e0))


## v0.4.0 (2024-01-03)

### Bug Fixes

- Import after app is ready
  ([`db1d1e6`](https://github.com/adfinis/django-generic-api-permissions/commit/db1d1e669f4fab8f7449d690ba7c8a36c51eb75c))

### Chores

- Fix version variable semantic release
  ([`83a33d2`](https://github.com/adfinis/django-generic-api-permissions/commit/83a33d25754883f789df5e69558c96ddaee45446))

- Fix semantic release action version
  ([`3ed75e0`](https://github.com/adfinis/django-generic-api-permissions/commit/3ed75e07f3550a1c27b23254837a53db4ee1418d))

- Fix release.yml ([#13](https://github.com/adfinis/django-generic-api-permissions/pull/13),
  [`6d6a0ee`](https://github.com/adfinis/django-generic-api-permissions/commit/6d6a0eeaffcfd1f90e920c663988f3e11c56db45))

### Features

- Migrate to poetry
  ([`41c9226`](https://github.com/adfinis/django-generic-api-permissions/commit/41c922646b76ee4f2d7b9e2affdf6ddde09a6786))

add sematic release


## v0.3.0 (2023-12-27)

### Bug Fixes

- Improve type checks
  ([`0ee7e0e`](https://github.com/adfinis/django-generic-api-permissions/commit/0ee7e0e53cf895fde4200903e328be3a2e038ec1))

- Prevent overwrite of hidden relations in patch
  ([`7247483`](https://github.com/adfinis/django-generic-api-permissions/commit/72474834f6384a90fc78b92e74d440d56aed7ab5))

- Remove unnecessary get_queryset from RelatedFieldMixin
  ([`15e2ea4`](https://github.com/adfinis/django-generic-api-permissions/commit/15e2ea4ecb34b3935eef5784e1301001947b368a))

- Fix test setup
  ([`a23d244`](https://github.com/adfinis/django-generic-api-permissions/commit/a23d244659f54422a955469a8f976b242af2c238))

- Change MRO for serializer relation fields
  ([`09f13fe`](https://github.com/adfinis/django-generic-api-permissions/commit/09f13fe014ab606a3962deecfcd96113a4d799c6))

- Add more python versions to test
  ([`2d988db`](https://github.com/adfinis/django-generic-api-permissions/commit/2d988db8a828e40bad296b1b79699ded83da21ca))

switch to ruff

- Fix test suite
  ([`7adea9e`](https://github.com/adfinis/django-generic-api-permissions/commit/7adea9e7552f8564020d64acebf9c63865d66a4b))

### Chores

- Release 0.3.0
  ([`4bdbc79`](https://github.com/adfinis/django-generic-api-permissions/commit/4bdbc79b6e804bdf58c4d761f18d78b4a8034765))

### Features

- Filter manytomany relations
  ([`34be60c`](https://github.com/adfinis/django-generic-api-permissions/commit/34be60cdd63adc276eac14108f578f7ce7cfff52))

- Implement foreignkey visibility filtering
  ([`7d01398`](https://github.com/adfinis/django-generic-api-permissions/commit/7d01398073c6058008cc49ab9906d87d5dbd9865))

- Add visibiility mixin for relationships
  ([`545c36a`](https://github.com/adfinis/django-generic-api-permissions/commit/545c36a34480c2b7ed6068aab98aece97e977f88))


## v0.2.0 (2021-08-26)

### Chores

- Version bump 0.2.0
  ([`ac19e5c`](https://github.com/adfinis/django-generic-api-permissions/commit/ac19e5c1565c4de98c8feee5e666f6c5f929c3fe))

- **tests**: Django changes
  ([`53b5352`](https://github.com/adfinis/django-generic-api-permissions/commit/53b5352faeca0afb302682697697f7d5ff8f929d))

Django 5 will set USE_TZ to default and warns if our settings.py doesn't contain it. Also, they
  renamed the master branc to main. Django-latest requires Python 3.8+, so we cannot test that
  combination anymore

### Refactoring

- Unify the code base, add validation
  ([`faa61d2`](https://github.com/adfinis/django-generic-api-permissions/commit/faa61d21c7200c88e33455c6dba2bfac84465012))

Since the code base baseicall does the same for four different objectives, we shouldn't have
  multiple, similar implementations of basically the same things.

This introduces a generic config class that is used to register permission, visibility, and
  validation classes. The interface to using the package has been cleaned up as well: The model
  classes won't need a mixin anymore for either visibility or permissions to work. The permission
  classes don't need to inherit from the `BasePermission` anymore either

There is now a clean import / usage structure to use this package:

* all permissions stuff can be imported from `generic_permissions.permissions` * all visibility
  stuff can be imported from `generic_permissions.visibilities` * all validation stuff can be
  imported from `generic_permissions.validation`


## v0.1.0 (2020-12-18)

### Chores

- Prepare first proper release
  ([`0d5d677`](https://github.com/adfinis/django-generic-api-permissions/commit/0d5d677db07af945447408044720fa5f93ba60c6))

- Prepare metadata for PyPI release
  ([`c89cf9c`](https://github.com/adfinis/django-generic-api-permissions/commit/c89cf9cfe488bd675aa642ebe87a5c76ac8ced46))

### Features

- Add initial implementation
  ([`2a8d8b4`](https://github.com/adfinis/django-generic-api-permissions/commit/2a8d8b4969b6a1917c397b86e8040493f26aa0df))
