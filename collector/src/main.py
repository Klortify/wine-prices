from messaging import publish_done_event
from etl import run_etl


def main():
    inserted = run_etl()

    publish_done_event(inserted)


if __name__ == "__main__":
    main()