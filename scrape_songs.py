import wikipedia
from bs4 import BeautifulSoup
import requests
import yt_dlp
import database
from preprocess import preprocess

hip_hop_artists = ["Kendrick Lamar", "J. Cole", "Drake", "Kanye West", "Chance the Rapper", "Childish Gambino", "Jay-Z", "Eminem", "Lil Wayne", "Travis Scott", "Nicki Minaj", "Future", "Post Malone", "Cardi B", "Migos", "Lil Uzi Vert", "Lil Yachty", "21 Savage", "Kodak Black", "Young Thug", "Gucci Mane", "Meek Mill", "A$AP Rocky", "A$AP Ferg", "Lil Baby", "DaBaby", "Lil Durk", "Pooh Shiesty", "Moneybagg Yo", "42 Dugg", "Key Glock", "YoungBoy Never Broke Again", "Young Dolph", "YNW Melly", "Polo G", "Kodak Black", "9lokkNine"]
edm_artists = ["Martin Garrix", "The Chainsmokers", "Marshmello", "Calvin Harris", "David Guetta", "Avicii", "Tiësto", "Zedd", "Steve Aoki", "Diplo", "Skrillex", "Kygo", "Afrojack", "Hardwell", "Axwell Λ Ingrosso", "DJ Snake", "Alan Walker", "Don Diablo", "R3hab", "KSHMR", "Alesso", "Armin van Buuren", "Galantis", "Dimitri Vegas & Like Mike", "Nicky Romero", "Sebastian Ingrosso", "Alok", "Swedish House Mafia", "Oliver Heldens", "W&W", "Above & Beyond", "Nervo", "Fedde Le Grand", "Vintage Culture", "Lost Frequencies", "Quintino", "Vicetone", "Carl Cox", "Eric Prydz", "Bassjackers", "Dillon Francis", "Headhunterz", "VINAI", "Blasterjaxx", "Yellow Claw", "Shapov", "Steve Angello", "Deadmau5", "Tchami", "Borgeous", "Quintino", "DVBBS", "Krewella", "Kura", "Tom Swoon", "Firebeatz", "Paul van Dyk", "Danny Avila", "Wolfpack", "Andrew Rayel", "Flume", "Aly & Fila", "Ummet Ozcan", "Ferry Corsten", "Axwell", "Daft Punk", "Showtek", "Bob Sinclar", "Major Lazer", "Blasterjaxx", "NERVO", "Above & Beyond", "Steve Angello", "Fedde Le Grand", "Alok", "Don Diablo", "Swedish House Mafia", "Dimitri Vegas & Like Mike", "Afrojack", "Steve Aoki", "R3hab", "KSHMR", "W&W", "Calvin Harris", "Axwell Λ Ingrosso", "Nicky Romero", "Oliver Heldens", "DVBBS", "Quintino", "Alesso", "Galantis", "DJ Snake", "Ummet Ozcan", "Zedd", "Deadmau5", "Above & Beyond", "Sebastian Ingrosso", "NERVO"]
country_artists = ["Luke Bryan", "Jason Aldean", "Kenny Chesney", "Florida Georgia Line", "Blake Shelton", "Keith Urban", "Eric Church", "Sam Hunt", "Thomas Rhett", "Chris Stapleton", "Dierks Bentley", "Carrie Underwood", "Tim McGraw", "Brad Paisley", "Miranda Lambert", "Luke Combs", "Brett Young", "Kane Brown", "Old Dominion", "Maren Morris", "Kelsea Ballerini", "Cole Swindell", "Jon Pardi", "Dustin Lynch", "Chris Young", "Dan + Shay", "Brett Eldredge", "Rascal Flatts", "Lady Antebellum", "Jason Aldean", "Kenny Chesney", "Luke Bryan", "Florida Georgia Line", "Blake Shelton", "Keith Urban", "Eric Church", "Sam Hunt", "Thomas Rhett", "Chris Stapleton", "Dierks Bentley", "Carrie Underwood", "Tim McGraw", "Brad Paisley", "Miranda Lambert", "Luke Combs", "Brett Young", "Kane Brown", "Old Dominion", "Maren Morris", "Kelsea Ballerini", "Cole Swindell", "Jon Pardi", "Dustin Lynch", "Chris Young", "Dan + Shay", "Brett Eldredge", "Rascal Flatts", "Lady Antebellum", "Jason Aldean", "Kenny Chesney", "Luke Bryan", "Florida Georgia Line", "Blake Shelton", "Keith Urban", "Eric Church", "Sam Hunt", "Thomas Rhett", "Chris Stapleton", "Dierks Bentley", "Carrie Underwood", "Tim McGraw", "Brad Paisley", "Miranda Lambert", "Luke Combs", "Brett Young", "Kane Brown", "Old Dominion", "Maren Morris", "Kelsea Ballerini", "Cole Swindell", "Jon Pardi", "Dustin Lynch", "Chris Young", "Dan + Shay", "Brett Eldredge", "Rascal Flatts", "Lady Antebellum", "Jason Aldean", "Kenny Chesney", "Luke Bryan", "Florida Georgia Line", "Blake Shelton", "Keith Urban", "Eric Church", "Sam Hunt", "Thomas Rhett", "Chris Stapleton"]

def get_album_list(artist):
    try:
        artist_page_url = wikipedia.page(artist + " discography").url
        html = requests.get(artist_page_url)
        soup = BeautifulSoup(html.text, 'html.parser')
        album_tables = soup.find_all('table', class_='wikitable plainrowheaders')
        album_list = []
        table = album_tables[0]
        for row in table.find_all('tr')[2:]:
            if row.find_all('th'):
                album_list.append(row.find_all('th')[0].find('a').get('href'))
        return album_list
    except Exception as e:
        print(e)
        return []

def get_songs_from_album(album_link):
    try:
        html = requests.get("https://en.wikipedia.org" + album_link)
        soup = BeautifulSoup(html.text, 'html.parser')
        song_list = []
        table = soup.find_all('table', class_='tracklist')[0]
        for row in table.find_all('tr')[1:-1]:
            if row:
                song_list.append(row.find_all('td')[0].text)
        return song_list
    except Exception as e:
        print(e)
        return []

def download_song(arg, genre, artist):
    file_base = "G:/music_clustering/downloaded_files/"
    save_dir = file_base + f"{genre}/"

    download_options = {'format' : 'bestaudio', 'noplaylist':'True',  'quiet' : 'True',
                        'outtmpl': save_dir+arg+'.%(ext)s', 'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }]}
    
    with yt_dlp.YoutubeDL(download_options) as ydl:
        try:
            requests.get(arg+' '+artist)
        except:
            video = ydl.extract_info(f"ytsearch:{arg+' '+artist}")['entries'][0]
        else:
            video = ydl.extract_info(arg+' '+artist)

    return save_dir, arg+".mp3"

def sanitize_songname(song):
    song.strip()
    song = song.replace('\n', ' ')
    song = song.replace('"', '')
    song = song.replace('/', '')
    song = song.replace('\\', '')
    song = song.replace(':', '')
    song = song.replace('*', '')
    song = song.replace('?', '')
    song = song.replace('<', '')
    song = song.replace("'", "")
    return song

def temp_scrape_song(yt_url, sess_prefix):
    download_options = {'format' : 'bestaudio', 'noplaylist':'True',  'quiet' : 'True',
                        'outtmpl': sess_prefix+'temp.%(ext)s', 'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }]}
    
    with yt_dlp.YoutubeDL(download_options) as ydl:
        try:
            requests.get(yt_url)
        except:
            video = ydl.extract_info(yt_url)['entries'][0]
        else:
            video = ydl.extract_info(yt_url)

    return sess_prefix+"temp.mp3"
    
def get_all_artist_songs(artist, genre, db):
    print(f"Getting albums for {artist}")
    album_list = get_album_list(artist)
    print(f"Found {len(album_list)} albums for {artist}\n")

    print(f"Getting songs for {artist}")
    song_list = []
    for album in album_list:
        song_list.extend(get_songs_from_album(album))
    print(f"Found {len(song_list)} songs for {artist}\n")

    print(f"Dowloading songs for {artist}")
    for song in song_list:
        song = sanitize_songname(song)
        if db.check_song(song):
            print(f"Song {song} already in database")
        else:
            print(f"Downloading {song}")
            try:
                save_dir, filename = download_song(song, genre, artist)
                preprocessed_filename = preprocess(save_dir, filename)
                db.add_song({"main_genre": genre, "artist": artist, "orig_file": save_dir + filename, "proc_file_0": preprocessed_filename, "src_url": wikipedia.page(artist + " discography").url, "song_name": song})
                print(f"Added {song} to database\n")
            except Exception as e:
                print(e)
                print(f"Failed to download {song}\n")
                with open("download_log.txt", "a") as f:
                    f.write(f"Failed to download {song} for {artist}\n")
    print(f"Finished downloading songs for {artist}\n\n\n")

    

if __name__ == "__main__":
    db = database.Database()
    for artist in hip_hop_artists[6:]:
        get_all_artist_songs(artist, "hip_hop", db)
    for artist in edm_artists:
        get_all_artist_songs(artist, "edm", db)
    for artist in country_artists:
        get_all_artist_songs(artist, "country", db)
