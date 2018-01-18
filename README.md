# Pirate Island
A Pirate Puzzle Game using spatial objects to create a challening puzzle that will keep the user engaged.

## Primary Concept
A puzzle game that challenges a user to navigate a pirates ship through treaturous waters during a lightening storm. There will be obstacles such as islands, crocodiles, whirlpools. The user will get 2 seconds to see the obstacles while lightening strikes and then have to enter their moves (left 5, up 6, right 4 etc) to get to the treasure island without hitting an obstacle. They will submit their moves and the game engine will return their result, highlighting if they hit an obstacle. This obstacle will then remain visibile and the user will get another go.

## Optional Extras
Every unsuccessful attempt to navigate will results in less treasure points awarded for the level. Bonuses will be awarded if you collect the floating booty on the route. The aim is to complete all levels with the highest overall score. An overall scoreboard will be displayed.

## How
A database structure that stores multiple spatial objects that define a level. These objects will be polygons, lines or circles and image objects. Different levels will reference different objects. A python script will load and display the objects into an SVG grid for the user display. All user interaction will then be in javascript handling the screen changes and submitting the requested moves back to the database via python. There will then be a stored procedure that determines whether the user path successfully gets to the other side of the grid. If not, it will return the object that was struck. The python script will return this back to the user display and the cycle will repeat.

Github will be used for code. A framework, object model and data model will be defined upfront, splitting the work in to components. Each team member will take a different component, such as the database structure, navigation stored procedure, python script, html/styling and javascript.

## Technical Reasoning
This project will contain a number of spatial operations and data structures, allowing us to improve our knowledge of Oracle Spatial, while creating something fun and interactive.

## Team Structure
* Overall Architecture: Martin
* Html/Javascript: Livia
* Python & Database: Marco & Callum
* Level Design: All


