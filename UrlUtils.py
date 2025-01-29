def createURL(url: str, **pathParams) -> str:
    for key, value in pathParams.items():
        url = url.replace(key, value)
    return url