YouTube Video Link: https://youtu.be/ffLDAFJHAfk

This is George Wanis’ 1st Assignment, I have walked through the official ros2 docs which you can view it through the following link:
https://docs.ros.org/en/kilted/Tutorials/Beginner-CLI-Tools/Introducing-Turtlesim/Introducing-Turtlesim.html

I then went to view the python libraries I’ll need to create scripts similar to what Mostafa did at the first session, you can look at the same docs I previewed here, just click on the following links:
rclpy provides the canonical Python API for interacting with ROS
it is built on the common C-API provided by rcl

https://github.com/ros2/rcl
https://docs.ros.org/en/iron/p/rclpy/
https://docs.ros.org/en/crystal/Tutorials/Topics/Understanding-ROS2-Topics.html
https://github.com/ros-industrial/ros2_i_training

<img width="940" height="563" alt="image" src="https://github.com/user-attachments/assets/22bcabff-0da5-427b-8185-de1283e3b946" />
<img width="940" height="325" alt="image" src="https://github.com/user-attachments/assets/adedc875-3a43-4d9b-bc48-16403f15dacb" />

There was this method .spin that really got me curious during Mostafa’s session, so I took a screenshot of the docs and attached it here:

<img width="940" height="303" alt="image" src="https://github.com/user-attachments/assets/d3fbe6fd-c528-4ad8-ac06-3ac163a9d1b7" />

It simply means: Keep this node alive and continuously process ROS events/callbacks.
Now let’s organize our working directory as follows in order to see our first node in place: 

<img width="940" height="208" alt="image" src="https://github.com/user-attachments/assets/f6bc3418-217c-49e9-b886-4d88206660cb" />

And here is the code I wrote for that message to show:

<img width="940" height="495" alt="image" src="https://github.com/user-attachments/assets/0a25524e-82a4-483a-be47-0a9590b1f71b" />

<img width="940" height="213" alt="image" src="https://github.com/user-attachments/assets/83a3718b-f11d-41ab-b41a-0ce5918f9a51" />

Now let’s start doing my 3 masterpieces, first I created a new package using the following command:

<img width="940" height="55" alt="image" src="https://github.com/user-attachments/assets/dc44d2c3-1554-4296-8b77-0892322bb31c" />

I then wrote the controller.py script inside the ~/ros2_ws/src/turtle_controller/turtle_controller directory as follows:

<img width="705" height="450" alt="image" src="https://github.com/user-attachments/assets/9ac92abb-42ca-4d72-95f9-ffbd5b6c6bf4" />

added this line to provide an entry point for when I’m using the command $ ros2 run

<img width="715" height="498" alt="image" src="https://github.com/user-attachments/assets/e3bc4f82-27e0-4d9d-a19b-3603d25f557b" />

You can check the create_timer function which is recommended by the docs shown here at the following screenshot:

<img width="940" height="642" alt="image" src="https://github.com/user-attachments/assets/c1987b76-242e-41fe-b6c3-128293791d50" />

<img width="940" height="178" alt="image" src="https://github.com/user-attachments/assets/3e89c2e3-8a34-481d-acc5-216a82917d7a" />

I have searched for a butterfly in mathematics and found this pretty one: 

<img width="391" height="391" alt="image" src="https://github.com/user-attachments/assets/473403fb-9700-4aaa-873b-35519f40998e" />

Formed by these pair of equations:

<img width="445" height="149" alt="image" src="https://github.com/user-attachments/assets/eea8eaa3-3371-4cca-b187-12ecab6a255f" />

Discovered by this guy here:

<img width="267" height="267" alt="image" src="https://github.com/user-attachments/assets/cb1e3798-646d-4715-9f4e-ebe5dbbbcefb" />

You can read more about it here at the following link:
https://en.wikipedia.org/wiki/Butterfly_curve_(transcendental)
https://mathworld.wolfram.com/ButterflyCurve.html
https://www.researchgate.net/publication/232899918_On_the_analysis_and_construction_of_the_butterfly_curve_using_Mathematica_R

<img width="526" height="546" alt="image" src="https://github.com/user-attachments/assets/fd1c6d11-e049-4366-9593-4a432336df75" />

After scaling the time steps the turtle takes, it looks so pretty.

<img width="533" height="548" alt="image" src="https://github.com/user-attachments/assets/e0b21578-49a8-4ef1-b6c9-781fabdca80c" />

Because we’re joining the racing team I thought of drawing a racing car that resembles برق بنزين

<img width="634" height="659" alt="image" src="https://github.com/user-attachments/assets/e1b70815-292e-4ba8-9800-ab46a6031457" />

Now something for the sake of showing ROS that I'm gratefull haha (:

<img width="507" height="532" alt="image" src="https://github.com/user-attachments/assets/34aabb0f-d8e4-489e-a5d8-3e0be208657b" />


For Part 2 of my mission, I went to watch this video explaining services:
https://youtu.be/FSqm0fDfxrk

For Part 2, I'm gonna document the commands I use:
george@LAPTOP-TPV6R8J3:~/ros2_ws$ ros2 service list

    /cinematic_ros_art/describe_parameters
    /cinematic_ros_art/get_parameter_types
    /cinematic_ros_art/get_parameters
    /cinematic_ros_art/list_parameters
    /cinematic_ros_art/set_parameters
    /cinematic_ros_art/set_parameters_atomically
    /turtle1/set_pen

after you do:

george@LAPTOP-TPV6R8J3:~$ ros2 run turtlesim turtlesim_node

    [INFO] [1789400093.134775409] [turtlesim]: Starting turtlesim with node name /turtlesim
    [INFO] [1789400093.143768914] [turtlesim]: Spawning turtle [turtle1] at x=[5.544445], y=[5.544445], theta=[0.000000]

you get:

george@LAPTOP-TPV6R8J3:~/ros2_ws$ ros2 service list

    /cinematic_ros_art/describe_parameters
    /cinematic_ros_art/get_parameter_types
    /cinematic_ros_art/get_parameters
    /cinematic_ros_art/list_parameters
    /cinematic_ros_art/set_parameters
    /cinematic_ros_art/set_parameters_atomically
    /clear
    /kill
    /reset
    /spawn
    /turtle1/set_pen
    /turtle1/teleport_absolute
    /turtle1/teleport_relative <=============================== This is the one Mostafa has mentioned
    /turtlesim/describe_parameters
    /turtlesim/get_parameter_types
    /turtlesim/get_parameters
    /turtlesim/list_parameters
    /turtlesim/set_parameters
    /turtlesim/set_parameters_atomically

george@LAPTOP-TPV6R8J3:~/ros2_ws$ ros2 service  type /turtle1/teleport_relative

    turtlesim/srv/TeleportRelative <========== We wanna see what is inside!

george@LAPTOP-TPV6R8J3:~/ros2_ws$ ros2 interface show turtlesim/srv/TeleportRelative

    float32 linear
    float32 angular
    ---
george@LAPTOP-TPV6R8J3:~/ros2_ws$ ros2 service call /turtle1/teleport_relative turtlesim/srv/TeleportRelative "{linear: 1, angular: 1}"
    
    requester: making request: turtlesim.srv.TeleportRelative_Request(linear=1.0, angular=1.0)
    response:
    turtlesim.srv.TeleportRelative_Response()
    
And if you look at your turtle now, you will see it moving as you commanded using this /turtle1/teleport_relative service!




  ### How to Run and Test

  Open three separate WSL terminals in ~/ros2_ws:

  #### Terminal 1: Launch Turtlesim
    ros2 run turtlesim turtlesim_node

  #### Terminal 2: Run the Stage 2 Controller Node
    source ~/ros2_ws/install/setup.bash
    ros2 run turtle_controller stage2_controller

  #### Terminal 3: Send Commands
  ##### Using the Interactive Client
    source ~/ros2_ws/install/setup.bash
    ros2 run turtle_controller stage2_client

  Then type:

    Enter command > butterfly
    Enter command > pause
    Enter command > resume
    Enter command > reset

      #### 1. Stage2Controller file://wsl.localhost/Ubuntu-22.04/home/george/ros2_ws/src/turtle_controller/turtle_controller/stage2_controller.py

  ### Implementation Details
  #### 1. Stage2Controller.py
  A service server node hosting /shape_command (turtle_interfaces/srv/ShapeCommand):
  • Shape Execution:
      • butterfly: Integrates the parametric adaptive butterfly curve from Stage 1
      ...
  • Pause & Resume:
      • pause: Freezes turtle motion (publishes zero velocity) while preserving trajectory progress.
      • resume (or start): Continues drawing the paused shape from where it stopped.
  • Reset:
      • reset: Stops velocity, calls /turtle1/teleport_absolute with (5.544445, 5.544445, 0.0) to place the turtle back in the middle, and clears the
      canvas via /clear.


  #### 2. Stage2Client.py
  A client node supporting both one-shot CLI usage and interactive prompting:
  • Registered as console script stage2_client in setup.py
