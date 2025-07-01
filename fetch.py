"""Script to fetch files from dbGaP using sratoolkit prefetch with a kart file."""

import argparse
import csv
import os
import shutil
import subprocess
import sys
import tempfile


class dbGaPFileFetcher:
    """Class to fetch files from dbGaP using sratoolkit prefetch with a kart file."""

    def __init__(self, ngc_file, prefetch, output_dir="dbgap_fetch_output"):
        """Initialize the dbGaPFileFetcher.

        Args:
            ngc_file (str): The path to the ngc file containing the project key.
            prefetch (str): The path to the prefetch executable.
            output_dir (str): The directory where files should be saved. (default: "dbgap_fetch_output"
        """
        self.ngc_file = os.path.abspath(ngc_file)
        self.prefetch = os.path.abspath(prefetch)
        self.output_dir = os.path.abspath(output_dir)

    def download_files(self, cart, verify='yes', n_retries=3, untar=False):
        """Download files from dbGaP using a kart file. Because prefetch sometimes fails to download a file
        but does not report an error, this method will retry downloading the cart a number of times.

        Args:
            cart (str): The path to the cart file.
            n_retries (int): The number of times to retry downloading the cart.

        Optional arguments:
            manifest (str): The path to the manifest file. If this is provided, the method will check
                            that each file was successfully downloaded.
            n_files (int): The number of files that should be downloaded. If this is provided, the method will
                           check that this many files were downloaded.
        """
        cart_file = os.path.abspath(cart)
        # Get the manifest from the cart file.
        manifest = self._read_manifest_from_cart(cart_file)
        # Work in a temporary directory to do the downloading.
        original_working_directory = os.getcwd()
        with tempfile.TemporaryDirectory() as temp_dir:
            os.chdir(temp_dir)
            # Download the files
            all_files_downloaded = False
            i = 1
            while not all_files_downloaded:
                print("Attempt {}/{} to download files.".format(i, n_retries))
                self._run_prefetch(cart_file, verify)
                if i == n_retries:
                    print("Failed to download all files.")
                    return True # Continue anyway
                all_files_downloaded = self._check_prefetch_against_manifest(
                    temp_dir, manifest
                )
                i = i + 1
            if untar:
                self._untar(temp_dir)
            # Copy files to the output directory
            os.chdir(original_working_directory)
            shutil.copytree(
                temp_dir, self.output_dir, copy_function=shutil.move, dirs_exist_ok=True
            )
            return True

    def _read_manifest_from_cart(self, cart_file):
        """Run the prefetch command to get the list of files from the cart file."""
        cmd = ("{prefetch} --cart {cart} --list > tmp.txt").format(
            prefetch=self.prefetch,
            cart=cart_file,
        )

        subprocess.call(cmd, shell=True)

        with open("tmp.txt") as f:
            out = f.readlines()
        # Remove the first and last lines - these are headers and footers.
        out = out[1 : (len(out) - 1)]
        # Split on | and get the 4th element
        manifest = [x.split("|")[3].strip() for x in out]

        return manifest

    def _run_prefetch(self, cart_file, verify):
        """Run the prefetch command to download files from dbGaP."""
        cmd = (
            "{prefetch} "
            "--ngc {ngc} "
            "--order kart "
            "--cart {cart} "
            "--verify {verify} "
            "--max-size 500000000"
        ).format(
            prefetch=self.prefetch,
            ngc=self.ngc_file,
            cart=cart_file,
            verify=verify,
        )
        if self.output_dir:
            cmd += " --output-directory {}".format(self.output_dir)

        print(cmd)
        returned_value = subprocess.call(cmd, shell=True)
        return returned_value

    def _check_prefetch_against_manifest(self, directory, manifest):
        """Check that prefetch downloaded all the files in the manifest."""
        expected_files = manifest
        downloaded_files = os.listdir(directory)
        print("Found downloaded files:")
        print(sorted(downloaded_files))
        print(
            "Expected {} files; found {} files.",
            len(expected_files),
            len(downloaded_files),
        )
        return set(downloaded_files) == set(expected_files)

    def _untar(self, directory):
        """Untar all tar files in the directory."""
        print("Untarring files.")
        tar_files = [
            f
            for f in os.listdir(directory)
            if f.endswith(".tar") or f.endswith(".tar.gz")
        ]
        for f in tar_files:
            extract_directory = os.path.join(directory, f.split(".tar")[0])
            os.mkdir(os.path.join(extract_directory))
            cmd = "tar -xvf {} -C {}".format(f, extract_directory)
            print(cmd)
            returned_value = subprocess.call(cmd, shell=True)
            if returned_value != 0:
                print("Failed to untar {}".format(f))
                raise RuntimeError("Failed to untar {}".format(f))
            # Remove the tar archive.
            os.remove(os.path.join(directory, f))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Fetches files from dbGaP using a kart file.",
        prog="fetch",
    )
    # Required arguments.
    parser.add_argument(
        "--ngc",
        help="The path to the ngc file containing the project key.",
        required=True,
    )
    parser.add_argument("--cart", help="The cart file to use.", required=True)
    parser.add_argument("--verify", help="Whether to verify the files. [yes|no]", default='yes')
    parser.add_argument(
        "--outdir", help="The directory where files should be saved.", required=True
    )
    # Optional arguments.
    parser.add_argument(
        "--prefetch", help="The path to the prefetch executable.", default="prefetch"
    )
    parser.add_argument(
        "--verbose", help="Print more information.", action="store_true"
    )
    parser.add_argument(
        "--untar",
        help="Untar any tar archives into a directory with the same basename as the archive.",
        action="store_true",
    )

    # Parse.
    args = parser.parse_args()

    # Set up the class.
    fetcher = dbGaPFileFetcher(args.ngc, args.prefetch, args.outdir)
    # Download.
    files_downloaded = fetcher.download_files(args.cart, verify=args.verify, untar=args.untar)
    if not files_downloaded:
        sys.exit(1)
    else:
        print("Files successfully downloaded.")
