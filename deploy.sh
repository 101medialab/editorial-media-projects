#!/bin/sh
set -eu
# --- Configuration ---
BUCKET_NAME="campaigns-hypebeast"
CLOUDFRONT_DISTRIBUTION_ID="E314LZW0NLEPEO"

# --- User argument
path="${1:-}"
build_output_dir="${2:-}"
bucket_directory="${3:-}"

if [ -z "$path" ] || [ -z "$build_output_dir" ] || [ -z "$bucket_directory" ]; then
  echo "Usage: $0 <project_path> <build_output_dir> <bucket_directory>" >&2
  exit 1
fi

absolute_output_dir="$path/$build_output_dir"

# Check if the path exists
if [ ! -d "$absolute_output_dir" ]; then
  echo "Error: The specified path '$absolute_output_dir' does not exist." >&2
  exit 1
fi

# A leading or trailing slash would produce a double slash in the S3 prefix and
# in the CloudFront invalidation path, which silently matches nothing.
while [ "${bucket_directory#/}" != "$bucket_directory" ]; do
  bucket_directory="${bucket_directory#/}"
done
while [ "${bucket_directory%/}" != "$bucket_directory" ]; do
  bucket_directory="${bucket_directory%/}"
done

if [ -z "$bucket_directory" ]; then
  echo "Error: The bucket directory is empty after removing slashes." >&2
  exit 1
fi

# `aws s3 sync --delete` mirrors the source exactly, so an empty build output
# would delete every object already deployed. Refuse rather than wipe the
# campaign.
if [ -z "$(find "$absolute_output_dir" -type f -print -quit)" ]; then
  echo "Error: '$absolute_output_dir' contains no files; refusing to sync --delete." >&2
  exit 1
fi

# Unlike `s3 ls`, this succeeds for an empty prefix and fails for API errors.
if aws s3api list-objects-v2 --bucket "$BUCKET_NAME" --prefix "$bucket_directory/" --max-keys 1 --no-paginate > /dev/null 2>&1; then
  echo "Deployment destination $bucket_directory checked."

  printf 'Do you want to proceed? (y/n): '
  if ! IFS= read -r answer; then
    echo "No confirmation received. Deployment cancelled." >&2
    exit 1
  fi

  case "$answer" in
    [yY]es|[yY])
      echo "You agreed."
      ;;
    [nN]o|[nN])
      echo "You disagreed."
      exit 1
      ;;
    *)
      echo "Invalid input. Please enter 'y', 'Y', 'yes', 'Yes', 'n', 'N', or 'no'."
      exit 1
      ;;
  esac
else
  echo "Could not inspect the deployment destination. Deployment cancelled." >&2
  exit 1
fi

# --- Deploy to S3 ---
echo "Deploying to S3..."
aws s3 sync "$absolute_output_dir" "s3://$BUCKET_NAME/$bucket_directory" --delete

# # --- Invalidate CloudFront Cache ---
echo "Invalidating CloudFront cache..."
aws cloudfront create-invalidation --distribution-id "$CLOUDFRONT_DISTRIBUTION_ID" --paths "/$bucket_directory/*"

echo "Deployment complete."
