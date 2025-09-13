# 🚀 ROS2 Servo Motor Controller

Hey there, robotics enthusiasts! 👋  
I'm **Ali Khaleghi**, a systems-oriented developer passionate about building resilient, scalable infrastructure for distributed robotics. This repository is part of my journey to create a robust servo motor controller using **ROS 2 Humble** — designed for precision, modularity, and real-world deployment.

---

## 🎯 Project Overview

This project provides a clean and extensible framework for controlling servo motors using ROS 2. Whether you're prototyping a robotic arm, building an autonomous rover, or experimenting with IoT devices, this package gives you the tools to command servo motors with accuracy and flexibility.

It’s built with maintainability in mind: annotated code, modular nodes, and clear separation between hardware interfaces and ROS logic. I’ve designed it to be beginner-friendly while still offering depth for advanced robotics workflows.

---

## 🧠 Key Features

- 🌀 **ROS 2 Topic-Based Control** — Send angle commands via standard ROS messages  
- ⚙️ **Parameterizable Nodes** — Easily configure motor limits, speed, and update rates  
- 🔁 **Modular Architecture** — Clean separation of logic, hardware, and configuration  
- 🧪 **Tested on Ubuntu 22.04 + ROS 2 Humble**  
- 📚 **Well-documented for reproducibility and collaboration**  

---

## 🖥️ GUI Controller Preview

Here’s a sneak peek of the GUI interface used to control the servo motor interactively:

<img width="602" height="639" alt="Screenshot from 2025-09-13 04-03-26" src="https://github.com/user-attachments/assets/2347629c-e499-4ba5-be47-fc248789955b" />

> The GUI allows real-time angle adjustment, feedback monitoring, and manual override. It’s built using Python and integrates seamlessly with ROS 2 topics.

---

## 📦 Installation & Setup

```bash
# Clone the repository
git clone https://github.com/Robo-Nova/ROS2-Servo-Motor-Control.git
cd ROS2-Servo-Motor-Control

# Build the workspace
colcon build --packages-select servo_motor_controller

# Source the setup file
source install/setup.bash
