#!/bin/bash

# Hardcoded GCS bucket and object path
GCS_BUCKET="truthfulness-check-asset"
GCS_OBJECT_PATH="binary"

# Read the current version from pyproject.toml
CURRENT_VERSION=$(poetry version --short)

# Display the current version
echo "Current module version: $CURRENT_VERSION"

# Prompt the user for the version bump
read -p "Do you want to bump the version (major/minor/micro/none)? " BUMP_VERSION

if [[ "$BUMP_VERSION" == "major" ]]; then
  # Bump the major version
  IFS='.' read -ra VERSION_PARTS <<< "$CURRENT_VERSION"
  NEW_MAJOR_VERSION=$((VERSION_PARTS[0] + 1))
  NEW_VERSION="$NEW_MAJOR_VERSION.0.0"
elif [[ "$BUMP_VERSION" == "minor" ]]; then
  # Bump the minor version
  IFS='.' read -ra VERSION_PARTS <<< "$CURRENT_VERSION"
  NEW_MINOR_VERSION=$((VERSION_PARTS[1] + 1))
  NEW_VERSION="${VERSION_PARTS[0]}.$NEW_MINOR_VERSION.0"
elif [[ "$BUMP_VERSION" == "micro" ]]; then
  # Bump the micro version
  IFS='.' read -ra VERSION_PARTS <<< "$CURRENT_VERSION"
  NEW_MICRO_VERSION=$((VERSION_PARTS[2] + 1))
  NEW_VERSION="${VERSION_PARTS[0]}.${VERSION_PARTS[1]}.$NEW_MICRO_VERSION"
else
  # Keep the same version
  NEW_VERSION="$CURRENT_VERSION"
fi

# Update pyproject.toml with the new version
poetry version $NEW_VERSION

# Build the wheel distribution
poetry build --format wheel

# Determine the wheel file name with the new version
WHEEL_FILES=(dist/*$NEW_VERSION*.whl)

# Ensure there is exactly one matching wheel file
if [[ ${#WHEEL_FILES[@]} -ne 1 ]]; then
  echo "Error: Expected one matching wheel file, but found ${#WHEEL_FILES[@]}."
  exit 1
fi

# Extract just the filename (without the 'dist/' directory)
BASENAME=$(basename "${WHEEL_FILES[0]}")

# Upload the wheel file to the GCS bucket
gsutil cp "${WHEEL_FILES[0]}" "gs://$GCS_BUCKET/$GCS_OBJECT_PATH/$BASENAME"

# Generate and print the pip install command
GCS_URL="https://storage.mtls.cloud.google.com/$GCS_BUCKET/$GCS_OBJECT_PATH/$BASENAME"
echo "pip install $GCS_URL"
