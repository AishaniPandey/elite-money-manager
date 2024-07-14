# Personal Finance Management System aka the Elite Money Manager

## Project Overview
The Personal Finance Management System is an advanced application designed to help users manage their finances effectively. It features automated payment logging, budget management, and financial notifications, along with insightful data visualizations to aid in financial planning. The application is built with an event-driven architecture, using Kafka for messaging and real-time data processing.

## Technologies Used
- **Python**: Primary programming language.
- **Kivy**: Used for creating the user interface.
- **Kafka**: Handles event-driven messaging and data processing.
- **SQLite/JSON**: Used for local data storage.
- **Matplotlib**: For generating data visualizations.

## Installation

To get started with the Personal Finance Tracker, follow these steps:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourgithubusername/finance-tracker.git
   cd finance-tracker
   ```
2. **Install required packages:**
   ```bash
   pip install -r requirements.txt

   ```
4. **Configure Kafka:**
   -Ensure Kafka and Zookeeper are running on your machine.
   -Configure the necessary Kafka topics as mentioned in the setup documentation.
6. **Run the application:**
   ```bash
   python main.py

   ```
