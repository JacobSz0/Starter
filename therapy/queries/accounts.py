from queries.pool import pool
from pydantic import BaseModel
from typing import List, Union


class Error(BaseModel):
    message: str


class AccountIn(BaseModel):
    username: str
    email: str
    password: str


class AccountOut(BaseModel):
    id: int
    username: str
    email: str


class AccountOutWithPassword(AccountOut):
    hashed_password: str


class DuplicateAccountError(ValueError):
    pass


class AccountQueries:
    def create(
        self,
        info: AccountIn,
        hashed_password: str,
    ) -> AccountOutWithPassword:
        with pool.connection() as conn:
            with conn.cursor() as cur:
                result = cur.execute(
                    """
                    INSERT INTO accounts
                    (
                        username,
                        email,
                        hashed_password
                    )
                    VALUES
                    (%s, %s, %s)
                    RETURNING id
                    """,
                    [info.username, info.email, hashed_password],
                )
                id = result.fetchone()[0]
                # Return new data
                old_data = info.dict()
                return AccountOut(id=id, **old_data)

    def get_one_account(self, username: str) -> AccountOutWithPassword:
        with pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                SELECT id, username, email, hashed_password
                FROM accounts
                WHERE username = %s
                """,
                    [username],
                )
                record = None
                row = cur.fetchone()
                if row is not None:
                    record = {}
                    for i, column in enumerate(cur.description):
                        record[column.name] = row[i]
                return record

    def get_all_accounts(self) -> Union[Error, List[AccountOut]]:
        with pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                SELECT id, username, email
                FROM accounts
                """
                )
                results = [
                    AccountOut(
                        id=row[0],
                        username=row[1],
                        email=row[2],
                    )
                    for row in cur.fetchall()
                ]
                return results

    def delete(self, id: int) -> bool:
        try:
            with pool.connection() as conn:
                with conn.cursor() as db:
                    db.execute(
                        """
                    DELETE FROM accounts
                    WHERE id = %s
                    """,
                        [id],
                    )
                    return True
        except Exception as e:
            print(e)
            return False
