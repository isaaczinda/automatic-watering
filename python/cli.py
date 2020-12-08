import inspect
import argparse


def argsFromCLI(f):
    spec = inspect.getfullargspec(f)._asdict()

    # make sure that there are no None values
    if spec.get('args', None) == None:
        spec['args'] = []
    if spec.get('defaults', None) == None:
        spec['defaults'] = ()

    arg_names = spec['args'][:len(spec['args']) - len(spec['defaults'])]
    kw_arg_names_values = [ (spec['args'][len(spec['args']) + i], spec['defaults'][i]) for i in range(len(spec['defaults'])) ]

    parser = argparse.ArgumentParser()

    # these are all strings by default
    for arg_name in arg_names:
        parser.add_argument('--' + arg_name, required=True)

    # for arguments which have defaults, we can do type conversion
    for kw_arg_name_value in kw_arg_names_values:
        parser.add_argument(
            '--' + kw_arg_name_value[0],
            nargs='?', # kwargs aren't required, becauase they have default
            default=kw_arg_name_value[1],
            type=type(kw_arg_name_value[1]))

    args = vars(parser.parse_args())

    # get list of argument values for normal arguments
    arg_vals = [ args[arg_name] for arg_name in arg_names ]

    # make dictionary of name:vaue for kw arguments
    kw_arg_vals = {}
    for kw_arg_name, _ in kw_arg_names_values:
        kw_arg_vals[kw_arg_name] = args[kw_arg_name]

    f(*arg_vals, **kw_arg_vals)
