import os
import sys
import openai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Debug: Print environment variable value (partial for security)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("Error: OPENAI_API_KEY environment variable is not set.")

# Debug: Print first 5 and last 5 characters of the key (for verification)
print(f"OPENAI_API_KEY loaded: {OPENAI_API_KEY[:5]}...{OPENAI_API_KEY[-5:]}")

# Set the API key for OpenAI
openai.api_key = OPENAI_API_KEY


def get_max_chapter(root_dir):
    """Return the highest numbered Chapter directory (Chapter01, Chapter02, etc.)."""
    max_chapter = 0
    for entry in os.listdir(root_dir):
        if entry.startswith("Chapter") and entry[7:].isdigit():
            max_chapter = max(max_chapter, int(entry[7:]))
    return max_chapter


def get_code_explanation(code_snippet: str) -> str:
    """
    Use ChatCompletion (GPT-3.5-turbo, for example) to summarize the given Python code
    in 1-3 sentences. Returns the AI-generated summary string.
    """
    try:
        client = openai.OpenAI(api_key=OPENAI_API_KEY)  # ✅ Create OpenAI client

        messages = [
            {
                "role": "system",
                "content": ("You are a helpful assistant that summarizes Python code. "
                            "Please be concise and clear.")
            },
            {
                "role": "user",
                "content": f"Summarize the following Python code in 1-3 sentences:\n\n{code_snippet}"
            }
        ]

        response = client.chat.completions.create(  # ✅ New API format
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=100,
            temperature=0.7
        )

        # Extract the assistant's response
        summary = response.choices[0].message.content.strip()
        return summary

    except Exception as e:
        sys.stderr.write(f"OpenAI API call failed: {e}\n")
        return "No description available due to an OpenAI API error."

def main():
    # Define the root directory
    root_dir = os.path.expanduser("~/GithubApps/Mastering-Python-Scripting-for-System-Administrators-")
    output_file = os.path.join(root_dir, "combined_scripts.py")

    # Get the maximum chapter number
    max_chapter = get_max_chapter(root_dir)

    # Open output file in write mode
    with open(output_file, "w", encoding="utf-8") as outfile:
        # Loop through Chapter01 to ChapterN
        for i in range(1, max_chapter + 1):
            chapter_dir = os.path.join(root_dir, f"Chapter{i:02d}")

            if os.path.isdir(chapter_dir):
                outfile.write(f"\n# --- {chapter_dir} ---\n\n")

                # Loop through .py files in this chapter directory
                for filename in sorted(os.listdir(chapter_dir)):
                    if filename.endswith(".py"):
                        file_path = os.path.join(chapter_dir, filename)

                        # Read the content of the file
                        with open(file_path, "r", encoding="utf-8") as infile:
                            code_text = infile.read()

                        # Write the code's header and content
                        outfile.write(f"# --- {filename} ---\n")
                        outfile.write(code_text + "\n\n")

                        # Get a short summary from OpenAI ChatCompletion
                        description = get_code_explanation(code_text)

                        # Append the summary as comments below the code
                        outfile.write("# AI Description:\n")
                        for line in description.splitlines():
                            outfile.write("# " + line + "\n")
                        outfile.write("\n")

    print(f"All scripts combined into: {output_file}")


if __name__ == "__main__":
    main()
