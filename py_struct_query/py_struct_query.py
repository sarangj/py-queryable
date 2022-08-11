import dataclasses
import sqlite3
import typing


class db:

    def __init__(self, **structs):
        self.conn = None
        self.structs = structs

    def fetchone(self, query: str):
        return self.conn.execute(query).fetchone()

    def fetchall(self, query: str):
        return self.conn.execute(query).fetchall()

    def __enter__(self):
        self.conn = sqlite3.connect(":memory:")
        for name, data in self.structs.items():
            table = db._table(data)
            print(name)
            self._create_table(name, table.columns)
            self._populate_table(name, len(table.columns), table.rows)
        return self

    def _create_table(self, name, columns):
        # This seems sketch
        q = f"CREATE TABLE {name} ({', '.join(columns)})"
        print(q)
        self.conn.execute(q)

    def _populate_table(self, name, num_columns, rows):
        insert_query = f"INSERT INTO {name} VALUES({', '.join('?' for _ in range(num_columns))})"
        self.conn.executemany(insert_query, list(rows))

    @staticmethod
    def _table(data):
        first = data[0]
        if isinstance(first, dict):
            return _Table(
                columns=first.keys(),
                rows=(tuple(d.values()) for d in data),
            )

        if isinstance(first, list):
            return _Table(columns=first, rows=(t for t in data[1:]))

        raise ValueError()

    def __exit__(self, *_args, **_kwargs):
        self.conn.close()


@dataclasses.dataclass
class _Table:

    columns: list[str]
    rows: typing.Iterator[tuple[typing.Any]]
