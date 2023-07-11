from flask import Flask, render_template,request,flash,Markup
import mysql.connector
import pandas as pd

app=Flask(__name__)
app.secret_key='hello'
db=mysql.connector.connect(host='localhost',
                        database='project',
                        user='root',
                        password='Aakash@123')
cursor=db.cursor()

def erase(eid):
    cursor.execute("delete from candidates where eid={}".format(eid))
    cursor.execute("delete from elections_current where eid={}".format(eid))
    cursor.execute("delete from votes where eid={}".format(eid))


def check():
    cursor.execute("Select now()")
    time=cursor.fetchall()
    time=time[0]
    time=time[0]
    cursor.execute("Select * from elections_current where end_time<\'{}\'".format(time))
    finished=cursor.fetchall()
    finished_eid=[]
    for f in finished:
        finished_eid.append(f[0])
    for i,eid in enumerate(finished_eid):
        cursor.execute("select cid,count(id) as c from votes where eid={} group by cid order by c desc limit 0,1".format(eid))
        cid=cursor.fetchone()
        if(cid==None):
            erase(eid)
            db.commit()
            continue
        cid=cid[0]
        cursor.execute("select cname from candidates where cid={} and eid={}".format(cid,eid))
        winner=cursor.fetchone()
        winner=winner[0]
        description=finished[i][1]
        start_time=finished[i][2]
        end_time=finished[i][3]
        dept=finished[i][4]
        year=finished[i][5]
        rank=finished[i][6]
        cursor.execute("Insert into elections_history values({},\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',{})".format(eid,description,winner,start_time,end_time,dept,year,rank))
        erase(eid)
        db.commit()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login',methods=["GET","POST"])
def login():
    ip_address=request.remote_addr
    y=0
    cursor.execute("Select * from AdminLoggedin where IP=\'{}\'".format(ip_address))
    x=cursor.fetchall()
    if(len(x)==0):
        y=1
    if y:
        if request.method=="POST":
            username = request.form.get("username")
            password = request.form.get("password")
            cursor.execute("Select * from AdminLogin where username=\'{}\' and password=\'{}\'".format(username,password))
            x=cursor.fetchall()
            ip_address = request.remote_addr
            if(len(x)==1):
                cursor.execute("Insert into AdminLoggedin values (\'{}\')".format(ip_address))
                db.commit()
                return render_template('welcome.html')
            else:  
                return render_template('wrong_login.html')
        return render_template('login.html')
    else:
        return render_template('welcome.html')

@app.route('/signup',methods=["GET","POST"])
def signup():
    ip_address=request.remote_addr
    y=0
    cursor.execute("Select * from AdminLoggedin where IP=\'{}\'".format(ip_address))
    x=cursor.fetchall()
    if(len(x)!=0):
        y=1
    if y:
        x=0
        if request.method=="POST":
            username = request.form.get("username")
            password = request.form.get("password")
            fname=request.form.get("First_name")
            lname=request.form.get("Last_name")
            dob=request.form.get("DOB")
            address=request.form.get("Address")
            phone_number=request.form.get("Phone_Number")
            dept=request.form.get('Department')
            year=request.form.get('Year')
            rank=request.form.get('Rank')
            cursor.execute("select max(id) from UserInfo")
            id=cursor.fetchall()
            try:
                id=id[0][0]
                id+=1
            except:
                id=1
            try:
                cursor.execute("Insert into UserInfo values ({},\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',{})".format(id,fname,lname,dob,address,phone_number,dept,year,rank))
                cursor.execute("Insert into UserLogin values ({},\'{}\',\'{}\')".format(id,username,password))
            except Exception as e:
                db.rollback()
                x=1
                return "Failed Duplicate Values are not allowed",e
            if x==0:
                db.commit()
                flash("Success")
        return render_template('signup.html')
    else:
        return render_template('pls_login.html')   

@app.route('/user_login',methods=["GET","POST"])
def user_login():
    ip_address=request.remote_addr
    y=0
    cursor.execute("Select * from UserLoggedIn where IP=\'{}\'".format(ip_address))
    x=cursor.fetchall()
    if(len(x)==0):
        y=1
    if y:
        if request.method=="POST":
            username = request.form.get("username")
            password = request.form.get("password")
            cursor.execute("Select * from UserLogin where username=\'{}\' and password=\'{}\'".format(username,password))
            x=cursor.fetchall()
            ip_address = request.remote_addr
            if(len(x)==1):
                cursor.execute("Insert into UserLoggedIn values(\'{}\',{})".format(ip_address,x[0][0]))
                db.commit()
                return render_template('welcome_1.html')
            else:  
                return render_template('wrong_login.html')
        return render_template('user_login.html')     
    else:
        return render_template('welcome_1.html')

@app.route('/make_elections',methods=["GET","POST"])
def make_elections():
    ip_address = request.remote_addr
    y=0
    cursor.execute("Select * from AdminLoggedin where IP=\'{}\'".format(ip_address))
    x=cursor.fetchall()
    if(len(x)!=0):
        y=1
    if y:
        if request.method=="POST":
            description=request.form.get("description")
            start_time=request.form.get("start_time")
            end_time=request.form.get("end_time")
            dept=request.form.get("department")
            rank=request.form.get("Rank")
            year=request.form.get("Year")
            cursor.execute("Select max(eid) from elections_current")
            id=cursor.fetchall()
            cursor.execute("Select max(eid) from elections_history")
            id1=cursor.fetchall()
            id2=0
            try:
                id2=id[0][0]
                id2=max(id2,id1[0][0])+1
            except:
                try:
                    id2=id[0][0]
                    id2+=1
                except:
                    try:
                        id2=id1[0][0]
                        id2+=1
                    except:
                        id2=1
            id=id2
            y=0
            try:
                cursor.execute("Insert into elections_current values({},\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',{})".format(id,description,start_time,end_time,dept,year,rank))
            except Exception as e:
                db.rollback()
                y=1
                return "Failed {}".format(e) 
            if y==0:
                db.commit()
                return render_template('made_elec.html',value=id)
        return render_template('make_elections.html')
                
    else:
        return render_template('pls_login.html')

@app.route('/enter_candidate',methods=["GET","POST"])
def enter_candidate():
    ip_address = request.remote_addr
    y=0
    cursor.execute("Select * from AdminLoggedin where IP=\'{}\'".format(ip_address))
    x=cursor.fetchall()
    if(len(x)!=0):
        y=1
    if y:
        if request.method=="POST":
            eid=request.form.get("eid")
            name=request.form.get("name")
            description=request.form.get("description")
            cursor.execute("Select max(cid) from candidates where eid={}".format(eid))
            id=cursor.fetchall()
            x=0
            try:
                id=id[0][0]
                id+=1
            except:
                id=1
            try:
                cursor.execute("Insert into candidates values({},{},\'{}\',\'{}\')".format(eid,id,name,description))
            except:
                db.rollback()
                x=1
                return "Failure The Corresponding Election doesnt exist or is over"
            if x==0:
                db.commit()
                flash("Success")
        return render_template('enter_candidate.html')
    else:
        return render_template('pls_login.html')

@app.route('/view_eligible_elections')
def view_eligible_elections():
    ip_address=request.remote_addr
    y=0
    cursor.execute("Select * from UserLoggedIn where IP=\'{}\'".format(ip_address))
    x=cursor.fetchall()
    if(len(x)!=0):
        y=1
    if y:
        id=x[0][1]
        cursor.execute("Select dept,year,rank_ from UserInfo where id={}".format(id))
        arr=cursor.fetchall()
        arr=arr[0]
        dept=arr[0]
        year=arr[1]
        rank=arr[2]
        check()
        df=pd.read_sql("Select eid,description1,start_time,end_time,cid,cname,description from (Select * from(Select eid as e,description as description1,start_time,end_time from elections_current where (dept='0' or dept=\'{}\') and (year='0' or year=\'{}\') and (rank_=0 or rank_={}))S left outer join candidates on S.e=candidates.eid order by eid,cid) C".format(dept,year,rank),con=db)
        return df.to_html(index=False)
    else:
        return render_template('pls_login.html')

@app.route('/view_all_ongoing')
def view_all_ongoing():
    ip_address = request.remote_addr
    y=0
    cursor.execute("Select * from AdminLoggedin where IP=\'{}\'".format(ip_address))
    x=cursor.fetchall()
    if(len(x)!=0):
        y=1
    if y:
        check()
        df=pd.read_sql('select eid,description_elec,start_time,end_time,year,rank_,cid,cname,description from (select * from (select eid as e,description as description_elec,start_time,end_time,dept,year,rank_ from elections_current)S left outer join candidates on S.e=candidates.eid)C order by eid,cid',con=db)
        return df.to_html(index=False)
    else:
        return render_template('pls_login.html')

@app.route('/vote',methods=["GET","POST"])
def vote():
    ip_address=request.remote_addr
    y=0
    cursor.execute("Select * from UserLoggedIn where IP=\'{}\'".format(ip_address))
    x=cursor.fetchall()
    if(len(x)!=0):
        y=1
    if y:
        id=x[0][1]
        cursor.execute("Select dept,year,rank_ from UserInfo where id={}".format(id))
        arr=cursor.fetchall()
        arr=arr[0]
        dept=arr[0]
        year=arr[1]
        rank=arr[2]
        check()
        cursor.execute('Select eid from elections_current where (dept=\'0\' or dept=\'{}\') and (year=\'0\' or year=\'{}\') and (rank_=0 or rank_={})'.format(dept,year,rank))
        arr1=cursor.fetchall()
        a1=[]
        for a in arr1:
            a1.append(a[0])
        if request.method=="POST":
            eid=int(request.form.get("eid"))
            cid=int(request.form.get("cid"))
            if eid not in a1:
                flash("Enter the correct Election ID")
            else:
                cursor.execute('Select cid from candidates where eid={}'.format(eid))
                c=cursor.fetchall()
                c1=[]
                for c_ in c:
                    c1.append(c_[0])
                if cid not in c1:
                    flash("Enter the Correct Candidate ID")
                else:
                    cursor.execute('Select * from votes where eid={} and id={}'.format(eid,id))
                    x=cursor.fetchall()
                    if(len(x)==0):
                        cursor.execute("Insert into votes values({},{},{})".format(eid,id,cid))
                        db.commit()
                        flash("Success")
                    else:
                        cursor.execute("Update votes set cid={} where eid={} and id={}".format(cid,eid,id))
                        db.commit()
                        flash("Success")
        return render_template('election.html')
    else:
        return render_template('pls_login.html')

@app.route('/view_completed_elections')
def view():
    ip_address = request.remote_addr
    y=0
    cursor.execute("Select * from AdminLoggedin where IP=\'{}\'".format(ip_address))
    x=cursor.fetchall()
    if(len(x)!=0):
        y=1
    if y:
        check()
        df=pd.read_sql("Select * from elections_history",con=db)
        return df.to_html(index=False)
    else:
        return render_template('pls_login.html')

@app.route('/view_completed_elections_user')
def view_user():
    ip_address = request.remote_addr
    y=0
    cursor.execute("Select * from UserLoggedIn where IP=\'{}\'".format(ip_address))
    x=cursor.fetchall()
    if(len(x)!=0):
        y=1
    if y:
        id=x[0][1]
        cursor.execute("Select dept,year,rank_ from UserInfo where id={}".format(id))
        arr=cursor.fetchall()
        arr=arr[0]
        dept=arr[0]
        year=arr[1]
        rank=arr[2]
        check()
        df=pd.read_sql("Select eid,description,start_time,end_time,winner from elections_history where (dept='0' or dept=\'{}\') and (year='0' or year=\'{}\') and (rank_=0 or rank_={})".format(dept,year,rank),con=db)
        return df.to_html(index=False)
    else:
        return render_template('pls_login.html')

@app.route('/change_password',methods=["GET","POST"])
def change_password():
    ip_address = request.remote_addr
    y=0
    cursor.execute("Select * from UserLoggedIn where IP=\'{}\'".format(ip_address))
    x=cursor.fetchall()
    if(len(x)!=0):
        y=1
    if y:
        id=x[0][1]
        if request.method=="POST":
            new_password=request.form.get("password")
            cursor.execute("Update UserLogin set password=\'{}\' where id={}".format(new_password,id))
            db.commit()
            flash("Success")
        return render_template('change_password.html')
    else:
        return render_template('pls_login.html')
        

@app.route('/logout')
def logout():
    ip_address = request.remote_addr
    cursor.execute("Delete from AdminLoggedin where IP=\'{}\'".format(ip_address))
    db.commit()
    return render_template('logout.html')

@app.route('/user_logout')
def user_logout():
    ip_address = request.remote_addr
    cursor.execute("Delete from UserLoggedIn where IP=\'{}\'".format(ip_address))
    db.commit()
    return render_template('logout.html')

@app.route('/remove_user',methods=["GET","POST"])
def remove_user():
    ip_address = request.remote_addr
    y=0
    cursor.execute("Select * from AdminLoggedin where IP=\'{}\'".format(ip_address))
    x=cursor.fetchall()
    if(len(x)!=0):
        y=1
    if y:
        if request.method=="POST":
            username=request.form.get("username")
            cursor.execute("Select id from UserLogin where username=\'{}\'".format(username))
            id=cursor.fetchone()
            if id==None:
                flash("Failed Enter Valid Username")
            else:
                id=id[0]
                cursor.execute("Delete from UserInfo where id={}".format(id))
                cursor.execute("Delete from UserLogin where id={}".format(id))
                cursor.execute("Delete from UserLoggedIn where id={}".format(id))
                db.commit()
                flash("Success")
        return render_template('remove_user.html')
    else:
        return render_template('pls_login.html')


if __name__=="__main__":
    app.run(debug=True)
