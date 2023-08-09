#!/usr/bin/env python3
"""Module that defines a function: filter_datum for Task_0"""
import logging
import mysql.connector
from os import getenv
import re
from typing import List


PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """Initializes any @RedactingFormatter instance"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.__fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Returns a formatted message"""
        msg: str = super().format(record)
        msg = filter_datum(self.__fields, self.REDACTION,
                           msg, self.SEPARATOR)
        return msg


def filter_datum(fields: List[str],
                 redaction: str,
                 message: str,
                 separator: str) -> str:
    """Returns a log message

    Args:
        fields (list): all fields to obfuscate
        redaction (str): a string representing by what the field will
                         be obfuscated
        message (str): log line
        separator (str): character separating all fields in the log line
    Returns:
        Log message as string
    """
    final_message: str = message
    for field in fields:
        pattern: str = r"({}=)([^{}]+)".format(field, separator)
        final_message = re.sub(pattern, r"\1" + redaction, final_message)

    return final_message


def get_logger() -> logging.Logger:
    """Returns a logging.Logger object"""
    log_obj = logging.getLogger(name="user_data")
    log_obj.setLevel(logging.INFO)
    log_obj.propagate = False
    handler = logging.StreamHandler()
    formatter = RedactingFormatter(PII_FIELDS)
    handler.setFormatter(formatter)

    log_obj.addHandler(handler)

    return log_obj


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Returns a connector to a database object"""
    username = getenv("PERSONAL_DATA_DB_USERNAME") or "root"
    password = getenv("PERSONAL_DATA_DB_PASSWORD") or ""
    host = getenv("PERSONAL_DATA_DB_HOST") or "localhost"
    db = getenv("PERSONAL_DATA_DB_NAME")
    conn = mysql.connector.connect(user=username,
                                   password=password,
                                   host=host,
                                   database=db)

    return conn


def main():
    """Main entry point"""
    db = get_db()
    table = "users"
    logger = get_logger()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    fields = cursor.column_names
    for row in cursor:
        message = "".join("{}={}; ".format(k, v) for k, v in zip(fields, row))
        logger.info(message.strip())

    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
