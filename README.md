# Spack Splices Results

![https://avatars.githubusercontent.com/u/85255731?s=200&v=4](https://avatars.githubusercontent.com/u/85255731?s=200&v=4)

This repository does an automated retrieval of results from [spack-splices](https://github.com/buildsi/spack-splices).
This works via the [GitHub workflow](.github/workflows/artifacts.yml) that runs
the script [get_artifacts.py](get_artifacts.py) nightly to do the following:

1. Get a listing of artifacts from [spack-splices](https://github.com/buildsi/spack-splices), which saves test results for doing splices as GitHub artifacts.
2. For artifacts that are not expired (they expire typically in 90 days) and that are within 2 days of today (we don't need to parse artifacts more than once) do the following:
 - If the filename does not exist under [artifacts](artifacts) copy it there because it's a new result.
 - If the filename already exists, compare the hashes of the two. If the hashes are different, only copy the artifact file if it's newer (it's a new version of a result).

## Usage

While this is a nightly job, you can also trigger it via dispath, or run locally:

```bash
$ export GITHUB_TOKEN=xxxxxxxxxxxxxx
$ export INPUT_REPOSITORY=buildsi/spack-splices
$ python get_artifacts.py
```

Please [open an issue](https://github.com/buildsi/spack-splices-results/issues)
if you have a question or point of discussion. 
