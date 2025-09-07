
NotebookLM failed-upload helper
Version: 1.2.0

This script serves as a utility for users of Google's NotebookLM who have
experienced upload failures with .txt or .pdf files. When uploads get stuck,
they often display a persistent loading spinner. This tool is designed to
identify and extract the names of these failed files directly from the
webpage's source code, streamlining the re-upload process.

The recommended workflow is as follows: On the NotebookLM page with the failed
uploads, open your browser's developer tools and reload the pag (usually with F12)
and inspect the page elements. Find the `<body>` element, right-click, click copy, then 
click "copy element". Paste this entire block of code into a plain text file.

Run this script from your terminal, providing the path to your saved text file
as an argument. The script will parse the file and output a clean list of all
filenames that failed to upload. For an even faster workflow, this list can be
used with search utilities like Everything by voidtools. By joining the
filenames with a "|" (OR) operator, you can quickly locate all the files at
once for a batch re-upload. The "NotebookLM source manager" browser extension
can then be used to automatically handle any duplicates
