# Contributing guide

To contribute to this project, you'll need [Poetry](https://python-poetry.org/).

```sh
poetry install --with dev

# run tests
poetry run pytest
```

We're also using [tox](https://tox.wiki) to run the tests in all supported environments. Running the full test suite is simple:

```sh
tox
```

If you'd like to run tests in a specific environment, use `-e`:
```sh
tox -e django42
```
