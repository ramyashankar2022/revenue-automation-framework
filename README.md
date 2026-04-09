# 🚗 Revenue NSW Automation Framework

This project demonstrates an end-to-end **UI and API automation framework** for validating the **Motor Vehicle Stamp Duty calculator**.

---

## 📌 Project Overview

The framework includes:

- ✅ UI Automation (Python + Selenium + Behave)
- ✅ API Automation (Java + Cucumber + Rest Assured)
- ✅ CI/CD Pipeline (GitHub Actions)
- ✅ BDD (Behavior Driven Development) approach
- ✅ Automated test execution with reporting

---

## 🧰 Tech Stack

### 🔹 UI Automation
- Python
- Behave (BDD)
- Selenium WebDriver

### 🔹 API Automation
- Java
- Cucumber (BDD)
- Rest Assured

### 🔹 DevOps
- GitHub
- GitHub Actions (CI/CD)

---
## 🚀 How to Run Tests Locally

---

1) Clone Repository

1. git clone https://github.com/ramyashankar2022/revenue-automation-framework.git
2. cd revenue-automation-framework

2) UI Automation (Python)

Install dependencies
1. cd ui-automation
2. pip install -r requirements.txt

Run tests
1. behave

3) API Automation (Java)

Prerequisites
1. Java 21
2. Maven


# Run tests
1. cd api-automation
2. mvn test

# CI/CD Pipeline (GitHub Actions)
1. Pipeline runs automatically on: Push to main

# Pipeline Steps:
1. Checkout code
2. Setup Python & install UI dependencies
3. Run UI tests (Behave)
4. Setup Java & Maven
5. Run API tests (Cucumber + Rest Assured)

# Reporting
1. Console-based execution logs
2. Clear assertion outputs for debugging

# Notes
1. UI tests run in headless mode in CI/CD
2. ChromeDriver is managed automatically
3. No manual setup required for drivers
