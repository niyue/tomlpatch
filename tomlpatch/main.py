#!/usr/bin/env python

import importlib.metadata
import argparse
import sys
from pathlib import Path
from tomlpatch import TomlFileManager, JsonFilePatcher
from tomlpatch.logger import logger

package_metadada = importlib.metadata.metadata("tomlpatch")
# info from pyproject.toml's `version` and `description`
TOML_PATCH_VERSION = package_metadada.get("Version")
TOML_PATCH_SUMMARY = package_metadada.get("Summary")


def _toml_patch_parser():
    parser = argparse.ArgumentParser(prog="tomlpatch")
    parser.add_argument(
        "toml_file",
        type=str,
        help="the path to a toml file to be patched",
    )
    parser.add_argument(
        "json_patch_file",
        type=str,
        help="the path to a json file with the patch",
    )
    return parser


def parse_sys_args(sys_args):
    parser = _toml_patch_parser()
    args = parser.parse_args(sys_args)
    return vars(args)


def main():
    args = parse_sys_args(sys.argv[1:])
    logger.info("toml_file: %s", args["toml_file"])
    toml_file = Path(args["toml_file"])
    json_patch_file = Path(args["json_patch_file"])

    logger.info(f"Applying patch {json_patch_file} to {toml_file}")
    with TomlFileManager(toml_file, toml_file) as patcher:
        JsonFilePatcher().patch(patcher, json_patch_file)
    logger.info(f"Patch applied to {toml_file}")


if __name__ == "__main__":
    main()
