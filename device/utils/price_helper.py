from re import compile


def parse_string_price_to_float(price: str) -> float:
    trimmer = compile(r"[^\d.,]+")
    trimmed = trimmer.sub("", price)
    decimal_separator = trimmed[-3:][0]
    if decimal_separator not in [".", ","]:
        decimal_separator = ""
    trimer = compile(rf"[^\d{decimal_separator}]+")
    trimmed = trimer.sub("", price)
    if decimal_separator == ",":
        trimmed = trimmed.replace(",", ".")
    result = float(trimmed)
    return result
