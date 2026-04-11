import os
import heapq

SKIP_DIRS = {"/proc", "/sys", "/dev", "/run"}

def dfs_traverse(root_path, heap, k):
    # walk through directory tree using depth-first search
    # it prints every file found along the way, and its size
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
            # avoid breaking the loop

        if  entry.is_dir():
            dfs_traverse(entry.path, heap, k)
        
        else:
            size = entry.stat().st_size
            # print(f"{size:>15,} bytes {entry.path}")
            heapq.heappush(heap, (size, entry.path))
            if len(heap) > k:
                heapq.heappop(heap)

if __name__ == "__main__":
    import sys

    paths = sys.argv[1:-1] if len(sys.argv) > 2 else [sys.argv[1]] if len(sys.argv) > 1 else ["."]
    k = int(sys.argv[-1]) if len(sys.argv) > 2 else 10

    print(f"Scanning: {', '.join(paths)}")
    print(f"Finding top {k} largest files...\n")

    heap = []
    for path in paths:
        dfs_traverse(path, heap, k)

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
