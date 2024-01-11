import argparse
import subprocess
import sys


class dbGaPFileFetcher:

    def __init__(self, ngc_file, prefetch, cart):
        """Initialize the dbGaPFileFetcher.

        Args:
            ngc_file (str): The path to the ngc file containing the project key.
            prefetch (str): The path to the prefetch executable.
        """
        self.ngc_file = ngc_file
        self.prefetch = prefetch
        self.cart = cart
        # self.manifest = manifest

    def download_files(self):
        """Download files from dbGaP using a kart file.

        Args:
            cart (str): The path to the cart file.
            manifest (str): The path to the manifest file.
            verbose (bool): Print more information.
        """
        cmd = "{prefetch} --ngc {ngc} --order kart --cart {cart}".format(
            prefetch=self.prefetch,
            ngc=self.ngc_file,
            cart=self.cart,
        )
        print(cmd)

        returned_value = subprocess.call(cmd, shell=True)
        sys.exit(returned_value)


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

    print("hello world!")

    fetcher = dbGaPFileFetcher(args.ngc, args.prefetch, args.cart)
    fetcher.download_files()
