## GBPM

TODO

### Running the tests

```
$ docker image build -t gbpm-tests -f tests/Dockerfile .
$ docker container run -v $(pwd):/gbpm --rm --name gbpm gbpm-tests:latest
```
