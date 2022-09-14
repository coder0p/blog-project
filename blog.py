import argparse
from ast import arg
from distutils.log import error
import logging
from flask import Flask, request

from website import db

logger = None

def parse_args():
    parser = argparse.ArgumentParser(description = "Web crawler")
    parser.add_argument("-d", "--debug", help = "Enable debug logging", action="store_true")
    parser.add_argument("--db", help="Name of database to use", action="store", default="blog")
    subcommands = parser.add_subparsers(help="Commands", dest="command", required=True)
    subcommands.add_parser("cdb", help="creating our database")
    subcommands.add_parser("ddt", help="deleting database table")

    return parser.parse_args()

def configure_logging(level=logging.INFO):
    global logger
    logger = logging.getLogger("blog_web")
    logger.setLevel(level)
    screen_handler = logging.StreamHandler()
    screen_handler.setLevel(level)
    formatter = logging.Formatter("[%(levelname)s] : %(filename)s(%(lineno)d) : %(message)s")
    screen_handler.setFormatter(formatter)
    logger.addHandler(screen_handler)



def main():
    args = parse_args()

    if args.debug:
        configure_logging(logging.DEBUG)
    else:
        configure_logging(logging.INFO)
    
    if args.command =="ctb":
        logger.info("Creating Database")
        db.create_all()
    
    elif args.command =="ddt":
        logger.info("deleting Database")
        db.drop_all()
    else:
        logger.warning("%s not implemented", args.command)

if __name__ == "__main__":
    main()