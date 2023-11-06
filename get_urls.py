from bs4 import BeautifulSoup
from seleniumbase import Driver
from requests.models import PreparedRequest

search_base_url = "https://www.discogs.com/search"

hip_hop_artists = ["Kendrick Lamar", "J. Cole", "Drake", "Kanye West", "Chance the Rapper", "Childish Gambino", "Jay-Z", "Eminem", "Lil Wayne", "Travis Scott", "Nicki Minaj", "Future", "Post Malone", "Cardi B", "Migos", "Lil Uzi Vert", "Lil Yachty", "21 Savage", "Kodak Black", "Young Thug", "Gucci Mane", "Meek Mill", "A$AP Rocky", "A$AP Ferg", "A$AP Mob", "A$AP Twelvyy", "A$AP Nast", "A$AP Ant", "A$AP TyY", "A$AP Bari", "A$AP Lou", "A$AP Illz", "A$AP Snacks", "A$AP K", "A$AP Josh", "A$AP Dom", "A$AP J. Scott"]
edm_artists = ["Martin Garrix", "The Chainsmokers", "Marshmello", "Calvin Harris", "David Guetta", "Avicii", "Tiësto", "Zedd", "Steve Aoki", "Diplo", "Skrillex", "Kygo", "Afrojack", "Hardwell", "Axwell Λ Ingrosso", "DJ Snake", "Alan Walker", "Don Diablo", "R3hab", "KSHMR", "Alesso", "Armin van Buuren", "Galantis", "Dimitri Vegas & Like Mike", "Nicky Romero", "Sebastian Ingrosso", "Alok", "Swedish House Mafia", "Oliver Heldens", "W&W", "Above & Beyond", "Nervo", "Fedde Le Grand", "Vintage Culture", "Lost Frequencies", "Quintino", "Vicetone", "Carl Cox", "Eric Prydz", "Bassjackers", "Dillon Francis", "Headhunterz", "VINAI", "Blasterjaxx", "Yellow Claw", "Shapov", "Steve Angello", "Deadmau5", "Tchami", "Borgeous", "Quintino", "DVBBS", "Krewella", "Kura", "Tom Swoon", "Firebeatz", "Paul van Dyk", "Danny Avila", "Wolfpack", "Andrew Rayel", "Flume", "Aly & Fila", "Ummet Ozcan", "Ferry Corsten", "Axwell", "Daft Punk", "Showtek", "Bob Sinclar", "Major Lazer", "Blasterjaxx", "NERVO", "Above & Beyond", "Steve Angello", "Fedde Le Grand", "Alok", "Don Diablo", "Swedish House Mafia", "Dimitri Vegas & Like Mike", "Afrojack", "Steve Aoki", "R3hab", "KSHMR", "W&W", "Calvin Harris", "Axwell Λ Ingrosso", "Nicky Romero", "Oliver Heldens", "DVBBS", "Quintino", "Alesso", "Galantis", "DJ Snake", "Ummet Ozcan", "Zedd", "Deadmau5", "Above & Beyond", "Sebastian Ingrosso", "NERVO"]
country_artists = ["Luke Bryan", "Jason Aldean", "Kenny Chesney", "Florida Georgia Line", "Blake Shelton", "Keith Urban", "Eric Church", "Sam Hunt", "Thomas Rhett", "Chris Stapleton", "Dierks Bentley", "Carrie Underwood", "Tim McGraw", "Brad Paisley", "Miranda Lambert", "Luke Combs", "Brett Young", "Kane Brown", "Old Dominion", "Maren Morris", "Kelsea Ballerini", "Cole Swindell", "Jon Pardi", "Dustin Lynch", "Chris Young", "Dan + Shay", "Brett Eldredge", "Rascal Flatts", "Lady Antebellum", "Jason Aldean", "Kenny Chesney", "Luke Bryan", "Florida Georgia Line", "Blake Shelton", "Keith Urban", "Eric Church", "Sam Hunt", "Thomas Rhett", "Chris Stapleton", "Dierks Bentley", "Carrie Underwood", "Tim McGraw", "Brad Paisley", "Miranda Lambert", "Luke Combs", "Brett Young", "Kane Brown", "Old Dominion", "Maren Morris", "Kelsea Ballerini", "Cole Swindell", "Jon Pardi", "Dustin Lynch", "Chris Young", "Dan + Shay", "Brett Eldredge", "Rascal Flatts", "Lady Antebellum", "Jason Aldean", "Kenny Chesney", "Luke Bryan", "Florida Georgia Line", "Blake Shelton", "Keith Urban", "Eric Church", "Sam Hunt", "Thomas Rhett", "Chris Stapleton", "Dierks Bentley", "Carrie Underwood", "Tim McGraw", "Brad Paisley", "Miranda Lambert", "Luke Combs", "Brett Young", "Kane Brown", "Old Dominion", "Maren Morris", "Kelsea Ballerini", "Cole Swindell", "Jon Pardi", "Dustin Lynch", "Chris Young", "Dan + Shay", "Brett Eldredge", "Rascal Flatts", "Lady Antebellum", "Jason Aldean", "Kenny Chesney", "Luke Bryan", "Florida Georgia Line", "Blake Shelton", "Keith Urban", "Eric Church", "Sam Hunt", "Thomas Rhett", "Chris Stapleton"]

# setup browser
driver = Driver(uc=True)
driver.implicitly_wait(5)

def get_song_list(artist):
    parameters = {"q": artist, "type": "artist"}
    url_preparer = PreparedRequest()
    url_preparer.prepare_url(search_base_url, parameters)
    driver.get(url_preparer.url)
    page = driver.page_source

    # find artist page
    soup = BeautifulSoup(page, "html.parser")
    results = soup.find_all("ul", id="search_results")[0]
    results = results.find_all("li")
    print(results[0])
    # extract link from first result
    artist_page = results[0].find("a")["href"]
    print(artist_page)

print(get_song_list("Kendrick Lamar"))