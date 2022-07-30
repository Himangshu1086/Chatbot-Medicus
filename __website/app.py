from time import time
from flask import Flask,redirect,url_for,render_template,request
import util
import time 

# jinja2 technique
'''
{{ value }}expression 
{%  %}statment
{#.....#}comment

'''
app=Flask(__name__)



@app.route('/')
def fun():
    return render_template('home.html')




@app.route('/submit',methods=['GET','POST'])
def submit():
    if request.method=='POST':
        res= dict(request.form)
        qns = res['query']
        ans = util.chat_response(qns)
        qn = util.get_text()
        print(qn)
        return render_template('home.html' , query = qns , answer=ans , top_five = qn)


@app.route('/top-five-query',methods=['GET','POST'])
def top_five_query():
    if request.method=='POST':
        res= dict(request.form)
        query_2 = int(res['query2'])
        txt = util.get_text()
        ans = util.query_2nd( txt[0][1] , query_2)   
        return render_template("home.html",answer = ans,query="query" )



if __name__=='__main__':
    app.run(debug=True)