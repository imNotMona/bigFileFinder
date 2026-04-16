FILE SYSTEM ANALYZER
====================
A command line tool that scans one or more directories and reports the largest
files found. Built using depth-first search (DFS) for traversal and a min-heap
for efficient top-K tracking.
 
 
REQUIREMENTS
------------
Python 3.x
No external libraries required.
 
 
USAGE
-----
Scan a single folder and show the top 10 largest files (default):
    python3 traversal.py /path/to/folder
 
Scan a single folder and show the top 20 largest files:
    python3 traversal.py /path/to/folder 20
 
Scan multiple folders at once and show the top 10 largest files:
    python3 traversal.py /path/one /path/two 10
 
Scan from the root of the filesystem (requires sudo on Linux):
    sudo python3 traversal.py / 10
 
 
ARGUMENTS
---------
paths   One or more directories to scan. Pass multiple paths separated by spaces.
k       The number of results to show. Must be the last argument. Defaults to 10.
 
 
HOW IT WORKS
------------
DFS Traversal
    The script walks the directory tree recursively using depth-first search.
    When it encounters a folder it immediately recurses into it before continuing
    with the current level. Symlinks are skipped to prevent infinite loops.
    Directories that cannot be read due to permissions are skipped with a warning.
 
Min-Heap (Top-K Tracking)
    As files are discovered they are pushed onto a min-heap of size K. If the
    heap exceeds K entries, the smallest file is immediately removed. This means
    only K files are held in memory at any time regardless of how large the
    filesystem is. After scanning, results are sorted largest-first and printed.
 
Multiple Drives
    Multiple paths can be passed in a single command. All paths feed into the
    same heap, so results are ranked across all locations combined.
 
 
SKIPPED DIRECTORIES (Linux)
---------------------------
The following virtual filesystems are skipped automatically as they do not
contain real files on disk and can cause errors if scanned:
 
    /proc   /sys   /dev   /run
 
 
OUTPUT
------
Results are printed as a ranked table with human-readable file sizes:
 
    Rank   Size             Path
    --------------------------------------------------------------------------------
    1       40.10 GB        /media/user/hdd/SteamLibrary/steamapps/...
    2       38.61 GB        /home/user/.local/share/Steam/steamapps/...
 
 
NOTES
-----
- On Linux, scanning from root (/) requires sudo to access all directories.
- On Windows, paths use backslashes e.g. python traversal.py C:\ D:\ 10
- File sizes reflect apparent size (st_size), not actual disk usage.
