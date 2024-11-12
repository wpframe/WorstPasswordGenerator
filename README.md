# WorstPasswordGenerator
Finds the worst possible passwords based on a password policy. To be used for testing common password checking.

Place password lists into `lists/`, run the program and specify your password policy, and the script will scan for common passwords that meet your password policy.

```
options:
  -h, --help            show this help message and exit
  -f F, -fast F, -fasttrack F
                        Fast-track mode: specify minimum total letters (e.g.,
                        -f 12), uses default values for all character
                        requirements
  -x, -cb, -copy, -clipboard, -xclip
                        Copy matching passwords to clipboard using xclip (if
                        installed)
```