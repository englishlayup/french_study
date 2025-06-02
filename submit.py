#!/usr/bin/env python3
"""
Script to copy text files to clipboard with optional prompt prepending.
"""

import argparse
import os
import sys
import subprocess
import platform


def copy_to_clipboard(text: str):
    """Copy text to system clipboard using platform-appropriate method."""
    system = platform.system()

    try:
        if system == "Darwin":  # macOS
            process = subprocess.Popen(["pbcopy"], stdin=subprocess.PIPE)
            process.communicate(text.encode("utf-8"))
        elif system == "Linux":
            # Try xclip first, then xsel as fallback
            try:
                process = subprocess.Popen(
                    ["xclip", "-selection", "clipboard"], stdin=subprocess.PIPE
                )
                process.communicate(text.encode("utf-8"))
            except FileNotFoundError:
                process = subprocess.Popen(
                    ["xsel", "--clipboard", "--input"], stdin=subprocess.PIPE
                )
                process.communicate(text.encode("utf-8"))
        elif system == "Windows":
            process = subprocess.Popen(["clip"], stdin=subprocess.PIPE, shell=True)
            process.communicate(text.encode("utf-8"))
        else:
            raise RuntimeError(f"Unsupported operating system: {system}")
    except FileNotFoundError as e:
        print(f"Error: Required clipboard utility not found. {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error copying to clipboard: {e}", file=sys.stderr)
        sys.exit(1)


def read_file(filepath: str):
    """Read and return the contents of a file."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found.", file=sys.stderr)
        sys.exit(1)
    except PermissionError:
        print(f"Error: Permission denied reading '{filepath}'.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file '{filepath}': {e}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Copy text file contents to clipboard, optionally prepending prompt file."
    )
    parser.add_argument("file_path", help="Path to the text file to copy")
    parser.add_argument(
        "-n",
        "--new",
        action="store_true",
        help="Prepend prompt.txt content before copying to clipboard",
    )

    args = parser.parse_args()

    # Read the main file
    file_content = read_file(args.file_path)

    # If --new flag is set, prepend prompt.txt content
    if args.new:
        # Get the directory where this script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        prompt_file = os.path.join(script_dir, "prompt.txt")

        prompt_content = read_file(prompt_file)
        final_content = prompt_content + file_content
    else:
        final_content = file_content

    # Copy to clipboard
    copy_to_clipboard(final_content)

    if args.new:
        print(f"Copied '{args.file_path}' with prompt to clipboard.")
    else:
        print(f"Copied '{args.file_path}' to clipboard.")


if __name__ == "__main__":
    main()
