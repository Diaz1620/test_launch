from flask import Flask, render_template,request, redirect, session, flash
from mysqlconnection import connectToMySQL
from flask_bcrypt import Bcrypt
app = Flask(__name__)
app.secret_key = "keychain"
bcrypt = Bcrypt(app)

import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
name = re.compile(r'^[a-zA-Z]{2,50}$')
password = re.compile(r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,20}$')


@app.route('/')
def home():
    return render_template("index.html")

@app.route('/register', methods=['POST'])
def register():
    mysql2 = connectToMySQL('thought_dashboard')
    query2 = "SELECT email FROM users WHERE email = %(user)s;"

    is_valid = True
    if not name.match(request.form['first']):
        is_valid = False
        flash("First Name Not A Valid Entry!")
        print(request.form['first'])
    if not name.match(request.form['last']):
        is_valid = False
        flash("Last Name Not A Valid Entry!")
        print(request.form['last'])
    if not EMAIL_REGEX.match(request.form['email']):
        is_valid = False
        flash("Email Not A Valid Entry!")
        print(request.form['email'])
    for email in query2:
        if email == request.form['email']:
            is_valid = False
            flash("Email Is Already In Use")
            print(email)
    if not password.match(request.form['pass']):
        is_valid = False
        flash("Password Not A Valid Entry!")
    if request.form['confirm'] != request.form['pass']:
        is_valid = False
        flash("Passwords Must Match!")
    data2 = {
        "user": request.form["email"]
    }
    result2 = mysql2.query_db(query2,data2)
    if len(result2) > 0:
        is_valid = False
        flash("Email already in use!")
    
    if not is_valid:
        return redirect('/')
    else:
        pw_hash = bcrypt.generate_password_hash(request.form['pass'])  
        print(pw_hash)
        confirm_hash = bcrypt.generate_password_hash(request.form['confirm'])
        mysql = connectToMySQL('thought_dashboard')
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (%(fn)s, %(ln)s, %(em)s, %(pass_hash)s, Now(), Now());"
        data = {
            "fn": request.form['first'],
            "ln": request.form['last'],
            "em": request.form['email'],
            "pass_hash": pw_hash
        }
        user_id = mysql.query_db(query,data)
        # save the id in session
        session['user_id'] = user_id
        flash("Registered Successfully, Please Login To Continue")
        return redirect('/')

@app.route('/login', methods=['POST'])
def login():
    mysql = connectToMySQL('thought_dashboard')
    query = "SELECT * FROM users where email = %(email)s;"
    data = {
        "email": request.form["loginemail"]
    }
    result = mysql.query_db(query,data)
    if len(result) > 0:
        if bcrypt.check_password_hash(result[0]['password'], request.form['loginpass']):
            session['userid'] = result[0]['id']
            flash("Login Successful")
            return redirect('/success')
        else:
            flash("Email/Username Combination Incorrect!")
            return redirect('/')


@app.route('/success')
def success():
    if "userid" not in session:
        flash('Must Be Logged In To Access Content')
        return redirect('/')
    print(session['userid'])
    # get the logged in user
    mysql = connectToMySQL('thought_dashboard')
    query = "SELECT * FROM users where id = %(id)s;"
    data = {
        "id": session['userid']
    }
    name = mysql.query_db(query,data)
    # get thoughts
    mysql = connectToMySQL('thought_dashboard')
    query = "SELECT * FROM thought_dashboard.users JOIN thoughts ON users.id = thoughts.user_id;"
    thoughts_added = mysql.query_db(query,data)
    # get likes
    mysql = connectToMySQL('thought_dashboard')
    query = "SELECT count(user_id) as num_likes, thought_id FROM thought_dashboard.likes group by thought_id;"
    likes = mysql.query_db(query,data)

    return render_template('success.html', user_name = name, thoughts = thoughts_added, likes=likes)#thought_dashboard = recipe_info)

@app.route('/add_thought', methods=['POST'])
def add():
    is_valid = True
    if len(request.form['thought']) < 5:
        is_valid = False
        flash("Thought must be entered")
        flash("Thought must be 5 characters long")
        print(request.form['thought'])
    if not is_valid:
        flash("All fields are required")
        return redirect('/success')
    else:
        mysql = connectToMySQL('thought_dashboard')
        query = "INSERT INTO thoughts (content, user_id) VALUES (%(thought)s, %(user_id)s);"
        data = {
            "thought": request.form['thought'],
            "user_id": session['userid']
        }
        mysql.query_db(query,data)
        return redirect('/success')

@app.route('/user_page/<otheruser_id>')
def user_page(otheruser_id):
    if "userid" not in session:
        flash('Must Be Logged In To Access Content')
        return redirect('/')
    mysql = connectToMySQL('thought_dashboard')
    query = "SELECT * FROM users JOIN thoughts ON users.id = thoughts.user_id  WHERE users.id = %(id)s;"
    data = {
        "id": otheruser_id
    }
    other_user_name = mysql.query_db(query,data)
    return render_template('user_page.html', other_name = other_user_name)



@app.route('/like',methods=['POST'])
def like():
    mysql = connectToMySQL('thought_dashboard')
    query = "SELECT * FROM likes WHERE thought_id = %(thought)s and user_id = %(user_id)s;"
    data = {
            "thought": request.form['thought_id'],
            "user_id": session['userid']
        }
    result = mysql.query_db(query,data)
    if len(result) > 0:
        return redirect('/success')
    else:
        mysql = connectToMySQL('thought_dashboard')
        query = "INSERT INTO likes (thought_id, user_id) VALUES (%(thought)s, %(user_id)s);"
        data = {
                "thought": request.form['thought_id'],
                "user_id": session['userid']
            }
        mysql.query_db(query,data)
        return redirect('/success')

@app.route('/unlike', methods = ['POST'])
def unlike():
    mysql = connectToMySQL('thought_dashboard')
    query = "DELETE FROM thought_dashboard.likes WHERE thought_id = %(thought)s and user_id = %(user_id)s;"
    data = {
            "thought": request.form['thought_unlike'],
            "user_id": session['userid']
        }
    mysql.query_db(query,data)
    return redirect('/success')

@app.route("/delete_post/<other_user_id>", methods=['POST'])
def delete(other_user_id):
    mysql = connectToMySQL('thought_dashboard')
    query = "DELETE FROM thought_dashboard.thoughts WHERE id = %(thought)s and user_id = %(user_id)s;"
    data = {
            "thought": request.form['delete_post'],
            "user_id": other_user_id
        }
    mysql.query_db(query,data)
    return redirect('/success')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)
