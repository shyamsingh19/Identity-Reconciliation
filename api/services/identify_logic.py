from fastapi import HTTPException
from datetime import datetime
import logging

from db.database import get_connection


logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)


async def identify_contact(email: str = None, phoneNumber: str = None):
    """
    Identifies a contact given an email and/or phone number.

    1. Find all matching contacts.
    2. If no match, insert new as primary.
    3. DFS to gather all connected contacts.
    4. Find the true primary (oldest contact).
    5. Convert any newer primaries to secondary if needed.
    6. If incoming email/phone not in any record, insert new secondary.
    7. Prepare response.
    """
    conn = get_connection()
    cursor = conn.cursor()

    # Find all matching contacts
    try:
        cursor.execute(
            """
            SELECT * FROM Contact
            WHERE deletedAt IS NULL
            AND (%s IS NOT NULL AND email = %s
                OR %s IS NOT NULL AND phoneNumber = %s)
        """,
            (email, email, phoneNumber, phoneNumber),
        )
        matching_contacts = cursor.fetchall()
    except Exception as e:
        logger.error(f"Error in matching contacts: {e}")

    # If no match, insert new as primary
    try:
        if not matching_contacts:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute(
                """
                INSERT INTO Contact (email, phoneNumber, linkedId, linkPrecedence, createdAt, updatedAt)
                VALUES (%s, %s, NULL, 'primary', %s, %s)
            """,
                (email, phoneNumber, now, now),
            )
            logger.info(f"Insert successful. ID: {cursor.lastrowid}")
            new_id = cursor.lastrowid

            return {
                "contact": {
                    "primaryContatctId": new_id,
                    "emails": [email] if email else [],
                    "phoneNumbers": [phoneNumber] if phoneNumber else [],
                    "secondaryContactIds": [],
                }
            }
    except Exception as e:
        logger.error(f"Error in inserting new contact: {e}")

    # DFS to gather all connected contacts
    try:
        all_contacts = []
        visited = set()

        def dfs(contact):
            """
            Performs a depth-first search starting from the given contact to gather all connected contacts.

            :param contact: The contact to start the DFS from.
            :return: None
            """
            if contact["id"] in visited:
                return
            visited.add(contact["id"])
            all_contacts.append(contact)

            if contact["linkedId"]:
                cursor.execute(
                    "SELECT * FROM Contact WHERE id = %s", (contact["linkedId"],)
                )
                parent = cursor.fetchone()
                if parent:
                    dfs(parent)
            else:
                cursor.execute(
                    "SELECT * FROM Contact WHERE linkedId = %s", (contact["id"],)
                )
                secondaries = cursor.fetchall()
                for sec in secondaries:
                    dfs(sec)

        for contact in matching_contacts:
            dfs(contact)
    except Exception as e:
        logger.error(f"Error in gathering all contacts: {e}")

    # Find the true primary (oldest contact)
    try:
        primary_contact = min(all_contacts, key=lambda c: c["createdAt"])

        # 5. Convert any newer primaries to secondary if needed
        for contact in all_contacts:
            if (
                contact["id"] != primary_contact["id"]
                and contact["linkPrecedence"] == "primary"
            ):
                cursor.execute(
                    """
                    UPDATE Contact
                    SET linkPrecedence = 'secondary', linkedId = %s
                    WHERE id = %s
                """,
                    (primary_contact["id"], contact["id"]),
                )
                conn.commit()
    except Exception as e:
        logger.error(f"Error in converting primaries to secondaries: {e}")

    # If incoming email/phone not in any record, insert new secondary
    try:
        emails_in_db = {c["email"] for c in all_contacts if c["email"]}
        phones_in_db = {c["phoneNumber"] for c in all_contacts if c["phoneNumber"]}
        new_email = email and email not in emails_in_db
        new_phone = phoneNumber and phoneNumber not in phones_in_db

        if new_email or new_phone:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute(
                """
                INSERT INTO Contact (email, phoneNumber, linkedId, linkPrecedence, createdAt, updatedAt)
                VALUES (%s, %s, %s, 'secondary', %s, %s)
            """,
                (email, phoneNumber, primary_contact["id"], now, now),
            )
            logger.info(f"Insert successful. ID: {cursor.lastrowid}")
            new_contact = {
                "id": cursor.lastrowid,
                "email": email,
                "phoneNumber": phoneNumber,
            }
            all_contacts.append(new_contact)
    except Exception as e:
        logger.error(f"Error in inserting new secondary contact: {e}")

    # Prepare response
    try:
        unique_emails = sorted({c["email"] for c in all_contacts if c["email"]})
        unique_phones = sorted(
            {c["phoneNumber"] for c in all_contacts if c["phoneNumber"]}
        )
        secondary_ids = sorted(
            [c["id"] for c in all_contacts if c["id"] != primary_contact["id"]]
        )

        return {
            "contact": {
                "primaryContatctId": primary_contact["id"],
                "emails": [primary_contact["email"]]
                + [e for e in unique_emails if e != primary_contact["email"]],
                "phoneNumbers": [primary_contact["phoneNumber"]]
                + [p for p in unique_phones if p != primary_contact["phoneNumber"]],
                "secondaryContactIds": secondary_ids,
            }
        }
    except Exception as e:
        logger.error(f"Error in preparing response: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
