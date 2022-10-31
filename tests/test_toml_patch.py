from tomlpatch import TomlFileManager, TomlPatcher, JsonFilePatcher
import os
import tomli


def _data_file(path):
    return os.path.join(os.path.dirname(__file__), "data", path)


def _test_cargo_file():
    return _data_file("Cargo.toml")


def _patched_cargo_file():
    return _data_file("Cargo.patched.toml")


def test_patch_toml():
    patcher = TomlPatcher({"a": 1})
    toml = patcher.patch({"a": 2, "b": 1})
    assert len(toml) == 2
    assert toml["a"] == 2
    assert toml["b"] == 1


def test_patch_nested_property():
    patcher = TomlPatcher({"a": {"b": 1}})
    toml = patcher.patch({"a": 2, "b": 1})
    assert len(toml) == 2
    assert toml["a"] == 2
    assert toml["b"] == 1


def test_patch_nested_toml():
    patcher = TomlPatcher({"a": {"b": 1}, "c": 2})
    toml = patcher.patch({"a.b": 2, "c": 3})
    assert len(toml) == 2
    assert toml["a"] == {"b": 2}
    assert toml["c"] == 3


def test_extend_list_in_toml():
    patcher = TomlPatcher({"a": [1, 2]})
    toml = patcher.extend_list("a", [3, 4])
    assert len(toml) == 1
    assert toml["a"] == [1, 2, 3, 4]


def test_remove_list_in_toml():
    patcher = TomlPatcher({"a": [1, 2, 3]})
    toml = patcher.remove_list("a", [3, 2])
    assert len(toml) == 1
    assert toml["a"] == [1]


def test_extend_nested_list_in_toml():
    patcher = TomlPatcher({"a": {"b": [1, 2]}, "c": 3})
    toml = patcher.extend_list("a.b", [3, 4])
    assert len(toml) == 2
    assert toml["a"]["b"] == [1, 2, 3, 4]


def test_remove_nested_list_in_toml():
    patcher = TomlPatcher({"a": {"b": [1, 2, 3]}, "c": 3})
    toml = patcher.remove_list("a.b", [2])
    assert len(toml) == 2
    assert toml["a"]["b"] == [1, 3]


def test_patch_toml_file_appending_list():
    with TomlFileManager(
        _test_cargo_file(),
        _patched_cargo_file(),
    ) as patcher:
        assert patcher is not None
        toml = patcher.extend_list("package.sources", ["s3"])
        assert len(toml) == 1
        assert toml["package"]["sources"] == ["s1", "s2", "s3"]
    assert os.path.exists(_patched_cargo_file())
    with open(_patched_cargo_file(), "rb") as f:
        patched_toml = tomli.load(f)
        assert patched_toml["package"]["sources"] == ["s1", "s2", "s3"]


def test_json_file_patch():
    with TomlFileManager(
        _test_cargo_file(),
        _patched_cargo_file(),
    ) as patcher:
        JsonFilePatcher().patch(patcher, _data_file("Cargo.patch.json"))
    assert os.path.exists(_patched_cargo_file())
    with open(_patched_cargo_file(), "rb") as f:
        patched_toml = tomli.load(f)
        assert "features" not in patched_toml["package"]["liberssl"]
        patched_toml["package"]["version"] == "0.0.2"
        assert patched_toml["package"]["sources"] == ["s1", "s2", "s4", "s5"]
        assert patched_toml["package"]["targets"] == ["t3"]
