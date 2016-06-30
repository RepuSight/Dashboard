from app import app, lm
from flask import request, redirect, render_template, url_for, flash,session
from flask.ext.login import login_user, logout_user, login_required
from .forms import LoginForm
from .user import User
from datetime import datetime
import pandas as pd
import json,time
from collections import defaultdict
import os, sys,csv
from pymongo import MongoClient
from bson import json_util

# from bson.json_util import dumps, loads
ip='127.0.0.1'
dbname="restaurent"
collectionname="data"
TopicCategories=["service","drink","value","hospitality","food","ambience"]


@app.route('/grouphotel',methods=["POST"])
def grouphotel():
	user_obj=session.get('user', None)
	user_obj['group'].append(user_obj['hotel'])
	test= list(set(user_obj['group']))
	return json.dumps(test)

@app.route('/hotel',methods=["POST"])
def hotel():
	client = MongoClient(ip, 27017)
	db = client[dbname]
	collection=db[collectionname]
	tags = collection.distinct("Name")
	client.close()
	return json.dumps(tags)

@app.route('/sentiment',methods=["POST"])
def sentiment(self):
	client = MongoClient(ip, 27017)
	db = client[dbname]
	collection=db[collectionname]
	tags = collection.distinct("Sentiment")
	client.close()
	return json.dumps(tags)
	
@app.route('/topic',methods=["POST"])
def  topic():
	tags=TopicCategories
	return json.dumps(tags)


@app.route('/channel',methods=["POST"])
def  channel():
	client = MongoClient(ip, 27017)
	db = client[dbname]
	collection=db[collectionname]
	tags = collection.distinct("Channel")
	client.close()
	return json.dumps(tags)

@app.route('/competive',methods=["POST"])
def  competive():
	client = MongoClient(ip, 27017)
	db = client[dbname]
	collection=db[collectionname]
	restd=collection.distinct("Name")
	user_obj=session.get('user', None)
	user_obj['group'].append(user_obj['hotel'])
	test= list(set(user_obj['group']))
	tags = list(set(test).intersection(restd))
	filter =request.get_json(force=True)
	startdate=int(time.mktime(datetime.strptime(filter['startdate'],'%d/%m/%Y').timetuple()))
	enddate=int(time.mktime(datetime.strptime(filter['enddate'],'%d/%m/%Y').timetuple()))
	data=[]
	for hotels in tags:
		name=hotels
		total_reviews_prev=collection.find({'Name': hotels,'Date':{'$gte': 2*startdate-enddate ,'$lt': startdate}}).count()
		postive_reviews_prev=collection.find({'Name': hotels,'Sentiment':'Postive','Date':{'$gte': 2*startdate-enddate, '$lt': startdate}}).count()
		negative_reviews_prev=collection.find({'Name': hotels,'Sentiment':'Negative','Date':{'$gte': 2*startdate-enddate, '$lt': startdate}}).count()	
		neutral_reviews_prev=collection.find({'Name': hotels,'Sentiment':'Neutral','Date':{'$gte': 2*startdate-enddate, '$lt': startdate}}).count()
		if total_reviews_prev==0:
			MRI_prev=0
		else:
			MRI_prev=(2*total_reviews_prev-negative_reviews_prev-0.5*neutral_reviews_prev)*100.0
			MRI_prev/=2*total_reviews_prev
		total_reviews=collection.find({'Name': hotels,'Date':{'$gte': startdate, '$lt': enddate}}).count()
		postive_reviews=collection.find({'Name': hotels,'Sentiment':'Postive','Date':{'$gte': startdate, '$lt': enddate}}).count()
		negative_reviews=collection.find({'Name': hotels,'Sentiment':'Negative','Date':{'$gte': startdate, '$lt': enddate}}).count()	
		neutral_reviews=collection.find({'Name': hotels,'Sentiment':'Neutral','Date':{'$gte': startdate, '$lt': enddate}}).count()
		if total_reviews ==0:
			MRI=0
		else:
			MRI=(2*total_reviews-negative_reviews-0.5*neutral_reviews)*100.0
			MRI/=2*total_reviews
		if MRI_prev !=0.0:
			change=(MRI_prev-MRI)*100.0
			change/=MRI
		else:
			change=-100.0
		if total_reviews_prev !=0.0:
			changemention=(total_reviews_prev-total_reviews)*100.0
			changemention/=total_reviews
		else:
			changemention=-100.0
		data.append({"Name":name,"MRI":round(MRI,2),"MRIchange":round(-change,2),"Totalprev":total_reviews_prev,"Totalchange":round(-changemention,2),"Total":total_reviews,"Postive":postive_reviews,"Negative":negative_reviews,"Neutral":neutral_reviews})
	client.close()
	return json.dumps(data)

@app.route('/getdata',methods=["POST"])
def  getdata():
	client = MongoClient(ip, 27017)
	db = client[dbname]
	collection=db[collectionname]
	filter =request.get_json(force=True)
	hh=filter['hotel']
	startdate=int(time.mktime(datetime.strptime(filter['startdate'],'%d/%m/%Y').timetuple()))
	enddate=int(time.mktime(datetime.strptime(filter['enddate'],'%d/%m/%Y').timetuple()))
	if hh == "null":
		user_obj=session.get('user', None)
		name = user_obj['hotel']
	else:
		name=hh
	tags = collection.find({'Name': name,'Date':{'$gte': startdate, '$lt': enddate}})
	tags1 = {"data":json.loads(json_util.dumps(tags))}
	client.close()
	return json.dumps(tags1)

@app.route('/singlelinechart',methods=["POST"])
def  singlelinechart():
	client = MongoClient(ip, 27017)
	db = client[dbname]
	collection=db[collectionname]
	filter =request.get_json(force=True)
	hh=filter['hotel']
	startdate=int(time.mktime(datetime.strptime(filter['startdate'],'%d/%m/%Y').timetuple()))
	enddate=int(time.mktime(datetime.strptime(filter['enddate'],'%d/%m/%Y').timetuple()))
	if hh == "null":
		user_obj=session.get('user', None)
		name = user_obj['hotel']
	else:
		name=hh
	columns = ['year', 'month', 'week','sentiment']
	df = pd.DataFrame(columns=columns) 
	total_reviews=collection.find({'Name': name,'Date':{'$gte': startdate, '$lt': enddate}})
	for x in total_reviews:
		df.loc[len(df)]=[datetime.fromtimestamp(int(x['Date'])).strftime('%Y'),datetime.fromtimestamp(int(x['Date'])).strftime('%m'),datetime.fromtimestamp(int(x['Date'])).strftime('%U'),x['Sentiment'] ]
	df_sentiment = pd.get_dummies(df['sentiment'])
	df_new = pd.concat([df, df_sentiment], axis=1)
	df= df_new.groupby(['year','month']).sum().reset_index()
	if 'Negative' not in list(df):
		df['Negative']=0.0
	if 'Postive' not in list(df):
		df['Postive']=0.0
	if 'Neutral' not in list(df):
		df['Neutral']=0.0
	data=[]
	for index,row in df.iterrows():
		total=row['Postive']+row['Neutral']+row['Negative']
		if total==0:
			MRI=0
		else:			
			MRI=total*2-row['Neutral']-row['Negative']*0.5
			MRI/=total*2
			MRI*=100.0
		data.append([int(datetime.strptime('01/'+row['month']+'/'+row['year'], '%d/%m/%Y').strftime("%s"))*1000,round(MRI,2)])
	tags1=  [{ "key": name,"mean": 1.5,"values":data}]


	client.close()
	return json.dumps(tags1)


@app.route('/multilinechart',methods=["POST"])
def multilinechart():
	client = MongoClient(ip, 27017)
	db = client[dbname]
	collection=db[collectionname]
	restd=collection.distinct("Name")
	user_obj=session.get('user', None)
	user_obj['group'].append(user_obj['hotel'])
	test= list(set(user_obj['group']))
	tags = list(set(test).intersection(restd))
	filter =request.get_json(force=True)
	startdate=int(time.mktime(datetime.strptime(filter['startdate'],'%d/%m/%Y').timetuple()))
	enddate=int(time.mktime(datetime.strptime(filter['enddate'],'%d/%m/%Y').timetuple()))
	result=[]
	for name in tags:
		columns = ['year', 'month', 'week','sentiment']
		df = pd.DataFrame(columns=columns) 
		total_reviews=collection.find({'Name': name,'Date':{'$gte': startdate, '$lt': enddate}})
		for x in total_reviews:
			df.loc[len(df)]=[datetime.fromtimestamp(int(x['Date'])).strftime('%Y'),datetime.fromtimestamp(int(x['Date'])).strftime('%m'),datetime.fromtimestamp(int(x['Date'])).strftime('%U'),x['Sentiment'] ]
		df_sentiment = pd.get_dummies(df['sentiment'])
		df_new = pd.concat([df, df_sentiment], axis=1)
		df= df_new.groupby(['year','month']).sum().reset_index()
		if 'Negative' not in list(df):
			df['Negative']=0.0
		if 'Postive' not in list(df):
			df['Postive']=0.0
		if 'Neutral' not in list(df):
			df['Neutral']=0.0
		data=[]
		for index,row in df.iterrows():
			total=row['Postive']+row['Neutral']+row['Negative']
			if total==0:
				MRI=0
			else:			
				MRI=total*2-row['Neutral']-row['Negative']*0.5
				MRI/=total*2
				MRI*=100.0
			data.append([int(datetime.strptime('01/'+row['month']+'/'+row['year'], '%d/%m/%Y').strftime("%s"))*1000,round(MRI,2)])
		result.append({ "key":name,"mean": 1.5,"values":data})

	client.close()
	return json.dumps(result)

@app.route('/topicdata',methods=["POST"])
def  topicdata():
	topics=TopicCategories
	client = MongoClient(ip, 27017)
	db = client[dbname]
	collection=db[collectionname]
	filter =request.get_json(force=True)
	hh=filter['hotel']
	startdate=int(time.mktime(datetime.strptime(filter['startdate'],'%d/%m/%Y').timetuple()))
	enddate=int(time.mktime(datetime.strptime(filter['enddate'],'%d/%m/%Y').timetuple()))	
	if hh == "null":
		user_obj=session.get('user', None)
		name = user_obj['hotel']
	else:
		name=hh
	data=[]
	for x in topics:
		b= collection.find({'Name': name,'Date':{'$gte': startdate, '$lt': enddate},x: { '$gte': 1 }})
		count_prev=0
		pos_prev=0
		neu_prev=0
		neg_prev=0
		for y in b:
			count_prev+=1
			if  y['Sentiment']=='Negative':
				neg_prev+=1
			if y['Sentiment']=='Postive':
				pos_prev+=1
			if y['Sentiment']=='Neutral':
				neu_prev+=1
		if count_prev==0:
			MRI_prev=0
		else:
			MRI_prev=(2*count_prev-neg_prev-0.5*neg_prev)*100.0
			MRI_prev/=2*count_prev
		a= collection.find({'Name': name,'Date':{'$gte': 2*startdate-enddate, '$lt': startdate},x: { '$gte': 1 }})
		count=0
		pos=0
		neu=0
		neg=0
		for y in a:
			count+=1
			if  y['Sentiment']=='Negative':
				neg+=1
			if y['Sentiment']=='Postive':
				pos+=1
			if y['Sentiment']=='Neutral':
				neu+=1
		if count==0:
			MRI=0
		else:
			MRI=(2*count-neg-0.5*neu)*100.0
			MRI/=2*count	
		if MRI_prev !=0.0:
			change=(MRI_prev-MRI)*100.0
			change/=MRI
		else:
			change=-100.0
		if count_prev !=0.0: 	
			changemention=(count_prev-count)*100.0
			changemention/=count
		else:
			changemention=-100.0
		data.append({"topic":x.upper(),"mri":round(MRI,2),"mrichange":round(-change,2),"mentionchange":round(-changemention,2),"mention":count,"postive":pos,"Negative":neg,"Neutral":neu})
	client.close()
	return json.dumps(data)

@app.route('/queriedhotel',methods=["POST"])
def  queriedhotel():
	client = MongoClient(ip, 27017)
	db = client[dbname]
	collection=db[collectionname]
	tags = collection.distinct("Name")
	data=[]	
	filter =request.get_json(force=True)
	hh=filter['hotel']
	startdate=int(time.mktime(datetime.strptime(filter['startdate'],'%d/%m/%Y').timetuple()))
	enddate=int(time.mktime(datetime.strptime(filter['enddate'],'%d/%m/%Y').timetuple()))
	print startdate,enddate
	if hh == "null":
		user_obj=session.get('user', None)
		name = user_obj['hotel']		
	else:
		name=hh
	hotels	=name
	total_reviews_prev=collection.find({'Name': hotels,'Date':{'$gte': 2*startdate-enddate ,'$lt': startdate}}).count()
	postive_reviews_prev=collection.find({'Name': hotels,'Sentiment':'Postive','Date':{'$gte': 2*startdate-enddate, '$lt': startdate}}).count()
	negative_reviews_prev=collection.find({'Name': hotels,'Sentiment':'Negative','Date':{'$gte': 2*startdate-enddate, '$lt': startdate}}).count()	
	neutral_reviews_prev=collection.find({'Name': hotels,'Sentiment':'Neutral','Date':{'$gte': 2*startdate-enddate, '$lt': startdate}}).count()
	if total_reviews_prev==0:
		MRI_prev=0
	else:
		MRI_prev=(2*total_reviews_prev-negative_reviews_prev-0.5*neutral_reviews_prev)*100.0
		MRI_prev/=2*total_reviews_prev
	total_reviews=collection.find({'Name': hotels,'Date':{'$gte': startdate, '$lt': enddate}}).count()
	postive_reviews=collection.find({'Name': hotels,'Sentiment':'Postive','Date':{'$gte': startdate, '$lt': enddate}}).count()
	negative_reviews=collection.find({'Name': hotels,'Sentiment':'Negative','Date':{'$gte': startdate, '$lt': enddate}}).count()	
	neutral_reviews=collection.find({'Name': hotels,'Sentiment':'Neutral','Date':{'$gte': startdate, '$lt': enddate}}).count()
	if total_reviews ==0:
		MRI=0
	else:
		MRI=(2*total_reviews-negative_reviews-0.5*neutral_reviews)*100.0
		MRI/=2*total_reviews
	if MRI_prev !=0.0:
		change=(MRI_prev-MRI)*100.0
		change/=MRI
		change=-100.0
	if total_reviews_prev !=0.0:
		changemention=(total_reviews_prev-total_reviews)*100.0
		changemention/=total_reviews
	else:
		changemention=-100.0
	b_pre=0
	b=0
	pos=0
	neg=0
	neu=0
	for x in TopicCategories:
		b_pre+= collection.find({'Name': name,'Date':{'$gte':2*startdate-enddate, '$lt': startdate},x: { '$gte': 1 }}).count()
		b+= collection.find({'Name': name,'Date':{'$gte': startdate, '$lt': enddate},x: { '$gte': 1 }}).count()
		pos+= collection.find({'Name': name,'Sentiment':'Postive','Date':{'$gte': startdate, '$lt': enddate},x: { '$gte': 1 }}).count()
		neg+= collection.find({'Name': name,'Sentiment':'Negative' ,'Date':{'$gte': startdate, '$lt': enddate},x: { '$gte': 1 }}).count()
		neu+= collection.find({'Name': name,'Sentiment':'Neutral','Date':{'$gte': startdate, '$lt': enddate},x: { '$gte': 1 }}).count()
		b+= collection.find({'Name': name,'Date':{'$gte': startdate, '$lt': enddate},x: { '$gte': 1 }}).count()
		pos+= collection.find({'Name': name,'Sentiment':'Postive','Date':{'$gte': startdate, '$lt': enddate},x: { '$gte': 1 }}).count()
		neg+= collection.find({'Name': name,'Sentiment':'Negative' ,'Date':{'$gte': startdate, '$lt': enddate},x: { '$gte': 1 }}).count()
		neu+= collection.find({'Name': name,'Sentiment':'Neutral','Date':{'$gte': startdate, '$lt': enddate},x: { '$gte': 1 }}).count()
	print b_pre,b,pos,neu,neg
	changing=b_pre-b
	changing*=100.0
	changing/=b
	data.append({"mention":b,"mention_pos":pos,"topicchange":round(-changing,2),"mention_neg":neg,"mention_neu":neu,"Name":name,"MRI":round(MRI,2),"MRIchange":round(-change,2),"Totalprev":total_reviews_prev,"Totalchange":round(-changemention,2),"Total":total_reviews,"Postive":postive_reviews,"Negative":negative_reviews,"Neutral":neutral_reviews})

	client.close()
	return json.dumps(data)

@app.route('/sourcesdata',methods=["POST"])
def  sourcesdata():
	client = MongoClient(ip, 27017)
	db = client[dbname]
	collection=db[collectionname]
	channel = collection.distinct("Channel")
	data=[]
	filter =request.get_json(force=True)
	startdate=int(time.mktime(datetime.strptime(filter['startdate'],'%d/%m/%Y').timetuple()))
	enddate=int(time.mktime(datetime.strptime(filter['enddate'],'%d/%m/%Y').timetuple()))
	hh=filter['hotel']
	if hh == "null":
		user_obj=session.get('user', None)
		name = user_obj['hotel']
	else:
		name=hh
	total=collection.find({'Name': name,'Date':{'$gte': startdate, '$lt': enddate}}).count()

	for x in channel:		
		rating=collection.aggregate([
	    { "$match": {'Name': name ,'Channel':x ,'Date':{'$gte': startdate, '$lt': enddate}}},
	    { "$group": {"_id": 'null',"rating": { "$avg": "$Rating" }}}])
		if len(rating['result'])>0:
			avg=rating['result'][0]['rating']
		else:
			avg="NA"
		data.append({'Avgrating':round(avg,2),'SourceIndex':round(collection.find({'Name': name ,'Channel':x,'Date':{'$gte': startdate, '$lt': enddate}}).count()*100.0/float(total),2),'Channel':x,'Count':collection.find({'Name': name ,'Channel':x,'Date':{'$gte': startdate, '$lt': enddate}}).count(),'PostiveCount':collection.find({'Name': name,'Channel':x,'Sentiment':'Postive','Date':{'$gte': startdate, '$lt': enddate}}).count(),'NegativeCount':collection.find({'Name': name,'Channel':x,'Sentiment':'Negative','Date':{'$gte': startdate, '$lt': enddate}}).count(),'NeutralCount':collection.find({'Name': name,'Channel':x,'Sentiment':'Neutral','Date':{'$gte': startdate, '$lt': enddate}}).count()})
	return json.dumps(data)


@app.route('/')
def home():
    return redirect(url_for("login"))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = app.config['USERS_COLLECTION'].find_one({"_id": form.username.data})
        if user and User.validate_login(user['password'], form.password.data) and user[u'status']==u'true':
            user_obj = User(user['_id'])
            login_user(user_obj)
	    session['logged_in'] = True
	    session['user'] = user            
	    flash("Logged in successfully!", category='success')
	    if user['role']=='admin':
	    	return render_template('admin.html', title='login', form=form)
            else:
            	return redirect(request.args.get("next") or url_for("index"))
        flash("Wrong username or password!", category='error')
    return render_template('login.html', title='login', form=form)

@app.route('/user',methods=["POST"])
def user():
	user_obj=session.get('user',None)
	user_obj['group']=list(set(user_obj['group']))
	return json.dumps(user_obj)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    logout_user()
    return redirect(url_for('login'))


@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    # user_obj=session.get('user', None)
    # print user_obj
    return render_template('index.html')


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    return render_template('profile.html')


@lm.user_loader
def load_user(username):
    u = app.config['USERS_COLLECTION'].find_one({"_id": username})
    if not u:
        return None
    return User(u['_id'])
