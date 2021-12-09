from enum import EnumMeta


def is_valid_enum_value(enum_meta_class: EnumMeta, value) -> bool:
    return value in set(item.value for item in enum_meta_class)
