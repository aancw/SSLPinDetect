import re
import os
import zipfile
import json
import shutil
import argparse
import time
import subprocess
from tqdm import tqdm
from colorama import Fore, Style, init
from concurrent.futures import ThreadPoolExecutor, as_completed
import mmap

init(autoreset=True)

def check_java():
    if os.system("java -version >nul 2>&1") != 0:
        print("Java is not installed or not in PATH. Please install JDK and ensure it's in your system PATH.")
        exit(1)

def check_apktool(apktool_path):
    if not os.path.isfile(os.path.expanduser(apktool_path)):
        raise SystemExit(f"Apktool not found at {apktool_path}")

def extract_apk(apktool_path, apk_path, output_dir, verbose):
    command = [
        "java", "-jar", apktool_path, "d", apk_path, "-o", output_dir
    ]

    try:
        subprocess.run(command, check=True, stdout=subprocess.PIPE if not verbose else None, stderr=subprocess.PIPE if not verbose else None)
        if verbose:
            print("APK successfully decompiled.")
        else:
            print("Processing APK...")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")

def load_patterns(pattern_file):
    with open(pattern_file, 'r', encoding='utf-8') as f:
        raw_patterns = json.load(f)

    patterns = {}
    for category, values in raw_patterns.items():
        combined_pattern = "|".join(values)
        patterns[category] = re.compile(combined_pattern)

    return patterns

def detect_frameworks(decompiled_dir):
    frameworks = []
    flutter_files = ["libflutter.so", "libapp.so"]
    flutter_folders = ["flutter_assets"]
    react_files = ["libreactnativejni.so", "index.android.bundle"]
    react_folders = ["assets/react"]

    for root, dirs, files in os.walk(decompiled_dir):
        if any(f in files for f in flutter_files) or any(d in dirs for d in flutter_folders):
            print(f"{Fore.BLUE}Detected Flutter framework. Skipping smali analysis.{Style.RESET_ALL}")
            shutil.rmtree(decompiled_dir, ignore_errors=True)
            exit(0)
        if any(f in files for f in react_files) or any(d in dirs for d in react_folders):
            frameworks.append("React Native")

    return set(frameworks)

def process_file(file_path, patterns):
    results = {}
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            with mmap.mmap(f.fileno(), length=0, access=mmap.ACCESS_READ) as mm:
                content = mm.read().decode('utf-8', errors='ignore')
                for category, regex in patterns.items():
                    for match in regex.finditer(content):
                        line_number = content.count('\n', 0, match.start()) + 1
                        line_preview = content[match.start():match.end()].strip()
                        if category not in results:
                            results[category] = []
                        results[category].append((file_path, line_number, line_preview))
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")

    return results

def search_ssl_pinning(smali_dir, patterns):
    smali_files = [
        os.path.join(root, file)
        for root, _, files in os.walk(smali_dir)
        for file in files if file.endswith(".smali")
    ]

    results = {}
    match_count = 0
    match_pbar = tqdm(desc=f"{Fore.GREEN}Pattern Matched{Style.RESET_ALL}", position=1, bar_format="{desc}: {n}")

    with ThreadPoolExecutor() as executor:
        futures = {executor.submit(process_file, file, patterns): file for file in smali_files}
        for future in tqdm(as_completed(futures), total=len(smali_files), desc="Scanning Smali Files", position=0):
            file_results = future.result()
            for category, matches in file_results.items():
                if category not in results:
                    results[category] = []
                results[category].extend(matches)
                match_count += len(matches)
                match_pbar.update(len(matches))

    return results, match_count

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SSL Pinning Detector for Android APKs by petruknisme")
    parser.add_argument("-f", "--file", required=True, help="Path to the APK file")
    parser.add_argument("-p", "--pattern", default="patterns.json", help="Path to the JSON file containing SSL pinning patterns")
    parser.add_argument("-a", "--apktool", required=True, help="Path to the apktool.jar file")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose mode")
    args = parser.parse_args()

    print(f"{Fore.YELLOW}SSLPinDetect by petruknisme{Style.RESET_ALL}\n")

    check_java()
    check_apktool(args.apktool)

    apk_name = os.path.basename(args.file).replace(".apk", "")
    timestamp = int(time.time())
    output_dir = f"{apk_name}_decompile_{timestamp}"

    extract_apk(args.apktool, args.file, output_dir, args.verbose)

    frameworks = detect_frameworks(output_dir)
    if frameworks:
        print(f"{Fore.BLUE}Detected Frameworks: {', '.join(frameworks)}{Style.RESET_ALL}")

    patterns = load_patterns(args.pattern)
    results, match_count = search_ssl_pinning(output_dir, patterns)

    if not results:
        print("No SSL Pinning patterns detected.")
    else:
        print(f"{Fore.GREEN}Total Patterns Matched: {match_count}{Style.RESET_ALL}")
        for category, matches in results.items():
            print(f"{Fore.GREEN}Pattern detected: {category}{Style.RESET_ALL}")
            for file_path, line_number, line_preview in matches:
                print(f"  - {file_path}\n\t[Line {line_number}]: {line_preview}")

    shutil.rmtree(output_dir, ignore_errors=True)
