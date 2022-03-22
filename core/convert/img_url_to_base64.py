def image_url_to_base64(url: str):
    """
    이미지 링크를 Base64로 전환
    """
    import base64
    from urllib.request import urlopen
    return base64.b64encode(urlopen(url).read()) if url else None


def image_url_to_base64_str(url: str):
    """
    이미지 링크를 Base64 String 으로 전환
    """
    return f'data:image/jpg;base64,{image_url_to_base64(url).decode("utf-8")}'
