from flask import Flask,redirect,url_for,render_template,request
import pymysql
import pymysql.cursors
app = Flask(__name__)

# Connect to the database.
def connect():
	print("connected")
	connection = pymysql.connect(host='localhost',
                             user='root',
                             password='deepanjali@2000',                             
                             db='grocery',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
	cursor = connection.cursor()
	return connection,cursor



#home
@app.route('/',methods=['GET','POST'])
def main():
	return render_template('home.html')
	print("inside home")
	# return render_template('index.html')
	if request.method=='POST':
		if request.form['Login']:
			return redirect(url_for('loginlink'))
		if request.form['Sign Up']:
			return redirect(url_for('signup'))
		if request.form['Admin']:
			return redirect(url_for('admin_login'))
		else:
			if request.method == 'GET':
				return render_template('home.html')



@app.route('/loginlink',methods = ['GET','POST'])
def loginlink():
	return render_template('login.html')

#storing signup details in db
@app.route('/signup',methods = ['GET','POST'])
def signup():
	connection,cursor=connect()
	print("enetred signup")
	error = None
	if request.method=='POST':
		inp = request.form
		name = inp['Username']
		password = inp['Password']
		email = inp['Email']
		phone = inp['Phone']
		cursor.execute("select email from user where email=%s",(str(email),))
		data = cursor.fetchall()
		if data:
			return redirect(url_for('loginlink'))
		else:
			querry = "insert into user values(%s,%s,%s,%s)"
			cursor.execute(querry,(name,password,email,phone))
			connection.commit()
			connection.close()	
			print("inserted")
			return redirect(url_for('login'))
	return render_template('signup.html')



#checking if usn matched from database else return signup page
@app.route('/login',methods = ['GET','POST'])
def login():
	connection,cursor=connect()
	if request.method=='POST':
		inp = request.form
		name = inp['Username']
		pas = inp['Password']
		cursor = connection.cursor()
		querry = "select password from user where username=%s"
		cursor.execute(querry,(name,))
		result = cursor.fetchall()
		if result: 
			tempp = str(result[0]['password'])
			if tempp == str(pas):
				return redirect(url_for('index'))
			else:
				return redirect(url_for('login'))
		else:
			return redirect(url_for('signup'))
	connection.close()
	return render_template('login.html')	


@app.route('/index',methods = ['GET','POST'])
def index():
	return render_template('index.html')


@app.route('/products',methods = ['GET','POST'])
def products():
	return render_template('products.html')


if __name__ == '__main__':
	app.run(debug=True)