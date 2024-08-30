import requests
import json
import sys
import colorama
import os
from time import sleep

colorama.init()

def type_out(words: str):
    for char in words:
        sleep(0.015)
        sys.stdout.write(char)
        sys.stdout.flush()
    print()

def scan_file(file_path, api):
    url = 'https://www.virustotal.com/api/v3/files'
    params = {"apikey": api}

    with open(file_path, "rb") as file:
        file_upload = {"file": file}
        response = requests.post(url, files=file_upload, params=params)

    return response.json().get('sha256')

def get_report(file_hash, api):
    file_url = f"https://www.virustotal.com/api/v3/files/{file_hash}"
    headers = {"accept": "application/json", "x-apikey": api}
    response = requests.get(file_url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return None

def process_file(file_path, api):
    file_hash = scan_file(file_path, api)
    type_out(f"Analysing {file_path}...")

    report = get_report(file_hash, api)

    if report:
        name = report["data"]["attributes"].get("meaningful_name", os.path.basename(file_path))
        file_hash = report["data"]["attributes"]["sha256"]
        descp = report["data"]["attributes"]["type_description"]
        size = report["data"]["attributes"]["size"] * 10**-3  # KB
        result = report["data"]["attributes"]["last_analysis_results"]

        print()
        type_out(f"{colorama.Fore.WHITE}Name: {colorama.Fore.YELLOW}{name}")
        type_out(f"{colorama.Fore.WHITE}Size: {colorama.Fore.YELLOW}{size:.2f} KB")
        type_out(f"{colorama.Fore.WHITE}Description: {colorama.Fore.YELLOW}{descp}")
        type_out(f"{colorama.Fore.WHITE}SHA-256 Hash: {colorama.Fore.YELLOW}{file_hash}")

        malicious_count = 0
        print()

        for key, values in result.items():
            key = f'{colorama.Fore.WHITE}{key}'
            verdict = values['category']
            if verdict == 'undetected':
                verdict = f'{colorama.Fore.GREEN}undetected'
            elif verdict == 'type-unsupported':
                verdict = f'{colorama.Fore.YELLOW}type-unsupported'
            elif verdict == 'malicious':
                malicious_count += 1
                verdict = f'{colorama.Fore.RED}malicious'
            type_out(f"{key}: {verdict}")

        if malicious_count != 0:
            type_out(colorama.Back.WHITE + colorama.Fore.RED + f'\t\t\t\t{malicious_count} detections: This file is malicious')
        else:
            type_out(colorama.Back.WHITE + colorama.Fore.GREEN + f'\t\t\t\tNo detections: This file is not malicious')
    else:
        type_out(colorama.Fore.RED + "Failed to retrieve the report. Please try again later.")

def scan_folder(folder_path, api):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            process_file(file_path, api)

if __name__ == "__main__":
    api = open("vt-api.txt").read().strip()
    folder_path = input("Enter the path of the folder: ")
    scan_folder(folder_path, api)