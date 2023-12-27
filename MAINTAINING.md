# Maintainer's Handbook
## Make a new release


1. Checkout main branch, ensure you have all tags
2. Figure out the next version
3. Update code ([setup.py](setup.py), [CHANGELOG.md](CHANGELOG.md))
4. Pull Request with the version bump.
5. Create tag and release on the merge commit with the changelog

```sh
# Ensure you're on the current `main` branch and have all release tags
git checkout main
git pull origin --tags
```

The new release will be built by GitHub Actions and automatically uploaded to PyPi.
