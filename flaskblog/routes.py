from flask import render_template, url_for, flash, redirect, request, session,jsonify
from flaskblog import app, bcrypt , mail
from flaskblog.forms import ConsentForm, PersonalForm, QuestionnaireForm
#from flaskblog.models import User, Post
#from flask_login import login_user, current_user, logout_user,login_required
from flask_mail import Message
import random,time,json
from datetime import datetime
import pandas as pd

buttonss = ["login,log"]

def checkTime():
    if session.get('Experiment-Active'):
            if session.get('Total-Time'):

                t1 = session['Total-Time']
            else:
                t1 = 0
            if session.get('Trail-Task-1-Time'):
                t2 = session['Trail-Task-1-Time']
            else:
                t2 = 0

            if session.get('Trail-Task-2-Time'):
                t3 = session['Trail-Task-2-Time']
            else:
                t3 = 0
                
            return [t1,t2,t3]
    else:
        return [-1,-1,-1]


def startsession():
    if session.get('Experiment-Active')==True:
        pass
    else:
        session['Experiment-Active'] = True
        session['Total-Time'] = int(time.time())   
    print(session)


def make_csv(my_dict):
        
    value = ",".join(my_dict.keys())+'\n'
    for i in range(len(my_dict[list(my_dict.keys())[0]])): 
        temp = ""
        for counter,j in enumerate(my_dict.keys()): 
            string = str(my_dict[j][i])
            if counter == 0:
                temp += string
            else:
                temp = ",".join([temp,string])
        value+= "%s\n"%(temp)
    return value

def endsession():
    now = datetime.now() # current date and time
    Date = now.strftime("%m/%d/%Y")
    
    #Date = "%s %s %s"%(self.Day.text(),self.Month.text(),self.Year.text())
    initials = ""
    if session.get('Initials') is not None:
        initials = session['Initials']
    folderName = "%s %s"%(initials,Date)

    msg = Message(folderName, sender = 'noreply@demo.com',
    recipients=['alibahadur1513@gmail.com','alibabadur1535@gmail.com'])
    
    QuestionnaireAnswers = {"Question No":[x for x in range(1,31)], "Answers":[0 for x in range(1,31)]}
    MentalQuestionnaireAnswers = {"Question No":[x for x in range(1,15)],"Output":['A1', 'D1', 'A2', 'D2', 'A3', 'D3', 'A4', 'D4', 'A5', 'D5', 'A6', 'D6', 'A7', 'D7'], "Answers":[0 for x in range(1,16)]}

    if session.get('Questions1_5'):
        QuestionnaireAnswers["Answers"][0:5] = session['Questions1_5']
    if session.get('Questions6_10'):
        QuestionnaireAnswers["Answers"][5:10] = session['Questions6_10']
    if session.get('Questions11_15'):
        QuestionnaireAnswers["Answers"][10:15] = session['Questions11_15']
    if session.get('Questions16_20'):
        QuestionnaireAnswers["Answers"][15:20] = session['Questions16_20']
    if session.get('Questions21_25'):
        QuestionnaireAnswers["Answers"][20:25] = session['Questions21_25']
    if session.get('Questions25_30'):
        QuestionnaireAnswers["Answers"][25:30] = session['Questions25_30']

    msg.attach("Questionnaire Output.csv", "text/csv", make_csv(QuestionnaireAnswers))

    if session.get('MQuestions1_5'):
        MentalQuestionnaireAnswers["Answers"][0:5] = session['MQuestions1_5']
    if session.get('MQuestions6_10'):
        MentalQuestionnaireAnswers["Answers"][5:10] = session['MQuestions6_10']
    if session.get('MQuestions11_15'):
        MentalQuestionnaireAnswers["Answers"][10:15] = session['MQuestions11_15']

    msg.attach("Mental Well-Being Questionnaire Output.csv", "text/csv", make_csv(MentalQuestionnaireAnswers))

    Quality=50
    if session.get('Quality'):
        Quality = session['Quality']

    msg.attach("Mental Well-Being Questionnaire Output.csv", "text/csv", "Quality of Life Ranking\n%s"%Quality)

    times = checkTime()
    if times[0]==-1:
        times = ["","",""]

    msg.attach("Experiment Times.csv", "text/csv", make_csv({"Trail Task 2nd Step Time":[times[1]], "Trail Task 4th Step Time":[times[2]],"Total Experimet Time":[time.strftime("%H:%M:%S", time.gmtime(time.time()-times[0]))]}))

    if session.get('keyPresses'):
        keyG = session['keyPresses']['KeyG']
        keyB = session['keyPresses']['KeyB']
        keyF = session['keyPresses']['KeyF']
        for key in keyF:
            KeyFPressTimes = [[],[]]
            ti = int(key)
            KeyFPressTimes[0].append(time.strftime("%H:%M:%S", time.gmtime(ti)))
            if (0 <=(ti%30)) and ((ti%30) <=30): 
                KeyFPressTimes[1].append(1)
            else:
                KeyFPressTimes[1].append(0)
    else:
        keyG = "0"
        keyB = "0"
        KeyFPressTimes = [[],[]]

    user_input=""
    if session.get('User-Input') is not None:
        user_input = session['User-Input']

    msg.attach("Key G B Pressed Time.csv", "text/csv", make_csv({"User Input":[user_input],"Sun": [keyG],"Moon":[keyB]}))
    msg.attach("Key F Pressed Time.csv", "text/csv", make_csv({"Pressed Time":KeyFPressTimes[0],"Output":KeyFPressTimes[1]}))

        
    dictionary = {""}
    if session.get('Personal') is not None:
        dictionary = {"Category":["Date","Initials","Sex","Age","Highest Level Of Education","Country of Residence","Years in the country","Ethnicity","Job Occupation","Substance Abuse"],
                         "User Input":[Date,initials,*session['Personal']]}
    

    msg.attach("Personal Information.csv", "text/csv", make_csv(dictionary))
    
    mail.send(msg)

    #print(session)
    #session.clear()
    #print(session)

def pageCheck(page):
    if session.get('Current-Page'):
        if session.get('Max-Page'):
            if session.get('Experiment-Active'):
                pass                
            else:
                session['Max-Page'] = 3
                
            if page==(session['Max-Page']+1):
                session['Current-Page'] = page
                session['Max-Page'] = page
                if page == 19 :
                    session['Max-Page'] = 1
                    return

            elif page<=session['Max-Page']:
                session['Current-Page'] = page
            

        else:
            session['Current-Page'] = 1
            session['Max-Page'] = 1

    else:
        session.clear()
        session['Current-Page'] = 1
        session['Max-Page'] = 1
        


@app.route("/")
@app.route("/Page-1",methods = ['GET','POST'])
def page1():
    pageCheck(1)
    return render_template('home.html', posts = [1,"login","Register"],times=checkTime())

@app.route("/Page-2",methods = ['GET','POST'])
def page2():
    pageCheck(2)
    if session['Current-Page'] != 2:
        return redirect(url_for('page%i'%session['Current-Page']))

    form = ConsentForm()
    page = int(request.args.get('page',2))
    print(page,form.validate(),request.args.get('next'))
    if form.validate_on_submit(): 
        session["Consent"] = True
        session["Initials"] = form.initials.data
        
        return redirect(url_for('page3'))

    if session.get("Consent"):
  
        form.consent1.data = True
        form.consent2.data = True
        form.consent3.data = True
        form.consent4.data = True
        form.consent5.data = True
        form.consent6.data = True
        form.consent7.data = True
        form.initials.data = session.get('Initials')
    return render_template('page2.html', title='Consent Form', form=form,times=checkTime())
    

@app.route("/Page-3",methods = ['GET','POST'])
def page3():
    pageCheck(3)
    if session['Current-Page'] != 3:
        return redirect(url_for('page%i'%session['Current-Page']))

    page = int(request.args.get('page',3))
    if page == 2:
        return redirect(url_for('page2'))

            

    return render_template('page3.html', posts = [],times=checkTime())

@app.route("/Page-4",methods = ['GET','POST'])
def page4():
    pageCheck(4)
    if session['Current-Page'] != 4:
        return redirect(url_for('page%i'%session['Current-Page']))

    startsession()
    #session['Total-Time'] = int(time.time())

    #session['Experiment-Active'] = True
    form = PersonalForm()
    if form.validate_on_submit(): 
        session["Personal"] = [form.gender.data,form.age.data,form.education.data,form.country.data,form.stay.data,form.ethinicity.data,form.job.data,form.society.data]
        print(session["Personal"])
        return redirect(url_for('page5'))

    if session.get("Personal"):
        form.gender.data =session.get("Personal")[0] 
        form.age.data = session.get("Personal")[1]
        form.education.data = session.get("Personal")[2]
        form.country.data = session.get("Personal")[3]
        form.stay.data = session.get("Personal")[4]
        form.ethinicity.data = session.get("Personal")[5]
        form.job.data = session.get("Personal")[6]
        form.society.data = session.get("Personal")[7]
    return render_template('page4.html', title='Consent Form', form=form,times=checkTime())

@app.route("/Page-5",methods = ['GET','POST'])
def page5():
    pageCheck(5)
    if session['Current-Page'] != 5:
        return redirect(url_for('page%i'%session['Current-Page']))

    if request.method == 'POST':
        print(request.form,'shit')
        
      
        session['User-Input'] = request.form['index']

        if request.form.get('Next'):
            return redirect(url_for('page6'))
        elif request.form.get('Previous'):
            return redirect(url_for('page4'))


    if session.get('User-Input'):
        done = session.get('User-Input')
    else:
        done = ''
    return render_template('page5.html',done=done,times=checkTime())

@app.route("/Page-6",methods = ['GET','POST'])
def page6():
    pageCheck(6)
    if session['Current-Page'] != 6:
        return redirect(url_for('page%i'%session['Current-Page']))
    #session.pop('Trail-Task-1')
    if  request.method=="POST":
        print(request.form,'shit')

        session['Trail-Task-1'] = True
        if request.form.get('t1time') :
            session['Trail-Task-1-Time'] = request.form['t1time']
        else:        
            t1time="0"

        if request.form.get('Next'):
            return redirect(url_for('page7'))
        elif request.form.get('Previous'):
            return redirect(url_for('page5'))

    if session.get('Trail-Task-1'):
        if session.get('Trail-Task-1-Time') :
            t1time=session['Trail-Task-1-Time']
        else:        
            t1time="0"
            
        done = '2'
        data = session.get('Trail-Task-1-Sequence')
    else:
        t1time="0"
        data = [str(i) for i in range(1,26)]
        done='1'
        session['Trail-Task-1-Sequence']=data
        random.shuffle(data)
        
    print("DONE:",done)
    return render_template('page6.html',data = data, done=done,t1time=t1time,times=checkTime())

@app.route("/Page-7",methods = ['GET','POST'])
def page7():
    pageCheck(7)
    if session['Current-Page'] != 7:
        return redirect(url_for('page%i'%session['Current-Page']))
    return render_template('page7.html',times=checkTime())

@app.route("/Page-8",methods = ['GET','POST'])
def page8():
    pageCheck(8)
    if session['Current-Page'] != 8:
        return redirect(url_for('page%i'%session['Current-Page']))

    #session.pop('Trail-Task-2')

    print(request.form)

    if  request.method=="POST":
        print(request.form,'shit')

        if request.form.get('t2time') :
            session['Trail-Task-2-Time'] = request.form['t2time']
        else:        
            t2time="0"

        session['Trail-Task-2'] = True
        if request.form.get('Next'):
            return redirect(url_for('page9'))
        elif request.form.get('Previous'):
            return redirect(url_for('page7'))
    
    if session.get('Trail-Task-2'):
        if session.get('Trail-Task-2-Time') :
            t2time=session['Trail-Task-2-Time']
        else:        
            t2time="0"

        done = '2'
        data = session.get('Trail-Task-2-Sequence')
    else:
        t2time="0"
        done='1'
        data = ['1','A', '2', 'B' ,'3', 'C', '4','D' ,'5','E', '6','F', '7', 'G', '8', 'H' ,'9','I' ,'10', 'J','11','K' ,'12', 'L']
        session['Trail-Task-2-Sequence']=data
        random.shuffle(data)
        
    return render_template('page8.html',  data = data ,done = done,t2time=t2time,times=checkTime())

@app.route('/postmethod', methods = ['POST'])
def get_post_javascript_data():
    jsdata = request.form['javascript_data']
    return jsdata


@app.route("/Page-9",methods = ['GET','POST'])
def page9():
    pageCheck(9)
    if session['Current-Page'] != 9:
        return redirect(url_for('page%i'%session['Current-Page']))

    print(request.form)
    if request.method=="POST":
        session['Questions1_5'] = [0,0,0,0,0]
        for i in request.form.keys():
            session['Questions1_5'][int(i[7:])-1] = int(request.form[i])

        if len(list(request.form.keys()))<5:
            flash('Please select all the questions', 'danger')
        else:
            return redirect(url_for('page10'))

    datas = [0,0,0,0,0]
    if session.get("Questions1_5"):
        for i in range(0,5):
            datas[i] = session['Questions1_5'][i]

    return render_template('page9.html', data = datas,times=checkTime())

@app.route("/Page-10",methods = ['GET','POST'])
def page10():
    pageCheck(10)
    if session['Current-Page'] != 10:
        return redirect(url_for('page%i'%session['Current-Page']))

    #session.pop('Sun-Show')
    print(request.form)
    if request.method=="POST":
        session['Sun-Show'] = True
        session['Questions6_10'] = [0,0,0,0,0]
        for i in request.form.keys():
            if i[:7]=="options":
                session['Questions6_10'][int(i[7:])-1] = int(request.form[i])

        if request.form.get('Next'):
            if len(list(request.form.keys()))<6:
                flash('Please select all the questions', 'danger')
            else:
                return redirect(url_for('page11'))
        elif request.form.get('Previous'):
            return redirect(url_for('page9'))
        

    if session.get('Sun-Show'):
        done = False
    else:
        done = True

    datas = [0,0,0,0,0]
    if session.get("Questions6_10"):
        for i in range(0,5):
            datas[i] = session['Questions6_10'][i]

    return render_template('page10.html', data = datas, done=done,times=checkTime())

@app.route("/Page-11",methods = ['GET','POST'])
def page11():
    pageCheck(11)
    if session['Current-Page'] != 11:
        return redirect(url_for('page%i'%session['Current-Page']))

    print(request.form)
    if request.method=="POST":
        session['Questions11_15'] = [0,0,0,0,0]
        for i in request.form.keys():
            session['Questions11_15'][int(i[7:])-1] = int(request.form[i])

        if len(list(request.form.keys()))<5:
            flash('Please select all the questions', 'danger')
        else:
            return redirect(url_for('page12'))

    datas = [0,0,0,0,0]
    if session.get("Questions11_15"):
        for i in range(0,5):
            datas[i] = session['Questions11_15'][i]

    return render_template('page11.html', data = datas,times=checkTime())

@app.route("/Page-12",methods = ['GET','POST'])
def page12():
    pageCheck(12)
    if session['Current-Page'] != 12:
        return redirect(url_for('page%i'%session['Current-Page']))

    print(request.form)
    if request.method=="POST":
        session['Questions16_20'] = [0,0,0,0,0]
        for i in request.form.keys():
            session['Questions16_20'][int(i[7:])-1] = int(request.form[i])

        if len(list(request.form.keys()))<5:
            flash('Please select all the questions', 'danger')
        else:
            return redirect(url_for('page13'))

    datas = [0,0,0,0,0]
    if session.get("Questions16_20"):
        for i in range(0,5):
            datas[i] = session['Questions16_20'][i]

    return render_template('page12.html', data = datas,times=checkTime())


@app.route("/Page-13",methods = ['GET','POST'])
def page13():
    pageCheck(13)
    if session['Current-Page'] != 13:
        return redirect(url_for('page%i'%session['Current-Page']))

    print(request.form)
    if request.method=="POST":
        session['Questions21_25'] = [0,0,0,0,0]
        for i in request.form.keys():
            session['Questions21_25'][int(i[7:])-1] = int(request.form[i])

        if len(list(request.form.keys()))<5:
            flash('Please select all the questions', 'danger')
        else:
            return redirect(url_for('page14'))

    datas = [0,0,0,0,0]
    if session.get("Questions21_25"):
        for i in range(0,5):
            datas[i] = session['Questions21_25'][i]

    return render_template('page13.html', data = datas,times=checkTime())

@app.route("/Page-14",methods = ['GET','POST'])
def page14():
    pageCheck(14)
    if session['Current-Page'] != 14:
        return redirect(url_for('page%i'%session['Current-Page']))

    print(request.form)
    if request.method=="POST":
        session['Questions25_30'] = [0,0,0,0,0]
        for i in request.form.keys():
            session['Questions25_30'][int(i[7:])-1] = int(request.form[i])

        if len(list(request.form.keys()))<5:
            flash('Please select all the questions', 'danger')
        else:
            return redirect(url_for('page15'))

    datas = [0,0,0,0,0]
    if session.get("Questions25_30"):
        for i in range(0,5):
            datas[i] = session['Questions25_30'][i]

    return render_template('page14.html', data = datas,times=checkTime())


@app.route("/Page-15",methods = ['GET','POST'])
def page15():
    pageCheck(15)
    if session['Current-Page'] != 15:
        return redirect(url_for('page%i'%session['Current-Page']))

    if request.method=="POST":
        print(request.form)
        session['Quality'] = request.form['slider']
        return redirect(url_for('page16'))

    data = 50
    if session.get("Quality"):
        data = session['Quality']

    return render_template('page15.html',data =data,times=checkTime())



@app.route("/Page-16",methods = ['GET','POST'])
def page16():
    pageCheck(16)
    if session['Current-Page'] != 16:
        return redirect(url_for('page%i'%session['Current-Page']))

    #session.pop('Moon-Show')
    print(request.form)
    if request.method=="POST":
        session['Moon-Show'] = True

        session['MQuestions1_5'] = [-1,-1,-1,-1,-1]
        for i in request.form.keys():
            if i[:7]=="options":
                session['MQuestions1_5'][int(i[7:])-1] = int(request.form[i])

        if request.form.get('Next'):
            if len(list(request.form.keys()))<6:
                flash('Please select all the questions', 'danger')
            else:
                return redirect(url_for('page17'))
        elif request.form.get('Previous'):
            return redirect(url_for('page15'))

    
    if session.get('Moon-Show'):
        done = False
    else:
        done = True

    datas = [-1,-1,-1,-1,-1]
    if session.get("MQuestions1_5"):
        for i in range(0,5):
            datas[i] = session['MQuestions1_5'][i]

    return render_template('page16.html', data = datas,done=done,times=checkTime())


@app.route("/Page-17",methods = ['GET','POST'])
def page17():
    pageCheck(17)
    if session['Current-Page'] != 17:
        return redirect(url_for('page%i'%session['Current-Page']))

    print(request.form)
    if request.method=="POST":
        
        session['MQuestions6_10'] = [-1,-1,-1,-1,-1]
        for i in request.form.keys():
            session['MQuestions6_10'][int(i[7:])-1] = int(request.form[i])

        if len(list(request.form.keys()))<5:
            flash('Please select all the questions', 'danger')
        else:
            return redirect(url_for('page18'))
    datas = [-1,-1,-1,-1,-1]
    if session.get("MQuestions6_10"):
        for i in range(0,5):
            datas[i] = session['MQuestions6_10'][i]

    return render_template('page17.html', data = datas,times=checkTime())

@app.route("/Page-18",methods = ['GET','POST'])
def page18():
    pageCheck(18)
    if session['Current-Page'] != 18:
        return redirect(url_for('page%i'%session['Current-Page']))

    if request.get_json(force=True, silent=True):
        session['keyPresses'] = request.get_json(force=True, silent=True)
        #print(session['keyPresses'])

    if request.method=="POST":

        session['MQuestions11_14'] = [-1,-1,-1,-1,-1]
        for i in request.form.keys():
            session['MQuestions11_14'][int(i[7:])-1] = int(request.form[i])

        if len(list(request.form.keys()))<4:
            flash('Please select all the questions', 'danger')
        else:
            endsession()
            return redirect(url_for('page19'))

    datas = [-1,-1,-1,-1,-1]
    if session.get("MQuestions11_14"):
        for i in range(0,5):
            datas[i] = session['MQuestions11_14'][i]

    return render_template('page18.html', data = datas,times=checkTime())

@app.route("/Page-19",methods = ['GET','POST'])
def page19():
    pageCheck(19)
    if session['Current-Page'] != 19:
        return redirect(url_for('page%i'%session['Current-Page']))
    session.clear()
    
    flash('Experimet Completed!', 'success')
    return render_template('page19.html',times=checkTime())


@app.route("/withdraw",methods = ['GET','POST'])
def withdraw():
    session.clear()
    return redirect(url_for('page1'))


