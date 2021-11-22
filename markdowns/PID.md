# PID controller
## What's PID controller?
Let's start with an example - imagine that you have a robot arm only capable of lifting things up and moving them down. You can control the amount of force that the arm uses by changing the amount of electrical power going to its motor. The goal is to create some kind of formula that controls the amount of electricity so that the arm can lift given objects (which can have different weight) to preset height.
## Before we start...
let us name some variables, so that the problem becomes clearer. Process value (PV) is the current altitude of the robot arm - it will be measured with sensors. Set point (SP) will be value of preset height (point to which we want to lift/drop objects). Error (e) will be the difference between PV and SP (e = PV - SP), we can see that sign of error will tell us about the direction in which we want to move the object and the absolute value will give us information about the amount of error which we want to reduce. Our input to robot's motor will be called controlled variable (CV). We can restate our problem in a following way: create a formula which will change CV in order to minimize e.

## Proportional Controller:
The simplest solution is to use proportional controller. It will set the amount of CV proportional to e. That way if we're further from SP we will give more power (and our arm will move with greater force) and if we're closer the arm will move with smaller force. For now our formula looks like this:

![equation](https://latex.codecogs.com/gif.latex?%5Cbg_white%20%5Clarge%20u%28t%29%20%3D%20K_pe%28t%29)

Where ![equation](https://latex.codecogs.com/gif.latex?%5Cinline%20%5Cbg_white%20%5Clarge%20K_p) can be set beforehand.

But the simplest solution does not work in that case - for example if the arm will have to lift a very heavy object it will not have enough power (the only thing that the arm knows is the distance between PV and SP and does not have the knowledge about the weight of the object).
## Integral Controller:
We can try to modify our formula - it will have a part responsible for increasing the power if an error has the same (or very similar) value for a long peroid of time. 
![equation](https://latex.codecogs.com/gif.latex?%5Cbg_white%20%5Clarge%20u%28t%29%20%3D%20K_pe%28t%29%20&plus;%20K_i%5Cint_%7B0%7D%5Ete%28%5Ctau%29d%5Ctau%20&plus;%20K_d%5Cfrac%7Bde%28t%29%7D%7Bdt%7D)