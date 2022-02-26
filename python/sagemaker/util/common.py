base_dir = "/opt/ml/processing"


def get_input_path(name):
    return f"{base_dir}/input/{name}"


def get_output_path(name):
    return f"{base_dir}/output/{name}"
