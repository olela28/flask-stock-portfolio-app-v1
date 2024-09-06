# Flask Stock Portfolio Web Application
## Project Overview
This Flask web application allows users to manage a stock portfolio by buying and selling shares. It integrates a user-friendly frontend with dynamic JavaScript features and a backend that handles authentication, data persistence, and real-time stock price lookups. The key functionalities include:

- **Buy and Sell Stocks**
- **Track Portfolio Value**
- **Display Cash and Stock Holdings**

  
## Features
- User Authentication: Secure login system with user-specific session management.
- Stock Lookup: Retrieves real-time stock prices using a third-party API.
- Portfolio Management: Tracks and displays the user’s holdings and allows them to sell stocks with a restricted number of shares.
- Dynamic Forms: Uses JavaScript to display options based on available stocks for sale.
- Responsive UI: Uses Bootstrap for a clean, responsive design.
  
## Technologies Used
- Backend: Flask (Python)
- Frontend: HTML, CSS, Bootstrap, JavaScript
- Database: SQLite for storing user data and transactions
- Stock Price Lookup API: (Yahoo Finance)
  
## Getting Started
### Prerequisites
1. Python 3.x
2. Flask
3. SQLite
4. Bootstrap

## Installation
1. Clone the repository
   
   ```
   git clone https://github.com/your-repo-name/flask-portfolio-app.git

   cd stock-portfolio-app
   ```

2. Install dependencies

   ``
   pip install -r requirements.txt
   ``

4. Setup the database

flask db init
flask db migrate
flask db upgrade

4. Run the application

``
flask run
``

5. Access the application

http://127.0.0.1:5000/

### Environment Variables
Create a .env file in the root directory of the project with the following environment variables:

FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your-secret-key
API_KEY=your-stock-api-key

## Usage
### Sign Up and Log In
- Navigate to the sign-up page to create a new account.
- Log in using your credentials.
### Buying and Selling Stocks
Use the Buy form to purchase stocks by entering the stock symbol and number of shares.
Use the Sell form to sell stocks, with the ability to select the number of shares based on your holdings.
### Portfolio Overview
On the home page, the portfolio displays your current cash, stocks, and the total value of your holdings.
## File Structure
.
├── app.py                   # Main Flask application
├── templates/
│   ├── layout.html          # Base layout template
│   ├── index.html           # Home page showing portfolio
│   ├── buy.html             # Buy stocks page
│   └── sell.html            # Sell stocks page
├── static/
│   ├── style.css            # Custom styles
├── models.py                # Database models
├── requirements.txt         # Dependencies
└── README.md                # Project documentation
## Key Routes
````
/login: Log in to the application
/register: Sign up for a new account
/buy: Buy stocks
/sell: Sell stocks
/quote: Lookup current stock prices
/history: View transaction history
````
## Future Enhancements
Transaction History Filter: Allow filtering based on time periods.
Stock Search Autocomplete: Improve stock symbol input with suggestions.
## Contributing
Contributions are welcome! Please fork this repository and create a pull request.
