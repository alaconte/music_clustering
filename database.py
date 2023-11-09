import psycopg2
import json
import os

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
        cur.execute(f"INSERT INTO all_songs (main_genre, artist, orig_file, proc_file_0, song_name) VALUES ('{info['main_genre']}', '{info['artist']}', '{info['orig_file']}', '{info['proc_file_0']}', '{info['song_name']}')")
        self.dbh.commit()
        cur.close()

    def check_song(self, songname):
        cur = self.dbh.cursor()

        cur.execute(f"SELECT * from all_songs WHERE song_name='{songname}'")
        records = cur.fetchall()
        cur.close()
        return len(records) > 0
    
    def get_artist_by_song_name(self, songname):
        cur = self.dbh.cursor()
        cur.execute(f"SELECT * from all_songs WHERE song_name='{songname}'")
        records = cur.fetchall()
        cur.close()
        return records[0][2]
    
    def get_file_by_song_name(self, songname):
        cur = self.dbh.cursor()
        cur.execute(f"SELECT * from all_songs WHERE song_name='{songname}'")
        records = cur.fetchall()
        cur.close()
        return records[0][3]

    def remove_song(self, songname):
        cur = self.dbh.cursor()
        cur.execute(f"SELECT * from all_songs WHERE song_name='{songname}'")
        records = cur.fetchall()
        for record in records:
            try:
                os.remove(record[3])
                os.remove(record[4]+".npy")
            except FileNotFoundError:
                print("File not found")
        cur.execute(f"DELETE FROM all_songs WHERE song_name='{songname}'")
        self.dbh.commit()
        cur.close()

    def remove_artist(self, artist_name):
        cur = self.dbh.cursor()
        cur.execute(f"DELETE FROM artists WHERE name='{artist_name}'")
        self.dbh.commit()
        cur.close()

if __name__ == "__main__":
    db = Database()
    db.remove_song("Common Ground")
    # remove all songs where the reference file doesn't exist
    # cur = db.dbh.cursor()
    # cur.execute("SELECT * FROM all_songs")
    # records = cur.fetchall()
    # cur.close()

    # for record in records:
    #     if not os.path.exists(record[3]):
    #         db.remove_song(record[5])