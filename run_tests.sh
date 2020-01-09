#!/bin/bash
#
# Generate actual output to compare against expected output in tests.

python3 cat.py LICENSE > tests/cat_LICENSE.temp

python3 dog.py LICENSE > tests/dog_wrap.temp
python3 dog.py -w 79 LICENSE > tests/dog_LICENSE.temp

python3 checksum.py md5 LICENSE > tests/checksum_md5.temp
python3 checksum.py md5 LICENSE sha1 > tests/checksum_sha1.temp
python3 checksum.py LICENSE sha256 > tests/checksum_sha256.temp

# Compare the expected output and the actual output generated above
# List all expected output | get their filenames (cut extension) | diff expected and actual output
ls tests/*.out | cut -d '.' -f1 | xargs -I "{}" diff -q "{}.out" "{}.temp"

# Clean up
rm tests/*.temp
