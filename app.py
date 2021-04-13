from datetime import datetime
from flask import Flask, render_template, request, Markup, url_for, session,flash
from flask_mysqldb import MySQL
from werkzeug.utils import redirect
# from dateutil.relativedelta import *

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


@app.route('/farmer_crops', methods=['GET', 'POST'])
def farmer_crops():
    if not session.get('Username') is None:
        cursor = mysql.connection.cursor()
        user_id = session.get('User_Id')
        cursor.execute(
            f"SELECT Crop_Name,crop_seller.Crop_Id,Quality_10 , Price_1kg,Quantity_Kg FROM crop_seller join crops on crop_seller.Crop_Id=crops.Crop_Id WHERE Seller_Id='{user_id}'")
        crop_data = cursor.fetchall()

        return render_template('/farmer/my_crops.html', data=crop_data)
    else:
        print("No username found in session")
        return redirect(url_for('check_login_info'))


@app.route('/farmer_insert', methods=['POST'])
def farmer_insert():
    if request.method == "POST":
        flash("Data Inserted Successfully")
        cursor = mysql.connection.cursor()
        crop_id = request.form['crop_id']
        quality = request.form['quality']
        quantity = request.form['quantity']
        price = request.form['price']
        user_id = session.get('User_Id')
        cursor.execute(
            f"INSERT INTO crop_seller (Seller_Id,Crop_Id,Quality_10 , Price_1kg,Quantity_Kg) VALUES(%s, %s, %s,%s,%s)",
            (user_id, crop_id, quality, price, quantity))
        mysql.connection.commit()
        return redirect(url_for('farmer_crops'))

@app.route('/farmer_policy_insert', methods=['POST'])
def farmer_policy_insert():
    if request.method == "POST":
        cursor = mysql.connection.cursor()
        policy_id = request.form['Policy_Id']
        user_id = session.get('User_Id')
        print(policy_id,user_id)
        cursor.execute(
            f"INSERT INTO seller_policy (Seller_Id,Policy_Id,Date_Registeration) VALUES(%s, %s, curdate())",
            (user_id, policy_id))
        mysql.connection.commit()
        return redirect(url_for('farmer_dashboard'))

@app.route('/update_crop_farmer',methods=['POST','GET'])
def update_crop_farmer():
    if request.method == 'POST':
        cursor = mysql.connection.cursor()
        crop_id = request.form['crop_id']
        print(crop_id)
        quality = request.form['quality']
        quantity = request.form['quantity']
        price = request.form['price']
        user_id =session.get('User_Id')
        print("PLS WORK")
        cursor.execute(f"UPDATE crop_seller SET  Quality_10 ='{quality}', Price_1kg='{price}',Quantity_Kg='{quantity}' WHERE Crop_Id='{crop_id}' AND Seller_Id='u1'")
        mysql.connection.commit()
        return redirect(url_for('farmer_crops'))


@app.route('/farmer_delete/<string:id_data>', methods=['POST', 'GET'])
def farmer_delete(id_data):
    user_id = session.get('User_Id')
    mysql.connection.cursor().execute(f"Delete From crop_seller WHERE Seller_Id='{user_id}' AND Crop_Id='{id_data}'")
    mysql.connection.commit()
    return redirect(url_for('farmer_crops'))


@app.route('/farmer_transactions', methods=['GET', 'POST'])
def farmer_transactions():
    if not session.get('Username') is None:
        cur = mysql.connection.cursor()
        cur.execute("select User_Id from dbms_project.trader")
        traders = list(cur.fetchall())
        # print(traders)
        traders.insert(0, {'User_Id': 'All'})
        # print(traders)
        UUser_Id = session.get('User_Id')
        # print(UUser_Id)
        cur.close()
        bbuyer_Id = None
        if request.method == 'GET':
            cur = mysql.connection.cursor()
            cur.execute(
                "Select Transaction_Id, Crop_Id, buyer_Id, seller_Id, Amount from dbms_project.transaction join dbms_project.trader on trader.User_Id = transaction.buyer_Id where transaction.seller_Id = '{}'".format(
                    UUser_Id))
            result = cur.fetchall()
            columns = [h[0] for h in cur.description]

            cur.close()

        if request.method == 'POST':
            bbuyer_Id = request.form.get('buyer_Id')
            print(bbuyer_Id)
            cur = mysql.connection.cursor()
            if bbuyer_Id == 'All':
                cur.execute(
                    "Select Transaction_Id, Crop_Id, buyer_Id, seller_Id, Amount from dbms_project.transaction join dbms_project.trader on trader.User_Id = transaction.buyer_Id where transaction.seller_Id = '{}'".format(
                        UUser_Id))
            else:
                cur.execute(
                    "Select Transaction_Id, Crop_Id, buyer_Id, seller_Id, Amount from dbms_project.transaction join dbms_project.trader on trader.User_Id = transaction.buyer_Id where transaction.seller_Id = '{}' and transaction.buyer_Id = '{}'".format(
                        UUser_Id, bbuyer_Id))
            result = cur.fetchall()
            columns = [h[0] for h in cur.description]
            cur.close()

        return render_template('/farmer/my_transactions.html', title='My Transactions', table=result, columns=columns,
                               traders=traders, buyer_Id=bbuyer_Id)

    else:
        print("No username found in session")
        return redirect(url_for('check_login_info'))


@app.route('/FPO_transactions', methods=['GET', 'POST'])
def FPO_transactions():
    if not session.get('Username') is None:
        cur = mysql.connection.cursor()
        cur.execute("select User_Id from dbms_project.trader")
        traders = list(cur.fetchall())
        traders.insert(0, {'User_Id': 'All Buyers'})
        UUser_Id = session.get('User_Id')
        cur.close()
        bbuyer_Id = None
        if request.method == 'GET':
            cur = mysql.connection.cursor()
            cur.execute(
                "Select Transaction_Id, Crop_Id, buyer_Id, seller_Id, Mandi_Board_Id, Amount from dbms_project.transaction join dbms_project.trader on trader.User_Id = transaction.buyer_Id where transaction.seller_Id = '{}'".format(
                    UUser_Id))
            result = cur.fetchall()
            columns = [h[0] for h in cur.description]

            cur.close()

        if request.method == 'POST':
            bbuyer_Id = request.form.get('buyer_Id')
            print(bbuyer_Id)
            cur = mysql.connection.cursor()
            if bbuyer_Id == 'All Buyers':
                cur.execute(
                    "Select Transaction_Id, Crop_Id, buyer_Id, seller_Id, Mandi_Board_Id, Amount from dbms_project.transaction join dbms_project.trader on trader.User_Id = transaction.buyer_Id where transaction.seller_Id = '{}'".format(
                        UUser_Id))
            else:
                cur.execute(
                    "Select Transaction_Id, Crop_Id, buyer_Id, seller_Id, Mandi_Board_Id, Amount from dbms_project.transaction join dbms_project.trader on trader.User_Id = transaction.buyer_Id where transaction.seller_Id = '{}' and transaction.buyer_Id = '{}'".format(
                        UUser_Id, bbuyer_Id))
            result = cur.fetchall()
            columns = [h[0] for h in cur.description]
            cur.close()

        return render_template('/FPO/transactions.html', title='My Transactions', table=result, columns=columns,
                               traders=traders, buyer_Id=bbuyer_Id)

    else:
        print("No username found in session")
        return redirect(url_for('check_login_info'))


@app.route('/trader_buy_crop',methods=['GET','POST'])
def trader_buy_crop():
    if not session.get('Username') is None:
        if request.method == 'POST':
            cursor=mysql.connection.cursor()
            buyer_Id=session.get['User_Id']
            crop_name=request.form['crop_name']
            mandi_name=request.form['Name']
            crop_price=request.form['crop_price']
            buyer_crop_quantity=int(request.form['crop_quantity'])
            seller_id=request.form['seller_id']
            cursor.execute(f"SELECT * FROM dbms_project.seller WHERE User_Id = '{seller_id}'")
            seller_data=cursor.fetchall()

            cursor.execute(f"SELECT * FROM dbms_project.mandi_board WHERE Name= '{mandi_name}'")
            mandi_board_data=cursor.fetchone()

            cursor.execute(f"SELECT * FROM crops WHERE Crop_Name='{crop_name}'")
            crop_data=cursor.fetchone()
            crop_id=crop_data['Crop_Id']

            cursor.execute(f"SELECT * FROM dbms_project.crop_seller WHERE Seller_Id='{seller_id}' AND Crop_Id='{crop_id}' ")
            crop_details=cursor.fetchone()
            seller_crop_quantity=int(crop_details['Quantity_Kg'])
            if buyer_crop_quantity<=seller_crop_quantity:
                flash("Successful Buy!")
                if seller_crop_quantity-buyer_crop_quantity == 0:
                    cursor.execute(f"DELETE FROM dbms_project.crop_seller WHERE Seller_Id='{seller_id}' AND Crop_Id='{crop_id}' ")
                else:
                    cursor.execute(f"UPDATE dbms_project.crop_seller SET Quantity_Kg ='{seller_crop_quantity-buyer_crop_quantity}' WHERE Seller_Id='{seller_id}' AND Crop_Id='{crop_id}'")

                cursor.execute("SELECT Transaction_Id FROM dbms_project.transaction")
                transaction_data=cursor.fetchall()
                transaction_ID = -1
                for val in transaction_data:
                    ID = val['Transaction_Id']
                    if int(ID[2:]) > transaction_ID:
                        transaction_ID = int(ID[2:])
                transaction_ID = 'tr' + str(transaction_ID + 1)
                transaction_amount= seller_crop_quantity * crop_price
                cursor.execute(f"INSERT INTO dbms_project.transaction(Transaction_Id,Crop_Id,buyer_Id,seller_Id,Mandi_Board_Id,Amount,Quantity_Kg,Quality_10,Date_Of_Transaction) VALUES \
                        '{transaction_ID}','{crop_id}','{buyer_Id}','{seller_id}','{mandi_board_data['User_Id']}','{transaction_amount}','{seller_crop_quantity}','{crop_details['Quality_10']}','{current_date}'")

                cursor.execute("SELECT Coupon_Id FROM dbms_project.coupon")
                coupon_data=cursor.fetchall()
                coupon_ID = -1
                for val in coupon_data:
                    ID = val['Coupon_Id']
                    if int(ID[2:]) > coupon_ID:
                        coupon_ID = int(ID[2:])
                coupon_ID = 'tr' + str(coupon_ID + 1)
                coupon_value= transaction_amount * 0.01
                Date = datetime.today()
                coupon_valid_date = Date + relativedelta(month=+10)
                coupon_valid_date = coupon_valid_date.strftime('%Y-%m-%d')

                cursor.execute(f"INSERT INTO dbms_project.coupon(Coupon_Id,Transaction_Id,Crop_Id,Value,Valid_Till,Seller_Status,Buyer_Status) VALUES \
                               '{coupon_ID}','{transaction_ID}','{crop_id}','{coupon_value}','{coupon_valid_date}','{'0'}','{'0'}'")
                Trade_charges=mandi_board_data['Trade_Charges']*transaction_amount

                cursor.execute(f"UPDATE dbms_project.mandi_board SET Revenue_Trading ='{mandi_board_data['Revenue_Trading']+Trade_charges}' WHERE User_Id='{mandi_board_data['User_Id']}'")

                cursor.execute(f"SELECT * FROM dbms_project.trader WHERE User_Id = '{buyer_Id}'")
                trader_data=cursor.fetchall()
                cursor.execute(f"UPDATE dbms_project.trader SET Total_Trade_Charges='{trader_data['Total_Trade_Charges']+Trade_charges}' WHERE User_Id = '{buyer_Id}' ")

                cursor.execute(f"UPDATE dbms_project.seller SET Total_Trade_Charges = '{seller_data['Trade_Charges']+Trade_charges}' WHERE User_Id = '{seller_id}' ")

                cursor.execute(f"UPDATE dbms_project.seller SET Income = '{seller_data['Income']+ buyer_crop_quantity*crop_price }' WHERE User_Id = '{seller_id}' ")

                mysql.connection.commit()
                cursor.close()

            else:
                flash("Invalid quantity of crop")
            return redirect(url_for('trader_crop_price'))
    else:
        print("No username found in session")
        return redirect(url_for('check_login_info'))


@app.route('/trader_transactions', methods=['GET', 'POST'])  # trader transaction
def trader_transactions():
    if not session.get('Username') is None:
        cur = mysql.connection.cursor()
        cur.execute("select User_Id_Linked from dbms_project.farmers")
        farmers = list(cur.fetchall())
        print(farmers)
        farmers.insert(0, {'User_Id_Linked': 'All'})
        print(farmers)
        UUser_Id = session.get('User_Id')
        print(UUser_Id)
        cur.close()
        sseller_Id = None
        if request.method == 'GET':
            cur = mysql.connection.cursor()
            cur.execute(
                "Select Transaction_Id, Crop_Id, buyer_Id, seller_Id, Amount from dbms_project.transaction join dbms_project.farmers on farmers.User_Id_Linked = transaction.seller_Id where transaction.buyer_Id = '{}'".format(
                    UUser_Id))
            result = cur.fetchall()
            columns = [h[0] for h in cur.description]

            cur.close()

        if request.method == 'POST':
            sseller_Id = request.form.get('seller_Id')
            # print(sseler_Id)
            cur = mysql.connection.cursor()
            if sseller_Id == 'All':
                cur.execute(
                    "Select Transaction_Id, Crop_Id, buyer_Id, seller_Id, Amount from dbms_project.transaction join dbms_project.farmers on farmers.User_Id_Linked = transaction.seller_Id where transaction.buyer_Id = '{}'".format(
                        UUser_Id))
            else:
                cur.execute(
                    "Select Transaction_Id, Crop_Id, buyer_Id, seller_Id, Amount from dbms_project.transaction join dbms_project.farmers on farmers.User_Id_Linked = transaction.seller_Id where transaction.buyer_Id = '{}' and transaction.seller_Id = '{}'".format(
                        UUser_Id, sseller_Id))
            result = cur.fetchall()
            columns = [h[0] for h in cur.description]
            cur.close()

        return render_template('/Trader/transaction.html', title='My Transactions', table=result, columns=columns,
                               farmers=farmers, seller_Id=sseller_Id)

    else:
        print("No username found in session")
        return redirect(url_for('check_login_info'))


@app.route('/trader_crop_price', methods=['GET', 'POST'])
def trader_crop_price():
    if not session.get('Username') is None:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT User_Id,Name FROM dbms_project.mandi_board")
        all_mandi_board_data = cursor.fetchall()

        cursor.execute("SELECT Crop_Id, Crop_Name FROM dbms_project.crops")
        all_crop_name = cursor.fetchall()

        cursor.execute("SELECT crops.Crop_Id,crops.Crop_Name,mandi_board.Name,Trade_Charges,Price_1kg,Seller_Id,Quantity_Kg FROM crop_seller join crops on crops.Crop_Id=crop_seller.Crop_Id\
            join mandi_board on mandi_board.User_Id = crop_seller.Mandi_Board")
        all_crops_table = cursor.fetchall()
        cursor.close()
        if request.method == "POST":
            cursor = mysql.connection.cursor()
            mandi_boardID_selected = request.form['mandi_board_selection']
            crop_output_data = request.form['crop_selection']
            crop_price = request.form['crop_price']
            if mandi_boardID_selected == 'All':
                if crop_output_data == 'All':
                    if crop_price == '':
                        pass
                    else:
                        cursor.execute(f"SELECT crops.Crop_Id,crops.Crop_Name,mandi_board.Name,Trade_Charges,Price_1kg,Seller_Id,Quantity_Kg FROM crop_seller join crops on crops.Crop_Id=crop_seller.Crop_Id\
                            join mandi_board on mandi_board.User_Id = crop_seller.Mandi_Board WHERE Price_1kg<='{crop_price}'")
                        all_crops_table=cursor.fetchall()
                else:
                    if crop_price == '':
                        cursor.execute(f"SELECT crops.Crop_Id,crops.Crop_Name,mandi_board.Name,Price_1kg,Trade_Charges,Seller_Id,Quantity_Kg FROM crop_seller join crops on crops.Crop_Id=crop_seller.Crop_Id\
                                                    join mandi_board on mandi_board.User_Id = crop_seller.Mandi_Board WHERE crops.Crop_Name ='{crop_output_data}'")
                        all_crops_table = cursor.fetchall()
                    else:
                        cursor.execute(f"SELECT crops.Crop_Id,crops.Crop_Name,mandi_board.Name,Price_1kg,Seller_Id,Trade_Charges,Quantity_Kg FROM crop_seller join crops on crops.Crop_Id=crop_seller.Crop_Id\
                                                                            join mandi_board on mandi_board.User_Id = crop_seller.Mandi_Board WHERE crops.Crop_Name ='{crop_output_data}' AND Price_1kg<='{crop_price}'")
                        all_crops_table = cursor.fetchall()
            else:
                if crop_output_data == 'All':
                    if crop_price == '':
                        cursor.execute(f"SELECT crops.Crop_Id,crops.Crop_Name,mandi_board.Name,Price_1kg,Seller_Id,Trade_Charges,Quantity_Kg FROM crop_seller join crops on crops.Crop_Id=crop_seller.Crop_Id\
                                                    join mandi_board on mandi_board.User_Id = crop_seller.Mandi_Board WHERE mandi_board.Name='{mandi_boardID_selected}'")
                        all_crops_table = cursor.fetchall()
                    else:
                        cursor.execute(f"SELECT crops.Crop_Id,crops.Crop_Name,mandi_board.Name,Price_1kg,Seller_Id,Trade_Charges,Quantity_Kg FROM crop_seller join crops on crops.Crop_Id=crop_seller.Crop_Id\
                            join mandi_board on mandi_board.User_Id = crop_seller.Mandi_Board WHERE mandi_board.Name='{mandi_boardID_selected}' AND Price_1kg<='{crop_price}' ")
                        all_crops_table = cursor.fetchall()
                else:
                    if crop_price == '':
                        cursor.execute(f"SELECT crops.Crop_Id,crops.Crop_Name,mandi_board.Name,Price_1kg,Seller_Id,Trade_Charges,Quantity_Kg FROM crop_seller join crops on crops.Crop_Id=crop_seller.Crop_Id\
                                                                       join mandi_board on mandi_board.User_Id = crop_seller.Mandi_Board WHERE crops.Crop_Name ='{crop_output_data}' AND mandi_board.Name='{mandi_boardID_selected}' ")
                        all_crops_table = cursor.fetchall()
                    else:
                        cursor.execute(f"SELECT crops.Crop_Id,crops.Crop_Name,mandi_board.Name,Price_1kg,Seller_Id,Trade_Charges,Quantity_Kg FROM crop_seller join crops on crops.Crop_Id=crop_seller.Crop_Id\
                                                                                               join mandi_board on mandi_board.User_Id = crop_seller.Mandi_Board WHERE crops.Crop_Name ='{crop_output_data}' AND Price_1kg<='{crop_price}' AND mandi_board.Name='{mandi_boardID_selected}'")
                        all_crops_table = cursor.fetchall()
            cursor.close()
        return render_template('/Trader/crop_price.html', mandiID_output_data=all_mandi_board_data,
                               crop_output_data=all_crop_name, all_crops_table=all_crops_table)
    else:
        print("No username found in session")
        return redirect(url_for('check_login_info'))

@app.route('/trader_coupon', methods=['GET','POST'])
def trader_coupon():
    if not session.get('Username') is None:
        cursor=mysql.connection.cursor()
        user_id = session.get('User_Id')
        cursor.execute(f"SELECT coupon.Coupon_Id, coupon.Transaction_Id, crops.Crop_Name, coupon.Value, coupon.Valid_Till, coupon.Buyer_Status\
                FROM coupon, crops, transaction WHERE transaction.buyer_Id='{user_id}' AND transaction.Transaction_Id = coupon.Transaction_Id and crops.Crop_Id = coupon.Crop_Id and coupon.Valid_Till>='{current_date}';")
        all_coupon_available=cursor.fetchall()
        cursor.execute(f"SELECT coupon.Coupon_Id, coupon.Transaction_Id, crops.Crop_Name, coupon.Value, coupon.Valid_Till, coupon.Buyer_Status\
                FROM coupon, crops, transaction WHERE transaction.buyer_Id='{user_id}' AND transaction.Transaction_Id = coupon.Transaction_Id and crops.Crop_Id = coupon.Crop_Id and coupon.Valid_Till<'{current_date}';")
        all_non_coupon_available=cursor.fetchall()
        return render_template('/Trader/coupon.html',all_coupon_available=all_coupon_available,all_non_coupon_available=all_non_coupon_available)
    else:
        print("No username found in session")
        return redirect(url_for('check_login_info'))

@app.route('/mandi_board_transactions', methods=['GET', 'POST'])  # mandiboard transactions
def mandi_board_transactions():
    if not session.get('Username') is None:
        cur = mysql.connection.cursor()
        cur.execute("select User_Id_Linked from dbms_project.farmers")
        farmers = list(cur.fetchall())
        farmers.insert(0, {'User_Id_Linked': 'All Sellers'})
        cur.execute("select User_Id from dbms_project.trader")
        traders = list(cur.fetchall())
        traders.insert(0, {'User_Id': 'All Buyers'})
        UUser_Id = session.get('User_Id')

        print(UUser_Id)
        cur.close()
        sseller_Id = None
        bbuyer_Id = None
        if request.method == 'GET':
            cur = mysql.connection.cursor()
            cur.execute(f"Select Transaction_Id, Crop_Id, buyer_Id, seller_Id, Mandi_Board_Id, Amount from dbms_project.transaction\
                join dbms_project.trader join dbms_project.farmers on trader.User_Id = transaction.buyer_Id and farmers.User_Id_Linked = transaction.seller_Id;")
            result = cur.fetchall()
            columns = [h[0] for h in cur.description]

            cur.close()

        if request.method == 'POST':
            sseller_Id = request.form.get('seller_Id')
            bbuyer_Id = request.form.get('bbuyer_Id')
            cur = mysql.connection.cursor()
            if sseller_Id == 'All Sellers':
                if bbuyer_Id == 'All Buyers':
                    cur.execute(f"Select Transaction_Id, Crop_Id, buyer_Id, seller_Id, Mandi_Board_Id, Amount from dbms_project.transaction\
                    join dbms_project.trader join dbms_project.farmers on trader.User_Id = transaction.buyer_Id and farmers.User_Id_Linked = transaction.seller_Id\
                    where transaction.Mandi_Board_Id = {UUser_Id};")
                else:
                    cur.execute(f"Select Transaction_Id, Crop_Id, buyer_Id, seller_Id, Mandi_Board_Id, Amount from dbms_project.transaction\
                    join dbms_project.trader join dbms_project.farmers on trader.User_Id = transaction.buyer_Id and farmers.User_Id_Linked = transaction.seller_Id\
                    where transaction.buyer_Id = '{bbuyer_Id}' and transaction.Mandi_Board_Id = '{UUser_Id}';")

            elif bbuyer_Id == 'All Buyers':
                if sseller_Id == 'All Sellers':
                    cur.execute(f"Select Transaction_Id, Crop_Id, buyer_Id, seller_Id, Mandi_Board_Id, Amount from dbms_project.transaction\
                    join dbms_project.trader join dbms_project.farmers on trader.User_Id = transaction.buyer_Id and farmers.User_Id_Linked = transaction.seller_Id\
                    where transaction.Mandi_Board_Id = {UUser_Id};")
                else:
                    cur.execute(f"Select Transaction_Id, Crop_Id, buyer_Id, seller_Id, Mandi_Board_Id, Amount from dbms_project.transaction\
                    join dbms_project.trader join dbms_project.farmers on trader.User_Id = transaction.buyer_Id and farmers.User_Id_Linked = transaction.seller_Id\
                    where transaction.seller_Id = '{sseller_Id}' and transaction.Mandi_Board_Id = '{UUser_Id}';")

            else:
                cur.execute(f"Select Transaction_Id, Crop_Id, buyer_Id, seller_Id, Mandi_Board_Id, Amount from dbms_project.transaction\
                    join dbms_project.trader join dbms_project.farmers on trader.User_Id = transaction.buyer_Id and farmers.User_Id_Linked = transaction.seller_Id\
                    where transaction.seller_Id = '{sseller_Id}' and transaction.buyer_Id = '{bbuyer_Id}' and transaction.Mandi_Board_Id = '{UUser_Id}';")

            result = cur.fetchall()
            columns = [h[0] for h in cur.description]
            cur.close()

        return render_template('/Mandi_Board/transactions.html', title='My Transactions', table=result, columns=columns,
                               farmers=farmers, traders=traders, seller_Id=sseller_Id, bbuyer_Id=bbuyer_Id)

    else:
        print("No username found in session")
        return redirect(url_for('check_login_info'))


@app.route('/trader_dashboard', methods=['GET', 'POST'])
def trader_dashboard():
    if not session.get('Username') is None:
        user_id = session.get('User_Id')
        tra1gv = []
        tra1gh = []
        cur = mysql.connection.cursor()
        cur.execute(f"SELECT  monthname((Date_Of_Transaction)) as month,SUM(Amount) as amount FROM dbms_project.transaction where buyer_Id = '{user_id}' and YEAR(Date_Of_Transaction) = '2020'GROUP BY MONTH(Date_Of_Transaction);")
        result = cur.fetchall()
        maximum = 0
        for d in result:
            tra1gv.append((round(d['amount'])))
            maximum = max(maximum, (round(d['amount'])))
            tra1gh.append(d['month'])

        tra2gv = []
        tra2gh = []

        # cur = mysql.connection.cursor()
        cur.execute(f"select Crop_Name,temp.Quantity,temp.Amount, temp.buyer_Id from crops,(SELECT Crop_Id,SUM(Quantity_Kg) as Quantity,SUM(Amount) as Amount, buyer_Id FROM dbms_project.transaction WHERE buyer_Id='{user_id}' group by(Crop_Id)) as temp where crops.Crop_Id=temp.Crop_Id;")
        result1 = cur.fetchall()
        maximum1 = 0
        for d in result1:
            tra2gv.append((round(d['Amount'])))
            maximum1 = max(maximum1, (round(d['Amount'])))
            tra2gh.append(d['Crop_Name'])


        cur.execute(
            f"select buyer_Id, sum(Amount) as Amount, sum(Quantity_Kg) as Quantity from transaction where buyer_Id='{user_id}' group by buyer_Id;")
        Total_Spending = cur.fetchall();total_spending = 0
        for i in Total_Spending:
            total_spending = i['Amount']
        cur.execute(
            f"select buyer_Id, Amount, Quantity_Kg, Trade_Charges from transaction join mandi_board where buyer_Id='{user_id}';")
        Total_Trade_Charges = cur.fetchall();total_tax = 0
        for i in Total_Trade_Charges:
            total_tax += round((i['Amount'] * i['Trade_Charges'])/100, 2)
        cur.execute(
            f"select buyer_Id,count(*) as count from transaction where buyer_Id='{user_id}';")
        Total_Transactions = cur.fetchall()
        total_transaction = 0
        for i in Total_Transactions:
            total_transaction = i['count']
        cur.close()
        print(tra2gh, tra2gv)
        colors = [
            "#7bd05e","#F7464A", "#2eb376", "#46BFBD", "#FDB45C", "#FEDCBA",
            "#ABCDEF", "#DDDDDD", "#ABCABC", "#4169E1",
            "#C71585", "#FF4500", "#FEDCBA", "#46BFBD"]
        return render_template('/Trader/dashboard.html', max=maximum + 1000,
                               labels=tra1gh, values=tra1gv, max1=maximum1 + 4,
                               set=zip(tra2gv, tra2gh, colors), Total_Spending=total_spending, Total_Trade_Charges=round(total_tax,2), Total_Transactions=total_transaction)
    else:
        print("No username found in session")
        return redirect(url_for('check_login_info'))


@app.route('/farmer_dashboard', methods=['GET', 'POST'])
def farmer_dashboard():
    if not session.get('Username') is None:
        user_id = session.get('User_Id')
        far1gv = []
        far1gh = []
        cur = mysql.connection.cursor()
        cur.execute(
            f"SELECT  monthname((Date_Of_Transaction)) as month,SUM(Amount) as amount FROM dbms_project.transaction where seller_Id = '{user_id}' and YEAR(Date_Of_Transaction) = '2020'GROUP BY MONTH(Date_Of_Transaction);")
        result = cur.fetchall()
        maximum = 0
        for d in result:
            far1gv.append((round(d['amount'])))
            maximum = max(maximum, (round(d['amount'])))
            far1gh.append(d['month'])

        far2gv = []
        far2gh = []
        cur.execute(
            f"select Crop_Name,temp.Quantity,temp.Amount from crops,(SELECT Crop_Id,SUM(Quantity_Kg) as Quantity,SUM(Amount) as Amount FROM dbms_project.transaction WHERE seller_Id='{user_id}' group by(Crop_Id)) as temp where crops.Crop_Id=temp.Crop_Id;")
        result1 = cur.fetchall()
        maximum1 = 0
        for d in result1:
            # if (d['Designation'] == 'F'):
            far2gv.append((round(d['Amount'])))
            maximum1 = max(maximum1, (round(d['Amount'])))
            far2gh.append(d['Crop_Name'])

        cur.execute(
            f"Select Crop_Name,SUM(Quantity_Kg) as Quantity,sum(Amount) as Amount from transaction join crops on transaction.Crop_Id = crops.Crop_Id  group by crops.Crop_Id order by sum(Amount) desc;-- year(Date_Of_Transaction)=year(curdate())")
        result1 = cur.fetchall()
        cur.execute(
            f"Select * from  government_policy where not exists ( select * from seller_policy where Seller_Id='{user_id}' and government_policy.Policy_Id = seller_policy.Policy_Id or Expires_On<curdate() or Implemented_On>curdate() );")
        result2 = cur.fetchall()
        cur.execute(
            f"select seller_Id,seller.Name,sum(Quantity_Kg) as Quantity,sum(Amount) as Amount from transaction join seller where seller.User_Id=transaction.seller_Id and seller.Designation='F' and seller_Id='{user_id}' group by seller_Id;")
        TotalIncome = cur.fetchall();
        totalincome = 0
        for i in TotalIncome:
            totalincome = i['Amount']
        cur.execute(
            f"select seller_Id,sum(Quantity_Kg) as Quantity,sum(Amount) as Amount from transaction where seller_Id='{user_id}' and month(transaction.Date_Of_Transaction)=month(curdate()) group by month(transaction.Date_Of_Transaction);")
        ThisMonthIncome = cur.fetchall();
        monthincome = 0
        for i in ThisMonthIncome:
            monthincome = i['Amount']
        cur.execute(
            f"select  mandi_board.User_Id, seller_Id, amount,Quantity, mandi_board.Trade_Charges from mandi_board join (SELECT seller_Id,sum(Quantity_Kg) as Quantity,SUM(Amount) as amount, Mandi_Board_Id FROM dbms_project.transaction  WHERE seller_Id='{user_id}' group by(seller_Id)) as temp where mandi_board.User_Id=temp.Mandi_Board_Id;")
        TotalTaxPaid = cur.fetchall();
        TotalTax = 0
        for i in TotalTaxPaid:
            TotalTax += round((i['amount'] * i['Trade_Charges']) / 100, 2)
        cur.execute(
            f"select  mandi_board.User_Id, seller_Id, amount,Quantity, mandi_board.Trade_Charges from mandi_board join (SELECT seller_Id,sum(Quantity_Kg) as Quantity,SUM(Amount) as amount, Mandi_Board_Id FROM dbms_project.transaction WHERE seller_Id='{user_id}' and month(transaction.Date_Of_Transaction)=month(curdate()) group by(seller_Id)) as temp where mandi_board.User_Id=temp.Mandi_Board_Id;")
        TaxThisMonth = cur.fetchall()
        MonthTax = 0
        for i in TaxThisMonth:
            MonthTax += round((i['amount'] * i['Trade_Charges']) / 100, 2)
        cur.close()

        print(result2)
        return render_template('/farmer/dashboard.html', max=maximum + 1000, labels=far1gh, values=far1gv,
                               max1=maximum1 + 4, labels1=far2gh, values1=far2gv, data=result1, data1=result2,
                               TotalIncome=totalincome, MonthIncome=monthincome, TotalTax=TotalTax, MonthTax=MonthTax)
    else:
        print("No username found in session")
        return redirect(url_for('check_login_info'))


@app.route('/farmer_my_policies', methods=['GET', 'POST'])
def farmer_my_policies():
    if not session.get('Username') is None:
        user_id = session.get('User_Id')
        cur = mysql.connection.cursor()
        cur.execute(
            f"select Seller_Id,seller_policy.Policy_Id,Name,Details,Date_Registeration from seller_policy join government_policy where  Seller_Id='{user_id}' and government_policy.Policy_Id=seller_policy.Policy_Id;")
        result = cur.fetchall()

        return render_template('/Farmer/my_policies.html', data = result)
    else:
        print("No username found in session")
        return redirect(url_for('check_login_info'))

@app.route('/analyst_dashboard', methods=['GET', 'POST'])
def analyst_dashboard():
    if not session.get('Username') is None:
        user_id = session.get('User_Id')
        return render_template('/Analyst/dashboard.html')
    else:
        print("No username found in session")
        return redirect(url_for('check_login_info'))


@app.route('/FPO_dashboard', methods=['GET', 'POST'])
def FPO_dashboard():
    if not session.get('Username') is None:
        user_id = session.get('User_Id')
        return render_template('/FPO/dashboard.html')
    else:
        print("No username found in session")
        return redirect(url_for('check_login_info'))


@app.route('/mandi_board__dashboard', methods=['GET', 'POST'])
def mandi_board_dashboard():
    if not session.get('Username') is None:
        user_id = session.get('User_Id')
        cursor = mysql.connection.cursor()
        cursor.execute(f"select * from mandi_board where User_Id='{user_id}';")
        name = cursor.fetchall();Mandiname='';Mandistate = '';Mandilocaltity = '';mandidistrict = '';
        for i in name:
            Mandiname = i['Name']
            Mandistate = i['State']
            Mandilocaltity = i['Locality']
            Mandidistrict = i['District']
        cursor.execute(f"select Mandi_Board_Id,Name, Trade_Charges, sum(Amount) as Amount,sum(Quantity_Kg) as Quantity from transaction join mandi_board where transaction.Mandi_Board_Id= mandi_board.User_Id  group by Mandi_Board_Id order by Amount desc;")
        table1 = cursor.fetchall()
        cursor.execute(f"select Name, temp.Mandi_Board_Id, temp.Charges from mandi_board join (select storage_mandi_board_rent.Mandi_Board_Id,sum(Charges) as Charges from storage_mandi_board_rent join storage_mandi_board where storage_mandi_board_rent.Mandi_Board_Id=storage_mandi_board.Mandi_Board_Id and storage_mandi_board_rent.Storage_Id=storage_mandi_board.Storage_Id group by storage_mandi_board_rent.Mandi_Board_Id) as temp where temp.Mandi_Board_Id=mandi_board.User_Id order by charges desc;")
        table2 = cursor.fetchall()
        count = 1
        for i in table1:
            i.update([("counter", count)])
            count = count+1
        count = 1
        for i in table2:
            i.update([("counter", count)])
            count = count+1

        year = ''; month = '';mtax=0;mspace=0
        if request.method == 'POST':
            year_month = request.form['year_month']
            # print(year_month)

            for i  in range(0, len(year_month)):
                if(year_month[i]=='-'):
                    year = year_month[:i]
                    month = year_month[i+1:len(year_month)]
            # print(year,month)

            cursor.execute(f"select month(curdate()),Mandi_Board_Id,Name, Trade_Charges, sum(Amount) as Amount,sum(Quantity_Kg) as Quantity from transaction join mandi_board where transaction.Mandi_Board_Id='{user_id}' and transaction.Mandi_Board_Id= mandi_board.User_Id and year(transaction.Date_Of_Transaction)='{year}' and month(transaction.Date_Of_Transaction)='{month}' group by Mandi_Board_Id order by Amount desc;")
            month_tax = cursor.fetchall()
            for i in month_tax:
                mtax = round((i['Amount']*i['Trade_Charges'])/100,2)
            cursor.execute(f"select storage_mandi_board_rent.Mandi_Board_Id, sum(Charges) as Charges from storage_mandi_board_rent join storage_mandi_board where storage_mandi_board.Mandi_Board_Id = '{user_id}' and year(storage_mandi_board_rent.timeFrom)='{year}' and month(storage_mandi_board_rent.timeFrom) = '{month}' and storage_mandi_board_rent.Mandi_Board_Id=storage_mandi_board.Mandi_Board_Id and storage_mandi_board_rent.Storage_Id=storage_mandi_board.Storage_Id group by storage_mandi_board_rent.Mandi_Board_Id;")
            month_space = cursor.fetchall()
            for i in month_space:
                mspace = (i['Charges'])
            # print(mtax,mspace,'post')
        else:
            cursor.execute(f"select month(curdate()),Mandi_Board_Id,Name, Trade_Charges, sum(Amount) as Amount,sum(Quantity_Kg) as Quantity from transaction join mandi_board where transaction.Mandi_Board_Id='{user_id}' and transaction.Mandi_Board_Id= mandi_board.User_Id group by Mandi_Board_Id order by Amount desc;")
            month_tax = cursor.fetchall()
            for i in month_tax:
                mtax = round((i['Amount']*i['Trade_Charges'])/100,2)
            cursor.execute(f"select storage_mandi_board_rent.Mandi_Board_Id, sum(Charges) as Charges from storage_mandi_board_rent join storage_mandi_board where storage_mandi_board.Mandi_Board_Id = '{user_id}' and storage_mandi_board_rent.Mandi_Board_Id=storage_mandi_board.Mandi_Board_Id and storage_mandi_board_rent.Storage_Id=storage_mandi_board.Storage_Id group by storage_mandi_board_rent.Mandi_Board_Id;")
            month_space = cursor.fetchall()
            for i in month_space:
                mspace = (i['Charges'])
            # print(mtax,mspace,'get')

        return render_template('/Mandi_Board/dashboard.html', data=table1,data1=table2, name=Mandiname, state=Mandistate, locality=Mandilocaltity, district=Mandidistrict, mtax=mtax, mspace=mspace)
    else:
        print("No username found in session")
        return redirect(url_for('check_login_info'))


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


@app.route('/mandi_board', methods=['GET', 'POST'])
def mandi_board():
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
            print("Mandi " + mandi_boardID_selected)
            print("Crops " + crop_selected)
        return render_template('mandi_board.html', data=mandi_data, crops_list=crops_list,
                               mandiID_output_data=all_mandi_board_data, crop_output_data=all_crop_name,profession=session['profession'])
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
        return redirect(url_for('FPO_dashboard'))

    elif session['profession'] == 'Trader':
        return redirect(url_for('trader_dashboard'))

    elif session['profession'] == 'Mandi_Board':
        return redirect(url_for('mandi_board_dashboard'))

    elif session['profession'] == 'Analyst':
        return redirect(url_for('analyst_dashboard'))

    return f"<h1>{account['Login']}</h1>"


@app.route('/check_login_info', methods=['GET', 'POST'])
def check_login_info():
    if request.method == 'POST':
        Username = request.form['Username']
        password = request.form['inputPassword']
        user_profession = request.form['profession']
        if user_profession == 'Farmer':
            cursor = mysql.connection.cursor()
            cursor.execute(f"SELECT * FROM seller WHERE Login = '{Username}' AND Password = '{password}' AND Designation = '{'F'}'")

            account = cursor.fetchone()
            cursor.close()
            if account:
                session['profession'] = user_profession
                return create_session(account)
            else:
                return render_template('Login.html')
        elif user_profession == 'FPO' :
            cursor = mysql.connection.cursor()
            cursor.execute(f"SELECT * FROM seller WHERE Login = '{Username}' AND Password = '{password}' AND Designation = '{'FP'}'")

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
