# Get Started

## Installation
1. Clone the repository `git clone https://github.com/ahemmatifar/sox.git`
2. Change to project directory and install the project
   ```bash
   cd sox
   make dev_install
   ```
   Alternatively, you can install without `make`
   ```bash
   cd sox
   python -m pip install --upgrade pip
   pip install -e .[dev]
   ```

## Testing
To run the tests, change to project directory and run `make test`

## Documentation
This project uses Sphinx for documentation. To build the documentation locally, change to docs directory (`cd docs`)
and run `make html`.