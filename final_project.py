from tkinter import * 
from tkinter import messagebox, Menu
import requests
import json
import sqlite3

pycrypto = Tk() #creating and instance with Tk class
pycrypto.title("My Crypto Portfolio")
pycrypto.iconbitmap("favicon.ico") #icon bitmap method 

con = sqlite3.connect('coin.db')
cursorObj = con.cursor()

cursorObj.execute("CREATE TABLE IF NOT EXISTS coin(id INTEGER PRIMARY KEY, symbol TEXT, amount INTEGER, price REAL)")
con.commit()

#cursorObj.execute("DELETE FROM coin WHERE id>5")
#con.commit() #//dummy data
def reset():
    for cell in pycrypto.winfo_children():
        cell.destroy()
    app_nav()
    app_header()
    my_portfolio()   

def app_nav():
    def clear_all():
        cursorObj.execute("DELETE FROM coin")
        con.commit() 
        messagebox.showinfo("Portfolio Notification", "Portfolio Cleared - Add New Coins")
        reset()

    def close_app():
        pycrypto.destroy()    

    menu = Menu(pycrypto)
    file_item = Menu(menu)
    file_item.add_command(label='Clear Portfolio', command=clear_all )
    file_item.add_command(label='Close App', command=close_app )
    menu.add_cascade(label="File", menu=file_item)
    pycrypto.config(menu=menu)



def my_portfolio(): 
    api_request = requests.get("https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?start=1&limit=10&convert=USD&CMC_PRO_API_KEY=8092d883-9a5b-4ef6-886c-b9c10dba5bca")
    # api_request is a variable that stores api link ka data
    api = json.loads(api_request.content) # helps to deliver the content of api_request

    cursorObj.execute("SELECT *  FROM coin")
    coins = cursorObj.fetchall()

    def font_color(amount): #if value = +ve return font_color as green,if value = -ve return font_color as red
        if amount >= 0:
            return "dark green"
        else:
            return "red4" 
    def insert_coin():
        cursorObj.execute("INSERT INTO coin(symbol, price, amount) VALUES(?, ?, ?)", (symbol_txt.get(), price_txt.get(),amount_txt.get()))
        con.commit()
        messagebox.showinfo("Portfolio Notification", "Coin Added To Portfolio Sucessfully!")
        reset()    

    def update_coin():
        cursorObj.execute("UPDATE coin SET symbol=?, price=?, amount=? WHERE id=?", (symbol_update.get(), price_update.get(), amount_update.get(), portfolioid_update.get()))  
        con.commit() 
        messagebox.showinfo("Portfolio Notification", "Coin Updated Sucessfully!")
        reset() 

    def delete_coin():
        cursorObj.execute("DELETE FROM coin WHERE id=?", (portfolioid_delete.get(), ))
        con.commit()  
        messagebox.showinfo("Portfolio Notification", "Coin Deleted From Portfolio")
        reset()     

    total_current_value = 0
    total_pl = 0
    coin_row = 1 #bcs 0th row is heading
    total_amount_paid = 0

    for i in range(0,10):
        for coin in coins:
            if api["data"][i]["symbol"] == coin[1]:
                total_paid = coin[2] * coin[3] 
                current_value = api["data"][i]["quote"]["USD"]["price"] * coin[2]
                pl_percoin =  api["data"][i]["quote"]["USD"]["price"] - coin[3]
                total_pl_coin = pl_percoin * coin[2]
                total_pl = total_pl + total_pl_coin #total_pl += total_pl_coin
                total_current_value = total_current_value + current_value #total_current_value += current_value
                total_amount_paid = total_amount_paid + total_paid #total_amount_paid += total_paid
                

                #print(api["data"][i]["name"] + " _ " + api["data"][i]["symbol"])
                #print("Price per coin - ${0:.2f}".format(api["data"][i]["quote"]["USD"]["price"]))
                #print("Number Of Coin:", coin[2])
                #print("Total Amount Paid", "${0:.2f}".format(total_paid))
                #print("Current value of Coin","${0:.2f}".format(current_value))
                #print("Profit/Loss per Coin", "${0:.2f}".format(pl_percoin))
                #print("Total Profit/Loss With Coin","${0:.2f}".format(total_pl_coin))
                #print("--------------") 
                portfolio_id = Label(pycrypto, text=coin[0] ,bg="#FFD8C5", fg="#00154F", font="Lato 12", borderwidth=2, relief="groove", padx="2", pady="2")
                portfolio_id.grid(row=coin_row, column=0, sticky=N+S+E+W)

                name = Label(pycrypto, text=api["data"][i]["symbol"], bg="#D4F4EC", fg="#00154F", font="Lato 12", borderwidth=2, relief="groove", padx="2", pady="2" )
                name.grid(row=coin_row, column=1, sticky=N+S+E+W)

                price_per_coin = Label(pycrypto, text="${0:.2f}".format(api["data"][i]["quote"]["USD"]["price"]),bg="#FFD8C5", fg="#00154F", font="Lato 12", borderwidth=2, relief="groove", padx="2", pady="2")
                price_per_coin.grid(row=coin_row, column=2, sticky=N+S+E+W)

                no_of_coins_owned = Label(pycrypto, text=coin[2], bg="#D4F4EC", fg="#00154F", font="Lato 12", borderwidth=2, relief="groove", padx="2", pady="2" )
                no_of_coins_owned .grid(row=coin_row, column=3, sticky=N+S+E+W)

                amount_paid = Label(pycrypto, text="${0:.2f}".format(total_paid),bg="#FFD8C5", fg="#00154F", font="Lato 12", borderwidth=2, relief="groove", padx="2", pady="2")
                amount_paid.grid(row=coin_row, column=4, sticky=N+S+E+W)

                current_value = Label(pycrypto, text="${0:.2f}".format(current_value),  bg="#D4F4EC", fg="#00154F", font="Lato 12", borderwidth=2, relief="groove", padx="2", pady="2")
                current_value.grid(row=coin_row, column=5, sticky=N+S+E+W)

                pl_coin = Label(pycrypto, text="${0:.2f}".format(pl_percoin),bg="#FFD8C5", fg=font_color(float("{0:.2f}".format(pl_percoin))), font="Lato 12", borderwidth=2, relief="groove", padx="2", pady="2")
                pl_coin.grid(row=coin_row, column=6, sticky=N+S+E+W)

                total_pl_coin = Label(pycrypto, text="${0:.2f}".format(total_pl_coin), bg="#D4F4EC", fg=font_color(float("{0:.2f}".format(total_pl_coin ))), font="Lato 12", borderwidth=2, relief="groove", padx="2", pady="2")
                total_pl_coin.grid(row=coin_row, column=7, sticky=N+S+E+W)
                
                coin_row += 1
    #Insert data symbol, price, coins owned
    symbol_txt = Entry(pycrypto, border=2, relief="groove")
    symbol_txt.grid(row=coin_row+1, column=1)
    
    price_txt = Entry(pycrypto, border=2, relief="groove")
    price_txt.grid(row=coin_row+1, column=2)
     
    amount_txt = Entry(pycrypto, border=2, relief="groove")
    amount_txt.grid(row=coin_row+1, column=3) 

    add_coin = Button(pycrypto, text="Add Coin", bg="#00154F", fg="#F4AF1B",command=insert_coin, font="mincho 13 ", borderwidth=2, relief="groove", padx="2", pady="2")
    add_coin.grid(row=coin_row + 1, column=4, sticky=N+S+E+W) # insert_coin coints sql query

    #update coin
    portfolioid_update = Entry(pycrypto, border=2, relief="groove")
    portfolioid_update.grid(row=coin_row+2, column=0)

    symbol_update = Entry(pycrypto, border=2, relief="groove")
    symbol_update.grid(row=coin_row+2, column=1)
    
    price_update = Entry(pycrypto, border=2, relief="groove")
    price_update.grid(row=coin_row+2, column=2)
     
    amount_update = Entry(pycrypto, border=2, relief="groove")
    amount_update.grid(row=coin_row+2, column=3) 

    update_coin_txt = Button(pycrypto, text="Update Coin", bg="#00154F", fg="#F4AF1B",command=update_coin, font="mincho 13 ", borderwidth=2, relief="groove", padx="2", pady="2")
    update_coin_txt.grid(row=coin_row + 2, column=4, sticky=N+S+E+W) 

    #delete coin
    portfolioid_delete= Entry(pycrypto, border=2, relief="groove")
    portfolioid_delete.grid(row=coin_row+3, column=0) 

    delete_coin_txt = Button(pycrypto, text="Delete Coin", bg="#00154F", fg="#F4AF1B",command=delete_coin, font="mincho 13 ", borderwidth=2, relief="groove", padx="2", pady="2")
    delete_coin_txt.grid(row=coin_row + 3, column=4, sticky=N+S+E+W) 




    total_amount_paid= Label(pycrypto, text="${0:.2f}".format(total_amount_paid),bg="#FFD8C5", fg="#00154F" , font="Lato 12 bold", borderwidth=2, relief="groove", padx="2", pady="2")
    total_amount_paid.grid(row=coin_row, column=4, sticky=N+S+E+W)               

    total_current_value = Label(pycrypto, text="${0:.2f}".format(total_current_value),  bg="#D4F4EC", fg="#00154F", font="Lato 12 bold", borderwidth=2, relief="groove", padx="2", pady="2")
    total_current_value.grid(row=coin_row, column=5, sticky=N+S+E+W)            
                
    total_pl = Label(pycrypto, text="${0:.2f}".format(total_pl), bg="#D4F4EC", fg=font_color(float("{0:.2f}".format(total_pl))), font="Lato 12 bold", borderwidth=2, relief="groove", padx="2", pady="2")
    total_pl.grid(row=coin_row, column=7, sticky=N+S+E+W)

    api = "" #this will delete all the data , on clicking the refresh button the func will call api requets and fill data with latest value
    refresh = Button(pycrypto, text="Refresh", bg="#00154F", fg="#F4AF1B",command=reset, font="mincho 13 ", borderwidth=2, relief="groove", padx="2", pady="2")
    refresh.grid(row=coin_row + 1, column=7, sticky=N+S+E+W)
    
                
def app_header():
    portfolio_id = Label(pycrypto, text="Portfolio ID", bg="#00154F", fg="#F4AF1B" , font="mincho 13 "  , padx="5", pady="5", borderwidth=2, relief="groove")
    portfolio_id.grid(row=0, column=0, sticky=N+S+E+W)

    name = Label(pycrypto, text="Coin Name", bg="#00154F", fg="#F4AF1B" , font="mincho 13 "  , padx="5", pady="5", borderwidth=2, relief="groove")
    name.grid(row=0, column=1, sticky=N+S+E+W)

    price_per_coin = Label(pycrypto, text="Price",bg="#00154F", fg="#F4AF1B", font="mincho 13 ",padx="5", pady="5", borderwidth=2, relief="groove")
    price_per_coin.grid(row=0, column=2, sticky=N+S+E+W)

    no_of_coins_owned = Label(pycrypto, text="Coin Owned",bg="#00154F", fg="#F4AF1B",font="mincho 13 " ,padx="5", pady="5", borderwidth=2, relief="groove")
    no_of_coins_owned .grid(row=0, column=3, sticky=N+S+E+W)

    amount_paid = Label(pycrypto, text="Total Amount Paid",bg="#00154F", fg="#F4AF1B", font="mincho 13 ",padx="5", pady="5", borderwidth=2, relief="groove")
    amount_paid.grid(row=0, column=4, sticky=N+S+E+W)

    current_value = Label(pycrypto, text="Current Value", bg="#00154F", fg="#F4AF1B", font="mincho 13 ",padx="5", pady="5", borderwidth=2, relief="groove" )
    current_value.grid(row=0, column=5, sticky=N+S+E+W)

    pl_coin = Label(pycrypto, text="P/L Per Coin",bg="#00154F", fg="#F4AF1B", font="mincho 13 ",padx="5", pady="5", borderwidth=2, relief="groove")
    pl_coin.grid(row=0, column=6, sticky=N+S+E+W)

    total_pl_coin = Label(pycrypto, text="Total P/L With Coin",  bg="#00154F", fg="#F4AF1B", font="mincho 13 ",padx="5", pady="5", borderwidth=2, relief="groove")
    total_pl_coin.grid(row=0, column=7, sticky=N+S+E+W)

app_nav()
app_header()
my_portfolio()
pycrypto.mainloop()

cursorObj.close()
con.close()

print("Program Completed")          












   



