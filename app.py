from datetime import datetime
from flask import Flask, render_template, request, Markup, url_for, session
from flask_mysqldb import MySQL
from werkzeug.utils import redirect

app = Flask(__name__)

app.secret_key = 'agroMetrics'
app.config['MYSQL_HOST'] = 'aws-sql.cdxdm2xen7r2.ap-south-1.rds.amazonaws.com'
app.config['MYSQL_USER'] = 'admin'
app.config['MYSQL_PASSWORD'] = 'SVerma08554'
app.config['MYSQL_DB'] = 'dbms_project'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)


@app.route('/', methods=['GET', 'POST'])
def start():
    if request.method == 'GET':
        return render_template('start.html')
    # return 'Phir kata'


@app.route('/base')
def base():
    return render_template('farmer/base.html')


@app.route('/my_transactions', methods=['GET', 'POST'])
def my_transactions():
    cur = mysql.connection.cursor()
    cur.execute("select Trader_Id from dbms_project.trader")
    traders = list(cur.fetchall())
    traders.insert(0, {'Trader_Id':'All'})
    cur.close()
    bbuyer_Id = None
    if request.method == 'GET':
        cur = mysql.connection.cursor()
        cur.execute(
            "Select Transaction_Id, Crop_Id, buyer_Id, seller_Id, Amount from dbms_project.transaction join dbms_project.trader on trader.Trader_Id = transaction.buyer_Id ")
        result = cur.fetchall()
        columns = [h[0] for h in cur.description]

        cur.close()

    if request.method == 'POST':
        bbuyer_Id = request.form.get('buyer_Id')
        print(bbuyer_Id)
        cur = mysql.connection.cursor()
        if (bbuyer_Id == 'All'):
            cur.execute("Select Transaction_Id, Crop_Id, buyer_Id, seller_Id, Amount from dbms_project.transaction join dbms_project.trader on trader.Trader_Id = transaction.buyer_Id ")
        else:
            cur.execute("Select Transaction_Id, Crop_Id, buyer_Id, seller_Id, Amount from dbms_project.transaction join dbms_project.trader on trader.Trader_Id = transaction.buyer_Id where transaction.buyer_Id = '{}'".format(bbuyer_Id))
        result = cur.fetchall()
        columns = [h[0] for h in cur.description]
        cur.close()

    return render_template('/farmer/my_transactions.html', title='My Transactions', table=result, columns=columns,
                           traders=traders, buyer_Id = bbuyer_Id)


@app.route('/transaction', methods=['GET', 'POST']) # trader transaction
def trader_transactions():
    cur = mysql.connection.cursor()
    cur.execute("select Farmer_Id from dbms_project.farmer")
    farmers = list(cur.fetchall())
    farmers.insert(0, {'Trader_Id':'All'})
    cur.close()
    bbuyer_Id = None
    if request.method == 'GET':
        cur = mysql.connection.cursor()
        cur.execute(
            "Select Transaction_Id, Crop_Id, buyer_Id, seller_Id, Amount from dbms_project.transaction join dbms_project.trader on trader.Trader_Id = transaction.buyer_Id ")
        result = cur.fetchall()
        columns = [h[0] for h in cur.description]

        cur.close()

    if request.method == 'POST':
        bbuyer_Id = request.form.get('buyer_Id')
        print(bbuyer_Id)
        cur = mysql.connection.cursor()
        if (bbuyer_Id == 'All'):
            cur.execute("Select Transaction_Id, Crop_Id, buyer_Id, seller_Id, Amount from dbms_project.transaction join dbms_project.trader on trader.Trader_Id = transaction.buyer_Id ")
        else:
            cur.execute("Select Transaction_Id, Crop_Id, buyer_Id, seller_Id, Amount from dbms_project.transaction join dbms_project.trader on trader.Trader_Id = transaction.buyer_Id where transaction.buyer_Id = '{}'".format(bbuyer_Id))
        result = cur.fetchall()
        columns = [h[0] for h in cur.description]
        cur.close()

    return render_template('/farmer/my_transactions.html', title='My Transactions', table=result, columns=columns,
                           traders=traders, buyer_Id = bbuyer_Id)

@app.route('/trader_dashboard', methods=['GET', 'POST'])
def trader_dashboard():
    tra1gv = []
    tra1gh = []
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM dbms_project.seller")
    result = cur.fetchall()
    maximum = 0
    for d in result:
        if d['Designation'] == 'F':
            tra1gv.append((round(d['Income'])))
            maximum = max(maximum, (round(d['Income'])))
            tra1gh.append(d['Name'])
            # cur.close()
    # print(Income)
    # print(Name)

    tra2gv = []
    tra2gh = []

    # cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM dbms_project.transaction")
    result1 = cur.fetchall()
    maximum1 = 0
    for d in result1:
        # if (d['Designation'] == 'F'):
        tra2gv.append((round(d['Quantity_Kg'])))
        maximum1 = max(maximum1, (round(d['Quantity_Kg'])))
        tra2gh.append(d['seller_Id'])

    cur.execute("SELECT User_Id, Login, Password, Name, State FROM dbms_project.seller;")
    result1 = cur.fetchall()

    cur.close()

    # print(Income1)
    # print(Name1)
    return render_template('/Trader/dashboard.html', title='Only Farmers Income Chart', max=maximum + 1000,
                           labels=tra1gh, values=tra1gv, title1='Tansaction Chat of Farmer', max1=maximum1 + 4,
                           labels1=tra2gh, values1=tra2gv, data=result1)


@app.route('/farmer_dashboard', methods=['GET', 'POST'])
def farmer_dashboard():
    far1gv = []
    far1gh = []
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM dbms_project.seller")
    result = cur.fetchall()
    maximum = 0
    for d in result:
        if d['Designation'] == 'F':
            far1gv.append((round(d['Income'])))
            maximum = max(maximum, (round(d['Income'])))
            far1gh.append(d['Name'])

    far2gv = []
    far2gh = []
    cur.execute("SELECT * FROM dbms_project.transaction")
    result1 = cur.fetchall()
    maximum1 = 0
    for d in result1:
        # if (d['Designation'] == 'F'):
        far2gv.append((round(d['Quantity_Kg'])))
        maximum1 = max(maximum1, (round(d['Quantity_Kg'])))
        far2gh.append(d['seller_Id'])

    cur.execute("SELECT User_Id, Login, Password, Name, State FROM dbms_project.seller;")
    result1 = cur.fetchall()
    cur.close()
    return render_template('/farmer/dashboard.html', title='Only Farmers Income Chart', max=maximum + 1000,
                           labels=far1gh, values=far1gv, title1='Tansaction Chat of Farmer', max1=maximum1 + 4,
                           labels1=far2gh, values1=far2gv, data=result1)


@app.route('/farmer_storage', methods=['GET', 'POST'])
def farmer_storage():
    user_id = 'u31'  # TODO: here assigning a fake farmer ID
    cursor = mysql.connection.cursor()
    farmer_storage_in_mandi_board = f"SELECT dbms_project.storage_mandi_board_rent.Storage_Id,Name,Email_Address,Charges,timeFrom,timeTo FROM dbms_project.storage_mandi_board_rent\
                    INNER JOIN dbms_project.mandi_board ON dbms_project.mandi_board.Mandi_Board_Id=dbms_project.storage_mandi_board_rent.Mandi_Board_Id \
                    INNER JOIN dbms_project.storage_mandi_board ON dbms_project.storage_mandi_board.Mandi_Board_Id=dbms_project.storage_mandi_board_rent.Mandi_Board_Id AND dbms_project.storage_mandi_board.Storage_Id=dbms_project.storage_mandi_board_rent.Storage_Id \
                    WHERE Renter_Person_Id='{user_id}' "
    all_mandi_board = "SELECT Mandi_Board_Id,Name FROM dbms_project.mandi_board"
    cursor.execute(farmer_storage_in_mandi_board)
    farmer_storage_data = cursor.fetchall()
    cursor.execute(all_mandi_board)
    all_mandi_board_data = cursor.fetchall()
    current_date = datetime.today().strftime('%Y-%m-%d')
    cursor.close()
    all_mandi_board_storage = None

    print('Hello outside Get')
    if request.method == 'GET':
        print('Hello Get')
        cursor = mysql.connection.cursor()  # TODO:write right query
        available_storage_space = f"SELECT dbms_project.storage_mandi_board_rent.Storage_Id,Name,Email_Address,State,Charges,Space FROM dbms_project.storage_mandi_board_rent \
            INNER JOIN dbms_project.mandi_board ON dbms_project.mandi_board.Mandi_Board_Id=dbms_project.storage_mandi_board_rent.Mandi_Board_Id \
            INNER JOIN dbms_project.storage_mandi_board ON dbms_project.storage_mandi_board.Mandi_Board_Id=dbms_project.storage_mandi_board_rent.Mandi_Board_Id AND dbms_project.storage_mandi_board.Storage_Id=dbms_project.storage_mandi_board_rent.Storage_Id \
            WHERE  timeTo <'{current_date}'"

        cursor.execute(available_storage_space)
        all_mandi_board_storage = cursor.fetchall()
        cursor.close()
        print(all_mandi_board_storage)

    if request.method == 'POST':
        cursor = mysql.connection.cursor()
        mandi_boardID_selected = request.form['mandi_board_selection']

        available_storage_space = f"SELECT dbms_project.storage_mandi_board_rent.Storage_Id,Name,Email_Address,State,Charges,Space FROM dbms_project.storage_mandi_board_rent \
                    INNER JOIN dbms_project.mandi_board ON dbms_project.mandi_board.Mandi_Board_Id=dbms_project.storage_mandi_board_rent.Mandi_Board_Id \
                    INNER JOIN dbms_project.storage_mandi_board ON dbms_project.storage_mandi_board.Mandi_Board_Id=dbms_project.storage_mandi_board_rent.Mandi_Board_Id AND dbms_project.storage_mandi_board.Storage_Id=dbms_project.storage_mandi_board_rent.Storage_Id \
                    WHERE  timeTo < '{current_date}' AND dbms_project.mandi_board.Mandi_Board_Id='{mandi_boardID_selected}' "
        cursor.execute(available_storage_space)
        all_mandi_board_storage = cursor.fetchall()
        cursor.close()

    return render_template('/farmer/Storage.html', storage_output_data=farmer_storage_data,
                           mandiID_output_data=all_mandi_board_data,
                           all_mandi_board_storage_output_data=all_mandi_board_storage)


@app.route('/add_storage_space', methods=['GET', 'POST'])
def add_storage_space():
    if request.method == 'POST':
        cursor = mysql.connection.cursor()
        Storage_Id = request.form['Storage_Id']
        Mandi_name = request.form['Mandi_Board_Name']
        current_date = datetime.today().strftime('%Y-%m-%d')
        date_to = request.form['date_to']
        User_Id = 'u9'

        sql_for_mandiDetails = f"SELECT * FROM dbms_project.mandi_board WHERE Name='{Mandi_name}'"
        cursor.execute(sql_for_mandiDetails)
        Mandi_Board_detail = cursor.fetchone()

        Mandi_Board_id = Mandi_Board_detail['Mandi_Board_Id']
        insert_mandiBoard_rent = f"INSERT INTO dbms_project.storage_mandi_board_rent (Storage_Id, Mandi_Board_Id, Renter_Person_Id, timeFrom, timeTo) VALUES('{Storage_Id}','{Mandi_Board_id}','{User_Id}','{current_date}','{date_to}')"
        cursor.execute(insert_mandiBoard_rent)
        mysql.connection.commit()

        sql_storage_charges = f"SELECT Charges FROM dbms_project.storage_mandi_board WHERE Storage_Id='{Storage_Id}' AND Mandi_Board_Id='{Mandi_Board_id}'"
        cursor.execute(sql_storage_charges)
        storage_charges = cursor.fetchone()

        mandi_storage_revenue = Mandi_Board_detail['Revenue_Storage_Space'] + storage_charges['Charges']

        update_mandi_storage_revenue = f"UPDATE dbms_project.mandi_board SET Revenue_Storage_Space ='{mandi_storage_revenue}'"
        cursor.execute(update_mandi_storage_revenue)
        mysql.connection.commit()

        cursor.close()

    return redirect(url_for('farmer_storage'))


def create_session(account):
    session['loggedin'] = True
    session['User_Id'] = account['User_Id']  # getting User_Id
    session['Username'] = account['Login']  # getting Username
    print(session['profession'])
    if session['profession'] == 'Farmer':
        return redirect(url_for('farmer_dashboard'))
    return f"<h1>{account['Login']}</h1>"


@app.route('/check_login_info', methods=['GET', 'POST'])
def check_login_info():
    if request.method == 'POST':
        Username = request.form['Username']
        password = request.form['inputPassword']
        user_profession = request.form['profession']
        if user_profession == 'Farmer' or user_profession == 'FPO':
            cursor = mysql.connection.cursor()
            cursor.execute('SELECT * FROM seller WHERE Login = % s AND Password = % s', (Username, password,))

            account = cursor.fetchone()
            cursor.close()
            if account:
                session['profession'] = user_profession
                return create_session(account)
            else:
                return render_template('Login.html')

        elif user_profession == 'Mandi_Board':
            cursor = mysql.connection.cursor()
            cursor.execute('SELECT * FROM mandi_board WHERE Login = % s AND Password = % s', (Username, password,))

            account = cursor.fetchone()
            cursor.close()
            if account:
                session['profession'] = user_profession
                return create_session(account)
            else:
                return render_template('Login.html')

        elif user_profession == 'Trader':
            cursor = mysql.connection.cursor()
            cursor.execute('SELECT * FROM trader WHERE Login = % s AND Password = % s', (Username, password,))

            account = cursor.fetchone()
            cursor.close()
            if account:
                session['profession'] = user_profession
                return create_session(account)
            else:
                return render_template('Login.html')
        elif user_profession == 'Analyst':
            cursor = mysql.connection.cursor()
            cursor.execute('SELECT * FROM analyst WHERE Login = % s AND Password = % s', (Username, password,))
            account = cursor.fetchone()
            cursor.close()
            if account:
                session['profession'] = user_profession
                print("Hello Analyst")
                return create_session(account)
            else:
                return render_template('Login.html')

    return render_template('Login.html')


if __name__ == '__main__':
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    app.run(debug=True)
