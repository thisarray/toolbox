#!/bin/bash
#
# Generate actual output to compare against expected output in tests.

ls -al LICENSE
python3 chmod_walk.py -f 600 LICENSE
ls -al LICENSE
python3 chmod_walk.py LICENSE
ls -al LICENSE

python3 cat.py LICENSE > tests/cat_LICENSE.temp

python3 dog.py LICENSE > tests/dog_wrap.temp
python3 dog.py -w 79 LICENSE > tests/dog_LICENSE.temp

python3 checksum.py md5 LICENSE > tests/checksum_md5.temp
python3 checksum.py md5 LICENSE sha1 > tests/checksum_sha1.temp
python3 checksum.py LICENSE sha256 > tests/checksum_sha256.temp

python3 subset.py tests tests/ > tests/subset1.temp
python3 subset.py tests/ tests > tests/subset2.temp

python3 wget.py https://raw.githubusercontent.com/thisarray/toolbox/master/LICENSE > tests/wget_LICENSE1.temp
python3 wget.py https://raw.githubusercontent.com/thisarray/toolbox/master/LICENSE -o LICENSE &> tests/wget_exists.temp
python3 wget.py https://raw.githubusercontent.com/thisarray/toolbox/master/LICENSE -o tests/wget_LICENSE2.temp

# Compare the expected output and the actual output generated above
# List all expected output | get their filenames (cut extension) | diff expected and actual output
ls tests/*.out | cut -d '.' -f1 | xargs -I "{}" diff -q "{}.out" "{}.temp"

# Clean up
rm tests/*.temp
