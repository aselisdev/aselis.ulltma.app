from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from .models import *
from django import forms

from ulltma.aifuncs import clean_string, correctspelling 

import random
import matplotlib.pyplot as plt 
import numpy as np
import io, urllib, base64
import datetime

auditorydesc = ['Learn through listening.', 'Like to read aloud.', 'Often like to talk to themselves or create musical jingles to learn new material',
	'Likes to have music when they study.', 'Remember by talking out loud.', 'Like to have things explained to them orally rather than through written instructions', 
	'Prefer information that is heard or spoken', 'Learn best from lectures, group discussions, radio, email, using mobile phones, speaking, webchat, and talking things through',
	'Email is included IF written in chat-style with abbreviations, colloquial terms, slang, and non-formal language.', 'Often want to sort things out by speaking first rather than sorting out their ideas and then speaking',
	'They may say again what has already been said or ask an obvious and previously answered question.']

kinestheticdesc = ['Use of experience and practice (simulated or real).', 'May use other modalities.', 'Prefer connection to reality, either through concrete personal experiences, examples, practice, or simulation', 
	'Prefer demonstrations, simulations, videos and movies of “real” things, as well as case studies, practice and applications', 'Prefer learning with tools that can be grasped, held, tasted, or felt', 
	'Learn by doing', 'value their own background of experiences and less so, the experiences of others', 'Enjoys assignments that requires the details of who will do what and when',
	'Enjoy building, marking off, highlighting, and compiling']

multimodaldesc = ['Those who do not have a standout mode with one preference well above others, are defined as multimodal.', 
	'TYPE 1 - Flexible in their communication processes. Switch from mode to mode. Depends on assignment. Context specific - choose a single mode to fit the situation. May have strength in two, three, or all the learning styles',
	'TYPE 2 - Not satisfied until they have had input (or output) in all of their preferred modes. Take long to gather from each mode. As a result, often have a deeper and broader understanding. May be seen as procrastinators or slow-deliverers but some may be merely gathering all the information before acting. Their decision making and learning may be better because of that breadth of understanding'] 	

visualdesc = ['Tend to be fast talkers.', 'Learn by seeing charts and diagrams.', 'Need quiet study time.', 'May think in pictures.', 'Likes to sit in front of the class', 
	'Prefers pictures, images, and analyzing spatial relationships (i.e., you are aware of space between things', 'DOES include designs, whitespace, patterns, shapes and the different formats that are used to highlight and communicate information',
	'Does NOT include still pictures or photographs of reality, movies, videos or PowerPoint', 'Draw or outline information you need to remember', 'Copy what\'s on the board', 'Diagram sentences',
	'Take notes and make lists', 'Color code, highlight, circle, and underline words in your notes', 'Use flashcards']	

readingdesc = ['Prefers information displayed as words.', 'Emphasizes text-based input and output - reading and writing in all its forms especially manuals, reports, essays and assignments.',
	'Often enjoy using PowerPoint, the Internet, lists, diaries, dictionaries, thesauri, quotations and words.']

class UploadForm(forms.ModelForm):
	class Meta:
		model = ProfilePicture
		fields = ('pfp',)

#helperfunca
def skillQueryResults(keywords):
	ret = BaseSkill.objects.filter(skill__icontains=keywords[0])

	if len(keywords) > 1:
		i = 1
		while i < len(keywords):
			ret = ret & BaseSkill.objects.filter(skill__icontains=keywords[i])
			i += 1

	return ret

# Create your views here.
def index(request):
	if not request.user.is_authenticated:
		return HttpResponseRedirect(reverse("login"))
	return render(request, "ulltma/homepage.html")

def login_view(request):
	if request.method == "POST":
		userinput = request.POST["email"]
		try:
			username = User.objects.get(email=userinput).username
			print(username)
		except User.DoesNotExist:
			username = userinput

		password = request.POST["password"]
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			return HttpResponseRedirect(reverse("dashboard"))
		else:
			return render(request, "ulltma/homepage.html", {
				"message" : "Username or password is incorrect"
				})
	return render(request, "ulltma/homepage.html")

def logout_view(request):
	logout(request)
	return render(request, "ulltma/homepage.html", {
		"message" : "Thank you for using ULLTMA. You have now logged out."
		})


def signin(request):
	if request.method == "POST":
		firstname = request.POST["firstname"]
		lastname = request.POST["lastname"]
		email = request.POST["email"]
		password = request.POST["password"]
		pconfirm = request.POST["pconfirm"]
		username = f"aselis{User.objects.count()}"
		user = authenticate(request, username=username, password=password)
		if user is not None:
			return render(request, "ulltma/signinp1.html", {
					"message" : "User exists."
					})
		else:
			if len(password) < 8:
				return render(request, "ulltma/signinp1.html", {
					"message" : "Password must be more than eight characters"
					})
			elif password != pconfirm:
				return render(request, "ulltma/signinp1.html", {
					"message" : "Passwords do not match."
					})
			else:
				user = User.objects.create_user(username=username, email=email, password=password)
				user.first_name = firstname
				user.last_name = lastname
				user.save()

				pfp = ProfilePicture.objects.create(user=user)
				pfp.save()
				login(request, user)
				return HttpResponseRedirect(reverse("ltprep"))
	return render(request,"ulltma/signinp1.html")

def ltprep(request):
	firstname = ""
	if request.user.is_authenticated:
		firstname = request.user.first_name
		print(firstname)
		if not LearningStyle.objects.filter(user=request.user).exists():
			ls = LearningStyle.objects.create(user=request.user)
			ls.datetaken = datetime.date.today()
			ls.visualscore = 0
			ls.auditoryscore = 0
			ls.readingscore = 0
			ls.kinestheticscore = 0
			ls.visualpercent = 0
			ls.auditorypercent = 0
			ls.readingpercent = 0
			ls.kinestheticpercent = 0
			ls.save()
		else:
			userls = LearningStyle.objects.get(user=request.user)
			userls.datetaken = datetime.date.today()
			userls.visualscore = 0
			userls.auditoryscore = 0
			userls.readingscore = 0
			userls.kinestheticscore = 0
			userls.visualpercent = 0
			userls.auditorypercent = 0
			userls.readingpercent = 0
			userls.kinestheticpercent = 0
			userls.save()
	return render(request,"ulltma/ltprep.html", {
		"firstname":firstname
		})

def ltestprop(request):

	assess = LearningAssessment.objects.all()
	assessbed = []

	visualbed = [v["visualquestion"] for v in list(assess.values("visualquestion"))]
	auditorybed = [a["auditoryquestion"] for a in list(assess.values("auditoryquestion"))]
	readingbed = [r["readingquestion"] for r in list(assess.values("readingquestion"))]
	kinestheticbed = [k["kinestheticquestion"] for k in list(assess.values("kinestheticquestion"))]

	visualscore = 0
	auditoryscore = 0
	readingscore = 0 
	kinestheticscore = 0
	total = 0
	
	for m in assess:
		ml = [m.visualquestion, m.auditoryquestion, m.readingquestion, m.kinestheticquestion]
		random.shuffle(ml)
		assessbed.append(ml)

	currbed = []
	for ax in assessbed:
		for c in ax:
			currbed.append(c)

	answerlist = []

	if request.method == "POST":
		a = 0
		while a < 4 * assess.count():
			answerlist.append(request.POST["freq_" + str(a)])
			a += 1

		b = 0
		while b < 4 * assess.count():
			if currbed[b] in visualbed and answerlist[b] == "often":
				visualscore += 3
				total += 3
			elif currbed[b] in auditorybed and answerlist[b] == "often":
				auditoryscore += 3
				total += 3
			elif currbed[b] in readingbed and answerlist[b] == "often":
				readingscore += 3
				total += 3
			elif currbed[b] in kinestheticbed and answerlist[b] == "often":
				kinestheticscore += 3
				total += 3
			b+=1

		userls = LearningStyle.objects.get(user=request.user)
		userls.visualscore = visualscore
		userls.auditoryscore = auditoryscore
		userls.readingscore = readingscore
		userls.kinestheticscore = kinestheticscore
		userls.visualpercent = round(100 * visualscore / total, 2) 
		userls.auditorypercent = round(100 * auditoryscore / total, 2) 
		userls.readingpercent = round(100 * readingscore / total, 2) 
		userls.kinestheticpercent = round(100 * kinestheticscore / total, 2) 
		userls.save()

		if userls.visualpercent > 40:
			userls.style = "VISUAL"
		elif userls.auditorypercent > 40:
			userls.style = "AUDITORY"
		elif userls.readingpercent > 40:
			userls.style = "READING / WRITING"
		elif userls.kinestheticscore > 40:
			userls.style = "KINESTHETIC"
		else:
			userls.style = "MULTIMODAL"
		userls.save()
		return HttpResponseRedirect(reverse("learnstylereport"))
	return render(request,"ulltma/qbed3.html", {
		"assess":assess, "assessbed":assessbed
		})

def learnstylereport(request):
	if request.user.is_authenticated:
		learnstyle = list(LearningStyle.objects.filter(user=request.user).values("style"))
		stylename = learnstyle[0]['style']
		desc = []
		imgurl = ""

		if stylename == "VISUAL":
			desc = visualdesc
			imgurl = "ulltma/images/VISUAL.jpg"
		elif stylename == "AUDITORY":
			desc = auditorydesc
			imgurl = "ulltma/images/AUDITORY.png"
		elif stylename == "READING / WRITING":
			desc = readingdesc
			imgurl = "ulltma/images/READING.png"
		elif stylename == "KINESTHETIC":
			desc = kinestheticdesc
			imgurl = "ulltma/images/KINESTHETIC.png"
		else:
			desc = multimodaldesc
			imgurl = "ulltma/images/MULTIMODAL.png"

		return render(request, "ulltma/learnreport.html", {
			"style" : learnstyle[0]['style'], 
			"desc" : desc, "imgurl" : imgurl
			})
	return render(request, "ulltma/learnreport.html")

def dashboard(request):
	if request.user.is_authenticated:
		userpfp = ProfilePicture.objects.get(user=request.user)
		userls = LearningStyle.objects.get(user=request.user)

		currdate = datetime.date.today()
		deadline = userls.datetaken + datetime.timedelta(days=60)
		datediff = deadline - currdate

		user_reports = UserReports.objects.filter(user=request.user)
		lavg = user_reports.values('posttestavg')

		avg = 0
		for l in lavg:
			avg += l['posttestavg']
		
		avg /= user_reports.count()

		retakebool = user_reports.count() > 10 and avg < 0.75
		
		return render(request, "ulltma/dashboard.html", {
			"firstname" : request.user.first_name, "daysleft":datediff.days, "rt":retakebool, "pfp":userpfp
			})
	return render(request, "ulltma/dashboard.html", {
		"firstname" : "User"
		})

def skillsearch(request):
	skill_list = BaseSkill.objects.all()
	subjects = [x['subject'] for x in list(skill_list.values("subject"))]
	subjects = list(dict.fromkeys(subjects))

	subjectTopics = {}
	for s in subjects:
		subjectTopics[s] = [x['topic'] for x in list(BaseSkill.objects.filter(subject=s).values('topic'))]
		subjectTopics[s] = list(dict.fromkeys(subjectTopics[s]))

	if request.method=="POST":
		skill_search = []
		skillquery = request.POST["searchtext"]

		if skillquery == "":
			skill_search = BaseSkill.objects.all()
		else:
			skillquery = correctspelling(skillquery).split()
			print(skillquery)
			skill_search = skillQueryResults(skillquery)

		subjects = [x['subject'] for x in list(skill_search.values("subject"))]
		subjects = list(dict.fromkeys(subjects))

		subjectTopics = {}
		for s in subjects:
			subjectTopics[s] = [x['topic'] for x in list(skill_search.filter(subject=s).values('topic'))]
			subjectTopics[s] = list(dict.fromkeys(subjectTopics[s]))

		return render(request, "ulltma/skills.html", {
		"skills": skill_search, "subtopics" :subjectTopics
		})
	return render(request, "ulltma/skills.html", {
		"skills": skill_list, "subtopics" : subjectTopics
		})

def reportsearch(request):
	userreports = UserReports.objects.filter(user=request.user)
	if request.method=="POST":
		searchquery = request.POST["searchtext"]
		searchreports =  UserReports.objects.filter(user=request.user, skill__icontains=searchquery)
		return render(request, "ulltma/reports.html", {
			"reports" : searchreports
			})

	return render(request, "ulltma/reports.html", {
		"reports" : userreports
		})

def changepassword(request):
	if request.method == "POST":
		password = request.POST["password"]
		pconfirm = request.POST["pconfirm"]
		if len(password) < 8:
			return render(request, "ulltma/changepw.html", {
				"message" : "Password must be more than eight characters"
				})
		elif password != pconfirm:
			return render(request, "ulltma/changepw.html", {
				"message" : "Passwords do not match."
				})
		else:
			u = request.user
			u.set_password(password)
			u.save()
			login(request,u)
			return HttpResponseRedirect(reverse("dashboard"))
	return render(request, "ulltma/changepw.html")

def skillprep(request, keyword):
	skill = BaseSkill.objects.filter(keyword=keyword)
	name = skill.values("skill")[0]["skill"]
	desc = skill.values("description")[0]["description"]

	sk = BaseSkill.objects.filter(keyword=keyword).first()
	if UserReports.objects.filter(user=request.user, skill=sk).exists():
		pass
	else:
		ls = UserReports.objects.create(user=request.user, skill=sk, finishdate = datetime.date.today())

	return render(request, "ulltma/skillprep.html", {
		"name" : name, "description" : desc, "keyword" : keyword
		})

def pretest(request, keyword):
	skill = BaseSkill.objects.filter(keyword=keyword).first()
	questions = list(SkillTestQuestions.objects.filter(skill=skill))

	if request.user.is_authenticated:
		ls = UserReports.objects.get(user=request.user, skill=skill)
		if request.method=="POST":
			print(request.POST["question_1"]==questions[0].answer)
			print(request.POST["question_2"]==questions[1].answer)
			print(request.POST["question_3"]==questions[2].answer)
			if request.POST["question_1"] == questions[0].answer:
				ls.q1pretestscore = 3
			else:
				ls.q1pretestscore = 0
				
			if request.POST["question_2"] == questions[1].answer:
				ls.q2pretestscore = 3
			else:
				ls.q2pretestscore = 0

			if request.POST["question_3"] == questions[2].answer:
				ls.q3pretestscore = 3
			else:
				ls.q3pretestscore = 0
			ls.save()
			return HttpResponseRedirect(reverse("ltools", args=(keyword,)))
	return render(request, "ulltma/pretest.html", {"questions" : questions, "keyword" : keyword})

def ltools(request, keyword):
	skill = BaseSkill.objects.filter(keyword=keyword).first()
	style = list(LearningStyle.objects.filter(user=request.user).values('style'))[0]['style']
	tools = LearningTool.objects.filter(skill=skill, modality=style[0])

	if request.method == "GET":
		url = request.GET.get('link')
		print(request.user)
		tool = tools.filter( url=url)
		md = list(tool.values('modality'))
		if len(md) > 0:
			print(md[0])
			print(len(md))
			cl = ClickedLink(skill=skill, modality=md[0]['modality'], url=url)
			cl.save()
			ltool = tool.first()
			ltool.clicked += 1
			ltool.save()


	return render(request, "ulltma/ltools.html", {"keyword" : keyword, "tools":tools})

def posttest(request, keyword):
	skill = BaseSkill.objects.filter(keyword=keyword).first()
	questions = list(SkillTestQuestions.objects.filter(skill=skill))

	skillname = str(skill.skill) 

	if request.user.is_authenticated:
		dt = datetime.date.today()
		ls = UserReports.objects.get(user=request.user, skill=skill)
		ls.finishdate = dt
		ls.save()
		if request.method=="POST":
			if request.POST["question_1"] == questions[0].answer:
				ls.q1posttestscore = 3
			else:
				ls.q1posttestscore = 0

			if request.POST["question_2"] == questions[1].answer:
				ls.q2posttestscore = 3
			else:
				ls.q2posttestscore = 0

			if request.POST["question_3"] == questions[2].answer:
				ls.q3posttestscore = 3
			else:
				ls.q3posttestscore = 0

			ls.posttestavg = (ls.q1posttestscore + ls.q2posttestscore + ls.q3posttestscore) / 9
			ls.save()
			return HttpResponseRedirect(reverse("learnresult", args=(skillname,)))
	return render(request, "ulltma/posttest.html", {"questions" : questions, "keyword" : keyword})

def results(request, keyword):
	skill = BaseSkill.objects.get(keyword=keyword)
	userrep = UserReports.objects.filter(user=request.user, skill=skill).first()

	dt = userrep.finishdate
	labels = ['Q.1', 'Q.2', 'Q.3']
	pretestscores = [userrep.q1pretestscore, userrep.q2pretestscore, userrep.q3pretestscore]
	posttestscores = [userrep.q1posttestscore, userrep.q2posttestscore, userrep.q3posttestscore]


	x = np.arange(len(labels))
	width = 0.35

	fig, ax = plt.subplots()
	rects1 = ax.barh(x - width/2, pretestscores, width, label='Pre-test', color="#800080")
	rects2 = ax.barh(x + width/2, posttestscores, width, label='Post-test', color="#E9D3FF")

	ax.set_yticks(x)
	ax.set_yticklabels(labels)
	ax.invert_yaxis()
	ax.legend()

	buf = io.BytesIO()
	fig.savefig(buf, format='png')
	buf.seek(0)
	string = base64.b64encode(buf.read())
	uri = urllib.parse.quote(string)

	return render(request, "ulltma/results.html", {"data":uri, "date":dt, "name":userrep.skill})


def test(request, page):
	currpage = page - 1
	total =  LearningAssessment.objects.all().count()
	item = LearningAssessment.objects.all()[currpage]

	qlist = [item.visualquestion, item.auditoryquestion, item.readingquestion, item.kinestheticquestion]
	random.shuffle(qlist)

	userls = LearningStyle.objects.filter(user=request.user).get()

	print(f"{userls.visualscore}")

	if request.method=='POST':
		s = 0
		while s < 3:
			answer = request.POST["freq_"+str(s)]
			if qlist[s] == item.visualquestion and answer == "often":
				userls.visualscore += 3
			elif qlist[s] == item.auditoryquestion and answer == "often":
				userls.auditoryscore += 3
			elif qlist[s] == item.readingquestion and answer == "often":
				userls.readingscore += 3
			elif qlist[s] == item.kinestheticquestion and answer == "often":
				userls.kinestheticscore += 3
			userls.save()
		return render(request, "ulltma/qbed.html", {
		"currpage" : page, "item":item, "qlist" : qlist, "total": total, "progress": page * 5
		})

	return render(request, "ulltma/qbed.html", {
		"currpage" : page, "item":item, "qlist" : qlist, "total": total, "progress": page * 5
		})

def learnresult(request, skillname):
	skill = BaseSkill.objects.get(skill=skillname)
	userrep = UserReports.objects.filter(user=request.user, skill=skill).first()

	dt = userrep.finishdate.strftime("%B") + " " + userrep.finishdate.strftime("%d") + ", " + userrep.finishdate.strftime("%Y")

	fname = request.user.first_name.upper()

	labels = ['QUESTION 1', 'QUESTION 2', 'QUESTION 3']
	pretestscores = [userrep.q1pretestscore, userrep.q2pretestscore, userrep.q3pretestscore]
	posttestscores = [userrep.q1posttestscore, userrep.q2posttestscore, userrep.q3posttestscore]

	x = np.arange(len(labels))
	width = 0.35

	fig, ax = plt.subplots()
	rects1 = ax.barh(x - width/2, pretestscores, width, label='Pre-test', color="#d2a8e3")
	rects2 = ax.barh(x + width/2, posttestscores, width, label='Post-test', color="#563463")

	ax.set_yticks(x)
	ax.set_yticklabels(labels)
	ax.invert_yaxis()
	ax.legend()

	buf = io.BytesIO()
	fig.savefig(buf, format='png')
	buf.seek(0)
	string = base64.b64encode(buf.read())
	uri = urllib.parse.quote(string)


	#viability
	allrep = UserReports.objects.filter(skill=skill).values("posttestavg")
	
	#aggregate average
	postsum = 0
	for al in allrep:
		postsum += al['posttestavg'] * 100
	postavg = postsum / len(allrep) 
	print(postavg)

	#aggregate viability
	alltools = LearningTool.objects.filter(skill=skill)
	for at in alltools:
		if at.clicked > 10:
			if postavg > 60:
				at.viability = 'VB'
			else:
				at.viability = 'NVB'
			at.save()

	return render(request, "ulltma/results.html", {"data":uri,  "fname":fname, "date":dt, "name":userrep.skill})

def pfpchange(request):
	userpfp = ProfilePicture.objects.get(user=request.user)
	if request.method == "POST":
		print("PFP found")
		form = UploadForm(request.POST, request.FILES)
		print(form.is_valid())
		if form.is_valid():
			userpfp.pfp = form.cleaned_data['pfp']
			userpfp.save()
			message = "PFP Changed successfully"
			return render(request, "ulltma/pfpchange.html", {
				"pfp" : userpfp, "form":form, "msg" : message
				})
	else:
		form = UploadForm()
	return render(request, "ulltma/pfpchange.html", {
		"pfp" : userpfp, "form":form
		})

def loglink(request):
	if request.method == "POST":
		print(request.POST['link'])

def faq(request):
	return render(request, "ulltma/faq.html")

def techsupport(request):
	return render(request, "ulltma/techsupport.html")

def reportissue(request):
	if request.method == "POST":
		sd = request.POST['shortdesc']
		ld = request.POST['longdesc']
		issue = AppIssue.objects.create(shortdesc=sd, longdesc=ld, issuedate=datetime.date.today())
	return render(request, "ulltma/reportissue.html")