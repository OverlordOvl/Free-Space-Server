def validate_code(status_code: dict):
    if 200 <= status_code['status'] < 300:
        return True
    elif 400 <= status_code['status'] < 500:
        raise Exception('Client error')
    elif 500 <= status_code['status'] < 600:
        raise Exception('Server error')
