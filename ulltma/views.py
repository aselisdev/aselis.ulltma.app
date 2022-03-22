from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from .models import *
from django import forms
from django.db import IntegrityError

# from ulltma.aifuncs import clean_string, correctspelling 
from ulltma.ulltmaforms import *

import random
import matplotlib.pyplot as plt 
import numpy as np
import io, urllib, base64
import datetime, pyotp

from django.views.generic import View, UpdateView
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from ulltma.tokens import account_activation_token

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

def isAnswer(qtype):
	return qtype == "shortanswer" or qtype == "longanswer"

# Create your views here.
def index(request):
	if not request.user.is_authenticated:
		return HttpResponseRedirect(reverse("login"))
	return render(request, "ulltma/content/home.html")

def login_view(request):
	if request.method == "POST":
		userinput = request.POST["email"]
		password = request.POST["password"]
		user = authenticate(request, username=userinput, password=password)
		if user is not None:
			login(request, user)

			profile = Profile.objects.get(user=user)
			subject = 'Login Notification'
			message = f"You've logged in to ULLTMA on {datetime.date.today()}."
			user.email_user(subject, message)

			if profile.first_time_taken_modality_test:
				return HttpResponseRedirect(reverse("dashboard"))
			else:
				return HttpResponseRedirect(reverse("ltprep"))
		else:
			return render(request, "ulltma/content/home.html", {
				"message" : "Username or password is incorrect"
				})
	return render(request, "ulltma/content/home.html")

def logout_view(request):
	logout(request)
	return render(request, "ulltma/content/home.html", {
		"message" : "Thank you for using ULLTMA. You have now logged out."
		})


def signin(request):
	if request.method == "POST":
		form = SignInForm(request.POST)
		if form.is_valid():
			firstname = form.cleaned_data['firstname']
			lastname = form.cleaned_data['lastname']
			email = form.cleaned_data['email']
			password = form.cleaned_data['pword']
			pconfirm = form.cleaned_data['pconfirm']
			user = authenticate(request, username=email, password=password)

			if user is not None:
				return render(request, "ulltma/signinp1.html", {
		 			"form" : form, "message" : "User exists."
		 			})
			else:
				if len(password) < 8:
					return render(request, "ulltma/signinp1.html", {
		 				"form" : form, "message" : "Passwords must be more than 8 characters."
		 				})
				elif password != pconfirm:
					return render(request, "ulltma/signinp1.html", {
		 				"form" : form, "message" : "Passwords do not match."
		 				})
				else:
					try:
						user = User.objects.create_user(username = email, email = email, password = password)
						user.first_name = firstname
						user.last_name = lastname
						user.is_active = False
						user.save()

						pf = Profile.objects.create(user=user)
						pf.save()

						pfp = ProfilePicture.objects.create(user=user)
						pfp.save()

						current_site = get_current_site(request)
						subject = 'Activate your Aselis account.'
						message = render_to_string('ulltma/account_activation_email.html', {
							'user' : user,
							'domain' : current_site.domain,
							'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
							'token' : account_activation_token.make_token(user)
							})

						user.email_user(subject, message)

						return render(request, "ulltma/signinp1.html", {
							"form" : form, "message" : "Please confirm email to continue"
							})
					except IntegrityError:

						return render(request, "ulltma/signinp1.html", {
							"form" : form, "message" : "User exists --- for debugging purposes"
							})
            		
	else:
		form = SignInForm()

	return render(request,"ulltma/signinp1.html", {"form" : form})

def signinotp(request):
	user_otp = UserOTP.objects.filter(user = request.user)
	qr_url = pyotp.totp.TOTP(user_otp.values()[0]['otp_secret']).provisioning_uri(name=request.user.email, issuer_name='Aselis')
	return render(request,"ulltma/signinp2.html", {"qr_url" : qr_url})

def ltprep(request):
	if request.user.is_authenticated:
		userls = LearningStyle.objects.get(user=request.user)
		user = userls.user
		firstname = user.first_name
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

	assess = LearningAssessment.objects.all()[:1]
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
			print(f"{currbed[b]}: {answerlist[b]}")
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
		try:
			userls.visualpercent = round(100 * visualscore / total, 2) 
			userls.auditorypercent = round(100 * auditoryscore / total, 2) 
			userls.readingpercent = round(100 * readingscore / total, 2) 
			userls.kinestheticpercent = round(100 * kinestheticscore / total, 2) 
		except ZeroDivisionError as e:
			userls.visualpercent = 0
			userls.auditorypercent = 0
			userls.readingpercent = 0 
			userls.kinestheticpercent = 0 
		
		userls.save()

		if userls.visualpercent > 40:
			userls.style = "VISUAL"
		elif userls.auditorypercent > 40:
			userls.style = "AUDITORY"
		elif userls.readingpercent > 40:
			userls.style = "READING / WRITING"
		elif userls.kinestheticpercent > 40:
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
		profile = Profile.objects.get(user=request.user)
		profile.first_time_taken_modality_test = True
		profile.save()

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
		
		if user_reports.count() > 0:
			avg /= user_reports.count()

		retakebool = user_reports.count() > 10 and avg < 0.75
		
		return render(request, "ulltma/dashboard.html", {
			"firstname" : request.user.first_name, "lastname" : request.user.last_name, "daysleft":datediff.days, "rt":retakebool, "pfp":userpfp
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
		form = ChangePWordForm(request.POST)
		if form.is_valid():
			password = form.cleaned_data['pword']
			pconfirm = form.cleaned_data['pconfirm']
			if len(password) < 8:
				form = ChangePWordForm()
				return render(request, "ulltma/changepw.html", {
					"message" : "Password must be more than 8 characters",
					"form" : form
					})
			elif password != pconfirm:
				form = ChangePWordForm()
				return render(request, "ulltma/changepw.html", {
					"message" : "Passwords do not match",
					"form" : form
					})
			else:
				u = request.user
				u.set_password(password)
				u.save()
				login(request, u)
				return HttpResponseRedirect(reverse("dashboard"))
	else:
		form = ChangePWordForm()
	return render(request, "ulltma/changepw.html", {"form":form})

def changepasswordlogin(request):
	if request.method == "POST":
		form = ChangePWordLoginForm(request.POST)
		if form.is_valid():
			no_user = False
			email = form.cleaned_data['email']
			password = form.cleaned_data['pword']
			pconfirm = form.cleaned_data['pconfirm']

			try:
				u = User.objects.get(email=email)
			except User.DoesNotExist:
				no_user = True

			if len(password) < 8:
				form = ChangePWordLoginForm()
				return render(request, "ulltma/changepwlogin.html", {
					"message" : "Password must be more than 8 characters",
					"form" : form
					})
			elif password != pconfirm:
				form = ChangePWordLoginForm()
				return render(request, "ulltma/changepwlogin.html", {
					"message" : "Passwords do not match",
					"form" : form
					})
			elif no_user:
				form = ChangePWordLoginForm()
				return render(request, "ulltma/changepwlogin.html", {
					"message" : "Account does not exist!",
					"form" : form
					})
			else:
				u.set_password(password)
				u.save()
				return render(request, "ulltma/changepwlogin.html", {
					"message" : "Password updated. Make sure to remember it on your next login!",
					"form" : form
					})
	else:
		form = ChangePWordLoginForm()
	return render(request, "ulltma/changepwlogin.html", {"form":form})

def skillprep(request, keyword):
	skill = BaseSkill.objects.filter(keyword=keyword)
	name = skill.values("skill")[0]["skill"]
	desc = skill.values("description")[0]["description"]

	sk = BaseSkill.objects.filter(keyword=keyword).first()
	learnstyle = list(LearningStyle.objects.filter(user=request.user).values("style"))
	stylename = learnstyle[0]['style']
	if UserReports.objects.filter(user=request.user, skill=sk).exists():
		pass
	else:
		ls = UserReports.objects.create(user=request.user, style=stylename, skill=sk, finishdate = datetime.date.today())

	return render(request, "ulltma/skillprep.html", {
		"name" : name, "description" : desc, "keyword" : keyword
		})

def pretest(request, keyword):
	skill = BaseSkill.objects.filter(keyword=keyword).first()
	questions = list(SkillTestQuestion.objects.filter(skill=skill))

	if request.user.is_authenticated:
		ls = UserReports.objects.get(user=request.user, skill=skill)
		if request.method=="POST":
			print(request.POST["question_2"])

			if isAnswer(questions[0].qtype):
				if request.POST["question_1"] == questions[0].answer:
					ls.q1pretestscore = questions[0].score
				else:
					ls.q1pretestscore = 0
			elif questions[0].qtype == "options":
				deductions = 0
				for rp in request.POST["question_1"]:
					if rp not in questions[0].answer: 
						deductions += 1
				ls.q1pretestscore = questions[0].score - 0.25 * deductions

			if isAnswer(questions[1].qtype):
				if request.POST["question_2"] == questions[1].answer:
					ls.q2pretestscore = questions[1].score
				else:
					ls.q2pretestscore = 0
			elif questions[1].qtype == "options":
				deductions = 0
				for rp in request.POST["question_2"]:
					if rp not in questions[1].answer: 
						deductions += 1
				ls.q2pretestscore = questions[1].score - 0.25 * deductions

			if isAnswer(questions[2].qtype):
				if request.POST["question_3"] == questions[2].answer:
					ls.q3pretestscore = questions[2].score
				else:
					ls.q3prettestscore = 0
			elif questions[2].qtype == "options":
				deductions = 0
				for rp in request.POST["question_3"]:
					if rp not in questions[2].answer: 
						deductions += 1
				ls.q3prettestscore = questions[2].score - 0.25 * deductions

			ls.save()
			return HttpResponseRedirect(reverse("ltools", args=(keyword,)))
	return render(request, "ulltma/pretest.html", {"questions" : questions, "keyword" : keyword})

def ltools(request, keyword):
	skill = BaseSkill.objects.filter(keyword=keyword).first()
	style = list(LearningStyle.objects.filter(user=request.user).values('style'))[0]['style']
	tools = LearningTool.objects.filter(skill=skill)
	modtools = tools.filter(modality=style[0])
	others = tools.exclude(modality=style[0]).order_by('modality')

	if request.method == "GET":
		url = request.GET.get('link')
		print(request.user)
		tool = tools.filter( url=url)
		md = list(tool.values('modality'))
		if len(md) > 0:
			ltool = tool.first()
			ltool.clicked += 1
			ltool.save()


	return render(request, "ulltma/ltools.html", {"keyword" : keyword, "tools":modtools, "others":others, "style":style})

def posttest(request, keyword):
	skill = BaseSkill.objects.filter(keyword=keyword).first()
	questions = list(SkillTestQuestion.objects.filter(skill=skill))

	skillname = str(skill.skill) 

	if request.user.is_authenticated:
		dt = datetime.date.today()
		ls = UserReports.objects.get(user=request.user, skill=skill)
		ls.finishdate = dt
		ls.save()
		if request.method=="POST":
			if isAnswer(questions[0].qtype):
				if request.POST["question_1"] == questions[0].answer:
					ls.q1posttestscore = questions[0].score
				else:
					ls.q1posttestscore = 0
			elif questions[0].qtype == "options":
				deductions = 0
				for rp in request.POST["question_1"]:
					if rp not in questions[0].answer: 
						deductions += 1
				ls.q1posttestscore = questions[0].score - 0.25 * deductions

			if isAnswer(questions[1].qtype):
				if request.POST["question_2"] == questions[1].answer:
					ls.q2posttestscore = questions[1].score
				else:
					ls.q2posttestscore = 0
			elif questions[1].qtype == "options":
				deductions = 0
				for rp in request.POST["question_2"]:
					if rp not in questions[1].answer: 
						deductions += 1
				ls.q2posttestscore = questions[1].score - 0.25 * deductions

			if isAnswer(questions[2].qtype):
				if request.POST["question_3"] == questions[2].answer:
					ls.q3posttestscore = questions[2].score
				else:
					ls.q3posttestscore = 0
			elif questions[2].qtype == "options":
				deductions = 0
				for rp in request.POST["question_3"]:
					if rp not in questions[2].answer: 
						deductions += 1
				ls.q3posttestscore = questions[2].score - 0.25 * deductions

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

#class for view.
class ActivateAccount(View):

    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            profile = Profile.objects.get(user = user)
            profile.email_confirmed = True
            user.save()
            profile.save()

            if not LearningStyle.objects.filter(user=user).exists():
            	ls = LearningStyle.objects.create(user=user)
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
            login(request, user)
            return render(request, "ulltma/ltprep.html", {"message":messages, "firstname" : user.first_name})
        else:
            return render(request, "ulltma/content/home.html", {"message":"The confirmation link was invalid, possibly because it has already been used. Fortunately, your account has already ben created, so why not log in and take the modality test?"})