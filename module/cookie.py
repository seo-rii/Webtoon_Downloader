class NCookie:
    def __init__(self, auth, sess):
        self._auth = auth
        self._sess = sess


class DCookie:
    def __init__(self, hm_cu, hts, prof, ts, lsid):
        self._hm_cu = hm_cu
        self._hts = hts
        self._prof = prof
        self._ts = ts
        self._lsid = lsid


class KCookie:
    def __init__(self, hm_cu, hts, prof, ts, lsid):
        self._hm_cu = hm_cu
        self._hts = hts
        self._prof = prof
        self._ts = ts
        self._lsid = lsid
