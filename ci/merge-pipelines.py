import sys
import yaml


pipeline = {}
for filename in sys.argv[1:]:
    with open(filename) as file:
        data = yaml.safe_load(file)
    # all top level pipeline values are lists, so just append the values of
    # eajch subsequent file to each key
    # import pdb; pdb.set_trace()
    for k, v in data.items():
        pipeline[k] = pipeline.get(k, []) + v
yaml.safe_dump(pipeline, sys.stdout, indent=2)
