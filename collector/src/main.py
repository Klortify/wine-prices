from db import init_db
from models import WinePrice
from etl import run_etl


def main():
    init_db([WinePrice])

    run_etl()


if __name__ == "__main__":
    main()