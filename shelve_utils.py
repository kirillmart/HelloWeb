import shelve
FILENAME = 'dev_shelf.db'


def write_to_shelve(key, value):
    with shelve.open(FILENAME, writeback=True) as s:
        s[key] = value


def read_from_shelve(key):
    with shelve.open(FILENAME, writeback=True) as s:
        return s[key]


if __name__ == "__main__":
    FILENAME = 'test_shelf.db'
    test_key = "test_key"
    test_value = "test_value"
    write_to_shelve(test_key, test_value)
    assert read_from_shelve(test_key) == test_value
    test_key_2 = "test_key_2"
    test_value_2 = "test_value_2"
    write_to_shelve(test_key_2, test_value_2)
    assert read_from_shelve(test_key_2) == test_value_2
    assert read_from_shelve(test_key) == test_value
