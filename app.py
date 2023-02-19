from flask import Flask, render_template, request, url_for, flash
from werkzeug.utils import redirect
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'many random bytes'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'crud'

mysql = MySQL(app)



@app.route('/')
def Index():

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM todos")
    data = cur.fetchall()
    cur.close()

    return render_template('index.html', todos = data)


@app.route('/insert', methods = ['POST'])
def insert():
    if request.method == "POST":
        flash("Data Inserted Successfully")
        title = request.form['title']
        description = request.form['description']
        remarks = request.form['remarks']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO todos (title, description, remarks) VALUES (%s, %s, %s)", (title, description, remarks))
        mysql.connection.commit()
        return redirect(url_for('Index'))

@app.route('/delete/<string:id_data>', methods = ['POST', 'GET'])
def delete(id_data):
    flash("Record Has Been Deleted Successfully")
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM todos WHERE id=%s", (id_data,))
    mysql.connection.commit()
    
    return redirect(url_for('Index'))

    # cur.close()



@app.route('/update', methods= ['POST', 'GET'])
def update():
    if request.method == 'POST':
        id_data = request.form['id']
        title = request.form['title']
        description = request.form['description']
        remarks = request.form['remarks']

        cur = mysql.connection.cursor()
        cur.execute("""
        UPDATE todos SET title=%s, description=%s, remarks=%s
        WHERE id=%s
        """, (title, description, remarks, id_data))
        mysql.connection.commit()
        flash("Data Updated Successfully")
        return redirect(url_for('Index'))




if __name__ == "__main__":
    app.run(debug=True)
