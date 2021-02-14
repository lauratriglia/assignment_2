#include "ros/ros.h"
#include "triglia_final_assignment/Server2.h"
#include <math.h>


//With pos_random we have the possibility to generate random target among all possible one.
bool pos_random (triglia_final_assignment::Server2::Request &req, triglia_final_assignment::Server2::Response &res)
{
	float x_values[]= {-4,-4,-4,5,5,5};
	float y_values[]= {-3,2,7,-7,-3,1};
	int index = rand()%6;
	
	res.x = x_values[index];
	res.y = y_values[index];
	return true;
}


//In the main function we can define the services /random
int main(int argc, char **argv)
{
   ros::init(argc, argv, "random_service");
   ros::NodeHandle n;
   ros::ServiceServer service= n.advertiseService("/random", pos_random);
   ros::spin();

   return 0;
}
