import dataclasses

SETUP_QUERY = """
CREATE TABLE IF NOT EXISTS resets (
    user_id BIGINT PRIMARY KEY,
    last_reset INTEGER NOT NULL
);
"""

GET_RESET_QUERY = """
SELECT last_reset
FROM resets
WHERE user_id = $1;
"""

UPDATE_RESET_QUERY = """
INSERT INTO resets (user_id, last_reset)
VALUES ($1, $2)
ON CONFLICT (user_id) DO UPDATE SET last_reset = $2;
"""


@dataclasses.dataclass(frozen=True, slots=True, kw_only=True)
class QueryHolder:
    setup: str
    get_reset: str
    update_reset: str


queries = QueryHolder(
    setup=SETUP_QUERY,
    get_reset=GET_RESET_QUERY,
    update_reset=UPDATE_RESET_QUERY,
)
