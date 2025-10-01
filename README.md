## Graphical calculator ##

This design is for a graphical calculator that I am making, which will be able to plot graphs on a screen provided in human-readable infix notation.

I decided to make this as a fun maths-based project for my Computer Science NEA.


## Introduction ##

Graphical calculators and software are widely used in advanced mathematics. They are an easy way to visualise and analyse graphs and are useful in a classroom setting as well as to verify solutions to problems. Free digital softwares such as Desmos and Geogebra are used extensively, but they work best on computers, and it is not desirable to have them on phones either in a lesson. Physical graphical calculators are therefore used, created by companies such as Casio and Texas Instruments.

However, these physical calculators are very expensive. The Casio fx-CG50, one of the leading devices in the field, costs £140 from the manufacturer. These calculators are very good, with a multitude of features, but a lot of these features are very rarely used, adding to the price point unnecessarily. Additionally, these calculators function as scientific calculators as well, but people that own them generally also own a scientific calculator anyway that they use mainly for calculations.

I aim to create a physical calculator that is only for plotting graphs. This will be less costly to build and produce, and I will be able to tailor it to the end user. The hardware will be specialised, having a screen with a higher resolution than the CG50, and I will 3D print parts specifically for ergonomics.


## Features ##

- Explicitly defined graphs
    - Polynomials
    - Radicals
    - Exponentials
    - Reciprocals
    - Logarithmic graphs
    - Trigonometric graphs (sin, cos, tan and reciprocals)
    - Parametric graphs
    - Differential equations
    - Indefinite integrals
    - Combinations of the above
    - x = f(y) graphs
- Implicitly defined graphs
    - Circles
    - Ellipses
    - Parabolas
    - Horizontal parabolas
    - Hyperbolas
    - Multiple graphs simultaneously
- Graph manipulation
    - Pan
    - Zoom
    - View window
        - Axis bounds
        - Axis scaling
    - Graph colouring
- Buttons
    - Golden button
    - Degrees-radians ~~rocker switch~~ toggle switch
    - Zoom ~~momentary toggle switch~~ tactile switches
- Other features
    - Auto power-off


## Demo ##

You can see a software demo at the website: https://layanjethwa.github.io/graphical-calculator/code/build/web/

Currently it is not complete and I have only implemented methods for a few functions. As they will be triggered by physical switches on the calculator, they are triggered by keys currently:

| Keyboard key |  Calculator function  |
|:-----|------:|
| SHIFT + =  | + (addition) |
| SHIFT + 9   |  ( (left bracket)  |
| SHIFT + 0   | ) (right bracket) |
| SHIFT + 8   | * (multiplication) |
| q   | squared |
| w   | cubed |
| x   | variable letter x |
| /   | divide |
| p   | pi |
| l   | log |
| s   | sin |
| c   | cos |
| t   | tan |
| r   | csc |
| y   | sec |
| u   | cot |

The syntax of the log function is [base]log([value]), e.g. 2log(x) means log base 2 of x. Implicit multiplication is not currently defined for all functions.


## Hardware ##

The PCB will be shaped like the calculator, and the switches for the buttons will be mounted to it directly. It will have connectors for the screen, CPU, and battery as well. 

The CPU I will be using is the Raspberry Pi Zero 2 W. It is 65mm x 30mm, so fairly small and will fit nicely in the calculator. It has 512 MB of RAM, and a clock speed of 1GHz, so it will not be able to handle more intensive computations. It has WiFi and Bluetooth connectivity, although I am not planning to use them, as well as a USB 2.0 port, a microSD card slot, a mini HDMI port, and a 40 pin I/O header. I will have to install an operating system on it, probably Raspbian, to run Python code.

The screen I have decided to use is a 3.5 inch LCD screen, intended for a display for a Raspberry Pi. It has a 320x480 pixel resolution, and also features resistive touch control, though I probably will not be utilizing that feature of it. The resolution is higher than the Casio fx-CG50, one of the leading graphical calculators, so it should be more than enough for my purposes. The screen is £24 directly from the manufacturer. The screen connects via ~~HDMI~~ TFT, and is powered by a micro USB connection.

I have decided to use tactile switches with attached shafts, which, as mentioned, will be soldered directly to the PCB. I plan on using the Omron B3F-1050 switches, which I can get from DigiKey, at around 12.5p each for the number I will require. They have dimensions of 6 x 6 mm with a height of 7.3 mm, which should be suitable for my purposes. I can buy keycaps for these switches, or 3D print them myself. I found many sites selling caps - there are some round ones on AliExpress for £2.79 per 100 caps, and also some square ones for £2.47 per 50 caps. I also found a model that I can 3D print, although this is for the larger 12x12x7.3 mm switches, but I can scale it down.


## Pictures ##

![Schematic](https://github.com/LayanJethwa/graphical-calculator/blob/main/images/schematic.png)
![3D model](https://github.com/LayanJethwa/graphical-calculator/blob/main/images/3d-model.png)
![PCB](https://github.com/LayanJethwa/graphical-calculator/blob/main/images/pcb.png)
![CAD case](https://github.com/LayanJethwa/graphical-calculator/blob/main/images/render.png)

## BOM ##

|Part name|Quantity needed|Lot|Price|Link|
|-|-|-|-|-|
|PCB|1|5|$16.77|https://cart.jlcpcb.com/shopcart/cart/	|
|Raspberry Pi Zero 2W|1|1|$16.25|https://www.aliexpress.com/item/1005008147614202.html|
|Osoyoo 3.5in TFT LCD screen|1|1|$33.32|https://www.aliexpress.com/i/1005006494047405.html	|
|LiPo flat battery 5V 9000mAh|1|1|$11.52|https://www.aliexpress.com/item/1005005621203243.html|
|Omron B3F-1050|40|100|$16.95|https://www.aliexpress.com/item/4000012348941.html|
|JS2011CQN|1|1|$16.77|https://www.mouser.co.uk/ProductDetail/611-JS102011CQN|
|DO-35 1N4148|40|100|$1.02|https://www.aliexpress.com/item/1005004103990376.html|