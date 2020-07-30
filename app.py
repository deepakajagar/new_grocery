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
	return render_template('index.html')
	print("inside home")
	# return render_template('index.html')
	if request.method=='POST':
		if request.form['Login']:
			return redirect(url_for('login'))
		if request.form['Sign Up']:
			return redirect(url_for('signup'))
		if request.form['Admin']:
			return redirect(url_for('admin_login'))
		else:
			if request.method == 'GET':
				return render_template('home.html')



#storing signup details in db
@app.route('/login',methods = ['GET','POST'])
def login():
	connection,cursor=connect()
	print("enetred login")
	if request.method=='POST':
		inp = request.form
		name = inp['Username']
		password = inp['Password']
		email = inp['Email']
		phone = inp['Phone']
		cursor.execute("select email from user where email=%s",(str(email),))
		data = cursor.fetchall()
		if data:
			return print("email already exists")
		else:
			querry = "insert into user values(%s,%s,%s,%s,%s)"
			cursor.execute(querry,(name,password,email,phone))
			connection.commit()
			connection.close()	
			return print("inserted successfully")
	return render_template('index.html')

@app.route('/index/')
def index():
	return print("index opened")



if __name__ == '__main__':
	app.run(debug=True)