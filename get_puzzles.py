import requests
import datetime
import os

year = 2023
current_day = datetime.datetime.now().day

with open('session_cookie.txt', 'r') as f:
    session_cookie = f.read()


for day in range(1, current_day + 1):
    # check if directory exists
    if os.path.exists(f'{day}'):
        continue

    # create directory
    os.mkdir(f'{day}')

    # create input file
    input_file = requests.get(f'https://adventofcode.com/{year}/day/{day}/input', cookies={"session": session_cookie})
    input_filename = f'{day}/input.txt'
    
    with open(input_filename, 'w') as f:
        f.write(input_file.text)
    
    # create solution file
    with open(f'{day}/solution.py', 'w') as f:
        f.write(f"with open('{input_filename}', 'r') as f:\n")
        f.write(f"    puzzle_input = [line.strip() for line in f.readlines()]\n")

