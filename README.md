# **🤖 Autonomous EKF-SLAM Navigation System**

<div align="center">
  
![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue)
![Pygame](https://img.shields.io/badge/Pygame-2.5%2B-green)
![NumPy](https://img.shields.io/badge/NumPy-1.24%2B-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Status](https://img.shields.io/badge/Status-Active-success)

**A Complete Simulation of Simultaneous Localization and Mapping with Autonomous Navigation**

*Visualize SLAM, Obstacle Avoidance, and Path Planning in Real-Time*
[![Demo Image](https://github.com/arun-Koushik-ba/Kalman-Filter_for-Differntial-Drive-Robot/blob/7b8c506ec01433a4cbda44efef998801ffdafe1c/image.png)
[![Demo Video](https://img.shields.io/badge/▶️-Watch_Demo-red)](https://github.com/arun-Koushik-ba/Kalman-Filter_for-Differntial-Drive-Robot/blob/7b8c506ec01433a4cbda44efef998801ffdafe1c/Preview1.mp4)

</div>

## **Table of Contents**
- [✨ Features](#-features)
- [🚀 Quick Start](#-quick-start)
- [📊 Technical Details](#-technical-details)
- [🛠️ Configuration](#️-configuration)
- [📄 License](#-license)
- [🙏 Acknowledgments](#-acknowledgments)

## **Features**

### **Core SLAM Engine**
-  **Extended Kalman Filter (EKF)** implementation with proper Jacobian calculations
-  **Differential Drive Kinematics** modeling
-  **Real-time State Estimation** with covariance visualization

### **Autonomous Navigation**
-  **Waypoint Following** 
-  **Reactive Obstacle Avoidance** 
-  **Multiple Goal Points** 

### **Advanced Visualization**
-  **Three Path Traces** (Ground Truth, Odometry, EKF Estimate)
- **Sensor Ray Visualization** with configurable range
- **Interactive Dashboard** with real-time system metrics
- **Dynamic Error Graph** showing convergence over time
- **Interactive Legend** explaining all visual elements


## **Quick Start**

### **Prerequisites**
```bash
python >= 3.8
pip install pygame numpy
```

### **Installation & Run**
```bash
# Clone the repository
git clone https://github.com/yourusername/autonomous-ekf-slam.git
cd autonomous-ekf-slam

# Run the simulation
python main.py
```

### **Controls**
- **Press `S`** - Toggle sensor range visualization
- **Press `ESC`** - Exit the simulation
- **Close Window** - Exit the simulation

*Note: The system runs fully autonomously - no manual control needed!*

### **System Components**
1. **EKF-SLAM Core** - State estimation and mapping
2. **Sensor Simulator** - Range-bearing measurements with noise
3. **Navigation Controller** - Waypoint following logic
4. **Obstacle Avoidance** - Reactive safety system
5. **Visualization Engine** - Real-time PyGame rendering
6. **Dashboard System** - Performance metrics display

## **Technical Details**

### **Mathematical Foundation**

#### **State Vector**
```
X = [x_r, y_r, θ_r, x_l1, y_l1, ..., x_lN, y_lN]^T
```
- **3 robot states** (position & orientation)
- **2N landmark states** (positions of N landmarks)

#### **EKF Prediction Step**
```python
# State prediction
X_pred = f(X_prev, u)  # Motion model
P_pred = F * P_prev * F.T + Q  # Covariance update

# Jacobian matrix F
F = [[1, 0, -v*sin(θ)*dt],
     [0, 1,  v*cos(θ)*dt],
     [0, 0,           1]]
```

#### **Sensor Model**
```python
# Range measurement
range = sqrt((x_landmark - x_robot)**2 + (y_landmark - y_robot)**2)

# Bearing measurement
bearing = atan2(y_landmark - y_robot, x_landmark - x_robot) - θ_robot
```


### **Key Concepts Covered**
1. **Bayesian Estimation** - Probabilistic state tracking
2. **Sensor Fusion** - Combining multiple information sources
3. **Non-linear Systems** - Handling trigonometric models
4. **Robot Kinematics** - Differential drive motion
5. **Control Theory** - PID-like navigation
6. **Computer Vision** - Landmark representation
7. **Real-time Systems** - 60 FPS simulation


### **File Descriptions**

| File | Purpose |
|------|---------|
| **main.py** | Core simulation loop integrating all components |
| **config.py** | Centralized configuration parameters |
| **utils.py** | Mathematical functions and drawing utilities |
| **assets.py** | Landmark textures and UI elements |

## **Applications & Use Cases**

### **Academic Applications**
- **Classroom Demonstrations** - Visualizing SLAM concepts
- **Student Projects** - Robotics course assignments
- **Research Prototyping** - Algorithm testing platform

### **Industry Applications**
- **Autonomous Vehicles** - SLAM for self-driving cars
- **Warehouse Robotics** - Inventory management robots
- **Agricultural Automation** - Field monitoring robots
- **Drone Navigation** - UAV localization and mapping


## **Acknowledgments**
We thank our college for Encouraging this course as a curicullum.<br>

We thank our Robotics HOD - Dr.Hongray for his teaching and his guidance.


## **Tools & Libraries**
- **Pygame** for real-time visualization
- **NumPy** for efficient numerical computations
- **GitHub** for version control and collaboration
- **Visual Studio Code** for development environment

## **License**

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

<div align="center">

**Built with ❤️ for the robotics community**
💼 LinkedIn: [Arun Koushik B A](www.linkedin.com/in/b-a-arun-koushik)  

*"The best way to predict the future is to create it." - Alan Kay*

</div>
