def secure_prompt(data: dict):
    sanitized = {}
    for k, v in data.items():
        if isinstance(v, str):
            sanitized[k] = v.replace("{", "").replace("}", "")
        else:
            sanitized[k] = v
    return sanitized