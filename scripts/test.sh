#!/bin/bash
# run python unit tests
python3 -m unittest -f src/test/tests/**.py

rm -f streamq_test.db
