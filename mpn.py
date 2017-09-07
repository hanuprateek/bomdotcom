class MPN(object):

    def __init__(self, mpn, manufacturer, designators):
        self.mpn = mpn
        self.manufacturer = manufacturer
        self.designators = set(designators)
        self.occurrences = 1

    def as_json(self):
        return {
            "MPN": self.mpn,
            "Manufacturer": self.manufacturer,
            "ReferenceDesignators": sorted([d for d in self.designators]),
            "NumOccurrences": self.occurrences,
        }

    def _cmp(self, other):
        if self.__eq__(other):
            return 0
        occurrences_dif = other.occurrences - self.occurrences
        if occurrences_dif:
            return occurrences_dif
        return len(other.designators) - len(self.designators)

    def __lt__(self, other):
        return self._cmp(other) < 0

    def __le__(self, other):
        return self._cmp(other) <= 0

    def __eq__(self, other):
        if type(other) != MPN:
            return False
        return (self.mpn == other.mpn and
                self.manufacturer == other.manufacturer)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __ge__(self, other):
        return self._cmp(other) >= 0

    def __gt__(self, other):
        return self._cmp(other) > 0


def generate_mpn(encoded_mpn):
    encoded_mpn = encoded_mpn.strip()
    mpn = manufacturer = designators = None
    semi_colon_split = encoded_mpn.split(";")
    if len(semi_colon_split) == 3:
        # Type 3
        designators, mpn, manufacturer = semi_colon_split
    else:
        colon_split = encoded_mpn.split(":")
        if len(colon_split) == 3:
            # Type 1
            mpn, manufacturer, designators = colon_split
        else:
            # Type 2
            manufacturer_mpn, designators = colon_split
            manufacturer, mpn = manufacturer_mpn.split(" -- ")
    return MPN(mpn, manufacturer, designators.split(","))
