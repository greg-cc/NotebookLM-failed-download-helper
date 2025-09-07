#!/usr/bin/env python3
"""
NotebookLM failed-upload helper
Version: 1.1.1

Use F11 and paste body element on NotebookLM page into text file for input.
Will extract a list of failed files. I use voidtools and join all filenames
with "|" divider to reupload them fast. "NotebookLM source manager"
extension will automatically delete duplicates.
"""

import re
import sys

__version__ = "1.1.1" # Version of the script

def extract_filenames(text_to_search):
  """
  Extracts filenames ending in .txt or .pdf that appear after each
  instance of 'loading-spinner-container'.

  Args:
    text_to_search: The string to search for filenames.

  Returns:
    A list of extracted filenames, or an empty list if none are found.
  """
  # To handle very large files efficiently and avoid potential regex performance
  # issues with '.*?', we first split the text by our key phrase.
  # This isolates the text that follows each instance of the phrase.
  search_key = "loading-spinner-container"
  chunks = text_to_search.split(search_key)

  found_files = []
  
  # The pattern now only needs to find the first valid filename.
  # We compile it for slightly better performance in a loop.
  filename_pattern = re.compile(r"(\b[\w-]+\.(?:txt|pdf)\b)")

  # We iterate through the chunks, starting from the second one (index 1),
  # as the first chunk is the text *before* the first search_key.
  for chunk in chunks[1:]:
      # We search for the first match in the chunk.
      # The search is multi-line by default, but we'll add re.DOTALL just in case
      # for patterns that might need it, though this one doesn't strictly require it.
      match = filename_pattern.search(chunk, re.DOTALL)
      if match:
          # If a match is found, we append the captured group (the filename) to our list.
          found_files.append(match.group(1))

  return found_files

def run_internal_test():
  """
  Runs a predefined test case to demonstrate the regex functionality.
  """
  print("--- Running Internal Test Case ---")
  # A sample string that contains the target pattern in a few places,
  # including one that spans multiple lines.
  test_text = """
  Some initial text here just for context.
  Here's a loading-spinner-container and the file is document-v1.pdf right after it.
  Another line, maybe with some other data.
  ignorethis.txt
  Then we see loading-spinner-container again for report-final.txt.
  
  And now for a multi-line case to test the DOTALL flag.
  The text is here: loading-spinner-container
  ... and the file is way down here on another line ...
  ... my-multiline-report.pdf ...
  
  And one more time for good measure: loading-spinner-container should find my-special-document.pdf.
  This one should not match: another-container report.docx
  """
  print("Searching in the following test text:\n" + test_text)
  
  test_results = extract_filenames(test_text)

  if test_results:
    print(f"Internal test found {len(test_results)} file(s):")
    for filename in test_results:
      print(f"- {filename}")
  else:
    print("Internal test found no matching files.")
  print("--- Internal Test Finished ---\n")


def main():
  """
  Main function to run the filename extraction program.
  It now accepts a file path as a command-line argument.
  """
  print("Python Filename Extractor")
  print(f"Version: {__version__}")
  print("=" * 25)

  # Run the internal test case first
  run_internal_test()

  # Check if a filename was provided as a command-line argument
  if len(sys.argv) > 1:
    filepath = sys.argv[1]
    print(f"\nReading from file: {filepath}...")
    try:
      # Open and read the entire file
      with open(filepath, 'r', encoding='utf-8') as f:
        file_contents = f.read()
      
      print("Searching for filenames...")
      extracted_files = extract_filenames(file_contents)

      if extracted_files:
        print(f"\nSuccessfully extracted {len(extracted_files)} filename(s):")
        for filename in extracted_files:
          print(f"- {filename}")
      else:
        print("\nNo matching filenames were found in the file.")

    except FileNotFoundError:
      print(f"\nError: The file '{filepath}' was not found.")
    except Exception as e:
      print(f"\nAn error occurred while reading the file: {e}")
  else:
    print("This script now reads from a file instead of pasted input.")
    print("Usage: python extract_filenames.py <path_to_your_file.txt>")


if __name__ == "__main__":
  main()

