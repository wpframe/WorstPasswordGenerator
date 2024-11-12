# WorstPasswordGenerator
Finds the worst possible passwords based on a password policy. To be used for testing common password checking.

Run the program, specify your password policy, and the script will scan for common passwords that meet your password policy.

Optionally, add additional password lists to `lists/`.

Example usage:
```
python3 worstpasswordgenerator.py
```

The `-f` flag enables fast-track mode, which takes a number of the minimum total letters, and uses default values for each character (1 lowercase letter, 1 uppercase letter, 1 digit, and 1 symbol):
```
python3 worstpasswordgenerator.py -f 12
```

The `-x` flag specifies to copy matching passwords to the clipboard. While the user is prompted for this option during normal use of the application, the flag makes it easy to spam enter through the remaining defaults if you know what you're doing.
```
python3 worstpasswordgenerator.py -x -f 12
```