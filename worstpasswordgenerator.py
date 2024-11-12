import os
import re
import argparse
import subprocess
import shutil

def get_input(prompt, default_value=None):
    user_input = input(prompt)
    if not user_input or user_input.lower() in ['y', 'yes']: return default_value
    return int(user_input)

parser = argparse.ArgumentParser(description="Find the worst possible passwords based on a password policy. To be used for testing common password checking.")
parser.add_argument('-f', '-fast', '-fasttrack', type=int, help="Fast-track mode: specify minimum total letters (e.g., -f 12), uses default values for all character requirements")
parser.add_argument('-x', '-cb', '-copy', '-clipboard', '-xclip', action='store_true', help="Copy matching passwords to clipboard using xclip (if installed)")
args = parser.parse_args()

if args.f:
    total_letters = args.f
    lowercase = 1
    uppercase = 1
    digits = 1
    symbols = 1
    print(f"Fast-track mode enabled with at least {total_letters} total letters.")
else:
    total_letters = get_input("How many total characters (default 8)? ", 8)
    lowercase = get_input("How many lowercase letters (default 1)? ", 1)
    uppercase = get_input("How many uppercase letters (default 1)? ", 1)
    digits = get_input("How many digits (default 1)? ", 1)
    symbols = get_input("How many symbols (default 1)? ", 1)

password_regex = r"" # I GPTed all the regex stuff so don't ask me about it
if lowercase > 0: password_regex += rf"(?=(.*[a-z]){{{lowercase}}})"
if uppercase > 0: password_regex += rf"(?=(.*[A-Z]){{{uppercase}}})"
if digits > 0: password_regex += rf"(?=(.*\d){{{digits}}})"
if symbols > 0: password_regex += rf"(?=(.*[\W_]){{{symbols}}})"
password_regex += rf".{{{total_letters},}}"

regex = re.compile(password_regex)

files = []

for filename in os.listdir("lists"):
    filepath = os.path.join("lists", filename)
    if os.path.isfile(filepath):
        with open(filepath, 'r') as file:
            passwords = file.readlines()
            matches = [pw.strip() for pw in passwords if regex.match(pw.strip())]
            if matches: files.append((filename, matches))

if files:
    if not args.f: 
        print("\nFiles containing matching passwords:")
        for index, (filename, matches) in enumerate(files):
            print(f"{index + 1}. {filename}:")
            for i, match in enumerate(matches[:5]):
                print(f"   {i + 1}. {match}")
            if len(matches) - 5 > 0: print(f"   ...and {len(matches) - 5} more\n")
    
    choice = None if args.f else input("Enter the number of the file you want to see all passwords from (or press Enter for all files): ").strip()

    matches = []

    while True:
        if choice == '*' or not choice:
            matches = []                                            # I'm doing it with a list instead of using a set
            for _, file_matches in files:                           # and adding them in this manner so that the order
                for match in file_matches:                          # is preserved, as most common password lists are
                    if match not in matches: matches.append(match)  # sorted with the most common passwords at the top.
            break
        elif choice.isdigit():
            file_index = int(choice) - 1
            if file_index < len(files):
                matches = files[file_index][1]
                break
            else: print("Invalid file number.")

    line_choice = "" if args.f else input("Enter number of lines to display (or press Enter for all): ").strip()

    if line_choice.isdigit(): matches = matches[:int(line_choice)]
    matches = "\n".join(matches)

    optional_copy = False if args.f else input("Use xclip to copy to keyboard (y/yes)? ").lower() in ['y', 'ye', 'yes']
    
    if args.x or optional_copy:
        if shutil.which('xclip'):
            try:
                process = subprocess.Popen(['xclip', '-sel', 'c'], stdin=subprocess.PIPE)
                process.communicate(input=matches.encode('utf-8'))
                print("Passwords copied to clipboard.")
            except Exception as e: print(f"Failed to copy to clipboard: {e}")
        else: print("xclip is not installed. Please install it or use another output method.")
    else:
        output_choice = False if args.f else input("Enter a filepath to save the results (or press Enter to print to terminal): ").strip()
        if output_choice:
            with open(output_choice, 'w') as f:
                f.write(matches)
            print(f"Passwords saved to {output_choice}")
        else: print(matches)

else: print("No matching passwords found.")
