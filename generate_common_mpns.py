import fileinput
import json

from mpn import generate_mpn
from mpn_aggregator import MPNAggregator


def run():
    aggregator = None
    for line in fileinput.input():
        if not aggregator:
            aggregator = MPNAggregator(int(line))
        else:
            mpn = generate_mpn(line)
            aggregator.update(mpn)
    print json.dumps(aggregator.as_json(), indent=4)


if __name__ == "__main__":
    run()
