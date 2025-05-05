# MyErgoApp

MyErgoApp is an ergonomic helper application designed to provide periodic tips to improve your posture and overall well-being while working.

## Features
- Displays ergonomic tips with images.
- Runs in the background and shows pop-ups at regular intervals.
- Customizable pop-up interval.

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- `pip` (Python package manager)

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/UmairBaig8/MyErgoApp.git
   cd MyErgoApp
   ```

2. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On macOS/Linux
   venv\Scripts\activate   # On Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   python main.py
   ```

## Usage
- The application runs in the background and periodically shows ergonomic tips.
- You can dismiss the pop-up by clicking the "Got it!" button.

## Testing
To run the unit tests:
```bash
python -m unittest discover tests
```

## Docker
To build and run the application using Docker:
1. Build the Docker image:
   ```bash
   docker build -t myergoapp .
   ```

2. Run the Docker container:
   ```bash
   docker run -it myergoapp
   ```

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request.

## License
This project is licensed under the MIT License.