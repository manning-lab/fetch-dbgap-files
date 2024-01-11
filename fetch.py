"""Script to fetch files from dbGaP using sratoolkit prefetch with a kart file."""

import argparse
import os
import shutil
import subprocess
import sys
import tempfile


class dbGaPFileFetcher:

    def __init__(self, ngc_file, prefetch, output_dir="."):
        """Initialize the dbGaPFileFetcher.

        Args:
            ngc_file (str): The path to the ngc file containing the project key.
            prefetch (str): The path to the prefetch executable.
        """
        self.ngc_file = os.path.abspath(ngc_file)
        self.prefetch = os.path.abspath(prefetch)
        self.output_dir = os.path.abspath(output_dir)

    def download_files(self, cart, manifest, n_retries=3):
        """Download files from dbGaP using a kart file. Because prefetch sometimes fails to download a file
        but does not report an error, this method will retry downloading the cart a number of times.

        Args:
            cart (str): The path to the cart file.
            manifest (str): The path to the manifest file.
            n_retries (int): The number of times to retry downloading the cart.
        """
        # Work in a temporary directory to do the downloading.
        cart_file = os.path.abspath(cart)
        original_working_directory = os.getcwd()
        with tempfile.TemporaryDirectory() as temp_dir:
            os.chdir(temp_dir)
            # Download the files
            for i in range(n_retries):
                print("Attempt {}/{} to download files.".format(i + 1, n_retries))
                self._run_prefetch(cart_file)
            # Copy files to the output directory
            os.chdir(original_working_directory)
            shutil.copytree(temp_dir, self.output_dir, dirs_exist_ok=True)


    def _run_prefetch(self, cart_file):
        """Run the prefetch command to download files from dbGaP."""
        cmd = "{prefetch} --ngc {ngc} --order kart --cart {cart}".format(
            prefetch=self.prefetch,
            ngc=self.ngc_file,
            cart=cart_file,
        )
        if self.output_dir:
            cmd += " --output-directory {}".format(self.output_dir)
        print(cmd)

        returned_value = subprocess.call(cmd, shell=True)
        return returned_value


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Fetches files from dbGaP using a kart file.",
        prog="fetch",
    )
    # Required arguments.
    parser.add_argument("--ngc", help="The path to the ngc file containing the project key.", required=True)
    parser.add_argument("--cart", help="The cart file to use.", required=True)
    parser.add_argument("--manifest", help="The manifest file to use.", required=True)
    parser.add_argument("--outdir", help="The directory where files should be saved.", required=True)
    # Optional arguments.
    parser.add_argument("--prefetch", help="The path to the prefetch executable.", default="prefetch")
    parser.add_argument("--verbose", help="Print more information.", action="store_true")
    # Parse.
    args = parser.parse_args()

    # Set up the class.
    fetcher = dbGaPFileFetcher(args.ngc, args.prefetch, args.outdir)
    # Download.
    fetcher.download_files(args.cart, args.manifest)
