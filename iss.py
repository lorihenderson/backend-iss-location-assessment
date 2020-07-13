#!/usr/bin/env python

__author__ = "Lori Henderson with some help from Joseph"

import requests
import time
import turtle
import tkinter as tk

iss_satelite = "iss.gif"
world_map = "map.gif"
api_url = "http://api.open-notify.org/"

def get_info():
    """Get a list of astronauts currently in space, include their names, and the name of the spacecraft they are on."""
    r = requests.get(api_url + "/astros.json")
    return r.json()["people"]


def number_of_astronauts_in_space():
    """Returns the number of astronauts in space."""
    r = requests.get(api_url + "/astros.json")
    return r.json()["number"]


def iss_location():
    """Retrieve the longitude and latitude (float tuple) of the ISS, along with a timestamp."""
    r = requests.get(api_url + "/iss-now.json")
    
    lat = float(r.json()["iss_position"]["latitude"])
    lon = float(r.json()["iss_position"]["longitude"])
    print('ISS Location lat = {} lon = {}'.format(lat,lon))


def iss_map(lat, lon):
    """Create a graphics screen with the world map background image.  Place ISS icon at lat, lon."""
    # methods to use: Screen(), setup(), bgpic(), setworldcoordinates()
    # create turtle.Turtle() to move the ISS to its current position
        # methods to use: shape(), setheading(), penup(), goto()
    screen = turtle.Screen()
    screen.setup(720, 360)
    screen.bgpic(world_map)
    screen.setworldcoordinates(-180, -90, 180, 90)

    screen.register_shape(iss_satelite)
    iss = turtle.Turtle()
    iss.shape(iss_satelite)
    iss.setheading(90)
    iss.penup()
    iss.goto(lon, lat)

    location = turtle.Turtle()
    location.penup()
    location.color("yellow")
    location.goto(-86.14996,39.76691)
    location.dot(5)
    next_time = passover(39.76691,-86.14996)
    location.write(next_time, align="center", font={"Arial", 14, "normal"})
    
    turtle.Screen().exitonclick()
    return screen


def passover(lat, lon):
    """Finds the next time that the ISS will be overhead of Indianapolis.  Plot a yellow dot on the map."""
    passover_coords = {"lat": lat, "lon": lon}
    r = requests.get(api_url + "iss-pass.json", params=passover_coords)

    passover_times = r.json()["response"][1]["risetime"]
    return time.ctime(passover_times)


def main():
    print(get_info())
    print("Number of Astronauts in Space:",number_of_astronauts_in_space())
    iss_location()
    iss_map(5.6475, 52.2727)
    print(passover(39.76691,-86.14996)) # Indianapolis

    


if __name__ == '__main__':
    main()