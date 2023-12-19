import os
import xacro
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():

    stroke = DeclareLaunchArgument(
        'stroke',
        default_value='0.085',
        description='gripper stroke'
    )
    comport = DeclareLaunchArgument(
        'comport',
        default_value='/dev/ttyUSB0',
        description='comport'
    )
    baud = DeclareLaunchArgument(
        'baud',
        default_value='115200',
        description='baudrate'
    )
    # robot_description_config = xacro.process_file(os.path.join(get_package_share_directory('robotiq_85_description'), 'urdf', 'robotiq_85_gripper.urdf.xacro'))
    # robot_description = {'robot_description': robot_description_config.toxml()}
    # robot_state_pub_node = Node(
    #     package='robot_state_publisher',
    #     executable='robot_state_publisher',
    #     output='screen',
    #     parameters=[robot_description]
    # )

    griperdriver_node = Node(package='robotiq_85_driver',
                             executable='robotiq_85_driver',
                             name='robotiq_85_driver',
                             parameters=[{"num_grippers": 1}, {"comport": LaunchConfiguration('comport')}, {"baud": LaunchConfiguration('baud')}, {"stroke": LaunchConfiguration('stroke')}],
                             output='screen',)

    action_server_node = Node(package='robotiq_85_driver',
                             executable='single_robotiq_85_action_server',
                             name='single_robotiq_85_action_server',
                             parameters=[{"timeout": 5.0}, {"position_tolerance": 0.005}, {"gripper_speed": 0.0565}, {"stroke": LaunchConfiguration('stroke')}],
                             output='screen',)

    return LaunchDescription([stroke, comport, baud, griperdriver_node, action_server_node])