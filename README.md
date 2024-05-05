

# Running Flask Application with MongoDB for Auth

This guide outlines the steps required to run the Flask application that uses MongoDB as the database. Follow these instructions to set up and run the application locally.

## Prerequisites

- Python 3 installed on your system
- MongoDB installed and running
- Git installed

## Installation

1. Clone the repository (if you haven't already):

   ```bash
   git clone https://github.com/hari3694/auth-flask-app.git
   ```

2. Navigate to the project directory:

   ```bash
   cd auth-flask-app
   ```

3. Install Python dependencies using pip in a virtualenvironment:

   ```bash
   python3 -m venv myenv
   
   windows:
   myenv\Scripts\activate 
   Unix/MacOS:
   source myenv/bin/activate

   pip install -r requirements.txt
   ```

## MongoDB Setup

1. Ensure MongoDB is installed and running on your system.

2. Create a new MongoDB database and collection for the application.

3. Import data into the MongoDB collection for the given customerdata dump

## Configuration

1. Add the following variables to the `.env` file:

   ```dotenv
   MONGO_URI= Monngodb URI
   AUTH_DB= Database containing the customer data
   AUTH_COLLECTION = Collection containing the customer data
   SECRET_KEY=  Create a secret key for JWT token generation
   
   ```

## Running the Application

1. Make sure MongoDB is running.

2. Run the Flask application:

   ```bash
   python main.py
   ```

3. Open a web browser and navigate to `http://localhost:5000` to access the application.

## Usage

- Use the application according to its functionality. Ensure that MongoDB is accessible and properly configured to interact with the application.

## Contributing

- Contributions are welcome! If you find any issues or have suggestions for improvements, please create an issue or submit a pull request.

## License

- [MIT License](LICENSE)
