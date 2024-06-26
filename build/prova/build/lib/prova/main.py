from collections import deque
import rclpy
from rclpy.node import Node
from turtlesim.srv import SetPen, Spawn, Kill
from geometry_msgs.msg import Twist
import sys
import select
import tty
import termios
import time



class DriverNode(Node):
    def __init__(self):
        super().__init__('driver_node')
        self.spawn_client = self.create_client(Spawn, 'spawn')
        self.kill_client = self.create_client(Kill, 'kill')
        self.pen_r = 255
        self.pen_g = 210
        self.pen_b = 20
        self.pen_width = 15
        self.pen_off = False
        self.spawn_turtle()
        self.dq = deque()

    def spawn_turtle(self):
        self.get_logger().info('Aguardando serviço de Spawn...')
        self.spawn_client.wait_for_service()
        spawn_request = Spawn.Request()
        spawn_request.x = 2.0
        spawn_request.y = 2.0
        spawn_request.theta = 1.57  
        spawn_request.name = 'turtle2'
        future = self.spawn_client.call_async(spawn_request)
        rclpy.spin_until_future_complete(self, future)
        try:
            response = future.result()
            self.turtle_name = response.name
            self.get_logger().info(f'Tartaruga de nome: {self.turtle_name} spawnada')
            self.setup_turtle_controls()
        except Exception as e:
            self.get_logger().error('Falha na hora de spawnar: %r' % (e,))

    def setup_turtle_controls(self):
        self.publisher_ = self.create_publisher(Twist, f'/{self.turtle_name}/cmd_vel', 10)
        self.pen_client = self.create_client(SetPen, f'/{self.turtle_name}/set_pen')
        self.timer = self.create_timer(0.1, self.timer_callback)
        self.set_initial_pen_settings()
        self.move_sequence = self.create_m_move_sequence()
        self.move_index = 0
        self.start_time = self.get_clock().now()

    def create_m_move_sequence(self):
        # Define the sequence of movements to draw "M": [linear speed, angular speed, duration]
#        moves = [
#            [2.0, 0.0, 2.0],   # Move straight up
#            [0.0, 0.0, 0.2],   # Stop
#            [0.0, -1.57, 0.5], # Turn -90 degrees
#            [1.5, 0.0, 1.0],   # Move diagonally down-right
#            [0.0, 0.0, 0.2],   # Stop
#            [0.0, 3.14, 0.5],  # Turn 180 degrees
#            [1.5, 0.0, 1.0],   # Move diagonally up-right
#            [0.0, 0.0, 0.2],   # Stop
#            [0.0, -1.57, 0.5], # Turn -90 degrees
#            [2.0, 0.0, 2.0]    # Move straight down
#        ]

        self.dq = self.dq.append(sys.argv[1], sys.argv[2], sys.argv[3])


        return self.dq

    def timer_callback(self):
        current_time = self.get_clock().now()
        elapsed_time = (current_time - self.start_time).nanoseconds / 1e9  # Convert to seconds

        if self.move_index < len(self.move_sequence):
            linear_speed, angular_speed, duration = self.move_sequence[self.move_index]
            msg = Twist()
            msg.linear.x = linear_speed
            msg.angular.z = angular_speed
            self.publisher_.publish(msg)

            if elapsed_time > duration:
                self.move_index += 1
                self.start_time = current_time
        else:
            self.kill_turtle()

    def set_initial_pen_settings(self):
        self.get_logger().info('Aguardando serviço de SetPen...')
        self.pen_client.wait_for_service()
        req = SetPen.Request()
        req.r = self.pen_r
        req.g = self.pen_g
        req.b = self.pen_b
        req.width = self.pen_width
        req.off = self.pen_off
        future = self.pen_client.call_async(req)
        rclpy.spin_until_future_complete(self, future)
        try:
            future.result()
            self.get_logger().info('Configurações da caneta setadas com sucesso.')
            self.get_logger().info('Para matar a tartaruga, pressione a tecla (Q)')
        except Exception as e:
            self.get_logger().error('Setagem da caneta falhada: %r' % (e,))

    def kill_turtle(self):
        self.get_logger().info('Esperando serviço de Kill...')
        self.kill_client.wait_for_service()
        kill_request = Kill.Request()
        kill_request.name = self.turtle_name
        future = self.kill_client.call_async(kill_request)
        rclpy.spin_until_future_complete(self, future)
        try:
            future.result()
            self.get_logger().info(f'Tartaruga de nome {self.turtle_name} foi morta. Fechando este terminal em 15 segundos')
        except Exception as e:
            self.get_logger().error(f'Falha na morte: {e}')