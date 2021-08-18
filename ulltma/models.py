from django.db import models
from django.conf import settings
import datetime

# Create your models here.

class LearningStyle(models.Model):
	user = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.CASCADE
		)
	datetaken = models.DateField(null=True)
	visualscore = models.IntegerField(default=0)
	auditoryscore = models.IntegerField(default=0)
	readingscore = models.IntegerField(default=0)
	kinestheticscore = models.IntegerField(default=0)
	visualpercent = models.FloatField(default=0)
	auditorypercent = models.FloatField(default=0)
	readingpercent = models.FloatField(default=0)
	kinestheticpercent = models.FloatField(default=0)
	style = models.CharField(max_length=20, default='VISUAL')

class LearningAssessment(models.Model):
	scenarionum = models.IntegerField()
	scenario = models.CharField(max_length=150)
	visualquestion = models.CharField(max_length=150)
	auditoryquestion = models.CharField(max_length=150)
	readingquestion = models.CharField(max_length=150)
	kinestheticquestion = models.CharField(max_length=150)

	def __str__(self):
		return f"{self.scenarionum}: {self.scenario} {self.visualquestion} {self.auditoryquestion} {self.readingquestion} {self.kinestheticquestion}"

class BaseSkill(models.Model):
	subject = models.CharField(max_length=200, default="")
	topic = models.CharField(max_length=300, default="")
	skill = models.CharField(max_length=500, default="")
	keyword = models.CharField(max_length=20, default="")
	description = models.CharField(max_length=2000)

	def __str__(self):
		return self.skill

class SkillTestQuestion(models.Model):
	skill = models.ForeignKey(BaseSkill, on_delete=models.CASCADE)
	qtype = models.CharField(max_length=20)
	question = models.CharField(max_length=2000)
	imgurl = models.CharField(max_length=300)
	op1 = models.CharField(max_length=2000)
	op2 = models.CharField(max_length=2000)
	op3 = models.CharField(max_length=2000)
	op4 = models.CharField(max_length=2000)
	op5 = models.CharField(max_length=2000)
	answer = models.CharField(max_length=300)	
	score = models.IntegerField(default=0)	

class UserReports(models.Model):
	user = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.CASCADE
		)
	style = models.CharField(max_length=20, default='VISUAL')
	skill = models.ForeignKey(BaseSkill, on_delete=models.CASCADE)
	finishdate = models.DateField()
	q1pretestscore = models.IntegerField(default=0)
	q2pretestscore = models.IntegerField(default=0)
	q3pretestscore = models.IntegerField(default=0)
	q1posttestscore = models.IntegerField(default=0)
	q2posttestscore = models.IntegerField(default=0)
	q3posttestscore = models.IntegerField(default=0)
	posttestavg = models.FloatField(default=0)

class ProfilePicture(models.Model):
	user = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.CASCADE
		)
	pfp = models.ImageField(upload_to='ulltma/pfp', default='ulltma/pfp/default.png')

class LearningTool(models.Model):
	MODALITIES = [
		('V', 'VISUAL'),
		('A', 'AUDITORY'),
		('R', 'READING / WRITING'),
		('K', 'KINESTHETIC'),
		('M', 'MULTIMODAL')
	]

	VIABILITY = [
		('VB', 'VIABLE'),
		('NVB', 'NOT VIABLE')
	]
	
	skill = models.ForeignKey(BaseSkill, on_delete=models.CASCADE)
	modality = models.CharField(max_length=25, choices=MODALITIES)
	title=models.CharField(max_length=300, default="")
	clicked = models.IntegerField(default=0)
	url = models.CharField(max_length=300, default="")
	viability = models.CharField(max_length=25, choices=VIABILITY, default='VB')



	def __str__(self):
		return '%s %s %s' % (self.skill, self.modality, self.title)

class ClickedLink(models.Model):
	skill = models.ForeignKey(BaseSkill, related_name="skill_clicked", on_delete=models.CASCADE)
	modality = models.CharField(max_length=25)
	url = models.CharField(max_length=300, default="")

class AppIssue(models.Model):
	shortdesc = models.CharField(max_length=500, default="")
	longdesc = models.CharField(max_length=1500, default="")
	issuedate = models.DateField()
