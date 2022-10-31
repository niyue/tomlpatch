from os import close
import tomli
import tomli_w
from dotty_dict import dotty
import json


class TomlPatcher:
    def __init__(self, toml: dict):
        self.toml = toml

    def patch(self, patched_toml: dict) -> dict:
        dotty_toml = dotty(self.toml)
        for key, value in patched_toml.items():
            if value is None:
                # remove the key if the value is None
                dotty_toml.pop(key, None)
            else:
                dotty_toml[key] = value
        self.toml = dotty_toml.to_dict()
        return self.toml

    def extend_list(self, key, value) -> dict:
        dotted_toml = dotty(self.toml)
        dotted_toml[key].extend(value)
        self.toml = dotted_toml.to_dict()
        return self.toml

    def remove_list(self, key, value) -> dict:
        dotted_toml = dotty(self.toml)
        dotted_toml[key] = [v for v in dotted_toml[key] if v not in value]
        self.toml = dotted_toml.to_dict()
        return self.toml

    @property
    def patched_toml(self) -> dict:
        return self.toml


class TomlFileManager:
    def __init__(self, toml_file_path, patched_toml_file_path=None):
        self.toml_file_path = toml_file_path
        self.patched_toml_file_path = patched_toml_file_path
        self.patcher = None

    def __enter__(self):
        with open(self.toml_file_path, "rb") as toml_file:
            toml_dict = tomli.load(toml_file)
            self.patcher = TomlPatcher(toml_dict)
            return self.patcher

    def __exit__(self, exc_type, exc_value, exc_traceback):
        patched_toml_file_path = self.patched_toml_file_path or self.toml_file_path
        with open(patched_toml_file_path, "wb") as patched_toml_file:
            tomli_w.dump(self.patcher.patched_toml, patched_toml_file)


class JsonFilePatcher:
    def __init__(self):
        pass

    def patch(self, patcher, json_patch_file_path):
        with open(json_patch_file_path, "rb") as json_patch_file:
            json_patch = json.load(json_patch_file)
            for key, value in json_patch.items():
                if key == "extend":
                    if isinstance(value, dict):
                        for extend_key, extend_value in value.items():
                            if isinstance(extend_value, list):
                                patcher.extend_list(extend_key, extend_value)
                            else:
                                raise ValueError(
                                    "extend value for key {} must be a list, not {}".format(
                                        extend_key, type(extend_value)
                                    )
                                )
                    else:
                        raise ValueError(
                            "The value of the 'extend' key must be a dictionary"
                        )
                elif key == "patch":
                    if isinstance(value, dict):
                        patcher.patch(value)
                    else:
                        raise ValueError(
                            "The value of the 'patch' key must be a dictionary"
                        )
                elif key == "remove":
                    if isinstance(value, dict):
                        for remove_key, remove_value in value.items():
                            if isinstance(remove_value, list):
                                patcher.remove_list(remove_key, remove_value)
                            else:
                                raise ValueError(
                                    "remove value for key {} must be a list, not {}".format(
                                        remove_key, type(remove_value)
                                    )
                                )
                else:
                    raise ValueError(
                        f"Unsupported key {key} in json patch file, only 'extend' and 'patch' are supported"
                    )
