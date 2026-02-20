#print(dir(dictionary_name))
#print(help(dictinary_name))

#1.empty list called songs and an empty dictionary called genre_count.

songs= []
genre_count={}

print("Hello! Welcome to Music Library Manager\nPlease enter your songs")


for i in range(5):
    song= input("Song name: ")
    genre= input("Genre: ")
    song_t= (song, genre)
    songs.append(song_t)
    
    if genre in genre_count:
        genre_count[genre] += 1
    else:
        genre_count[genre] = 1


print("\n---> YOUR MUSIC LIBRARY <---")

for i in range(5):
    print(f"{i+1}. {songs[i][0]} ({songs[i][1]})")

print("\n---> GENRE STATISTICS <---")

for genre_name, count in genre_count.items():
    print(f"{genre_name}: {count} songs.")

most_popular = max(genre_count, key=genre_count.get)
print("\nMost popular genre: " + most_popular + ".")

