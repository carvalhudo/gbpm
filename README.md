## GUR

[![CI](https://github.com/carvalhudo/gur/actions/workflows/ci.yml/badge.svg)](https://github.com/carvalhudo/gur/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/carvalhudo/gur/branch/develop/graph/badge.svg)](https://codecov.io/gh/carvalhudo/gur)

TODO

### Running the tests

```
$ docker image build -t gur-tests -f tests/Dockerfile .
$ docker container run -v $(pwd):/gur --rm --name gur gur-tests:latest
```
