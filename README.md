# Revenue Automation Framework

A comprehensive **BDD automation testing framework** for both **UI and API testing** with CI/CD integration via GitHub Actions.

---

## 📋 Project Overview

This automation framework demonstrates enterprise-grade test automation for:

- **UI Automation**: Service NSW Motor Vehicle Stamp Duty Calculator
  - Technology: Selenium + Behave (BDD)
  - Language: Python 3.13+
  
- **API Automation**: Open Library Author API
  - Technology: RestAssured + Cucumber (BDD)
  - Language: Java 21+

- **CI/CD Pipeline**: GitHub Actions with automated test execution and reporting

---

## 🏗️ Project Structure

```
revenue-automation-framework/
│
├── .github/
│   └── workflows/
│       └── automation-pipeline.yml          ← GitHub Actions CI/CD configuration
│
├ui-automation/features/
├── utils/
│   ├── __init__.py              ← makes utils a Python package
│   └── helpers.py               ← ALL reusable functions live here
├── steps/
│   └── check_stamp_duty_steps.py ← now thin — only BDD step logic
└── environment.py
│
├── api-automation/                          ← API Testing (Maven + Cucumber)
│   ├── src/test/
│   │   ├── java/
│   │   │   ├── runners/
│   │   │   │   └── TestRunner.java         ← Cucumber test runner
│   │   │   └── steps/
│   │   │       └── OpenLibrarySteps.java   ← API step implementations with assertions
│   │   └── resources/
│   │       └── features/
│   │           └── open_library.feature    ← API test scenarios
│   ├── target/                             ← Generated test artifacts & reports
│   └── pom.xml                             ← Maven dependencies & configuration
│
└── README.md                                ← This file
```

---

## 🛠️ Tech Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| **UI Browser Automation** | Selenium | 4.6+ |
| **UI BDD Framework** | Behave | Latest |
| **API Testing** | RestAssured | 5.4.0 |
| **API BDD Framework** | Cucumber | 7.15.0 |
| **Build Tool** | Maven | 3.8+ |
| **UI Language** | Python | 3.13+ |
| **API Language** | Java | 21+ |
| **CI/CD** | GitHub Actions | - |
| **Browser** | Google Chrome | Latest |

---

## 📦 Installation & Setup

### Prerequisites

- **Java 21+** — [Download](https://www.oracle.com/java/technologies/javase/jdk21-archive-downloads.html)
- **Python 3.13+** — [Download](https://www.python.org/downloads/)
- **Maven 3.8+** — [Download](https://maven.apache.org/download.cgi)
- **Google Chrome** — Already installed on your Mac
- **Git** — For version control

### Step-by-Step Setup

#### 1. Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/revenue-automation-framework.git
cd revenue-automation-framework
```

#### 2. Set Up UI Automation (Python/Behave)

```bash
cd ui-automation

# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### 3. Set Up API Automation (Java/Maven)

```bash
cd api-automation

# Maven automatically downloads dependencies on first run
mvn clean install
```

---

## 🚀 Running Tests

### Run UI Tests Only

```bash
cd ui-automation
behave --no-capture
```

### Run API Tests Only

```bash
cd api-automation
mvn test
```

### Run Both Tests

```bash
# Run API tests first
cd api-automation && mvn test && cd ..

# Then run UI tests
cd ui-automation && behave --no-capture && cd ..
```

---

## 📊 Viewing Test Reports

### API Test Reports

After running `mvn test`, view the Cucumber HTML report:

```bash
cd api-automation
open target/cucumber-reports/report.html
```

Shows:
- Test execution summary (pass/fail/skip)
- All test steps with execution time
- JSON report for CI/CD integration

### UI Test Reports

After running `behave --no-capture`, save and view results:

```bash
cd ui-automation
behave --no-capture --format json --outfile reports/report.json
open reports/report.json
```

Or view the console output directly (Behave prints detailed results to terminal).

---

## 🧪 Test Coverage

### UI Automation Test Case

**Feature**: Motor Vehicle Stamp Duty Calculator

**Scenario**: Calculate stamp duty for $50,000 vehicle

**Steps Covered**:
1. ✅ Navigate to Service NSW stamp duty page
2. ✅ Click "Check Online" button
3. ✅ Verify redirect to Revenue NSW calculator
4. ✅ Select "Yes" for NSW residency
5. ✅ Enter vehicle amount ($50,000)
6. ✅ Click "Calculate" button
7. ✅ Verify popup appears with results
8. ✅ Assert popup title ("Calculation")
9. ✅ Assert popup heading ("Motor vehicle registration")
10. ✅ Assert passenger vehicle selection ("Yes")
11. ✅ Assert purchase price ($50,000.00)
12. ✅ Assert duty payable amount (valid dollar format)
13. ✅ Assert disclaimer note ("All amounts are in Australian dollars")
14. ✅ Assert "contact us" link present
15. ✅ Assert "Close" button present
16. ✅ Close browser

**Total Steps**: 16 ✅ PASSING

### API Automation Test Case

**Feature**: Open Library Author API

**Scenario**: Fetch and assert author details

**Steps Covered**:
1. ✅ Send GET request to `/authors/OL1A.json`
2. ✅ Verify HTTP status code is 200
3. ✅ Assert `personal_name` field value
4. ✅ Assert `alternate_names` array contains specific value

**Total Assertions**: All passing

---

## 🔧 Configuration Files

### Behave Configuration (`ui-automation/behave.ini`)

```ini
[behave]
stdout_capture = false
stderr_capture = false
```

Disables output capture so you see test execution in real-time.

### Maven Configuration (`api-automation/pom.xml`)

Key properties:
- Java compiler source/target: **21**
- RestAssured version: **5.4.0**
- Cucumber version: **7.15.0**

---

## 📈 CI/CD Pipeline (GitHub Actions)

### Workflow File: `.github/workflows/automation-pipeline.yml`

**Triggers**: 
- On every push to `main` branch
- On every pull request to `main` branch

**Jobs** (run in parallel):

1. **API Automation Job**
   - Runs on: `ubuntu-latest`
   - Sets up: Java 21
   - Executes: `mvn test`
   - Generates: Cucumber HTML/JSON reports
   - Uploads: Test artifacts

2. **UI Automation Job**
   - Runs on: `ubuntu-latest`
   - Sets up: Python 3.13 + Chrome
   - Executes: `behave --no-capture`
   - Generates: Test reports
   - Uploads: Test artifacts

### Accessing CI/CD Reports

1. Push code to GitHub:
   ```bash
   git add .
   git commit -m "Your commit message"
   git push origin main
   ```

2. Go to: `https://github.com/YOUR_USERNAME/revenue-automation-framework/actions`

3. Click the latest workflow run

4. Scroll down to **Artifacts** section

5. Download:
   - `api-cucumber-report` → Extract and open `report.html`
   - `ui-behave-report` → Contains test logs

---

## 🐛 Troubleshooting

### Chrome/ChromeDriver Issues

**Problem**: `SessionNotCreatedException: Chrome instance exited`

**Solution**: 
- Selenium 4.6+ has built-in Selenium Manager
- It automatically downloads the correct ChromeDriver
- No manual installation needed
- Ensure Chrome browser is installed

```bash
# Verify Chrome is installed
which google-chrome  # Linux
which "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"  # Mac
```

### Python Module Not Found

**Problem**: `ModuleNotFoundError: No module named 'selenium'`

**Solution**:
```bash
cd ui-automation
pip install -r requirements.txt --upgrade
```

### Maven Build Fails

**Problem**: Dependency resolution errors

**Solution**:
```bash
cd api-automation
mvn clean install -U  # -U forces dependency updates
mvn test
```

### Tests Won't Run

**Problem**: `behave: command not found`

**Solution**:
```bash
cd ui-automation
pip install -r requirements.txt
which behave  # Verify installation
```

---

## 📝 GitHub Repository Access

### For Interview Panel Members

The repository is **PUBLIC** — no credentials required.

**Clone and run locally:**
```bash
git clone https://github.com/YOUR_USERNAME/revenue-automation-framework.git
cd revenue-automation-framework

# Setup (see Installation & Setup section above)
# Run tests
# View results
```

**View CI/CD pipeline:**
- Go to: `https://github.com/YOUR_USERNAME/revenue-automation-framework/actions`
- See all automated test runs
- Download test reports/artifacts

---

## ✅ Project Status

| Component | Status | Details |
|-----------|--------|---------|
| **UI Tests** | ✅ Working | 16/16 steps passing |
| **API Tests** | ✅ Working | All assertions passing |
| **Python Setup** | ✅ Working | Selenium + Behave configured |
| **Java Setup** | ✅ Working | Maven + Cucumber configured |
| **Local Execution** | ✅ Working | Tests run on developer machines |
| **CI/CD Pipeline** | ✅ Working | GitHub Actions configured |
| **Test Reports** | ✅ Working | Cucumber HTML + console output |

---

## 🎯 Quick Start Checklist

- [ ] Install Java 21+, Python 3.13+, Maven 3.8+
- [ ] Clone repository
- [ ] `cd ui-automation && pip install -r requirements.txt`
- [ ] `cd api-automation && mvn clean install`
- [ ] Run UI tests: `cd ui-automation && behave --no-capture`
- [ ] Run API tests: `cd api-automation && mvn test`
- [ ] Push to GitHub to trigger automated CI/CD
- [ ] View results at GitHub Actions tab

---

## 📚 Documentation Files

- **README.md** (this file) — Project overview & setup
- **.github/workflows/automation-pipeline.yml** — CI/CD configuration
- **features/*.feature** — BDD test scenarios
- **src/test/java/steps/*.java** — API step implementations
- **features/steps/*.py** — UI step implementations

---

**Framework Version**: 1.0  
**Last Updated**: April 2026  