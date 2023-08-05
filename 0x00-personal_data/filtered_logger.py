#!/usr/bin/env python3
"""_summary"""
import re
import logging
import os
import mysql.connector
from typing import List

PII_FIELDS = ("email", "phone", "ssn", "password", "ip")


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"
    __fields = ""

    def __init__(self, fields):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.__fields = fields

    def format(self, record: logging.LogRecord) -> str:
        return filter_datum(self.__fields, self.REDACTION,
                            super().format(record), self.SEPARATOR)


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """_summary_

    Args:
        fields (_type_): _description_
        redaction (_type_): _description_
        message (_type_): _description_
        separator (_type_): _description_

    Returns:
        _type_: _description_
    """
    pattern = f"({'|'.join(fields)})=[^{separator}]+"
    return re.sub(pattern, rf"\1={redaction}", message)


def get_logger() -> logging.Logger:
    """_summary_

    Returns:
        logging.Logger: _description_
    """
    user_data = logging.getLogger('user_data')
    user_data.setLevel(logging.INFO)

    # Create a console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    console_handler.setFormatter(RedactingFormatter)

    user_data.addHandler(console_handler)

    return user_data


def get_db():
    """_summary_

    Returns:
        _type_: _description_
    """
    host = os.getenv('PERSONAL_DATA_DB_HOST')
    db = os.getenv('PERSONAL_DATA_DB_NAME')
    username = os.getenv('PERSONAL_DATA_DB_USERNAME')
    password = os.getenv('PERSONAL_DATA_DB_PASSWORD')
    con = mysql.connector.connect(host=host, database=db,
                                  user=username, password=password)
    return con


def main():
    """_summary_
    """
    conn = get_db()
    curr = conn.cursor(dictionary=True)
    curr.execute("SELECT * FROM users")

    logger = get_logger()
    for row in curr:
        message = ';'.join(["{}={}".format(key, value)
                           for key, value in row.items()])
        logger.info(message)

    curr.close()
    conn.close()


if __name__ == "__main__":
    main()
