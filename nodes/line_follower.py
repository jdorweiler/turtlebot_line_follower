#!/usr/bin/env python
import roslib; roslib.load_manifest('line_follower')
import rospy
from geometry_msgs.msg import Twist
from turtlebot_node.msg import TurtlebotSensorState

#global
turn = 0.0
 
def processSensing(TurtlebotSensorState):
    global turn
    
	# turn right if we set off the left cliff sensor
    if( TurtlebotSensorState.cliff_left_signal > 1100 ):
		turn = 2
	# turn left if we set off the right cliff sensor
    if( TurtlebotSensorState.cliff_right_signal > 900 ):
		turn = -2
   
def run():

	# publish twist messages to /cmd_vel
    pub = rospy.Publisher('/cmd_vel', Twist)

	#subscribe to the robot sensor state
    rospy.Subscriber('/turtlebot_node/sensor_state', TurtlebotSensorState, processSensing)
    rospy.init_node('Line_Follower')

    global turn
    twist = Twist()

    while not rospy.is_shutdown():

		# turn if we hit the line
        if ( turn != 0.0 ):
            str = "Turning  %s"%turn
            rospy.loginfo(str)
            twist.linear.x = 0.2; twist.linear.y = 0; twist.linear.z = 0
            twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = turn
            turn = 0.0

		# straight otherwise
        else:
            str = "Straight %s"%turn
            rospy.loginfo(str)
            twist.linear.x = 0.2; twist.linear.y = 0; twist.linear.z = 0
            twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = 0

		# send the message and delay
        pub.publish(twist)
        rospy.sleep(0.1)

if __name__ == '__main__':
    try:
        run()
    except rospy.ROSInterruptException: pass
