import psycopg2
import json

class Database:
    def __init__(self):
        db   = 'music_clustering'
        host = 'localhost'
        port = '5432'
        user = 'postgres'
        
        # load password from json
        with open('db_pw.json') as json_file:
            pw = json.load(json_file)['password']

        conn_str = (r"dbname='"+db+"' host='"+host+"' port='"+port+"' user='"+user+"' password='"+pw+"'")
        # print(f"Connection string: {conn_str}")
        dbh = psycopg2.connect(conn_str)
        self.dbh = dbh

    def add_song(self, info):
        cur = self.dbh.cursor()

        # check if artist exists
        cur.execute(f"SELECT * from artists WHERE name='{info['artist']}'")
        records = cur.fetchall()
        if len(records) == 0:
            cur.execute(f"INSERT INTO artists (name, src_url) VALUES ('{info['artist']}', '{info['src_url']}')")
        cur.execute(f"INSERT INTO all_songs (main_genre, artist, orig_file, proc_file_0) VALUES ('{info['main_genre']}', '{info['artist']}', '{info['orig_file']}', '{info['proc_file_0']}')")
        self.dbh.commit()
        cur.close()

    def remove_song(self, songname):
        cur = self.dbh.cursor()
        cur.execute(f"DELETE FROM all_songs WHERE orig_file='{songname}'")
        self.dbh.commit()
        cur.close()

    def remove_artist(self, artist_name):
        cur = self.dbh.cursor()
        cur.execute(f"DELETE FROM artists WHERE name='{artist_name}'")
        self.dbh.commit()
        cur.close()

if __name__ == "__main__":
    db = Database()
    # db.add_song({"main_genre": "hip-hop", "artist": "Kendrick Lamar", "orig_file": "test", "proc_file_0": "test", "src_url": "test"})
    db.remove_song("test")
    db.remove_artist("Kendrick Lamar")