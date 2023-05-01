import time


def get_ttl_hash(seconds):
    """
    Return the same value withing `seconds` time period
    :param seconds: TTL wanted
    :return: "hash" for ttl period
    """
    return round(time.time() / seconds)
