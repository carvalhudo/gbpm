## GBPM

[![gbpm tests](https://github.com/carvalhudo/gbpm/workflows/tests/badge.svg)](https://github.com/carvalhudo/gbpm/actions?query=workflow%3Atests)
[![gbpm lint](https://github.com/carvalhudo/gbpm/workflows/lint/badge.svg)](https://github.com/carvalhudo/gbpm/actions?query=workflow%3Alint)

### Overview

TODO

### Running the tests

```
$ docker image build -t gbpm-tests -f tests/Dockerfile .
$ docker container run -v $(pwd):/gbpm --rm --name gbpm gbpm-tests:latest
```
