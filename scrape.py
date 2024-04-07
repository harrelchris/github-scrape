import argparse
import csv
import datetime
import json
import pathlib
import urllib.request


def request(url: str) -> dict:
    response = urllib.request.urlopen(url)
    content = response.read()
    return json.loads(content)


def flatten_json(data: dict, prefix: str = None) -> dict:
    output = {}
    for key, value in data.items():
        if prefix:
            key = f"{prefix}_{key}"
        if isinstance(value, dict):
            output.update(flatten_json(data=value, prefix=key))
        else:
            output[key] = value
    return output


def write(data: dict, fp: str) -> None:
    path = pathlib.Path(fp)
    header = False if path.exists() else True

    with path.open(mode="a", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        if header:
            writer.writerow(data.keys())
        writer.writerow(data.values())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="url to scrape data from", type=str)
    parser.add_argument("--output", help="output file path", type=str)
    args = parser.parse_args()
    response = request(url=args.url)
    response["datetime"] = datetime.datetime.utcnow().isoformat()
    data = flatten_json(data=response)
    fp = args.output or "data.csv"
    write(data=data, fp=fp)


if __name__ == '__main__':
    main()
