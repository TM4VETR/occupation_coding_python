import argparse
import sys

from occupation_coding import code_occupations


def main(occupation: str):
    """ CLI entrypoint """
    results = code_occupations([occupation])
    print(results)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Queries an occupational code using the R package by (Schierholz et al., 2021).",
        epilog="Example: python run.py --occupation 'Bürokauffrau'",
    )
    parser.add_argument(
        "-o", "--occupation",
        help="Job title to match (required)",
        required=True,
    )
    args = parser.parse_args()

    occupation = args.occupation.strip()
    if not occupation:
        print("Please provide a valid occupation name.")
        sys.exit(1)

    main(occupation)
