#!/usr/bin/env python3

from colorama import Fore, Style

from lib.args import process_args
from lib.embed import embed, extract


def main():

  args = process_args()

  print(Fore.YELLOW + f"PDF File Embedder")
  print(Style.RESET_ALL)

  if args.command == "embed":
     embed(args.pdf, args.cloak, args.key, args.files, args.output)

  elif args.command == "extract":
     extract(args.pdf, args.key, args.output)

  else:
     raise(f"Command must be either embed or extract: {args.command}")


if __name__ == "__main__":
    main()

