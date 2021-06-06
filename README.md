## GUR

[![CI](https://github.com/carvalhudo/gur/actions/workflows/ci.yml/badge.svg)](https://github.com/carvalhudo/gur/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/carvalhudo/gur/branch/develop/graph/badge.svg)](https://codecov.io/gh/carvalhudo/gur)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/carvalhudo/gur.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/carvalhudo/gur/context:python)
[![Total alerts](https://img.shields.io/lgtm/alerts/g/carvalhudo/gur.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/carvalhudo/gur/alerts/)

**G**it **U**ser **R**epository is a package manager made to improve the
management (install, remove, update) of packages based on git repositories.

### Running the tests

```
$ docker image build -t gur-tests -f tests/Dockerfile .
$ docker container run -v $(pwd):/gur --rm --name gur gur-tests:latest
```
