#!/usr/bin/env python3

from colorama import Fore, Style

from lib.args import process_args
from lib.embed import PdfFileEmbedder
from lib.extract import extract
from lib.files import compute_files


def main():

  args = process_args()

  print(Fore.YELLOW + f"PDF File Embedder")
  print(Style.RESET_ALL)

  if args.command == "embed":
     files = compute_files(args.files, args.dirs)
     embedder = PdfFileEmbedder(args.pdf)
     embedder.embed_files_in_pdf(files, args.output, args.cloak, True, args.key, )

  elif args.command == "extract":
     extract(args.pdf, args.key, args.output)

  else:
     raise(f"Command must be either embed or extract: {args.command}")


if __name__ == "__main__":
    main()
