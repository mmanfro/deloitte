def locale_float(number):
    return float(str(number).replace(",", "."))


def get_version(string):
    return string.split("_")[1]
