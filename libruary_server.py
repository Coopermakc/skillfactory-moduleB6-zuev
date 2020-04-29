#!/usr/bin/env python3
# -*- coding: utf-8 -*-

 #импортируем модуль  album
import album as al

from bottle import run, route, request, HTTPError




@route("/albums/<artist>")
def albums(artist):
    albums_list = al.find(artist)
    if not albums_list:
        message = "Альбомов {} не найдено".format(artist)
        result = HTTPError(404,message)
    else:
        album_names = [album.album for album in albums_list]
        counts = len(album_names)
        result = "Найдено {} альбомов исполнителя {}<br>".format(counts,artist)
        result += "<br>".join(album_names)
    return result

@route("/albums", method="POST")
def user():
    result = "Hello"
    user_data = {
        "year": request.forms.get("year"),
        "artist": request.forms.get("artist"),
        "genre": request.forms.get("genre"),
        "album": request.forms.get("album")
    }
    doubles = al.find_doubles(user_data["album"], user_data["artist"])
    check_year = al.check_year(user_data["year"])
    if check_year != True:
        return check_year
    if doubles:
        message = "Альбом {} исполнителя {} уже существует".format(user_data["album"], user_data["artist"])
        return HTTPError(409, message)
    al.save_album(user_data)
    return "Альбом добавлен"

def main():
    run(host="localhost", port=8080, debug=True)

if __name__ == "__main__":
    main()
