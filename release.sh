#!/usr/bin/env bash

if [ -z "$1" ]; then
	echo "Please provide a tag."
	echo "Usage: ./release.sh v[X.Y.Z]"
	exit 1
fi

new_version=$1
echo "Preparing $new_version..."

# Convert to proper SemVer only for tauri.conf.json
to_semver() {
	local raw="$1"
	if [[ "$raw" =~ ^([0-9]+\.[0-9]+\.[0-9]+)([a-zA-Z]+)([0-9]+)$ ]]; then
		echo "${BASH_REMATCH[1]}-${BASH_REMATCH[2]}.${BASH_REMATCH[3]}"
	else
		echo "$raw"
	fi
}
semver_version=$(to_semver "$new_version")

# update the pyproject version
uv version "$new_version"

# build the latest version
uv build

# update the tauri.conf.json version (with SemVer-compliant string)
jq --arg new_version "$semver_version" '.version = $new_version' tauri/src-tauri/tauri.conf.json > temp.json && mv temp.json tauri/src-tauri/tauri.conf.json

# update the changelog
git cliff --unreleased --tag "$(uv version --short)" --prepend CHANGELOG.md
git add -A -ip && git commit -m "chore(release): prepare for $new_version"

export GIT_CLIFF_TEMPLATE="\
	{% for group, commits in commits | group_by(attribute=\"group\") %}
	{{ group | upper_first }}\
	{% for commit in commits %}
		- {% if commit.breaking %}(breaking) {% endif %}{{ commit.message | upper_first }} ({{ commit.id | truncate(length=7, end=\"\") }})\
	{% endfor %}
	{% endfor %}"

# create a signed tag
git tag "v$new_version"

echo "Done!"
echo "Now push the commit (git push) and the tag (git push --tags)."
