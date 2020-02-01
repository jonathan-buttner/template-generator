# YAML schema to Elasticsearch template creator
This script will convert a directory of yaml files to an elasticsearch template file

## Setup
Make sure you have at least python 3.5 installed

```bash
pip install -r requirements.txt
```

## To run
```bash
python3.5 gen_template.py <path to schema directory> <out directory>
```

`gen_template.py` will write the template file to the `out` directory passed in on the commandline


