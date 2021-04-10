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

current_date = datetime.today().strftime('%Y-%m-%d')


@app.route('/', methods=['GET', 'POST'])
def start():
    if request.method == 'GET':
        return render_template('start.html')
    # return 'Phir kata'


@app.route('/base')
def base():
    return render_template('farmer/base.html')


@app.route('/farmer/my_transactions', methods=['GET', 'POST'])
def farmer_transactions():
    if not session.get('Username') is None:
        cur = mysql.connection.cursor()
        cur.execute("select User_Id from dbms_project.trader")
        traders = list(cur.fetchall())
        # print(traders)
        traders.insert(0, {'User_Id':'All'})
        # print(traders)
        UUser_Id = session.get('User_Id')
        # print(UUser_Id)
        cur.close()
        bbuyer_Id = None
        if request.method == 'GET':
            cur = mysql.connection.cursor()
            cur.execute(
                "Select Transaction_Id, Crop_Id, buyer_Id, seller_Id, Amount from dbms_project.transaction join dbms_project.trader on trader.User_Id = transaction.buyer_Id where transaction.seller_Id = '{}'".format(UUser_Id))
            result = cur.fetchall()
            columns = [h[0] for h in cur.description]

            cur.close()

        if request.method == 'POST':
            bbuyer_Id = request.form.get('buyer_Id')
            print(bbuyer_Id)
            cur = mysql.connection.cursor()
            if (bbuyer_Id == 'All'):
                cur.execute("Select Transaction_Id, Crop_Id, buyer_Id, seller_Id, Amount from dbms_project.transaction join dbms_project.trader on trader.User_Id = transaction.buyer_Id where transaction.seller_Id = '{}'".format(UUser_Id))
            else:
                cur.execute("Select Transaction_Id, Crop_Id, buyer_Id, seller_Id, Amount from dbms_project.transaction join dbms_project.trader on trader.User_Id = transaction.buyer_Id where transaction.seller_Id = '{}' and transaction.buyer_Id = '{}'".format(UUser_Id, bbuyer_Id))
            result = cur.fetchall()
            columns = [h[0] for h in cur.description]
            cur.close()

        return render_template('/farmer/transactions.html', title='My Transactions', table=result, columns=columns, traders=traders, buyer_Id = bbuyer_Id)

    else:
        print("No username found in session")
        return redirect(url_for('check_login_info'))


@app.route('/trader_transactions', methods=['GET', 'POST']) # trader transaction
def trader_transactions():
    if not session.get('Username') is None:
        cur = mysql.connection.cursor()
        cur.execute("select User_Id_Linked from dbms_project.farmers")
        farmers = list(cur.fetchall())
        print(farmers)
        farmers.insert(0, {'User_Id_Linked':'All'})
        print(farmers)
        UUser_Id = session.get('User_Id')
        print(UUser_Id)
        cur.close()
        sseller_Id = None
        if request.method == 'GET':
            cur = mysql.connection.cursor()
            cur.execute("Select Transaction_Id, Crop_Id, buyer_Id, seller_Id, Amount from dbms_project.transaction join dbms_project.farmers on farmers.User_Id_Linked = transaction.seller_Id where transaction.buyer_Id = '{}'".format(UUser_Id))
            result = cur.fetchall()
            columns = [h[0] for h in cur.description]

            cur.close()

        if request.method == 'POST':
            sseller_Id = request.form.get('seller_Id')
            # print(sseler_Id)
            cur = mysql.connection.cursor()
            if (sseller_Id == 'All'):
                cur.execute("Select Transaction_Id, Crop_Id, buyer_Id, seller_Id, Amount from dbms_project.transaction join dbms_project.farmers on farmers.User_Id_Linked = transaction.seller_Id where transaction.buyer_Id = '{}'".format(UUser_Id))
            else:
                cur.execute("Select Transaction_Id, Crop_Id, buyer_Id, seller_Id, Amount from dbms_project.transaction join dbms_project.farmers on farmers.User_Id_Linked = transaction.seller_Id where transaction.buyer_Id = '{}' and transaction.seller_Id = '{}'".format(UUser_Id, sseller_Id))
            result = cur.fetchall()
            columns = [h[0] for h in cur.description]
            cur.close()

        return render_template('/Trader/transaction.html', title='My Transactions', table=result, columns=columns,
                               farmers=farmers, seller_Id = sseller_Id)

    else:
        print("No username found in session")
        return redirect(url_for('check_login_info'))


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
    if not session.get('Username') is None:  # checking if session exists
        user_id = session.get('User_Id')
        cursor = mysql.connection.cursor()
        farmer_storage_in_mandi_board = f"SELECT dbms_project.storage_mandi_board_rent.Storage_Id,Name,Email_Address,Charges,timeFrom,timeTo FROM dbms_project.storage_mandi_board_rent\
                        INNER JOIN dbms_project.mandi_board ON dbms_project.mandi_board.User_Id=dbms_project.storage_mandi_board_rent.Mandi_Board_Id \
                        INNER JOIN dbms_project.storage_mandi_board ON dbms_project.storage_mandi_board.Mandi_Board_Id=dbms_project.storage_mandi_board_rent.Mandi_Board_Id AND dbms_project.storage_mandi_board.Storage_Id=dbms_project.storage_mandi_board_rent.Storage_Id \
                        WHERE Renter_Person_Id='{user_id}' "
        all_mandi_board = "SELECT User_Id,Name FROM dbms_project.mandi_board"
        cursor.execute(farmer_storage_in_mandi_board)
        farmer_storage_data = cursor.fetchall()
        cursor.execute(all_mandi_board)
        all_mandi_board_data = cursor.fetchall()
        cursor.close()
        all_mandi_board_storage = None

        if request.method == 'GET':
            cursor = mysql.connection.cursor()  # TODO:write right query
            available_storage_space = f"SELECT Storage_Id,Name,Email_Address,State,Charges,Space From storage_mandi_board inner join mandi_board on mandi_board.User_Id = storage_mandi_board.Mandi_Board_Id where not exists(\
                    SELECT Mandi_Board_ID,Storage_Id FROM storage_mandi_board_rent \
                    WHERE timeTo>'{current_date}' and storage_mandi_board_rent.Mandi_Board_ID=storage_mandi_board.Mandi_Board_Id AND storage_mandi_board_rent.Storage_Id=storage_mandi_board.Storage_Id)"
            cursor.execute(available_storage_space)
            all_mandi_board_storage = cursor.fetchall()
            cursor.close()
            print(all_mandi_board_storage)

        if request.method == 'POST':
            cursor = mysql.connection.cursor()
            mandi_boardID_selected = request.form['mandi_board_selection']

            available_storage_space = f"SELECT Storage_Id,Name,Email_Address,State,Charges,Space From storage_mandi_board inner join mandi_board on mandi_board.User_Id = storage_mandi_board.Mandi_Board_Id where storage_mandi_board.Mandi_Board_ID = '{mandi_boardID_selected}' AND not exists(\
                    SELECT Mandi_Board_ID,Storage_Id FROM storage_mandi_board_rent \
                    WHERE timeTo>'{current_date}' and storage_mandi_board_rent.Mandi_Board_ID=storage_mandi_board.Mandi_Board_Id AND storage_mandi_board_rent.Storage_Id=storage_mandi_board.Storage_Id )"
            cursor.execute(available_storage_space)
            all_mandi_board_storage = cursor.fetchall()
            cursor.close()

        return render_template('/farmer/Storage.html', storage_output_data=farmer_storage_data,
                               mandiID_output_data=all_mandi_board_data,
                               all_mandi_board_storage_output_data=all_mandi_board_storage)
    else:
        print("No username found in session")
        return redirect(url_for('check_login_info'))


@app.route('/add_storage_space', methods=['GET', 'POST'])
def add_storage_space():
    if request.method == 'POST':
        if not session.get('Username') is None:
            cursor = mysql.connection.cursor()
            Storage_Id = request.form['Storage_Id']
            Mandi_name = request.form['Mandi_Board_Name']
            date_to = request.form['date_to']
            User_Id = session.get('User_Id')

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

            update_mandi_storage_revenue = f"UPDATE dbms_project.mandi_board SET Revenue_Storage_Space ='{mandi_storage_revenue}' WHERE User_Id='{Mandi_Board_id}'"
            cursor.execute(update_mandi_storage_revenue)
            mysql.connection.commit()

            cursor.close()

        return redirect(url_for('farmer_storage'))


@app.route('/farmer_mandi_board', methods=['GET', 'POST'])
def farmer_mandi_board():
    if not session.get('Username') is None:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM dbms_project.mandi_board")
        mandi_data = cursor.fetchall()
        cursor.execute("SELECT dbms_project.mandi_board.Name,dbms_project.crops.Crop_Name,Msp from dbms_project.crop_mandi_board\
                    INNER JOIN dbms_project.crops ON dbms_project.crop_mandi_board.Crop_Id=dbms_project.crops.Crop_Id\
                    INNER JOIN dbms_project.mandi_board ON dbms_project.crop_mandi_board.Mandi_Board_Id=dbms_project.mandi_board.User_Id")
        crops_list = cursor.fetchall()
        cursor.execute("SELECT User_Id,Name FROM dbms_project.mandi_board")
        all_mandi_board_data = cursor.fetchall()

        cursor.execute("SELECT Crop_Id, Crop_Name FROM dbms_project.crops")
        all_crop_name = cursor.fetchall()

        cursor.close()

        if request.method == 'POST':
            cursor = mysql.connection.cursor()
            mandi_boardID_selected = request.form['mandi_board_selection']
            crop_selected = request.form['crop_selection']
            if mandi_boardID_selected == 'All':
                if crop_selected == 'All':
                    pass
                else:
                    cursor.execute(f"SELECT dbms_project.mandi_board.Name,dbms_project.crops.Crop_Name,Msp from dbms_project.crop_mandi_board\
                                        INNER JOIN dbms_project.crops ON dbms_project.crop_mandi_board.Crop_Id=dbms_project.crops.Crop_Id\
                                        INNER JOIN dbms_project.mandi_board ON dbms_project.crop_mandi_board.Mandi_Board_Id=dbms_project.mandi_board.User_Id WHERE dbms_project.crops.Crop_Id='{crop_selected}'")
                    crops_list = cursor.fetchall()
            elif crop_selected == 'All':
                if mandi_boardID_selected == 'All':
                    pass
                else:
                    cursor.execute(f"SELECT dbms_project.mandi_board.Name,dbms_project.crops.Crop_Name,Msp from dbms_project.crop_mandi_board\
                                                            INNER JOIN dbms_project.crops ON dbms_project.crop_mandi_board.Crop_Id=dbms_project.crops.Crop_Id\
                                                            INNER JOIN dbms_project.mandi_board ON dbms_project.crop_mandi_board.Mandi_Board_Id=dbms_project.mandi_board.User_Id WHERE dbms_project.mandi_board.User_Id='{mandi_boardID_selected}'")
                    crops_list = cursor.fetchall()
            else:
                cursor.execute(f"SELECT dbms_project.mandi_board.Name,dbms_project.crops.Crop_Name,Msp from dbms_project.crop_mandi_board\
                                                                            INNER JOIN dbms_project.crops ON dbms_project.crop_mandi_board.Crop_Id=dbms_project.crops.Crop_Id\
                                                                            INNER JOIN dbms_project.mandi_board ON dbms_project.crop_mandi_board.Mandi_Board_Id=dbms_project.mandi_board.User_Id WHERE dbms_project.mandi_board.User_Id='{mandi_boardID_selected}' AND dbms_project.crops.Crop_Id='{crop_selected}'")
                crops_list = cursor.fetchall()
            print("Mandi "+mandi_boardID_selected)
            print("Crops "+crop_selected)
        return render_template('/farmer/farmer_mandi_board.html', data=mandi_data, crops_list=crops_list,
                               mandiID_output_data=all_mandi_board_data, crop_output_data=all_crop_name)
    else:
        print("No username found in session")
        return redirect(url_for('check_login_info'))


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('User_Id', None)
    session.pop('Username', None)
    session.pop('profession', None)
    return render_template('start.html')


def create_session(account):
    session['loggedin'] = True
    session['User_Id'] = account['User_Id']
    session['Username'] = account['Login']

    if session['profession'] == 'Farmer':
        return redirect(url_for('farmer_dashboard'))

    elif session['profession'] == 'FPO':
        return render_template('/FPO/dashboard.html')

    elif session['profession'] == 'Trader':
        return redirect(url_for('trader_dashboard'))

    elif session['profession'] == 'Mandi_Board':
        return render_template('/Mandi_Board/dashboard.html')

    elif session['profession'] == 'Analyst':
        return render_template('/Analyst/dashboard.html')

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


@app.route('/Trader_signUp', methods=['GET', 'POST'])
def Trader_signUp():
    if request.method == 'POST':
        cursor = mysql.connection.cursor()
        Name = request.form.get('Name')
        Username = request.form.get('Username')
        Phone_Number = request.form.get('phone_no')
        Password = request.form.get('inputPassword')
        BankAccount = request.form.get('inputAccount')
        cursor.execute("SELECT User_Id from dbms_project.trader")
        trader_data = cursor.fetchall()
        trader_Id = -1
        for val in trader_data:
            ID = val['User_Id']
            if int(ID[1:]) > trader_Id:
                trader_Id = int(ID[1:])
        trader_Id = 't' + str(trader_Id + 1)
        new_Trader_Sql = f"INSERT INTO dbms_project.trader(User_Id, Login, Password, Name, Mobile_Number, Bank_Account_Number, Total_Trade_Charges)" \
                         f"VALUES ('{trader_Id}','{Username}','{Password}','{Name}','{Phone_Number}','{BankAccount}','{'0'}')"
        cursor.execute(new_Trader_Sql)
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('check_login_info'))
    return render_template("/Trader/trader_registration.html")


@app.route('/Seller_signUp/<string:seller_type>', methods=['GET', 'POST'])
def Seller_signUp(seller_type):
    if request.method == 'POST':
        cursor = mysql.connection.cursor()
        Name = request.form.get('Name')
        Email = request.form.get('email')
        password = request.form.get('inputPassword')
        Username = request.form.get('Username')
        Income = request.form.get('inputIncome')
        Locality = request.form.get('inputLocality')
        State = request.form.get('State')
        District = request.form.get('inputDistrict')
        Zip = request.form.get('inputZip')
        BankAccount = request.form.get('inputAccount')
        cursor.execute('SELECT User_Id FROM seller')
        seller_data = cursor.fetchall()
        User_Id = -1
        for val in seller_data:
            ID = val['User_Id']
            if int(ID[1:]) > User_Id:
                User_Id = int(ID[1:])
        User_Id = 'u' + str(User_Id + 1)

        Designation = 'F'
        if seller_type == 'FPO':
            Designation = 'FP'
        sql_formula = f"INSERT INTO dbms_project.seller(User_Id,Login,Password,Name,Locality,District,State,Pincode,Bank_Account_No,Income,Designation,Email) VALUES('{User_Id}','{Username}','{password}','{Name}','{Locality}','{District}','{State}','{Zip}','{BankAccount}','{Income}','{Designation}','{Email}') "

        cursor.execute(sql_formula)
        mysql.connection.commit()

        if seller_type == 'FPO':  # inserting data into FPO table
            cursor.execute('SELECT Fpo_Id FROM dbms_project.fpo')
            fpo_data = cursor.fetchall()
            FPO_Id = -1
            for val in fpo_data:
                ID = val['Fpo_Id']
                if int(ID[2:]) > FPO_Id:
                    FPO_Id = int(ID[2:])
            FPO_Id = 'fp' + str(FPO_Id + 1)
            new_fpo_sql = f"INSERT INTO dbms_project.fpo(Fpo_Id, User_Id_Linked, Fpo_Registration_Date) VALUES('{FPO_Id}','{User_Id}','{current_date}')"
            cursor.execute(new_fpo_sql)

        else:  # inserting data into farmer table
            cursor.execute('SELECT Farmer_Id FROM dbms_project.farmers')
            farmer_data = cursor.fetchall()
            farmer_ID = -1
            for val in farmer_data:
                ID = val['Farmer_Id']
                if int(ID[1:]) > farmer_ID:
                    farmer_ID = int(ID[1:])
            farmer_ID = 'f' + str(farmer_ID + 1)
            new_farmer_sql = f"INSERT into dbms_project.farmers(Farmer_Id, User_Id_Linked, Land_Area, Fpo_Id, Trade_Charges) VALUES('{farmer_ID}','{User_Id}','{0}','{'fp1'}','{0}')"
            # TODO: here assigning fp1 to each farmer,farmer can change it after farmer login
            cursor.execute(new_farmer_sql)

        print("USER_ID: " + str(User_Id))
        mysql.connection.commit()
        cursor.close()

        return redirect(url_for('check_login_info'))

    return render_template("/FPO/seller_registration.html")


@app.route('/Farmer_signUp', methods=['GET', 'POST'])
def Farmer_SignUp():
    return redirect(url_for('Seller_signUp', seller_type='Farmer'))


@app.route('/FPO_signUp', methods=['GET', 'POST'])
def FPO_SignUp():
    return redirect(url_for('Seller_signUp', seller_type='FPO'))


@app.route('/Mandi_Board_signUp', methods=['GET', 'POST'])
def Mandi_Board_signUp():
    if request.method == 'POST':
        cursor = mysql.connection.cursor()
        Name = request.form.get('Name')
        Username = request.form.get('Username')
        Email = request.form.get('email')
        password = request.form.get('inputPassword')
        phone_no = request.form.get('phone_no')
        trade_charges = request.form.get('trade_charges')
        Locality = request.form.get('inputLocality')
        State = request.form.get('State')
        District = request.form.get('inputDistrict')
        Zip = request.form.get('inputZip')
        cursor.execute("SELECT Mandi_Board_Id FROM dbms_project.mandi_board")
        mandi_board_data = cursor.fetchall()
        Mandi_board_ID = -1
        for val in mandi_board_data:
            ID = val['Mandi_Board_Id']
            if int(ID[2:]) > Mandi_board_ID:
                Mandi_board_ID = int(ID[2:])
        Mandi_board_ID = 'mb' + str(Mandi_board_ID + 1)
        new_Mandi_Board_sql = f"INSERT INTO dbms_project.mandi_board (User_Id, Login, Password, Name, State, Locality, District, Pincode, Rating, Trade_Charges, Registered_Users, Revenue_Trading, Revenue_Storage_Space, Email_Address, Contact_No)" \
                              f"VALUES('{Mandi_board_ID}','{Username}','{password}','{Name}','{State}','{Locality}','{District}','{Zip}','{'0'}','{trade_charges}','{'0'}','{'0'}','{'0'}','{Email}','{phone_no}') "
        cursor.execute(new_Mandi_Board_sql)
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('check_login_info'))
    return render_template("/Mandi_Board/Mandi_Board_registration.html")


@app.route('/Analyst_signUp', methods=['GET', 'POST'])
def Analyst_signUp():
    if request.method == 'POST':
        cursor = mysql.connection.cursor()
        Name = request.form.get('Name')
        Username = request.form.get('Username')
        email = request.form.get('email')
        password = request.form.get('inputPassword')
        cursor.execute('SELECT Analyst_Id from analyst')
        analyst_data = cursor.fetchall()
        analyst_ID = -1
        for val in analyst_data:
            ID = val['Analyst_Id']
            if int(ID[1:]) > analyst_ID:
                analyst_ID = int(ID[1:])
        analyst_ID = 't' + str(analyst_ID + 1)
        new_analyst_sql = f"INSERT INTO dbms_project.analyst(User_Id, Login, Password, Analyst_Name, email) VALUES('{analyst_ID}','{Username}','{password}','{Name}','{email}')"
        cursor.execute(new_analyst_sql)
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('check_login_info'))
    return render_template("/Analyst/analyst_registration.html")


if __name__ == '__main__':
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    app.run(debug=True)
