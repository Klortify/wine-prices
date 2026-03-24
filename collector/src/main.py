from messaging import publish_done_event
from db import init_db
from models import WinePrice
from etl import run_etl


def main():
    init_db([WinePrice])

    inserted = run_etl()

    publish_done_event(inserted)


if __name__ == "__main__":
    main()