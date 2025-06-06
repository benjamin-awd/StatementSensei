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
fi

# create a signed tag
git tag "v$new_version"
sh .github/hooks/include_webapp_in_requirements.sh
rm -rf dist/.gitignore

echo "Done!"
echo "Now push the commit (git push) and the tag (git push --tags)."
