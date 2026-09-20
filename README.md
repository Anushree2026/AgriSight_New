# AgriSight – AI-Based Real-Time Fruit Detection System

AgriSight is an AI-based real-time fruit detection system that uses **YOLOv8** and **OpenCV** to detect fruits and assess their ripeness from live video. The system integrates a **Raspberry Pi camera** for real-time image capture and provides a **Flask-based web application** for presenting detection results.

## Features

* 🍎 Real-time fruit detection using YOLOv8
* 🔍 Fruit ripeness assessment from live video
* 📷 Raspberry Pi camera integration for live image capture
* 🎥 Real-time video processing using OpenCV
* 🌐 Flask-based web application
* 🔐 OTP-based user authentication
* 🗄️ SQLite database for application data
* ⚙️ SQLAlchemy for database management
* 📊 Web interface for viewing fruit detection results

## Technology Stack

| Technology   | Purpose                                 |
| ------------ | --------------------------------------- |
| Python       | Core programming language               |
| YOLOv8       | Fruit detection and ripeness assessment |
| OpenCV       | Image and video processing              |
| Raspberry Pi | Hardware and camera integration         |
| Flask        | Web application development             |
| SQLite       | Database                                |
| SQLAlchemy   | Database management                     |

## How It Works

The system follows these main steps:

1. The **Raspberry Pi camera** captures live video.
2. **OpenCV** processes the video frames.
3. **YOLOv8** analyzes the frames to detect fruits.
4. The system identifies the detected fruit and assesses its ripeness.
5. The detection results are processed through the **Flask web application**.
6. Users can view the results through the web interface.
7. Application and user-related data are managed using **SQLite and SQLAlchemy**.

## Project Structure

```text
AgriSight/
│
├── app.py
├── app_pi.py
├── new_rpi_app.py
├── cam.py
├── tomato.py
│
├── best.pt
├── tomato.pt
│
├── templates/
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── detect.html
│   └── ...
│
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│
└── instance/
```

## Future Improvements

* Support for additional fruit varieties
* Improved detection accuracy under different lighting conditions
* Mobile-friendly interface
* Cloud-based storage and monitoring
* Automated agricultural insights based on detection results
* Deployment on edge devices with optimized models

## Author

**Anushree Sawant**

B.E. Computer Engineering
Smt. Kashibai Navale College of Engineering, Pune

## License

This project was developed as an academic project for learning and demonstrating applications of **Artificial Intelligence, Computer Vision, Web Development, and IoT/Edge Computing**.
