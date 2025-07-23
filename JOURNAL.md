---
title: "Graphical calculator"
author: "Layan Jethwa"
description: "A custom-built graphical calculator with implementation from scratch"
created_at: "2025-06-09"
---
# June 9th: Began to create a list of goals for the project

I created a list of 10 objectives, and began to create subcategories under them after a bit of research into parsing methods.

![Objectives](https://github.com/LayanJethwa/graphical-calculator/blob/main/images/09-06.png)

**Total time spent: 1h**

# June 16th: Completed breakdown of objectives

I completed all the subcategories for the breakdown of my different objectives, and did research into the algorithms and maths needed, and the hardware components needed. I have uploaded my complete objectives breakdown and current list of links to this repository.

![Completed objectives](https://github.com/LayanJethwa/graphical-calculator/blob/main/images/16-06.png)

**Total time spent: 3h**

# June 23rd: Started modelling algorithms needed, and created a form for requirements gathering

I created a list of algorithms to explain, and started to create a plan for them. I also created a Microsoft Form asking people about their experiences with calculators, in order to get ideas and see what people wanted.

![Modelling algorithms](https://github.com/LayanJethwa/graphical-calculator/blob/main/images/23-06-1.png)
![Microsoft Form](https://github.com/LayanJethwa/graphical-calculator/blob/main/images/23-06-2.png)

**Total time spent: 2h**

# June 30th: Started modelling the algorithms used in the project

I did some research into the shunting yard algorithm, and created an explanation of the modelling with diagrams. I also started work on an explanation of my plotter function.

![Modelling](https://github.com/LayanJethwa/graphical-calculator/blob/main/images/30-06.png)

**Total time spent: 2h**

# July 2nd: Completed the modelling section for the project write-up

I completed my research into the algorithms needed for my project, and wrote them up into the modelling section, so I will be ready to write the code.

![Modelling 1](https://github.com/LayanJethwa/graphical-calculator/blob/main/images/02-07-1.png)
![Modelling 2](https://github.com/LayanJethwa/graphical-calculator/blob/main/images/02-07-2.png)

**Total time spent: 4h**

# July 3rd: Started doing some research into current systems

I began researching current systems, namely the Casio fx-9750GII and the Casio fx-CG50, and examined the pros and cons of their design.

![Casio 1](https://github.com/LayanJethwa/graphical-calculator/blob/main/images/03-07-1.png)
![Casio 2](https://github.com/LayanJethwa/graphical-calculator/blob/main/images/03-07-2.png)

**Total time spent: 2h**

# July 21st: Completed full analysis of the project

I completed the entire analysis, which comes to 49 pages and 7970 words. This includes the introduction, features list, end user identification, requirements gathering, research into current systems, modelling, SMART objectives list, hardware, and full bibliography.

![Hardware](https://github.com/LayanJethwa/graphical-calculator/blob/main/images/21-07-1.png)
![Desmos](https://github.com/LayanJethwa/graphical-calculator/blob/main/images/21-07-2.png)

**Total time spent: 6h**

# July 22nd: Wrote parser, evaluator and basic Pygame display for arbitrary polynomials

I created a parser that pre-processes an equation entered in infix notation and then converts it to postfix. I then created an evaluator that evaluates the expression at a number of evenly spaced points. I then made a basic Pygame display that plots and interpolates the points to create a graph. Below is an image of a graph plotted with Desmos, then the user input for the graph, and finally the output of my code for the graph.

![Desmos graph](https://github.com/LayanJethwa/graphical-calculator/blob/main/images/22-07-1.png)
![My input](https://github.com/LayanJethwa/graphical-calculator/blob/main/images/22-07-2.png)
![Pygame output](https://github.com/LayanJethwa/graphical-calculator/blob/main/images/22-07-3.png)

**Total time spent: 3h**

# July 23rd: Added an input display screen, fleshed out the graph display screen, and brought it all together

I created a screen where inputs of graphs can be entered, up to 7, with different colours, and a placeholder view window at the top. You can navigate between the graphs with arrow keys and enter, and you can go to the graph screen which plots all the graphs with enter. I brought both screens together with the main function, keeping all the modules nicely integrated with each other.