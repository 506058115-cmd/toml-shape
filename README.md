# toml-shape

Inspect the structure of a TOML file without printing configured values. It lists table/key paths and their value types; arrays are summarized by element type and count. This is useful for checking an unfamiliar `pyproject.toml`, Cargo manifest, or application config without dumping settings and values into a terminal transcript.

Requires Python 3.11+ and uses the standard-library `tomllib` parser. Input is limited to 16 MiB.

~~~sh
python toml_shape.py pyproject.toml
~~~

Paths are printed as JSON-escaped key arrays so unusual key names cannot inject terminal control characters. Array items and their values are not expanded; an array of tables is reported as `array[table×N]`. This describes structure, not whether the settings are valid for a particular application. The parser follows TOML 1.0.0.

See the [Python `tomllib` documentation](https://docs.python.org/3.11/library/tomllib.html) and the [TOML 1.0.0 specification](https://toml.io/en/v1.0.0).

## Linux x86_64 downloads

- [Single-file build](https://github.com/506058115-cmd/toml-shape/releases/download/v1.0.0/toml-shape-linux-x86_64-onefile.tar.gz)
- [Directory build](https://github.com/506058115-cmd/toml-shape/releases/download/v1.0.0/toml-shape-linux-x86_64-onedir.tar.gz)
- [v1.0.0 release](https://github.com/506058115-cmd/toml-shape/releases/tag/v1.0.0)

Archives include build information and dependency licenses; the Release includes SHA-256 checksums. Built in WSL Ubuntu 24.04 (Python 3.12.3, PyInstaller 6.22.2) for GNU/Linux x86_64. Older Linux distributions may require a compatible glibc. The packaged executable has not been run for functional validation.

## License

MIT. See [LICENSE](LICENSE).
