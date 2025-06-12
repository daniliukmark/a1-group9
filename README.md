# Report for Assignment 1

## Project

Description: A secure password manager

Programming language: Python

## Initial tests

### Tests

TODO: Add their code here

### Coverage of initial tests

TODO: Inform the name of the existing tool that was executed and how it was executed

TODO: Show the coverage results provided by the existing tool with a screenshot

## Coverage improvement

### Individual tests

Tijn:

![Screenshot 1](resources/Screenshot%20from%202025-06-12%2022-31-55.png)
  
![Screenshot 2](resources/Screenshot%20from%202025-06-12%2022-54-06.png)

Initial test coverage was 22%. After adding two additional tests—covering the functions `create_new_store()` and `print_help()`—coverage increased to 28%.

This increase was expected since the new tests are relatively simple helper tests. The `print_help()` test may seem redundant, but including it helps improve coverage and ensures that the printed help text is less likely to be changed accidentally.

Overall, while the coverage gain is modest, these tests contribute to the total coverage and are important for maintaining code quality.

### Overall

TODO: Provide a screenshot of the old coverage results by running an existing tool (the same as you already showed above)

TODO: Provide a screenshot of the new coverage results by running the existing tool using all test modifications made by the group

## Statement of individual contributions

Mark:I wrote 2 functions,3 tests and helped finish the readme.md report file.

Tijn: I wrote 3 functions in vault.py: Savestore, createnewstore, and printhelp.

Arek: I wrote 3 functions in vault.py and 4 tests

Felix:

| Member | Three functions created | Initial test (name) | Other tests (names) |
| --- | --- | --- | --- |
| Member Mark | derive_key, load store | | |
| Member Arek | handle_get, handle_set, handle_list| test_store_roundtrip | test_save_is_atomic, test_invalid_master_password, test_create_new_store|
| Member C | | | |
| Member D | | | |
