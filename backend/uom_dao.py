from sql_connection import get_sql_connection


def get_uoms(connection):
    cursor = connection.cursor()
    try:
        query = ("SELECT * FROM uom")
        cursor.execute(query)

        response = []
        for (uom_id, uom_name) in cursor:
            response.append({
                "uom_id": uom_id,
                "uom_name": uom_name
            })
        return response
    except Exception as err:
        print(f'The error while performing sql query for getting unit of measures: {err}')
    finally:
        cursor.close()


# making the code modular
if __name__ == "__main__":
    connection = get_sql_connection()
    if connection is not None:
        print(get_uoms(connection))