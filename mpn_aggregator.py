import bisect


class MPNAggregator(object):

    def __init__(self, result_size):
        self.result_size = result_size
        self.results = []
        self._results_keys = set()
        self.mpns = {}

    def _generate_key(self, mpn):
        return "{0}:{1}".format(mpn.mpn, mpn.manufacturer)

    def as_json(self):
        return [mpn.as_json() for mpn in self.results]

    def update(self, mpn):
        mpn_key = self._generate_key(mpn)
        if mpn_key in self.mpns:
            existing_mpn = self.mpns[mpn_key]
            existing_mpn.occurrences += 1
            existing_mpn.designators.update(mpn.designators)
            mpn = existing_mpn
        else:
            self.mpns[mpn_key] = mpn
        if mpn_key not in self._results_keys:
            bisect.insort(self.results, mpn)
            self._results_keys.add(mpn_key)
            if len(self._results_keys) > self.result_size:
                removed_mpn = self.results.pop(-1)
                removed_key = self._generate_key(removed_mpn)
                self._results_keys.remove(removed_key)
        else:
            new_index = bisect.bisect_left(self.results, mpn)
            if self.results[new_index] != mpn:
                # Swap the MPNs
                tmp = self.results[new_index]
                self.results[new_index] = mpn
                self.results[new_index + 1] = tmp
