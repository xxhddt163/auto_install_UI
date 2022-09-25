import platform


def system_info() -> str:
    """返回操作系统的版本。
    

    Returns:
        str: [win7: return "7" ,win10 or win11: return "10"]
    """
    return platform.uname().release
