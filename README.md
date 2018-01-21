# Project Proposal: Pirate Island Game

**Group Members:** S1790173, S1783947 ......

**Project Summary:** The goal of this project is to create an online puzzle game using spatial objects stored in a database that will keep the user engaged.

**Technical Reasoning:** This project will contain a number of spatial operations and data structures, allowing us to improve our knowledge of Oracle Spatial, while creating something fun and interactive.

## 1 Game Description

### 1.1 Primary Concept
*Pirate Island* is a puzzle game that challenges a user to navigate a pirate ship through treacherous waters during a lightening storm. Each level consists of a piece of sea with obstacles such as rocks, crocodiles and whirlpools that will complicate the navigation. The user gets to see the obstacles only for a short time while lightening strikes (e.g. for two seconds) and then has to enter moves (left 5, up 6, right 4 etc.) to get to the treasure island without hitting an obstacle. They submit their moves and the game engine returns the result visually, highlighting if they hit an obstacle. This obstacle then remains visible and the user gets another go. Every unsuccessful attempt to navigate the water results in less treasure points awarded for the level. The aim is to complete as many levels as possible with the highest overall score.


### 1.2 Optional Functionalities
* An overall scoreboard is kept and displayed
* Obstacles have more complex characteristics (e.g. hitting a rock doesn't bring the pirate ship to sink completely but throws a man overboard which results in a loss of points)
* Bonuses are awarded if the user collects the floating booty on the route


## 2 Project Plan


### 2.1 Architecture Overview
An Oracle database structure stores multiple spatial objects that define a level. These objects are polygons, lines or circles and image objects. Different levels reference different objects. A python script loads and displays the objects into an SVG grid for the user display. Screen changes and animations are handled within JavaScript. After the user submits moves the requested path is passed back to the database via python. A stored procedure determines whether the user path successfully navigates the ship to the other side of the grid. If not, the object that was struck is returned over the python script back to the user display resulting in an animation and the cycle will repeat. New levels will be added to the database using a stored procedure that validates the inputs and calculates game parameters using spatial and regular operations.

### 2.2 Technologies
* Oracle Spatial - spatial data plus stored procs and views
* SVG - game display
* Python - db interaction and SVG rendering
* Jinja2 - html templates
* HTML5/CSS/Bootstrap - website styling and adaptive for devices
* JavaScript - client side controls and animations

### 2.3 Team Organisation
A framework, object model and data model will be defined upfront, splitting the work into components. Each team member will be responsible for a different component, such as the database structure, stored procedure for the user navigation, python script, data display and animation. Github will be used to share code between team members and place it under version control (see <https://github.com/maewart/pirateisland/>).

**Responsibilities:**

* Martin: Overall architecture and component interfaces
* Marco and Callum: Database structure and python script
* Livia: Web display and animation effects
* All: Level design, testing

### 2.4 Time plan

An iterative software development model will be applied. In a first cycle the minimal requirements for the game will be implemented and tested. Further cycles will add more functionalities and complexity to the game.

**We create a Gantt chart with the following tasks:**

* Clarification of architecture, responsibilities of components and their interactions (first week?)
* Data Model (first week – third week)
* First cycle with minimal requirements (until second/third week?)
* User Interface Design testing (third week?)
* Level design (first week – due)
* ..
* ..

### 2.5 References

# Notes for squadra!!!
* maybe describe technical aspects in more detail (e.g. that we're using templates...) ??
* I'm a pirate! - Arrrrrrr!
