def NCookie(auth, sess):
    return {
        'NID_AUT': auth,
        'NID_SES': sess
    }


def DCookie(hm_cu, hts, prof, ts, lsid):
    return {
        'HM_CU': hm_cu,
        'HTS': hts,
        'PROF': prof,
        'TS': ts,
        'LSID': lsid
    }


def KCookie(hm_cu, hts, prof, ts, lsid):
    return {
        'HM_CU': hm_cu,
        'HTS': hts,
        'PROF': prof,
        'TS': ts,
        'LSID': lsid
    }
