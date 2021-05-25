import sqlite3

# get me all details for this particular project(Projet Name ,Total plots, sold_plots, TotalArea, AreaSold)
# apply seraching for a particular plot no
# apply filters for soldplot and unsold plot, plot whose balance is 0, plot whose balance is not 0, plot whose due dates have been exceeded (red color)
# record file banani padegi  Project(plotNo, rate, area, Amount , sold, Balance, customer, rebate, interest_of_first_payment, dealer, commission)  
# Click on this plotNO to find Due Dates and Payments corresponding to this plot
# For a particular project, we have to create a CSV file of all the details, and for the plots, we have to make CSV file for "Dues" and CSV file for "Payments"


# Entering Data --------------------------------
# Creating New Project --------------------------------
# Ek Project m plots daalenge
# Plot sale hoga to uski saari details daalenge, uske corressponding saari due dates daalenge, 
# jab plot dikh raha hoga, vahi pr Edit krne ka option dedenge like Edit Plot info, Edit Deal Info... Edit Deal Info m Due Dates ko bhi edit krne ka option hoga
# Last m aayega payment ka option, plot select krna hoga, make payment pr click krna hoga, payment amount, payment interest or date daalni hogi, make payment pr click krna hoga



# To find Balance from plotNo
# from plotno get plotid and amount = rate*area
# using that plotid in Deals table, get rebate and commission  and dealid
# using that dealid get amount_paid for the deal and add them all
# Balance = amount - (sum(amount_paid) - rebate - commission)

conn = sqlite3.connect("first_try.db")
cursor = conn.cursor()

def findBalance(plot_no): # finding Balance of a Plot No., Balance may not exist incase it is note sold
    cursor.execute("select id,rate*area as amount from Plot where plot_no = ?",(plot_no,))
    (plot_id, plot_price) = cursor.fetchone() 
    cursor.execute("select id,rebate,commission from Deals where plotid = ?",(plot_id,)) 
    data = cursor.fetchone()
    print(data)
findBalance(1)

conn.commit()
conn.close()