import yaml
import sys
import json
import os
import functools

def usage():
    print('yaml file not provided')
    print('Usage: {} <path to schema directory> <out directory>'.format(sys.argv[0]))


def handle_field_value(mapping_obj, field):
    if 'fields' in field:
        mapping_obj[field['name']] = {'properties': handle_fields_key(field['fields'])}
    else:
        mapping_obj[field['name']] = {'type': field['type']}


def handle_fields_key(fields):
    properties = {}
    for field in fields:
        handle_field_value(properties, field)
    return properties


def parse_yaml_file(file_to_parse):
    with open(file_to_parse) as yaml_file:
        yaml_cont = yaml.full_load(yaml_file)
    fields = []
    for key, val in yaml_cont.items():
        if key == 'fields':
            fields = val
            break

    return handle_fields_key(fields)


def merge_dict(a, b, path=None):
    if path is None:
        path = []
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                merge_dict(a[key], b[key], path + [str(key)])
            elif a[key] == b[key]:
                pass  # same leaf value
            else:
                raise Exception('Conflict at {}'.format('.'.join(path + [str(key)])))
        else:
            a[key] = b[key]
    return a


def main():
    if len(sys.argv) != 3:
        usage()
        sys.exit(1)
    prop_dictionaries = []
    for f in os.listdir(sys.argv[1]):
        file_with_path = os.path.join(sys.argv[1], f)
        if os.path.isfile(file_with_path) and '_template' not in f:
            file_props = parse_yaml_file(file_with_path)
            prop_dictionaries.append(file_props)

    properties = functools.reduce(merge_dict, prop_dictionaries)
    template = {
        'index_patterns': ['endpoint-events*'],
        'mappings': {
            'properties': properties
        }
    }

    os.makedirs(sys.argv[2], mode=0o775, exist_ok=True)

    # ignore the extension
    dir_name = os.path.basename(sys.argv[1])
    template_file = dir_name + '_template.json'
    out_path = os.path.join(sys.argv[2], template_file)
    with open(out_path, 'w') as out:
        out.write(json.dumps(template, sort_keys=True, indent=2))

    print('template written to: {}'.format(os.path.abspath(out_path)))


if __name__ == '__main__':
    main()
