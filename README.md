# Thrust-Based Beam Balancing System (Bare-Metal Control)

## 1. Project Overview
This project involves the design and implementation of an inherently unstable mechanical system—a single-axis beam—stabilized using differential thrust. The system is controlled by a **Texas Instruments TM4C123G (Tiva C Series)** microcontroller. Using a **bare-metal programming approach**, the system integrates real-time sensor feedback from an MPU6050 IMU, Hall-effect sensors, and current sensors to execute a high-speed PID control loop that maintains equilibrium.

This system mirrors the fundamental control principles used in UAV pitch/roll stabilization, camera gimbals, and self-balancing robotics.

---

## 2. Key Features
* **Bare-Metal Architecture:** Firmware developed with direct register-level access (no OS or high-level abstraction) to ensure maximum timing precision and low-latency execution.
* **Real-Time PID Control:** Implements a feedback loop with Proportional, Integral, and Derivative terms, including output saturation to protect actuators.
* **Multi-Sensor Fusion:** * **I2C Interface:** High-speed communication with the MPU6050 IMU for angle estimation.
    * **ADC Interfacing:** Real-time current monitoring via ACS712 sensors for power analysis.
    * **Interrupt-Based Sensing:** Hall-effect pulse counting for precise motor RPM feedback.
* **Safety Engineering:** Includes a predefined "Slow-Start" phase and hardware saturation limits to prevent mechanical failure during initialization.
* **Telemetry Dashboard:** Streams real-time tilt, RPM, and current data via UART to a PC-based GUI for performance logging and analysis.

---

## 3. System Architecture
### 3.1 Hardware Components
| Component | Specification | Role |
| :--- | :--- | :--- |
| **Microcontroller** | TM4C123GH6PM (16 MHz) | Central processing and control logic. |
| **Actuators** | 2x A2212 1400 kV BLDC | Provides thrust for beam stabilization. |
| **Motor Drivers** | 2x 30A ESCs | Converts PWM signals to high-current motor drive. |
| **IMU** | MPU6050 (6-Axis) | Measures pitch angle via I2C at 50-100 Hz. |
| **Current Sensors** | 2x ACS712 (30A) | Monitors electrical load for safety and telemetry. |
| **Speed Sensors** | Hall-Effect Modules | Provides magnetic feedback for RPM calculation. |
| **Power Supply** | 12V DC / 60A | High-capacity regulated power source. |

### 3.2 Pin Mapping (GPIO Configuration)
| Function | TM4C123 Pin | Peripheral |
| :--- | :--- | :--- |
| **ESC Control 1** | PB6 | Timer 0A (Hardware PWM) |
| **ESC Control 2** | PB7 | Timer 1A (Hardware PWM) |
| **IMU SCL** | PA6 | I2C1 Serial Clock |
| **IMU SDA** | PA7 | I2C1 Serial Data |
| **Hall Sensor 1** | PB2 | GPIO Interrupt (Pulse Input) |
| **Hall Sensor 2** | PB3 | GPIO Interrupt (Pulse Input) |
| **Current Sensor 1**| PE2 | ADC Channel (Analog Input) |
| **Current Sensor 2**| PE1 | ADC Channel (Analog Input) |
| **UART0 TX/RX** | PA1 / PA0 | Serial Telemetry (9600 Baud) |

---

## 4. Software Implementation
### 4.1 Peripheral Initialization
* **Clock Configuration:** The system clock is fixed at 16 MHz using the internal oscillator for consistent timing.
* **PWM Generation:** Timers are configured to produce standard RC-compatible signals (1ms to 2ms pulse width) for the ESCs.
* **I2C Protocol:** Configured at standard 100kbps to sample the MPU6050 accelerometer and gyroscope data.

### 4.2 PID Control Logic
The controller continuously compares the desired setpoint (0° tilt) with the measured value:
1.  **Proportional (P):** Generates immediate corrective action based on the current angle error.
2.  **Integral (I):** Accumulates the error over time to eliminate steady-state offsets.
3.  **Derivative (D):** Predicts future behavior based on the rate of change of the error, reducing oscillations and smoothing response.
4.  **Saturation:** Final commands are clamped within safe PWM duty cycle limits to prevent motor/ESC damage.

---

## 5. Operations & Setup
1.  **System Inspection:** Verify all structural mounts and electrical common grounds.
2.  **Safe Start:** Upon power-up, the system enters a delay-based slow-start phase, sending a low-pulse command to initialize the ESCs safely.
3.  **Feedback Acquisition:** The IMU provides pitch data while Hall sensors monitor motor speeds.
4.  **Closed-Loop Operation:** The PID controller activates, adjusting motor thrust to stabilize the beam.
5.  **Data Logging:** Performance is monitored via PuTTY or a custom Python GUI to analyze stability and transient behavior.

---

## 6. Bill of Materials (BOM)
* **Total Project Cost:** ~25,830 PKR
* **Key Vendors:** The I.C. Shop, Mekatroniks, and Electronic Solution (Lahore, PK).
* **Mechanical Frame:** Dual drone-arm construction with a 18.5" wooden beam and ball-bearing center pivot.

---

## 7. Conclusions
The system successfully demonstrates the application of real-time embedded control on an ARM-based platform. By leveraging bare-metal programming, the project achieves the high-frequency response required to stabilize an inherently unstable system through precise motor synchronization.
