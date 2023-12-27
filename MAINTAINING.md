# Maintainer's Handbook
## Make a new release


1. Checkout main branch, ensure you have all tags
2. Figure out the next version
3. Update code ([setup.py](setup.py), [CHANGELOG.md](CHANGELOG.md))
4. Pull Request with the version bump.
5. Create tag and release on the merge commit with the changelog
6. Build release locally for pypi
7. Upload to pypi

```sh
# Ensure you're on the current `main` branch and have all release tags
git checkout main
git pull origin --tags
# build release
python3 -m build --sdist
# upload to pypi
twine upload dist/*
```