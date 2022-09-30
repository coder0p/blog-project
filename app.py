from website import create_app
import logging
import argparse
from website import db


def parse_args():
    parser = argparse.ArgumentParser(description = "Blog website")
    parser.add_argument("-d", "--debug", help = "Enable debug logging", action="store_true")
    parser.add_argument("--db", help="Name of database to use", action="store", default="blog")
    subcommands = parser.add_subparsers(help="Commands", dest="command", required=True)
    subcommands.add_parser("create_db", help="creating our database")
    subcommands.add_parser("delete_db", help="deleting database table")
    subcommands.add_parser("run", help="for running flask app")

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
    
    if args.command =="create_db":
        logger.info("Creating Database")
        db.create_all()
    
    elif args.command =="delete_db":
        logger.info("deleting Database")
        db.drop_all()
        
    elif args.command =="run":
        logger.info("Running flask app...")
        app = create_app()
        app.run(debug=True)
    
    else:
        logger.warning("%s not implemented", args.command)

  
if __name__ == "__main__":
    main()

