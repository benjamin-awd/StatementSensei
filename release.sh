#!/usr/bin/env bash

if [ -z "$1" ]; then
	echo "Please provide a tag."
	echo "Usage: ./release.sh v[X.Y.Z]"
	exit 1
fi

new_version=$1
echo "Preparing $new_version..."

# Strip pre-release (e.g., -rc.3) from version for tauri.conf.json
strip_rc() {
	local raw="$1"
	# Remove leading 'v' if present
	raw="${raw#v}"
	# Extract only major.minor.patch
	if [[ "$raw" =~ ^([0-9]+\.[0-9]+\.[0-9]+) ]]; then
		echo "${BASH_REMATCH[1]}"
	else
		echo "$raw"
	fi
}

semver_version=$(strip_rc "$new_version")

# update the pyproject version
uv version "$new_version"

# build the latest version
uv build

# update the tauri.conf.json version
jq --arg new_version "$semver_version" '.version = $new_version' tauri/src-tauri/tauri.conf.json > temp.json && mv temp.json tauri/src-tauri/tauri.conf.json

if [[ "$new_version" == *"rc"* ]]; then
  echo "Skipping changelog for release candidate: $new_version"
else
  # update the changelog
  git cliff --unreleased --tag "$new_version" --prepend CHANGELOG.md
  git add -A -ip && git commit -m "chore(release): prepare for $new_version"
  git add -A -ip && git commit --amend --no-edit
fi

# create a signed tag
git tag "v$new_version"
sh .github/hooks/include_webapp_in_requirements.sh

# override uv default behaviour of creating a gitignore in dist
rm -rf dist/.gitignore

# remove all dist files except the one matching the current version
dist_name="statement_sensei-${new_version}.tar.gz"
dist_path="dist/${dist_name}"
find dist/ -type f -name 'statement_sensei-*.tar.gz' ! -name "$dist_name" -exec rm -v {} +

# If the hook or anything above made changes, add and amend
if ! git diff --quiet; then
  echo "Changes detected after commit, staging and amending commit..."
  git add -A
  git commit --amend --no-edit
  git tag -f "v$new_version"
fi

echo "Done!"
echo "Now push the commit (git push) and the tag (git push --force --tags)."
