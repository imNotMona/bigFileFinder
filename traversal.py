import os
import heapq

SKIP_DIRS = {"/proc", "/sys", "/dev", "/run"}
# these directories contain virtual file systems not containing any meaningful data
# skips these on linux filesystems

def dfs_traverse(root_path, heap, k):
    # Recursively explores directories to find the largest files.
    # Uses a min-heap to maintain only the top 'k' files efficiently.
    if root_path in SKIP_DIRS:
        return
    try: 
        entries = list(os.scandir(root_path))
    except PermissionError: 
        print(f" [skipped - no permissions]: {root_path}")
        return
    
    for entry in entries:
        if entry.is_symlink():
            continue
            # Skip symlinks to prevent circular references or redundant scanning
        if  entry.is_dir():
            # Recursive call to dive deeper into the directory tree
            dfs_traverse(entry.path, heap, k)
        
        else:
            try:
                size = entry.stat().st_size
                # Push current file onto heap. heapq stores smallest items at the top.
                heapq.heappush(heap, (size, entry.path))

                # If heap exceeds size k, remove the smallest item.
                # This ensures the heap always contains the k largest files seen so far.
                if len(heap) > k:
                    heapq.heappop(heap)
            except (OSError, FileNotFoundError):
                # Handle cases where files disappear or are inaccessible during scan
                continue

if __name__ == "__main__":
    import sys

    # Argument Parsing Logic:
    # 1. If >2 args: everything except the last is a path; the last is 'k'.
    # 2. If 1 arg: treat as path, default k=10.
    # 3. If no args: use current directory, default k=10.

    if len(sys.argv) > 2 and sys.argv[-1].isdigit():
        paths = sys.argv[1:-1]
        k = int(sys.argv[-1])
    elif len(sys.argv) >= 2:
        paths = sys.argv[1:]
        k = 10
    else:
        paths = ["."]
        k = 10

    print(f"Scanning: {', '.join(paths)}")
    print(f"Finding top {k} largest files...\n")

    heap = []
    for path in paths:
        dfs_traverse(path, heap, k)

    # Sort the final heap in descending order for the final report
    results = sorted(heap, reverse=True)
    
    print(f"{'Rank':<6} {'Size':>15}  {'Path'}")
    print("-" * 80)
    for rank, (size, path) in enumerate(results, start=1):
        # Convert bytes to a human-readable format
        if size >= 1_073_741_824:
            size_str = f"{size / 1_073_741_824:.2f} GB"
        elif size >= 1_048_576:
            size_str = f"{size / 1_048_576:.2f} MB"
        elif size >= 1024:
            size_str = f"{size / 1024:.2f} KB"
        else:
            size_str = f"{size} B"
        print(f"{rank:<6} {size_str:>15}  {path}")
