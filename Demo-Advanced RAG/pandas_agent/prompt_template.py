# from langchain import PromptTemplate
from langchain_core.prompts import PromptTemplate


header_for_query = """ You are a data analyst prespective and answer the above question.
Whose job is to answer user query 
User Query:""" 
footer_query = """
You won't ask from me any question as an expert you will take all the decision involved by your own and present me with the final answer to the user.
Note this is important that you use your intelligence very wisely dont ask any question from me and present me with the final answer.
The location of excel file from where you have to answer the query is present in file located in current folder with name 'data.xlsx' 

You have already used the tool python_code_executor 2 twice here is the code by you and respective outputs
1st call code: 
    import pandas as pd

    # Load the data from the provided Excel file
    file_path = 'data.xlsx'

    # Load the Excel file to inspect its contents
    xls = pd.ExcelFile(file_path)
    print(xls.sheet_names)
Note instead of writing xls.sheet_names you wrote print(xls.sheet_names) as the you are only able to look at the output of print statements
1st call output:
['Sheet1']
Looking at the output you made a 2nd call to tool using the following code 
2nd call code 
    sales_df = pd.read_excel(xls, 'Sheet1')

    # Display the first few rows of each sheet to understand their structure
    print({
        'sales': products_df.head()
    })
Note again you used print statement to look at the output
2nd call output 
    {'products': shortname  company_id transaction_type  payment_id  \
0  keywestsebago        2473           refund    13461722   
1  keywestsebago        2473           refund    13461776   
2  keywestsebago        2473           refund    13461815   
3  keywestsebago        2473           refund    13462349   
4  keywestsebago        2473           refund    13462761   

                   created_at  booking_id payment_type is_refunded  \
0  2024-03-20 01:53:59.360785   203665913    affiliate           t   
1  2024-03-20 02:24:47.258515   214364854    affiliate           t   
2  2024-03-20 02:36:17.929397   214902773    affiliate           t   
3  2024-03-20 06:16:05.987796   214905272    affiliate           t   
4  2024-03-20 08:09:44.930758   212427293    affiliate           t   

   original_booking_id  payment_gross  payment_proc_fee  payout_id card_type  \
0            203665913        -119.90               0.0        NaN       NaN   
1            214364854        -119.90               0.0        NaN       NaN   
2            214902773        -119.90               0.0        NaN       NaN   
3            214905272         -79.95               0.0        NaN       NaN   
4            212427293        -159.90               0.0        NaN       NaN   

  postal_code in_store_payment_type   ledger        user user_dashboard  \
0         NaN                   NaN  Default  Viator-API         viator   
1         NaN                   NaN  Default  Viator-API         viator   
2         NaN                   NaN  Default  Viator-API         viator   
3         NaN                   NaN  Default  Viator-API         viator   
4         NaN                   NaN  Default  Viator-API         viator   

  payout_date payout_status  
0         NaN           NaN  
1         NaN           NaN  
2         NaN           NaN  
3         NaN           NaN  
4         NaN           NaN  


Columns Unique values: These are the unique values of categorical columns
shortname: ['keywestsebago', 'cruzbaywatersports', 'lovangoresortstjohn',
       'ritzcarlton-tcwatersports', 'aliinuimaui', 'divewailea',
       'appledorekeywest', 'redhospitalitytransportationinc']
transaction_type: ['refund', 'payment']
payment_type: ['affiliate', 'balanced-cc', 'in-store', 'stored-value-card']
is_refunded: ['t', 'f']
card_type: ['applepay', 'visa', 'american express', 'mastercard', 'googlepay',
       'discover', 'diners club', 'jcb']
in_store_payment_type: ["Westin Frenchman's Reef - Room Charge", 'Room Charge',
       'westin room charge', 'Room Charge - Wymara', 'Clover (On Boat)',
       'Room Charge - Ritz Carlton', 'Dive Wailea / Maka / Nui Transfer',
       'Hotel - Ritz Room Charge',
       "Buoy Haus Frenchman's Reef - Room Charge",
       'Collected by Outside Boat Vendor', 'Club - Ritz Room Charge',
       'Wire', 'Cash', 'Seven Stars Voucher', 'Hyatt Beyond',
       'Credit Card', 'Hotel Master Bill - Ritz-Carlton, St. Thomas',
       'AL Pro', 'Check', 'Clover (Tips)', 'USVI Travel Voucher',
       'RDP Room Charge/Prepaid', 'Sebago Dashboard',
       'Reservation Transfer', 'Sebago Sales', 'Hotel Bike Voucher',
       'Wire Transfer', 'Sand Dollars', 'cash',
       'Hyatt Confirmation Calls', 'Direct Bill - Paid by RED',
       "Hotel Master Bill - Frenchman's Reef",
       'Room Charge - Grace Bay Club',
       'Hotel Master Bill - Westin, St. John', 'Collected by CLC',
       'Gift Card Refund', 'Open Table', 'Hotel Master Bill',
       'Sea Dream Invoice', 'check', 'Gift Card',
       'Hyatt Gift Certificate', 'westin recreation certificate',
       'Resort Pass', 'Voucher', 'dispute', 'Bill to Ottomatic Marine',
       'Prepaid RDP Cabana']
ledger: ['Default', 'Cruz Bay Watersports', 'Alii Nui Charters',
       'Transportation', 'Maui Dive Shop', 'Nani']
payout_date: date format- ['2024-02-27', '2024-02-20', '2024-03-12',.......]
payout_status: ['succeeded', 'pending']

From here you have proper understanding of excel file and data, next proceed with python_code_executor tool provided to you and find the answer to the user query.
Note you are smart you will take all decision by your own and return the user with potential answer. Also current date is 29 March 2025.
"""


final_response_template = PromptTemplate(
    input_variables= ["query", "bot_response"],
    template ="""
I am proving you with user query and the output from the bot.
Act as you are a BOT in Harbor company which is designed to answer query from given excel file
User Query: 
{query}
Bot Response : 
{bot_response}

Generate only the final response that needs to be presented to the user nothing else. 
What ever you will generate now will be shown to the user so make sure you generate only the text that is shown to the user
Use HTML in text wherever necessary.
""")