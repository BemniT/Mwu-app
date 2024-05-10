from flask import *
import pyrebase
import uuid


firebaseConfig={
     "apiKey": "AIzaSyDFzehYTECLohOI8O1hHY5C32p2CWHlPGE",
  "authDomain": "mwu-app-219e9.firebaseapp.com",
  "projectId": "mwu-app-219e9",
  "storageBucket": "mwu-app-219e9.appspot.com",
  "messagingSenderId": "298667497938",
  "appId": "1:298667497938:web:8ac9e0be713b2d4b64d00b",
  "measurementId": "G-F0VZGF9JNM",
  "databaseURL":"https://mwu-app-219e9-default-rtdb.firebaseio.com"
}

app = Flask(__name__)
app.secret_key = '@bemnet1221'
firebase = pyrebase.initialize_app(firebaseConfig)

real_db = firebase.database()
storage = firebase.storage()


@app.route('/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['firstName']
        last_name = request.form['lastName']
        email = request.form['signupEmail']
        password = request.form['signupPassword']
        gender = request.form['sex']
        age = request.form['age']
        datetime = request.form['dateTimePicker']

        user_id = str(uuid.uuid4())
        user_data = {
                "firstname":first_name,
               "lastname":last_name,
               "email":email,
               "age":age,
               "gender":gender,
               "datetime":datetime,
               "user_id":user_id,
               "password":password
        }
        real_db.child('User').child(user_id).set(user_data)
        flash('Registration successful. You can now login.', 'success')
        return redirect(url_for('login'))

    return render_template('index.html')

@app.route('/login.html', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_name = request.form['user_name']
        password = request.form['password']
        
        user = real_db.child('User').order_by_child("email").equal_to(user_name).get().val()
        
        if user:
            user_id = list(user.keys())[0]
            user_data = user[user_id]
            
            if password == user_data.get('password'):
                # Session management
                session['user_id'] = user_id
                session['user_name'] = user_name
                session['user_data'] = user_data
                
                return redirect(url_for('profile'))
            else:
                flash('Incorrect password. Please try again.', 'error')
        else:
            flash('User not found. Please register first.', 'error')
    
    return render_template('login.html')
@app.route('/adminLogin.html')
def adminLogin():
        
        return render_template('adminLogin.html')
@app.route('/profile.html')
def profile():
        return render_template('profile.html')
@app.route('/edit', methods=['GET', 'POST'])
def edit():
    if 'user_id' in session:
        user_id = session['user_id']
        user_name = session['user_name']
        user_data = session['user_data']
        
        if request.method == 'POST':
            first_name = request.form['firstName']
            last_name = request.form['lastName']
            email = request.form['email']
            age = request.form['age']
            gender = request.form['sex']
            datetime = request.form['dateOfBirth']
            
            # Update user data in session
            user_data['firstname'] = first_name
            user_data['lastname'] = last_name
            user_data['email'] = email
            user_data['age'] = age
            user_data['gender'] = gender
            user_data['datetime'] = datetime
            
            # Update user data in the database
            real_db.child('User').child(user_id).update({
                'firstname': first_name,
                'lastname': last_name,
                'email': email,
                'age': age,
                'gender': gender,
                'datetime': datetime
            })
            
            # Update session with new user data
            session['user_data'] = user_data
            
            flash('Profile updated successfully', 'success')
        
        return render_template('edit_profile.html', user_name=user_name, user_data=user_data)
    else:
        flash('User not logged in', 'error')
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
        session.clear
        return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)