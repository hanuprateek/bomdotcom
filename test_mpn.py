import unittest
from mpn import generate_mpn


class MPNTests(unittest.TestCase):

    def test_generate_mpn(self):
        assert generate_mpn("TSR-1002:Panasonic:A1,D2").as_json() == {
            "MPN": "TSR-1002",
            "ReferenceDesignators": ["A1", "D2"],
            "NumOccurrences": 1,
            "Manufacturer": "Panasonic"
        }
        assert generate_mpn("Panasonic -- TSR-1002:A1").as_json() == {
            "MPN": "TSR-1002",
            "ReferenceDesignators": ["A1"],
            "NumOccurrences": 1,
            "Manufacturer": "Panasonic"
        }
        assert generate_mpn("A1,B2,C8;TSR-1002;Keystone").as_json() == {
            "MPN": "TSR-1002",
            "ReferenceDesignators": ["A1", "B2", "C8"],
            "NumOccurrences": 1,
            "Manufacturer": "Keystone"
        }

    def test_MPN_cmp(self):
        keystone = generate_mpn("A1,B2,C8;TSR-1002;Keystone")
        panasonic = generate_mpn("Panasonic -- TSR-1002:A1")
        # Identity
        assert keystone._cmp(keystone) == 0
        assert keystone.__eq__(keystone)
        assert keystone.__eq__(1) is False
        assert keystone.__ne__(keystone) is False
        assert keystone.__ne__(panasonic)
        # Designators
        assert panasonic._cmp(keystone) == 2
        assert keystone.__lt__(panasonic)
        assert panasonic.__gt__(keystone)
        keystone.occurrences += 1
        # Occurrences
        assert panasonic._cmp(keystone) == 1
        assert keystone._cmp(panasonic) == -1


if __name__ == "__main__":
    unittest.main()
