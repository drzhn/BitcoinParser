import psycopg2


class PgHash:
    index = 0  # POINTER TO THE NEXT HASH

    def __init__(self):
        self.conn = psycopg2.connect(database="bitcoindb", user="klever", password="")
        self.cur = self.conn.cursor()
        self.conn.autocommit = True
    def refresh_db(self):
        try:
            self.cur.execute("DROP TABLE IF EXISTS idbyhash;")
            self.cur.execute("DROP TABLE IF EXISTS idprevious;")
            self.cur.execute("CREATE TABLE idbyhash(id integer, hash char(64), PRIMARY KEY(id,hash));")
            self.cur.execute("CREATE TABLE idprevious(id integer, id_prev integer, PRIMARY KEY(id,id_prev));")
            self.conn.commit()
        except:
            print "some error"

    def insert_hash(self, hash):
        try:
            self.cur.execute("INSERT INTO idbyhash values (" + str(self.index) + ", \'" + hash + "\');")
            self.conn.commit()
            self.index += 1
        except:
            print "some error"

    def insert_previous(self, hash_current, hash_prev_list):
        try:
            id_current = self.get_id_by_hash(hash_current)[0]
        except IndexError:
            self.insert_hash(hash_current)
            id_current = self.index - 1

        for hash in hash_prev_list:
            try:
                id = self.get_id_by_hash(hash)[0]
            except IndexError:
                self.insert_hash(hash)
                id = self.index - 1
            try:
                self.cur.execute("INSERT INTO idprevious values (" + str(id_current) + ", " + str(id) + ");")
                self.conn.commit()
            except psycopg2.IntegrityError: # if keys are already exists
                pass

    def get_hash_by_id(self, id):
        self.cur.execute("SELECT hash FROM idbyhash WHERE id=" + str(id) + ";")
        self.conn.commit()
        rows = self.cur.fetchall()
        if len(rows) == 0:
            return rows
        else:
            return [rows[0][0]]

    def get_id_by_hash(self, hash):
        # print hash
        self.cur.execute("SELECT id FROM idbyhash WHERE hash=\'" + hash + "\';")
        self.conn.commit()
        rows = self.cur.fetchall()
        if len(rows) == 0:
            return rows
        else:
            return [rows[0][0]]

#
# pghash = PgHash()
# pghash.refresh_db()
# pghash.insert_hash("a")
# pghash.insert_hash("b")
# pghash.insert_hash("c")
# pghash.insert_previous("d", 'c')
