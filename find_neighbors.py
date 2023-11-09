from sklearn.neighbors import NearestNeighbors
import database
import preprocess
import numpy as np
import os

def find_neighbors(test_song):
    db = database.Database()

    # check if features and song_names file exists
    if not os.path.exists("features.npy") or not os.path.exists("song_names.npy"):
        # get all songs from database
        cur = db.dbh.cursor()
        cur.execute("SELECT * FROM all_songs")
        records = cur.fetchall()
        cur.close()

        # get all features
        features = []
        for record in records:
            features.append(np.load(record[4]+".npy").flatten())
        features = np.array(features)

        # normalize features
        features = features / np.linalg.norm(features, axis=1)[:,None]

        # save features
        np.save("features", features)

        # get all song names
        song_names = []
        for record in records:
            song_names.append(record[5])
        
        # save song names
        np.save("song_names", song_names)
    else:
        features = np.load("features.npy")
        song_names = np.load("song_names.npy")

    # fit nearest neighbors model
    nbrs = NearestNeighbors(n_neighbors=10, algorithm='ball_tree').fit(features)

    # get neighbor for test song
    test_features = preprocess.preprocess_in_mem("", test_song).flatten()
    distances, indices = nbrs.kneighbors([test_features])

    # print results
    # print(f"Neighbors for {test_song}:")
    # for i in range(len(indices[0])):
    #     print(f"{song_names[indices[0][i]]} - {db.get_artist_by_song_name(song_names[indices[0][i]])}")

    # create a list of results
    results = []
    for i in range(len(indices[0])):
        results.append((song_names[indices[0][i]], db.get_artist_by_song_name(song_names[indices[0][i]])))
    return results

if __name__ == "__main__":
    results = find_neighbors("new4Demov5.mp3")

    print("Nearest neighbors for new4Demov5.mp3:")
    for result in results:
        print(result)