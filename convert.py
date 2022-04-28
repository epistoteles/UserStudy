# don't forget to `pip install toml`
# taken from https://gist.github.com/pgilad/e8ffd8ce2bde81a1a375e86df77a34ab

import json
import sys
import toml

if len(sys.argv) < 3:
    raise Exception("Usage is `python convert.py input.json output.toml`")
json_file = sys.argv[1]
output_file = sys.argv[2]

with open(json_file) as source:
    config = json.loads(source.read())

toml_config = toml.dumps(config)

with open(output_file, "w") as target:
    target.write(toml_config)
