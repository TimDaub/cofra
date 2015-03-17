# Testing

cofra uses `py.test` for testing. This package either installs itself by installing the requirements in `requirement.txt` or it must manually be installed afterwards.

The most easiest way to test specific functionality of the application use:

    `py.test -s tests/test_db.py`

Only use this command **from the root folder**, as dependencies will not resolve correctly otherwise.