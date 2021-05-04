## GBPM

[![CI](https://github.com/carvalhudo/gbpm/actions/workflows/ci.yml/badge.svg)](https://github.com/carvalhudo/gbpm/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/carvalhudo/gbpm/branch/master/graph/badge.svg)](https://codecov.io/gh/carvalhudo/gbpm)

TODO

### Running the tests

```
$ docker image build -t gbpm-tests -f tests/Dockerfile .
$ docker container run -v $(pwd):/gbpm --rm --name gbpm gbpm-tests:latest
```
