def handle_pydentic_errors(errors):
    return {error['loc'][0]: error['msg'] for error in errors}
