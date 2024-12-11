#!/bin/bash

# Extract version from extension.toml
VERSION=$(grep 'version = ' extension.toml | cut -d '"' -f 2)

if [ -z "$VERSION" ]; then
    echo "Error: Could not find version in extension.toml"
    exit 1
fi

echo "Creating release v$VERSION..."

# Create and push git tag
git tag -a "v$VERSION" -m "Release v$VERSION"
git push origin "v$VERSION"

echo "Release v$VERSION created and pushed!"
echo "Check GitHub Actions for the release progress: https://github.com/jenslys/zed-catppuccin-blur/actions"
