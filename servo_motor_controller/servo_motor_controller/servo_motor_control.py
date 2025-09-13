#!/usr/bin/env python3
# -*- coding: utf-8 -*-



###################################################################
#                     made by Ali Khaleghi                        #
#                   Release: Septomber 2025                       #
#             github: https://github.com/Robo-Nova                #
###################################################################



import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32
import pygame
import sys
import threading
import math

# Window settings
WIDTH, HEIGHT = 600, 600
TRACKER_SIZE = 250

# Colors
BACKGROUND = (30, 30, 40)
TRACKER_BG = (50, 50, 60)
TRACKER_CIRCLE = (70, 70, 80)
HANDLE_COLOR = (65, 105, 225)
HANDLE_ACTIVE = (220, 60, 60)
TEXT_COLOR = (240, 240, 240)
BUTTON_COLOR = (80, 80, 100)
BUTTON_HOVER = (100, 100, 120)
SLIDER_COLOR = (90, 90, 110)
SLIDER_HANDLE = (70, 130, 180)
ANGLE_LINE_COLOR = (255, 200, 50)

class ServoTracker(Node):
    def __init__(self):
        super().__init__('servo_control')
        
        # Publisher for servo with Int32
        self.servo_pub = self.create_publisher(Int32, 'servo', 10)
        self.speed_pub = self.create_publisher(Int32, 'servo_speed', 10)
        
        # State variables
        self.center_x = WIDTH // 2
        self.center_y = HEIGHT // 2
        self.angle = 90  # Initial angle (90 degrees - center)
        self.is_dragging = False
        self.speed_value = 20
        
        # Initialize Pygame in separate thread
        self.pygame_thread = threading.Thread(target=self.run_pygame)
        self.pygame_thread.daemon = True
        self.pygame_thread.start()
        
        self.get_logger().info('Servo Control Node Has Been Started!')

    def run_pygame(self):
        """Run Pygame UI in separate thread"""
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Servo Angle Tracker")
        
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 20)
        self.title_font = pygame.font.SysFont("Arial", 28, bold=True)
        
        running = True
        while running and rclpy.ok():
            running = self.handle_events()
            self.draw_ui()
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()
        if not rclpy.ok():
            sys.exit(0)

    def draw_ui(self):
        """Draw the user interface"""
        # Background
        self.screen.fill(BACKGROUND)
        
        # Title
        title = self.title_font.render("Servo Angle Tracker", True, TEXT_COLOR)
        self.screen.blit(title, (WIDTH//2 - title.get_width()//2, 20))
        
        # Angle tracker
        self.draw_tracker()
        
        # Display angle
        angle_text = self.font.render(f"Angle: {self.angle}°", True, TEXT_COLOR)
        self.screen.blit(angle_text, (50, HEIGHT - 80))
        
        speed_text = self.font.render(f"Speed: {self.speed_value}ms", True, TEXT_COLOR)
        self.screen.blit(speed_text, (50, HEIGHT - 50))
        
        # Buttons
        self.draw_buttons()
        
        # Speed slider
        self.draw_slider()

    def draw_tracker(self):
        """Draw the angle tracker"""
        # Tracking circle
        pygame.draw.circle(self.screen, TRACKER_CIRCLE, (self.center_x, self.center_y), TRACKER_SIZE//2)
        pygame.draw.circle(self.screen, TRACKER_BG, (self.center_x, self.center_y), TRACKER_SIZE//2 - 2)
        
        # Guide lines (0°, 90°, 180°)
        for guide_angle in [0, 90, 180]:
            rad_angle = math.radians(guide_angle)
            end_x = self.center_x + (TRACKER_SIZE//2 - 10) * math.cos(rad_angle)
            end_y = self.center_y - (TRACKER_SIZE//2 - 10) * math.sin(rad_angle)
            pygame.draw.line(self.screen, (100, 100, 120), (self.center_x, self.center_y), (end_x, end_y), 1)
            
            # Display degree
            text_x = self.center_x + (TRACKER_SIZE//2 + 15) * math.cos(rad_angle) - 10
            text_y = self.center_y - (TRACKER_SIZE//2 + 15) * math.sin(rad_angle) - 10
            angle_text = self.font.render(f"{guide_angle}°", True, TEXT_COLOR)
            self.screen.blit(angle_text, (text_x, text_y))
        
        # Angle indicator line
        rad_angle = math.radians(self.angle)
        end_x = self.center_x + (TRACKER_SIZE//2 - 20) * math.cos(rad_angle)
        end_y = self.center_y - (TRACKER_SIZE//2 - 20) * math.sin(rad_angle)
        pygame.draw.line(self.screen, ANGLE_LINE_COLOR, (self.center_x, self.center_y), (end_x, end_y), 3)
        
        # Position handle
        handle_color = HANDLE_ACTIVE if self.is_dragging else HANDLE_COLOR
        handle_x = self.center_x + (TRACKER_SIZE//2 - 30) * math.cos(rad_angle)
        handle_y = self.center_y - (TRACKER_SIZE//2 - 30) * math.sin(rad_angle)
        pygame.draw.circle(self.screen, handle_color, (int(handle_x), int(handle_y)), 12)

    def draw_buttons(self):
        """Draw buttons"""
        # Center button
        button_rect = pygame.Rect(WIDTH - 150, HEIGHT - 100, 120, 40)
        mouse_pos = pygame.mouse.get_pos()
        is_hovered = button_rect.collidepoint(mouse_pos)
        
        pygame.draw.rect(self.screen, BUTTON_HOVER if is_hovered else BUTTON_COLOR, button_rect, border_radius=8)
        pygame.draw.rect(self.screen, TEXT_COLOR, button_rect, 2, border_radius=8)
        
        text = self.font.render("CENTER", True, TEXT_COLOR)
        self.screen.blit(text, (button_rect.centerx - text.get_width()//2, button_rect.centery - text.get_height()//2))
        
        return button_rect

    def draw_slider(self):
        """Draw speed slider"""
        slider_x = 200
        slider_y = HEIGHT - 30
        slider_width = 300
        
        # Slider line
        pygame.draw.line(self.screen, SLIDER_COLOR, (slider_x, slider_y), (slider_x + slider_width, slider_y), 3)
        
        # Slider handle
        handle_x = self.map_value(self.speed_value, 5, 100, slider_x, slider_x + slider_width)
        pygame.draw.circle(self.screen, SLIDER_HANDLE, (int(handle_x), slider_y), 10)
        
        # Speed text
        text = self.font.render(f"Speed: {self.speed_value}ms", True, TEXT_COLOR)
        self.screen.blit(text, (slider_x + slider_width + 20, slider_y - 10))

    def map_value(self, value, in_min, in_max, out_min, out_max):
        """Map value from one range to another"""
        return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

    def handle_events(self):
        """Handle events"""
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Check click on tracker area
                distance = ((mouse_pos[0] - self.center_x)**2 + (mouse_pos[1] - self.center_y)**2)**0.5
                if distance <= TRACKER_SIZE//2:
                    self.is_dragging = True
                    self.update_angle_from_mouse(mouse_pos)
                    self.send_angle()
                
                # Check click on button
                button_rect = self.draw_buttons()
                if button_rect.collidepoint(mouse_pos):
                    self.center_servo()
                
                # Check click on slider
                if HEIGHT - 40 <= mouse_pos[1] <= HEIGHT - 20:
                    self.speed_value = int(self.map_value(mouse_pos[0], 200, 500, 5, 100))
                    self.speed_value = max(5, min(100, self.speed_value))
                    self.send_speed()
            
            elif event.type == pygame.MOUSEBUTTONUP:
                self.is_dragging = False
            
            elif event.type == pygame.MOUSEMOTION:
                if self.is_dragging:
                    self.update_angle_from_mouse(mouse_pos)
                    self.send_angle()
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    self.center_servo()
                elif event.key == pygame.K_UP:
                    self.speed_value = min(100, self.speed_value + 5)
                    self.send_speed()
                elif event.key == pygame.K_DOWN:
                    self.speed_value = max(5, self.speed_value - 5)
                    self.send_speed()
                elif event.key == pygame.K_LEFT:
                    self.angle = max(0, self.angle - 5)
                    self.send_angle()
                elif event.key == pygame.K_RIGHT:
                    self.angle = min(180, self.angle + 5)
                    self.send_angle()
        
        return True

    def update_angle_from_mouse(self, mouse_pos):
        """Update angle based on mouse position"""
        dx = mouse_pos[0] - self.center_x
        dy = self.center_y - mouse_pos[1]  # Invert Y direction
        
        # Calculate angle (0-180 degrees)
        angle_rad = math.atan2(dy, dx)
        angle_deg = math.degrees(angle_rad)
        
        # Convert to 0-180 degree range
        if angle_deg < 0:
            angle_deg += 360
        
        # Limit to 0-180 degrees
        if angle_deg > 180:
            if angle_deg < 270:  # Close to 180 degrees
                angle_deg = 180
            else:  # Close to 0/360 degrees
                angle_deg = 0
        else:
            angle_deg = max(0, min(180, angle_deg))
        
        self.angle = int(angle_deg)

    def send_angle(self):
        """Send angle as Int32 to /servo topic"""
        msg = Int32()
        msg.data = self.angle
        self.servo_pub.publish(msg)
        self.get_logger().info(f'Published angle: {self.angle}°')

    def send_speed(self):
        """Send speed as Int32"""
        msg = Int32()
        msg.data = self.speed_value
        self.speed_pub.publish(msg)
        self.get_logger().info(f'Published speed: {self.speed_value}ms')

    def center_servo(self):
        """Return servo to center position (90 degrees)"""
        self.angle = 90
        self.send_angle()
        self.get_logger().info('Servo centered to 90°')

def main(args=None):
    rclpy.init(args=args)
    node = ServoTracker()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
