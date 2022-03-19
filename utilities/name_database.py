import sqlite3

# connect to database
conn = sqlite3.connect('name_database.db')

# create name table with columns first_name, last_name, full_name, birth_place, birth_date
conn.execute('''CREATE TABLE IF NOT EXISTS geo_names
                (first_name TEXT, last_name TEXT, full_name TEXT NOT NULL, birth_place TEXT NOT NULL, birth_date TEXT NOT NULL)''')

def add_record_to_database(first_name, last_name, full_name, birth_place, birth_date):
    # add record to database
    if any(a for a in [first_name, last_name, full_name]) and all([a for a in [birth_place, birth_date]]):
        conn.execute("INSERT INTO geo_names VALUES (?,?,?,?,?)", (first_name, last_name, full_name, birth_place, birth_date))
        conn.commit()
        return True
    else:
        print("Error: Missing required fields")


def get_records_from_database(search_term, column):
    # get records from database
    if search_term and column:
        try:
            records = conn.execute("SELECT * FROM geo_names WHERE (?) LIKE '%(?)%'", (column, search_term))
            return records
        except sqlite3.OperationalError:
            print("Error: No records found")
    else:
        print("Error: Missing required fields")

def delete_record_from_database(full_name):
    """Delete record using complete full name"""
    if full_name:
        try:
            conn.execute("DELETE FROM geo_names WHERE full_name = (?)", (full_name,))
            conn.commit()
            return True
        except sqlite3.OperationalError:
            print("Error: No records found")
    else:
        print("Error: Missing required fields")