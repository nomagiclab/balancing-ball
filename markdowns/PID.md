# PID controller
## What's PID controller?
Let's start with an example - imagine that you have a robot arm only capable of lifting things up and moving them down. You can control the amount of force that the arm uses by changing the amount of electrical power going to its motor. The goal is to create some kind of formula that controls the amount of electricity so that the arm can lift given objects (which can have different weight) to preset height.
## Before we start...
let us name some variables, so that the problem becomes clearer. Process value (PV) is the current altitude of the robot arm - it will be measured with sensors. Set point (SP) will be value of preset height (point to which we want to lift/drop objects). Error (e) will be the difference between PV and SP (e = PV - SP), we can see that sign of error will tell us about the direction in which we want to move the object and the absolute value will give us information about the amount of error which we want to reduce. Our input to robot's motor will be called controlled variable (CV). We can restate our problem in a following way: create a formula which will change CV in order to minimize e.

## Proportional Controller
The simplest solution is to use proportional controller. It will set the amount of CV proportional to e. That way if we're further from SP we will give more power (and our arm will move with greater force) and if we're closer the arm will move with smaller force. For now our formula looks like this:

![equation](https://latex.codecogs.com/gif.latex?%5Cbg_white%20%5Clarge%20u%28t%29%20%3D%20K_pe%28t%29)

Where K_p is a constant we can set beforehand, u(t) is the current value of CV and e(t) is current value of error.

But the simplest solution does not work in that case - for example if the arm will have to lift a very heavy object it will not have enough power (the only thing that the arm knows is the distance between PV and SP and does not have the knowledge about the weight of the object).
## Integral Controller
We can try to modify our formula - it will have a part responsible for increasing the power if an error has the same (or very similar) value for a long peroid of time and we can use integrals to do this! Our modified formula will look like this:

![equation](https://latex.codecogs.com/gif.latex?%5Cbg_white%20%5Clarge%20u%28t%29%20%3D%20K_pe%28t%29%20&plus;%20K_i%5Cint_%7B0%7D%5Ete%28%5Ctau%29d%5Ctau)

Similarly K_p and K_i are constants. 

This solves our problem, but we can still see some problems. For example if we would hold our robot arm while it's trying to lift an object, the amount of force with which the arm tries to go upwards will increase and if we let it go the arm will rise very fast (lifting the object above SP) and then oscilate around SP for (possibly) a long time. We need to find something to slow it down in order to prevent those kind of situations...

## Derivative controller
Last piece to our puzzle will be a derivative controller. We know that derivatives measure the rate of change of a function, so if we have a function e(t) we can measure its rate of change and correct CV accordingly. After final change forumula will look like this:

![equation](https://latex.codecogs.com/gif.latex?%5Cbg_white%20%5Clarge%20u%28t%29%20%3D%20K_pe%28t%29%20&plus;%20K_i%5Cint_%7B0%7D%5Ete%28%5Ctau%29d%5Ctau%20&plus;%20K_d%5Cfrac%7Bde%28t%29%7D%7Bdt%7D)

Similarly K_p, K_i and K_d are (again) preset constants. 

## Are I and D components always necesarry? - Some problems that you should have in mind
# When does controller with only I component create problems?
- Mathemtatics here is used to model the real world - a world in which things have their limitations. 
- Consider a drone with PID controller used to control its altitude - if we hold it, the propeller will try to move faster and faster possibly destroying itself.
- If we let the drone go, the I component will have a very big value for a long time (despite the fact that the error function is decreasing) and will increase it's speed instead of slowing down.
# Solutions:
- Integral anti-windup - we choose a bound on integral and do not let it exceed that bound (similarly we can choose a bound on CV)
- Clamping - if we see that the sign of CV is the same as the sign of error and CV is in saturation then turn off the Integral controller
# When does controller with only D component create problems?
- In physicall processes we have to take 'noise' into account and D component is sensitive to high frequency noise. (If we have a function f(t)	= A\sin(\omega_a t + \phi_a) then f'(t) = A\omega_a\sin(\omega_a t + \phi_a) - for high frequency functions - which is equivalent to |\omega_a| being big - we can see that f'(t) values are oscilating rapidly around 0 with values from range (-|A\omega_a|, |A\omega_a|).
# Solution:
- low-pass filter - a device/algorithm that filters out high frequency noise
# When is the D component unnecesarry?
- Assume that derivative is bounded (in a certain environment), then the D component can give values from a closed range.
- That means it can be replaced by setting proper values of K_i and K_p.
- We simplify PID to PI.
# And when is the I Component unnecesary?
- Integration is used mainly when we need big values of CV to decrease error, but in certain environments we have a bound on needed CV.
- Can be replaced by P controller with proper K_p.
# Conclusion
- In order to use a proper controller you need to understand the problem and choose the controller accordingly.

## Is this everything?
Well, we found a satisfying formula that gives us the amount of CV used to minimize e, but we still don't know:
- how to set K_p, K_i and K_d