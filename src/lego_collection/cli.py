import argparse
import getpass
import sys

from . import auth as auth_mod
from . import build as build_mod


def main():
    parser = argparse.ArgumentParser(
        prog="lego-collection",
        description="Build a local SQLite database of Rebrickable LEGO data and your personal set lists.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    auth_parser = sub.add_parser("auth", help="Store Rebrickable credentials")
    auth_parser.set_defaults(func=_cmd_auth)

    build_parser = sub.add_parser("build", help="Build the database")
    build_parser.add_argument(
        "--db",
        default="bricks.db",
        help="Output database path (default: bricks.db)",
    )
    build_parser.set_defaults(func=_cmd_build)

    args = parser.parse_args()
    try:
        args.func(args)
    except (FileNotFoundError, KeyError, RuntimeError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def _cmd_auth(_args):
    api_key = input("Rebrickable API key: ").strip()
    username = input("Rebrickable username: ").strip()
    password = getpass.getpass("Rebrickable password: ").strip()
    if not api_key or not username or not password:
        print("All three fields are required.", file=sys.stderr)
        sys.exit(1)
    auth_mod.write_config(api_key, username, password)
    print(f"Credentials saved to {auth_mod.CONFIG_PATH}")


def _cmd_build(args):
    build_mod.build(args.db)