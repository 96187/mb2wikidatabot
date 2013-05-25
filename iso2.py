"""
This is a bot to automatically add ISO 3166-2 codes to Wikidata.

Usage: python2 iso2.py [options]

Command line options:

-dryrun:    Don't write anything on the server
-limit:x:   Only handle x artists
"""
from bot import common, const


MB_WIKI_AREA_QUERY =\
"""
SELECT
	i2.code,
	url
FROM
	area
JOIN iso_3166_2 i2
	ON i2.area = area.id
JOIN l_area_url
	ON entity0 = area.id
JOIN url
	url.id = entity1
WHERE
	url ~ 'wikidata'
ORDER BY
	i2.code
LIMIT %s;
"""
#LEFT JOIN bot_wikidata_artist_processed AS bwap
#    ON a.gid=bwap.gid
#WHERE
#    lt.id=179
#AND
#    bwap.gid is NULL

CREATE_PROCESSED_TABLE_QUERY =\
"""
CREATE TABLE IF NOT EXISTS bot_wikidata_area_code_processed (
    code VARCHAR NOT NULL PRIMARY KEY,
    processed timestamp with time zone DEFAULT now()
);

"""

AREA_DONE_QUERY = \
"""
INSERT INTO bot_wikidata_area_code_processed (GID)
    SELECT (%(code)s)
    WHERE NOT EXISTS (
        SELECT 1
        FROM bot_wikidata_area_code_processed
        WHERE code = (%(code)s)
);
"""


def area_done(mbid):
    common.db.cursor().execute(AREA_DONE_QUERY, {'code': mbid})


if __name__ == '__main__':
    common.mainloop(const.ARTIST_MBID_PID, CREATE_PROCESSED_TABLE_QUERY,
                MB_WIKI_AREA_QUERY, area_done)
