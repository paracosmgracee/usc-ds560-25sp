from mysql_helper import create_connection, commit_and_close
import initialize_helper as helper

def user_create():
    input_name = input("Enter your username: ")
    
    if helper.validate_user(input_name):
        print("User already exists")
        return
    
    input_password = input("Create new password: ")
    
    
    helper.create_user(input_name, input_password)
    
def user_login():
    input_name = input("Enter your username: ")
    
    if not helper.validate_user(input_name):
        print("User does not exist")
        return
    
    input_password = input("Enter your password: ")
    
    user = helper.validate_user(input_name, input_password)
    
    if not user:
        print("Invalid password")
        return
    
    print("Logged in successfully")
    return user

def portfolio_create(user_id):
    input_name = input("Enter portfolio name: ")
    
    if helper.validate_portfolio(user_id, input_name):
        print("Portfolio already exists")
        return
    
    helper.create_portfolio(user_id, input_name)
    
def porfolio_select(user_id):
    portfolios = helper.list_portfolios(user_id)
    
    if not portfolios:
        print("Create a portfolio first")
        return None
    
    print("Select a portfolio")
    
    for i, portfolio in enumerate(portfolios):
        print(f"{i+1}. {portfolio[2]}")
        
    choice = input("Enter your choice: ")
    
    return portfolios[int(choice) - 1]

def stock_add(portfolio_id):
    ticker = input("Enter ticker name: ")
    valid = helper.check_ticker(ticker)
    
    if not valid:
        return None
    
    helper.add_ticker(ticker, portfolio_id)
    
    return True

def stock_delete(portfolio_id,stock_list):
    input_id = int(input("Enter stock number to delete: "))
    
    stock_id = stock_list[input_id-1][1]
    helper.delete_ticker_from_portfolio(portfolio_id,stock_id)
    
    return True


    
    

if __name__ == "__main__":
    # create_and_insert()
    helper.initialize_database()
    
    logged_in_user = None
    selected_portfolio = None
    
    while True:
        print("\n\n")
        
        if selected_portfolio and logged_in_user:
            
            stocks_list = helper.list_stocks(logged_in_user[0], selected_portfolio[0])
            if not stocks_list:
                print("No stocks in portfolio "+ selected_portfolio[2])
                
            print("Stocks in Portfolio " + selected_portfolio[2])
            for i, stocks in enumerate(stocks_list):
                print(f"{i+1}. {stocks_list[i][3]}")
                
            print("\n\n Operations")
            
            
            print("1. Add Stock")
            print("2. Delete Stocks")
            print("3. Go to previous menu")
            
            choice = input("Enter your choice: ")
            
            if choice == "1":
                if stock_add(selected_portfolio[0]):
                    continue
            elif choice == "2":
                if stock_delete(selected_portfolio[0],stocks_list):
                    continue
            elif choice == "3":
                selected_portfolio = None
                continue
            else:
                print("Invalid choice")
                continue
        
        if logged_in_user:
            print("1. Create Portfolio")
            print("2. Select Existing Portfolio")
            print("3. Logout")
            
            choice = input("Enter your choice: ")
            
            if choice == "1":
                portfolio_create(logged_in_user[0])
                continue
            elif choice == "2":
                selected_portfolio = porfolio_select(logged_in_user[0])
                continue
                if selected_portfolio == None:
                    continue
            elif choice == "3":
                logged_in_user = None
                continue
            else:
                print("Invalid choice")
                continue
            
            
            
        else:
            print("1. Create User")
            print("2. Login")
            print("3. Exit")
            
            choice = input("Enter your choice: ")
            
            if choice == "1":
                user_create()
            elif choice == "2":
                logged_in_user = user_login()
            elif choice == "3":
                break
            else:
                print("Invalid choice")
        
            
    