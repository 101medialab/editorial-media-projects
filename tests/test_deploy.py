import os
from pathlib import Path
import subprocess
import tempfile
import unittest


class DeployTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.output = self.root / "build output"
        self.output.mkdir()
        (self.output / "index.html").write_text("<html></html>")
        # A build output with no files at all: `sync --delete` would wipe the
        # campaign, so deploy.sh must refuse before calling aws.
        self.empty = self.root / "empty output"
        self.empty.mkdir()
        self.log = self.root / "calls"
        self.args = self.root / "args"
        aws = self.root / "aws"
        aws.write_text('''#!/bin/sh
printf '%s %s\\n' "$1" "$2" >> "$DEPLOY_TEST_CALLS"
printf '%s\\n' "$*" >> "$DEPLOY_TEST_ARGS"
case "$1 $2" in
  "s3api list-objects-v2")
    printf '{"KeyCount": %s}\\n' "${DEPLOY_TEST_KEY_COUNT:-1}"
    exit "${DEPLOY_TEST_LIST_EXIT:-0}" ;;
  "s3 sync") exit "${DEPLOY_TEST_SYNC_EXIT:-0}" ;;
  "cloudfront create-invalidation") exit "${DEPLOY_TEST_INVALIDATE_EXIT:-0}" ;;
esac
exit 99
''')
        aws.chmod(0o700)

    def deploy(self, answer="y\n", source=None, bucket_directory="test-campaign",
               **statuses):
        result = subprocess.run(
            ["/bin/sh", str(Path(__file__).resolve().parents[1] / "deploy.sh"),
             str(source or self.output), ".", bucket_directory],
            input=answer, text=True, capture_output=True,
            env={**os.environ, "PATH": str(self.root) + ":/usr/bin:/bin",
                 "DEPLOY_TEST_CALLS": str(self.log),
                 "DEPLOY_TEST_ARGS": str(self.args), **statuses},
        )
        calls = self.log.read_text().splitlines() if self.log.exists() else []
        args = self.args.read_text().splitlines() if self.args.exists() else []
        return result, calls, args

    def assertFailed(self, result):
        self.assertNotEqual(0, result.returncode)
        self.assertNotIn("Deployment complete.", result.stdout)

    def test_unconfirmed_deployments_never_upload(self):
        for answer in ["n\n", "invalid\n", "\n", ""]:
            with self.subTest(answer=answer):
                self.log.unlink(missing_ok=True)
                result, calls, _ = self.deploy(answer)
                self.assertFailed(result)
                self.assertEqual(["s3api list-objects-v2"], calls)

    def test_destination_lookup_failure_stops(self):
        result, calls, _ = self.deploy(DEPLOY_TEST_LIST_EXIT="7")
        self.assertFailed(result)
        self.assertEqual(["s3api list-objects-v2"], calls)

    def test_upload_failure_does_not_invalidate_cache(self):
        result, calls, _ = self.deploy(DEPLOY_TEST_SYNC_EXIT="9")
        self.assertFailed(result)
        self.assertEqual(["s3api list-objects-v2", "s3 sync"], calls)

    def test_invalidation_failure_is_not_success(self):
        result, calls, _ = self.deploy(DEPLOY_TEST_INVALIDATE_EXIT="8")
        self.assertFailed(result)
        self.assertEqual(["s3api list-objects-v2", "s3 sync", "cloudfront create-invalidation"], calls)

    def test_success_requires_both_commands(self):
        result, calls, _ = self.deploy()
        self.assertEqual(0, result.returncode)
        self.assertIn("Deployment complete.", result.stdout)
        self.assertEqual(["s3api list-objects-v2", "s3 sync", "cloudfront create-invalidation"], calls)

    def test_empty_destination_can_be_deployed_with_confirmation(self):
        result, calls, _ = self.deploy(DEPLOY_TEST_KEY_COUNT="0")
        self.assertEqual(0, result.returncode)
        self.assertEqual(["s3api list-objects-v2", "s3 sync", "cloudfront create-invalidation"], calls)

    def test_empty_output_dir_never_syncs(self):
        result, calls, _ = self.deploy(source=self.empty)
        self.assertFailed(result)
        self.assertIn("contains no files", result.stderr)
        self.assertEqual([], calls)

    def test_missing_path_is_rejected_without_calling_aws(self):
        result, calls, _ = self.deploy(source=self.root / "does not exist")
        self.assertFailed(result)
        self.assertEqual([], calls)

    def test_missing_arguments_print_usage(self):
        result = subprocess.run(
            ["/bin/sh", str(Path(__file__).resolve().parents[1] / "deploy.sh")],
            text=True, capture_output=True,
        )
        self.assertNotEqual(0, result.returncode)
        self.assertIn("Usage:", result.stderr)

    def test_bucket_directory_slashes_are_normalized(self):
        for given in ["test-campaign/", "/test-campaign", "/test-campaign/"]:
            with self.subTest(given=given):
                self.log.unlink(missing_ok=True)
                self.args.unlink(missing_ok=True)
                result, _, args = self.deploy(bucket_directory=given)
                self.assertEqual(0, result.returncode)
                self.assertTrue(any(a.startswith("s3 sync ") and
                                    a.endswith("s3://campaigns-hypebeast/test-campaign --delete")
                                    for a in args), args)
                self.assertIn("cloudfront create-invalidation --distribution-id "
                              "E314LZW0NLEPEO --paths /test-campaign/*", args)
                self.assertNotIn("//", " ".join(args).replace("s3://", ""))


if __name__ == "__main__":
    unittest.main()
