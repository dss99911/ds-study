import argparse

base_dir = "/opt/ml/processing"


def get_input_path(name):
    return f"{base_dir}/input/{name}"


def get_output_path(name):
    return f"{base_dir}/output/{name}"



def get_args(name, arg_type=str, default=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--" + name, type=arg_type, default=default)
    args, _ = parser.parse_known_args()
    return getattr(args, name)


def get_args_schema():
    return get_args("schema", default="stage")


def get_args_schema_path():
    return get_args("schema_path", default="s3://hyun/stage")


def log_info(*message):
    print(f"sage_maker_info : {message}")


def log_error(message):
    print(f"sage_maker_error : {message}")