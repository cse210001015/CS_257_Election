# Election Management System

The Election Management System is a web-based application built using Flask, a Python web framework. It provides functionality for administrators to manage elections, candidates, and users, as well as allows users to vote in eligible elections.

## Features

- *Administrator Functionality:*
  - Login: Administrators can log in using their username and password.
  - Create Elections: Administrators can create new elections by providing the description, start time, end time, department, rank, and year.
  - Enter Candidates: Administrators can enter candidates for a specific election by providing the election ID, candidate name, and description.
  - View Ongoing Elections: Administrators can view all ongoing elections, including their details and candidates.
  - View Completed Elections: Administrators can view the history of completed elections, including the winner.
  - Remove User: Administrators can remove a user from the system by specifying their username.
  - Logout: Administrators can log out of the system.

- *User Functionality:*
  - Login: Users can log in using their username and password.
  - View Eligible Elections: Users can view a list of eligible elections based on their department, year, and rank.
  - Vote: Users can vote in eligible elections by selecting the election ID and candidate ID.
  - View Completed Elections: Users can view the history of completed elections, including the winner.
  - Change Password: Users can change their password.
  - Logout: Users can log out of the system.

## Installation

1. Clone the repository: `git clone https://github.com/cse210001015/CS_257_Election`
2. Install the required dependencies: `pip install -r requirements.txt`
3. Set up the MySQL database with the necessary tables and configurations.
4. Update the database connection details in the code (`app.py`) to match your MySQL database.
5. Run the application: `python app.py`
6. Access the application in your web browser at `http://localhost:5000`

## Dependencies

- Flask: A micro web framework for Python.
- MySQL Connector: A Python driver for connecting to MySQL databases.
- pandas: A data manipulation and analysis library.

## Database Schema

The application uses a MySQL database with the following tables:

- `AdminLogin`: Stores the administrator login details.
- `AdminLoggedIn`: Stores the IP addresses of logged-in administrators.
- `UserInfo`: Stores user information, including their ID, name, date of birth, address, phone number, department, year, and rank.
- `UserLogin`: Stores user login details.
- `UserLoggedIn`: Stores the IP addresses of logged-in users.
- `elections_current`: Stores information about ongoing elections, including the election ID, description, start time, end time, department, year, and rank.
- `elections_history`: Stores information about completed elections, including the election ID, description, winner, start time, end time, department, year, and rank.
- `candidates`: Stores information about candidates, including the candidate ID, election ID, name, and description.
- `votes`: Stores information about votes, including the election ID, user ID, and candidate ID.

## Contributing

Contributions to the Election Management System are welcome! If you find any bugs or want to add new features, please submit an issue or a pull request.

## License

The Election Management System is open source software licensed under the [MIT license](https://opensource.org/licenses/MIT). Feel free to use, modify, and distribute the code for your own purposes.
