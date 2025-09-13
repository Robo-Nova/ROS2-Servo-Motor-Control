#include <micro_ros_arduino.h>
#include <ESP32Servo.h>
#include <rcl/rcl.h>
#include <rcl/error_handling.h>
#include <rclc/rclc.h>
#include <rclc/executor.h>
#include <std_msgs/msg/int32.h>

Servo myservo;  
const int servoPin = 12;

rcl_subscription_t servo_subscriber;
std_msgs__msg__Int32 servo_msg;

rclc_executor_t executor;
rclc_support_t support;
rcl_allocator_t allocator;
rcl_node_t node;

#define DOMAIN_ID 42

#define RCCHECK(fn) { rcl_ret_t temp_rc = fn; if((temp_rc != RCL_RET_OK)){error_loop();}}
#define RCSOFTCHECK(fn) { rcl_ret_t temp_rc = fn; if((temp_rc != RCL_RET_OK)){}}

void error_loop(){
  while(1){
    delay(100);
  }
}

int limitToMaxValue(int value, int maxLimit) {
  if (value > maxLimit) {
    return maxLimit;
  } else {
    return value;
  }
}

void servo_callback(const void* msgin) {
  const std_msgs__msg__Int32* msg = (const std_msgs__msg__Int32*)msgin;
  int32_t angle = msg->data;
  int servo_position;
  servo_position = limitToMaxValue(angle, 180);
  myservo.write(servo_position);
}

void setup() {
  // Micro-ROS WiFi configuration - replace with your network credentials
  // Parameters: SSID, Password, Agent IP, Agent Port
  set_microros_wifi_transports("YOUR_WIFI_SSID", "YOUR_WIFI_PASSWORD", "RASPBERRY_PI_IP_ADDRESS", 8888);

  ESP32PWM::allocateTimer(0);
  ESP32PWM::allocateTimer(1);
  ESP32PWM::allocateTimer(2);
  ESP32PWM::allocateTimer(3);
  myservo.setPeriodHertz(50);    
  myservo.attach(servoPin, 1000, 2000); 

  allocator = rcl_get_default_allocator();

  rcl_init_options_t init_options = rcl_get_zero_initialized_init_options();
  RCCHECK(rcl_init_options_init(&init_options, allocator));
  
  // ROS 2 Domain ID - must match between all nodes in the same ROS domain
  // Change if needed to avoid conflicts with other ROS networks
  size_t domain_id = DOMAIN_ID;
  rcl_ret_t rc = rcl_init_options_set_domain_id(&init_options, domain_id);
  if (rc != RCL_RET_OK) {
    error_loop();
  }

  RCCHECK(rclc_support_init_with_options(&support, 0, NULL, &init_options, &allocator));
  RCCHECK(rcl_init_options_fini(&init_options));

  RCCHECK(rclc_node_init_default(&node, "servo_controller_esp32", "", &support));

  RCCHECK(rclc_subscription_init_default(
      &servo_subscriber,
      &node,
      ROSIDL_GET_MSG_TYPE_SUPPORT(std_msgs, msg, Int32),
      "/servo"));

  RCCHECK(rclc_executor_init(&executor, &support.context, 1, &allocator));
  RCCHECK(rclc_executor_add_subscription(&executor, &servo_subscriber, &servo_msg, &servo_callback, ON_NEW_DATA));
}

void loop() {
  delay(100);
  RCCHECK(rclc_executor_spin_some(&executor, RCL_MS_TO_NS(100)));
}
