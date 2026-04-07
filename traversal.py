import os
import heapq


def dfs_traverse(root_path):
    # walk through directory tree using depth-first search
    # it prints every file found along the way, and its size

    try: 
        entries = list(os.scandir(root_path))
    except PermissionError: 
        print(f" [skipped - no permissions]: {root_path}")
        return
    
    for entry in entries:
        if entry.is_symlink():
            continue
            # avoid breaking the loop

        if  entry.is_dir():
            dfs_traverse(entry.path)
        
        else:
            size = entry.stat().st_size
            print(f"{size:>15,} bytes {entry.path}")

if __name__ == "__main__":
    import sys

    path  =  sys.argv[1] if len(sys.argv) > 1 else "."

    print(f"Scanning: {path}\n")
    dfs_traverse(path)
