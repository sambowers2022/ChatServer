import hashlib

register_query = ("INSERT INTO login (username, password) VALUES (%s,%s)")

def login(db, opts):
    print(opts)
    cursor = db.cursor(buffered=True)
    try:
        cursor.execute("SELECT password FROM login WHERE username = %s", [opts[1]])
        if opts[2]==cursor.fetchone()[0]:
            return 200
        return 403
    except Exception as e:
        print(e)
        if opts[0]=="l":
            return 403
        cursor.execute(register_query, [opts[1], opts[2]])
        db.commit()
        return 201

