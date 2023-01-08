#!/usr/bin/python3

import requests, json, time

volumio_url='http://volumio.local/api/v1/browse?uri=music-library/USB/79edfdb0-7b02-442d-98d6-c268b0682618'
volumio_base='http://volumio.local/api/v1/browse'


def get(url):
    response = requests.get(url, timeout=(6.0, 15.0))
    return(response)

def post(url, data):
    response = requests.post(url, data=data)
    return(response)


def get_song_list(artist):
    response = get(volumio_url)
    jsonData = response.json()

    for jsonObj  in jsonData["navigation"]["lists"][0]["items"]:
        if (jsonObj["title"] == artist):
            print(jsonObj)
            uri_artist = jsonObj["uri"]
            break

    response = get(volumio_base + '?uri=' + uri_artist)
    jsonData = response.json()
            
    for jsonObj  in jsonData["navigation"]["lists"][0]["items"]:
        print(jsonObj["title"])


def get_artist():
    response = get(volumio_url)
    jsonData = response.json()
    
    for jsonObj  in jsonData["navigation"]["lists"][0]["items"]:
        print(jsonObj["title"])
        
def write_header(fp):
    fp.write("<!DOCTYPE html>\n")
    fp.write("<html lang=\"ja\">\n")
    fp.write("<meta charset=\"utf-8\">\n")
    fp.write("<head>\n")
    fp.write("<title>album list</title>\n")
    fp.write("</head>\n")
    fp.write("<html>")

def write_footer(fp):
    fp.write("</html>")

def all_albums_html(filename):
    response = get(volumio_url)
    jsonData = response.json()

    fp = open(filename,'w')
    write_header(fp)
    
    artists = []
    i=0
    for jsonObj  in jsonData["navigation"]["lists"][0]["items"]:
        artists.append([jsonObj["title"],jsonObj["uri"]])
        #print(jsonObj["title"])
        
    
    for [artist_name,artist_uri] in artists:
        response2 = get(volumio_base + '?uri=' + artist_uri )
        jsonData2 = response2.json()
        time.sleep(10)

        print(artist_name)
        fp.write("<h3>" + artist_name + "</h3>\n")
        for jsonObj2  in jsonData2["navigation"]["lists"][0]["items"]:
            print("        " + jsonObj2["title"])
            fp.write(jsonObj2["title"]+'<br>\n')
        i=i+1
        print("artists # ",i)
        #if (i==4):
        #    break

    write_footer(fp)
    fp.close()


if __name__ == '__main__':
#    get_song_list('Mr.Children')
#    get_artist()
    all_albums_html('albums.html')




