# tomlpatch
Do you want to patch your toml file structurally like modifying a nested python dictionary? This is a tool for you.

# Description
Sometimes, you want to edit/patch a toml file, but you don't want to use the [diff](https://en.wikipedia.org/wiki/Patch_(computing)#Source_code_patches) between two source files to patch the toml file since it may introduce conflicts that requires human intervention to resolve.
For example, `Cargo.toml` is used by Rust projects, and this tool can be used to patch the `Cargo.toml` file with an external JSON file that contains the structural patch information so that you don't need to manually resolve the `Cargo.toml` file.

# Installation
```
pip install tomlpatch
```

# Usage
```
tomlpatch original_toml_file patch_json_file
```

# Example
Suppose you have a `Cargo.toml` file like this:
```toml
[package]
name = "my_package"
version = "0.0.1"

liberssl = { version = "0.10.42", default-features = false, features=["vendered"] }
sources = ["s1", "s2"]
```

And you want to patch the `Cargo.toml` file with a JSON file like this:
```json
{
  "patch": {
    "package.version": "0.0.2",
    "package.liberssl.features": null
  },
  "extend": {
    "package.sources": ["s4", "s5"]
  }
}
```

Then you can use the following command to patch the `Cargo.toml` file:
```
tomlpatch Cargo.toml patch.json
```

After the patch, the `Cargo.toml` file will be like this:
```toml
[package]
name = "my_package"
version = "0.0.2"
sources = [
    "s1",
    "s2",
    "s4",
    "s5",
]

[package.liberssl]
version = "0.10.42"
default-features = false
```

# TODO
* Switch to [tomkit](https://github.com/sdispater/tomlkit) for style preserving patching