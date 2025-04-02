#!/bin/sh
# --- Configuration ---
BUCKET_NAME="campaigns-hypebeast"
CLOUDFRONT_DISTRIBUTION_ID="E314LZW0NLEPEO"

# --- User argument
path="$1"
build_output_dir="$2"
bucket_directory="$3"

absolute_output_dir="$path/$build_output_dir"

# Check if the path exists
if [ ! -e "$absolute_output_dir" ]; then
  echo "Error: The specified path '$absolute_output_dir' does not exist."
  exit 1
fi

if [ -z "$bucket_directory" ]; then
  echo "Error: The bucket directory is not given."
  exit 1
fi

# --- Check if given directory is not empty ---
if aws s3 ls s3://$BUCKET_NAME/$bucket_directory/ > /dev/null 2>&1; then
  echo "Directory $bucket_directory exists (or has contents)."

  read -p "Do you want to proceed? (y/n): " answer

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
      ;;
  esac
fi

# --- Deploy to S3 ---
echo "Deploying to S3..."
aws s3 sync "$absolute_output_dir" "s3://$BUCKET_NAME/$bucket_directory" --delete

# # --- Invalidate CloudFront Cache ---
echo "Invalidating CloudFront cache..."
aws cloudfront create-invalidation --distribution-id "$CLOUDFRONT_DISTRIBUTION_ID" --paths "/$bucket_directory/*"

echo "Deployment complete."
