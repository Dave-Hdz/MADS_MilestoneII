
import requests
import json
import pandas as pd
import time 

apikey= '&apikey=5d27f59037445ed4eacdf5bc01d0d757'
root_url = 'https://api.musixmatch.com/ws/1.1/'
format_url = "?format=json&callback=callback&"

#OBJECTS
# track_id = #Musixmatch track id
# artist_id = #Musixmatch artist id
# album_id = #Musixmatch album id
# commontrack_id = #Musixmatch commontrack id
# track_mbid = #musicbrainz recording or track id
# artist_mbid = #musicbrainz artist id
# album_mbid = #musicbrainz release id

#QUERYING
api_method = 'matcher.lyrics.get'
q_tracksearch = '&q_track={track}' # for a text string among song titles
q_artistsearch = 'q_artist={artist}'#for a text string among artist names


#genres = ['blues', 'classical', 'country', 'electronic', 'heavy-metal', 'hip-hop', 'indie', 'k-pop', 'pop',
#               'punk', 'reggae', 'reggaeton', 'rock', 'r-n-b', 'salsa']

genres = ['rock', 'r-n-b', 'salsa']


#df = pd.read_csv("data/1000_songs.csv")
#print(df.head())

lyrics_dataset = {}
artist_list = []
track_list = []
lyrics_list = []
genre_list = []
for genre in genres:
    if genre == 'classical':
        continue
    file_path = 'data/{genre}.csv'.format(genre=genre)
    df = pd.read_csv(file_path)
    #df = df.head(2)
 
    for index,row in df.iterrows():
        artist = row['artist']
        track = row['song_name']
        print('{genre} - fetching lyrics for artist : {artist}, song_name: {track}'.format(genre=genre,artist=artist, track=track))

        url_string = root_url + api_method + format_url + q_artistsearch.format(artist=artist) + q_tracksearch.format(track=track)+apikey
        request = requests.get(url_string)
        data = request.json()
        #data = json.dumps(data, sort_keys=True, indent=2)
        try:
            lyrics_sample = data['message']['body']['lyrics']['lyrics_body']
        except:
            lyrics_sample = "lyrics not found"

        #df.loc[df['artsit'] == artist, 'rating'] = 0
        df.at[index,'lyrics'] = lyrics_sample

        artist_list.append(artist)
        track_list.append(track)
        lyrics_list.append(lyrics_sample)
        genre_list.append(genre)
        df.to_csv('data/{genre}_lyrics.csv'.format(genre=genre))
        if index == 100:
            time.sleep(60)
            print("I am so sleepy. I just pulled like 100 songs. I am going to bed for a quick minute.")

#lyrics_dataset = {'artist' : artist_list, 'song_name' : track_list, 'lyrics' : lyrics_list, 'genre' : genre_list}
#lyrics_df = pd.DataFrame.from_dict(lyrics_dataset)
#lyrics_df.to_csv("lyrics_data.csv")




# q_lyricssearch = #for a text string among lyrics
# qsearch = #for a text string among song titles,artist names and lyrics

# #FILTERING
# f_has_lyricsFilter = # by objects with available lyrics
# f_is_instrumentalFilter = #instrumental songs
# f_has_subtitleFilter = #by objects with available subtitles
# f_music_genre_idFilter = #by objects with a specific music category
# f_subtitle_lengthFilter = #subtitles by a given duration in seconds
# f_subtitle_length_max_deviationApply = #a deviation to a given subtitle duration (in seconds)
# f_lyrics_languageFilter = #the tracks by lyrics language
# f_artist_idFilter = #by objects with a given Musixmatch artist_id
# f_artist_mbidFilter = #by objects with a given musicbrainz artist id

# #GROUPING
# g_commontrackGroup = #a track result set by commontrack_id
# #SORTING
# s_track_ratingSort = #the results by our popularity index for tracks, possible values are ASC | DESC
# s_track_release_dateSort = #the results by track release date, possible values are ASC | DESC
# s_artist_ratingSort = #the results by our popularity index for artists, possible values are ASC | DESC

# #RESULT SET PAGINATION
# pageRequest = #specific result page (default=1)
# page_sizeSpecify = #number of items per result page (default=10, range is 1 to 100)

# #OUTPUT FORMAT
# subtitle_formatDesired = #output format for the subtitle body. Possible values LRC|DFXP|STLEDU. Default to LRC.
# #LOCALIZATION
# countryThe = #country code of the desired country.


