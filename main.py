import argparse
import os
from pypdf import PdfWriter

def valid_filepath(path):
    if not os.path.exists(path):
        raise argparse.ArgumentTypeError(f"The path {path}, does not exists")
    return path

parent_parser = argparse.ArgumentParser(description="PDF tool", add_help=False)
group = parent_parser.add_mutually_exclusive_group(required=True)
group.add_argument('-f', '--file', help='Provide File to PDFify', type=valid_filepath)
group.add_argument('-d', '--dir', help='Provide Directory to PDFify', type=valid_filepath)

parent_parser.add_argument('-o', '--output', help='Provide Output Filepath to PDFify', required=True)

parser = argparse.ArgumentParser(description="PDF tool")
subparsers = parser.add_subparsers(dest="command", required=True)

merge_parser = subparsers.add_parser(
    "merge",
    parents=[parent_parser],
    help="Merge multiple PDFs into one"
)

convert_parser = subparsers.add_parser(
    "convert",
    parents=[parent_parser],
    help="Convert files to PDF"
)

args = parser.parse_args()

# Make output file
os.makedirs(args.output, exist_ok=True)
OUTPUT_DIR = os.path.join(".", args.output)

if args.file and not os.path.isfile(args.file):
    raise IsADirectoryError(f"Expected file but recieved directory, {args.file}")

if args.dir and not os.path.isdir(args.dir):
    raise NotADirectoryError(f"Expected folder but got a file, {args.dir}")

def merge_files():
    merger = PdfWriter()
    for pdf in os.listdir(args.dir):
        fullpath = os.path.join(args.dir, pdf)
        merger.append(fullpath)
    merger.write(f"{OUTPUT_DIR}/test.png")

match args.command:
    case "merge":
        merge_files()
    case "convert":
        print("Convert")

# python3 main.py merge -d example
