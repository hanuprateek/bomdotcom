import unittest
from mpn import generate_mpn
from mpn_aggregator import MPNAggregator


class MPNAggregatorTests(unittest.TestCase):

    def test_as_json(self):
        panasonic = generate_mpn("TSR-1002:Panasonic:A1,D2")
        keystone = generate_mpn("A1,B2,C8;TSR-1002;Keystone")
        aggregator = MPNAggregator(2)
        aggregator.update(panasonic)
        aggregator.update(keystone)
        assert aggregator.as_json() == [
            keystone.as_json(),
            panasonic.as_json(),
        ]

    def test_generate_key(self):
        panasonic = generate_mpn("TSR-1002:Panasonic:A1,D2")
        keystone = generate_mpn("A1,B2,C8;TSR-1002;Keystone")
        aggregator = MPNAggregator(1)
        assert aggregator._generate_key(panasonic) == "TSR-1002:Panasonic"
        assert aggregator._generate_key(keystone) == "TSR-1002:Keystone"

    def test_update(self):
        aggregator = MPNAggregator(2)
        panasonic = generate_mpn("TSR-1002:Panasonic:A1,D2")
        panasonic_key = aggregator._generate_key(panasonic)
        keystone = generate_mpn("A1,B2,C8;TSR-1002;Keystone")
        keystone_key = aggregator._generate_key(keystone)
        garbage = generate_mpn("A1;TSR-1002;Garbage")
        garbage_key = aggregator._generate_key(garbage)

        # Ensure MPN added to results
        aggregator.update(panasonic)
        assert panasonic in aggregator.results
        assert panasonic_key in aggregator._results_keys

        # Ensure existing MPN is updated
        panasonic = generate_mpn("TSR-1002:Panasonic:A1,D2")
        aggregator.update(panasonic)
        assert aggregator.results[0].occurrences == 2

        aggregator.update(garbage)
        aggregator.update(garbage)

        # Ensure when a new MPN comes in,
        # it doesn't replace higher occurrence MPNs
        aggregator.update(keystone)
        assert keystone not in aggregator.results
        assert keystone_key not in aggregator._results_keys

        # Boot the garbage result, which has same occurrences,
        # but fewer designators
        aggregator.update(keystone)
        assert keystone in aggregator.results
        assert keystone_key in aggregator._results_keys
        assert garbage not in aggregator.results
        assert garbage_key not in aggregator._results_keys

        # Reorder results
        assert aggregator.results[0].manufacturer == "Keystone"
        assert aggregator.results[1].manufacturer == "Panasonic"
        aggregator.update(panasonic)
        assert aggregator.results[0].manufacturer == "Panasonic"
        assert aggregator.results[1].manufacturer == "Keystone"


if __name__ == "__main__":
    unittest.main()
