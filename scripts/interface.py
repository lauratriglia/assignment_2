#! /usr/bin/env python

import rospy
from std_srvs.srv import *
from geometry_msgs.msg import Twist, Point
from nav_msgs.msg import Odometry
from move_base_msgs.msg import MoveBaseActionGoal
from actionlib_msgs.msg import GoalID
from triglia_final_assignment.srv import *
import math
import time

actual_position = Point()

##To publish new goals
pub_goal = None

##Initiliaze the wall_follower client
sub_odom = None

pub_target_reached = None

def actual_position(odom_data):
	global actual_position
	actual_position = odom_data.pose.pose.position

##The scope of move_target is to use move_base service to reach the target itself
def move_randomly_to_target(target_x, target_y):
    global pub_goal
    
    ##Initialize a MoveBaseActionGoal target to move my robot
    target_goal = MoveBaseActionGoal()
    
    target_goal.goal.target_pose.header.frame_id = "map"
    target_goal.goal.target_pose.pose.orientation.w = 1

    target_goal.goal.target_pose.pose.position.x = target_x
    target_goal.goal.target_pose.pose.position.y = target_y

    pub_goal.publish(target_goal)
    return
   
def reaching_the_target(target_x,target_y):
    global sub_odom
    global actual_position
    global pub_target_reached
    ##define the distance between the robot and the distance
    distance = math.sqrt(pow(actual_position.x - target_x,2) + pow(actual_position.y - target_y,2))
    while distance > 1:
	print("I'm going to reach the target, the distance between us is:")
	print(distance)
	distance = math.sqrt(pow(actual_position.x - target_x,2) + pow(actual_position.y - target_y,2))
        rospy.sleep(1)

    target_reached = GoalID()
    pub_target_reached.publish(target_reached)
    print(target_reached)
    return 

def user_set_position():
	target_x=None
	target_y=None
	
	while not((target_x==-4 and target_y==-3)or
	          (target_x==-4 and target_y== 2)or
	          (target_x==-4 and target_y== 7)or
	          (target_x== 5 and target_y==-7)or
	          (target_x== 5 and target_y==-3)or
	          (target_x== 5 and target_y== 1)):
				print("Now you can choose the next target. You have a choice between these:")
				print("(-4,-3);(-4,2);(-4,7);(5,-7);(5,-3);(5,1)")
				print("The coordinate x of the target is: ")
				target_x = input()
				print("The coordinate y of the target is: ")
				target_y = input()
	return target_x,target_y

def main():
	global pub_goal,sub_odom,pub_target_reached
	global actual_position
	pub_target_reached = rospy.Publisher('move_base/cancel',GoalID,queue_size=1)
	pub_cmd_vel = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
	pub_goal = rospy.Publisher('move_base/goal', MoveBaseActionGoal, queue_size=1)
	sub_odom = rospy.Subscriber('/odom',Odometry,actual_position)
	client_random = rospy.ServiceProxy('/random', Server2)
	client_wall_follow = rospy.ServiceProxy('/wall_follower_switch', SetBool)
	rospy.init_node('interface', anonymous=True)
	rate = rospy.Rate(50) # 50hz
	
	while not rospy.is_shutdown():
		print("Hello! Please insert a command to start")
		print("1) Reach random target")
		print("2) Choose the target that you prefer")
		print("3) Follow the wall")
		print("4) Stop the robot")
		
		command= input()
		
		#First Command: reach a random target 
		if command ==1 : 
			resp = client_wall_follow(False)
			pos_random=client_random()
			print("Coordinate x of the target: ")
			print(pos_random.x)
			print("Coordinate y of the target: ")
			print(pos_random.y)
			
			move_randomly_to_target(pos_random.x,pos_random.y)
			reaching_the_target(pos_random.x,pos_random.y)		
		
		#Second command: choose next target to reach		 
		elif command == 2 :	
			resp = client_wall_follow(False)		
			target_x,target_y = user_set_position()
			move_randomly_to_target(target_x,target_y)
			reaching_the_target(target_x,target_y)
		
		#Third command:_ follow the wall
		elif command == 3 :			
			resp = client_wall_follow(True)
			print("Now the robot starts following the wall")
		
		#Fourth command: Stop the robot	
		elif command == 4 :
			msg = Twist()
			msg.linear.x = 0
			msg.angular.z = 0		
    	
			resp = client_wall_follow(False)	
			pub_cmd_vel.publish(msg)
			print("Now the robot has stopped")
			
		else:	
			print("You choose a wrong command! Try again!")
			
	rate.sleep()

if __name__ == '__main__':
  time.sleep(2)
  main()
  
