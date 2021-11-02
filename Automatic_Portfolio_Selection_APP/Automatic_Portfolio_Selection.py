# A Database CLI Application

# Import modules
import pandas as pd
import sqlalchemy as sql
import os
import alpaca_trade_api as tradeapi
from dotenv import load_dotenv
import questionary

# Load .env file
load_dotenv()

# Set the variables for the Alpaca API and secret keys
alpaca_api_key = os.getenv("ALPACA_API_KEY")
alpaca_secret_key = os.getenv("ALPACA_SECRET_KEY")






# Create a function called `Portfolio_selection` that will select portfolio for investors who are in the different level of risk-averse.
# This function will be called from the `__main__` loop.

def sector_report(risk_averse_level):

    # Print a welcome message for the application
    print("\n......Welcome to the Portflio Selection APP.....\n")
    print("The portfolio with be recommended to you based on your risk-aversion level\n")

    # Using questionary, ask the investor what is his/her risk-aversion level
    risk_averse_coefficient = questionary.select("Which sector do you wish to report on?", choices=risk_averse_level).ask()

    print("Running report ...")


    # Create a statement that displays the `results` of your sector_yearly_return calculation.
    # On a separate line (\n) ask the use if they would like to continue running the report.
    results = f"The cumulative return for the {sector} sector for the past year is {sector_yearly_rtn * 100}%.\nWould you like to choose another sector to analyze?"

    # Using the `results` statement created above,
    # prompt the user to run the report again (`y`) or exit the program (`n`).
    continue_running = questionary.select(results, choices=['y', 'n']).ask()

    # Return the `continue_running` variable from the `sector_report` function
    return continue_running


# The `__main__` loop of the application.
# It is the entry point for the program.
if __name__ == "__main__":

    # Database connection string to the clean NYSE database
    database_connection_string = 'sqlite:///../Resources/nyse.db'

    # Create an engine to interact with the database
    engine = sql.create_engine(database_connection_string)

    # Read the NYSE table into a dataframe called `nyse_df`
    nyse_df = pd.read_sql_table('NYSE', engine)

    # Get a list of the sector names from the `nyse_df` DataFrame
    # Be sure to drop n/a values and capture only unique values.
    # You will use this list of `sector` names for the user options in the report.
    sectors = nyse_df['Sector']
    sectors = sectors.dropna()
    sectors = sectors.unique()

    # Create a variable named running and set it to True
    running = True

    # While running is `True` call the `sector_report` function.
    # Pass the `nyse_df` DataFrame `sectors` and the database `engine` as parameters.
    while running:
        continue_running = sector_report(sectors, engine)
        if continue_running == 'y':
            running = True
        else:
            running = False
