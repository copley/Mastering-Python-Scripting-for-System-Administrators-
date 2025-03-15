import os

# Define root directory
root_dir = os.path.expanduser("~/GithubApps/Mastering-Python-Scripting-for-System-Administrators-")
output_file = os.path.join(root_dir, "combined_scripts.py")

# Determine the highest numbered Chapter directory
def get_max_chapter(root_dir):
    max_chapter = 0
    for entry in os.listdir(root_dir):
        if entry.startswith("Chapter") and entry[7:].isdigit():
            max_chapter = max(max_chapter, int(entry[7:]))
    return max_chapter

max_chapter = get_max_chapter(root_dir)

# Open output file in write mode
with open(output_file, "w", encoding="utf-8") as outfile:
    # Loop through Chapter01 to ChapterN
    for i in range(1, max_chapter + 1):
        chapter_dir = os.path.join(root_dir, f"Chapter{i:02d}")

        # Check if directory exists
        if os.path.isdir(chapter_dir):
            outfile.write(f"\n# --- {chapter_dir} ---\n\n")

            # Loop through files in directory
            for filename in sorted(os.listdir(chapter_dir)):
                if filename.endswith(".py"):  # Process only .py files
                    file_path = os.path.join(chapter_dir, filename)

                    with open(file_path, "r", encoding="utf-8") as infile:
                        outfile.write(f"# --- {filename} ---\n")
                        outfile.write(infile.read() + "\n\n")

print(f"All scripts combined into: {output_file}")
