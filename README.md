# Report for Assignment 1

## Project

Description: A secure password manager

Programming language: Python

## Initial tests

### Tests

```
import os
import pytest
from unittest.mock import patch, mock_open, MagicMock, call
import json
import base64
import sys

from src import vault

# arek
def test_store_roundtrip(tmp_path):
    test_passwords = {"test_service": {"username": "test_user", "password": "test_pass"}}
    master_password = "master123"
    file_path = str(tmp_path / "test_vault.json")
    
    with patch('os.urandom', return_value=b'fixed_salt_12345'):
        mock_file = mock_open()
        with patch('builtins.open', mock_file), \
             patch('os.rename') as mock_rename:
            vault.save_store(file_path, test_passwords, master_password)
            
            written = "".join(call.args[0] for call in mock_file().write.call_args_list)
            file_content = json.loads(written)
            assert "salt" in file_content
            assert "encrypted_data" in file_content
            
            mock_rename.assert_called_with(file_path + ".tmp", file_path)

# mark
def test_load_store_success(tmp_path):
    file_path = tmp_path / "vault.json"
    original_passwords = {"service1": {"username": "user1", "password": "password1"}}
    master_password = "correct_password"

    vault.save_store(str(file_path), original_passwords, master_password)

    with patch("getpass.getpass", return_value=master_password), patch(
        "builtins.print"
    ):
        loaded_passwords, loaded_master_pw = vault.load_store(str(file_path))

    assert loaded_passwords == original_passwords
    assert loaded_master_pw == master_password

# felix

    def test_handle_del_ServiceExists_RemovedSuccessfully(self):

        """Should remove the service when it exists and print confirmation."""

        passwords = {"gmail": {"username": "john", "password": "123"}, "github": {"username": "jane", "password": "abc"}}
        parts = ["del", "gmail"]
        
        captured_output = StringIO()
        sys.stdout = captured_output
        handle_del(passwords, parts)
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        self.assertNotIn("gmail", passwords)
        self.assertIn("deleted", output.lower())

# tijn
def test_create_new_store_success():

    with patch("getpass.getpass", side_effect=["lalala123", "lalala123"]):
        f = io.StringIO()

        with redirect_stdout(f):
            store, password = create_new_store()

    out = f.getvalue()

    assert "NO current vault, creating new one...." in out
    assert "New vault created" in out
    assert store == {}
    assert password == "lalala123"

```

### Coverage of initial tests

Tools: pytest unitets

initial:
![Screenshot 1](resources/initial.png)

## Coverage improvement

### Individual tests

Tijn:

![Screenshot 1](resources/Screenshot%20from%202025-06-12%2022-31-55.png)
  
![Screenshot 2](resources/Screenshot%20from%202025-06-12%2022-54-06.png)

Initial test coverage was 22%. After adding two additional tests—covering the functions `create_new_store()` and `print_help()`—coverage increased to 28%.

This increase was expected since the new tests are relatively simple helper tests. The `print_help()` test may seem redundant, but including it helps improve coverage and ensures that the printed help text is less likely to be changed accidentally.

Overall, while the coverage gain is modest, these tests contribute to the total coverage and are important for maintaining code quality.

Arek: 

<img width="810" alt="Screenshot 2025-06-12 at 23 20 04" src="https://github.com/user-attachments/assets/52895360-dc46-495d-beae-e5a3c6adc28d" />

<img width="384" alt="Screenshot 2025-06-12 at 23 19 41" src="https://github.com/user-attachments/assets/bb1f4663-2e87-45d7-8d21-952ceac3a743" />

Managed to achieve a 13% increase in test coverage. My original tests were test_store_roundtrip and test_save_is_atomic, then I eended up adding test_invalid_master_password and test_create_new_store

Mark:

Screenshot 1: Initial Coverage Report

![Screenshot 3](resources/mark1.png)

Screenshot 2: Final Coverage Report

![Screenshot 4](resources/mark2.png)

Initial test coverage for src/vault.py was 35%, established by a single baseline test. After adding three new, targeted tests, the coverage for the application source code increased significantly to 54%. This represents a total improvement of 19%.
The substantial increase in coverage is due to the strategic addition of tests that target previously uncovered execution paths, including error handling, specific logic branches, and interactive loop conditions.

Felice: 

Only the first test case was active, targeting the `handle_del` function when the service is present in the password dictionary.

![image](https://github.com/user-attachments/assets/c2016557-8160-446c-b077-1d334509a789)

The relatively low coverage of 29% is mainly due to the fact that this test exercises only one path of one function (`handle_del`), all the rest remains cutted out. Then we added other two tests and improved the coverage to 39%.

![image](https://github.com/user-attachments/assets/e7a1533a-7568-4b33-9ae7-0390da6cffd3)

Since handle_del() is one of the few fully tested functions, your total coverage improves by ~10%. In fact, each test covers a different logical branch inside handle_del().

### Overall
initial:
![Screenshot 1](resources/initial.png)

after:
![Screenshot 1](resources/final.png)

## Statement of individual contributions

Mark:I wrote 2 functions,3 tests and helped finish the readme.md report file.

Tijn: I wrote 3 functions in vault.py: Savestore, createnewstore, and printhelp. Created 3 tests, found in tests/tests_tijn.py. Helped with the README.md.

Arek: I wrote 3 functions in vault.py and 4 tests

Felix:

| Member | Three functions created | Initial test (name) | Other tests (names) |
| --- | --- | --- | --- |
| Member Mark | derive_key, load store | test_load_store_success | test_interactive_session_unknown_command test_handle_list_sorted_output test_load_store_corrupted_file |
| Member Arek | handle_get, handle_set, handle_list| test_store_roundtrip | test_save_is_atomic, test_invalid_master_password, test_create_new_store|
| Member Tijn | create_new_store, print_store, print_help | test_create_new_store_success | test_create_new_store_password_mismatch, test_print_help_output|
| Member Felice | handle_del, interactive_session, main() | test_serviceExists_RemovedSuccessfully | test_serviceNotFound_PrintsMessage, test_missingArgument_PrintsUsage|
