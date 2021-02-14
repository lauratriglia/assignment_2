# Research Track I - Final Assignment

In this repository you will find a package required for the construction of an interface whose the scope is to take commands from the user and execute them. 
The possible commands are:
1) Reach a random target
2) Choose a target among some possibilities which are (-4,-3);(-4,2);(-4,7);(5,-7);(5,-3);(5,1)
3) Follow the wall
4) Stop the robot

## Prerequisites
To execute successfully the code, there are required two other package. Clone the following repository in you workspace:
- https://github.com/CarmineD8/slam_gmapping
- https://github.com/CarmineD8/final_assignment

After the clonation of each package, do a catkin_make. 

## Nodes
### interface.py 

It takes the commands from the user and execute them

### random_service

It generate the random target required for the first command


## How the node communicate to each other

You can find in the doc directory, the ros_graph -> it shows how the node communicate to each othere

## How to run the code:
- As first step it is necessary to run a command to create the master 
```
roscore & 
```
- As second step run the simulation space with
```
roslaunch final_assignment simulation_gmapping.launch
```
- As third step in another shell use the command to run the launch move_base
```
roslaunch final_assignment move_base.launch
```
- As last step, in another shell, use the command to run the interface
```
roslaunch triglia_final_assignment assignment2.launch
```

