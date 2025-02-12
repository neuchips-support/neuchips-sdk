import os
import glob
import sys

def generate_requirements(platform):
    pattern = f"../../neu_pytorch_extension/*/*{platform}*.whl"

    output_file = "requirements.txt"
    try:
        with open(output_file, 'w') as f:
            for whl in glob.glob(pattern):
                f.write(f"{whl}\n")
        print(f"Generated {output_file} for platform: {platform}")
    except Exception as e:
        print(f"Error generating {output_file}: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 gen_requires.py <platform>")
        print("Example: python3 gen_requires.py linux")
        sys.exit(1)

    platform = sys.argv[1].lower()
    if platform not in ['linux', 'win']:
        print("Error: Platform must be 'linux' or 'win'")
        sys.exit(1)

    generate_requirements(platform)
