from django.contrib import admin
from .models import *

# Register your models here.
class LearningStyleAdmin(admin.ModelAdmin):
	list_display=("user", "datetaken", "visualscore", "auditoryscore", "readingscore", "kinestheticscore", "visualpercent", "auditorypercent", "readingpercent", "kinestheticpercent",  "style")
	ordering=('user',)

class LearningQuestionsAdmin(admin.ModelAdmin):
	list_display=("scenarionum", "scenario", "visualquestion", "auditoryquestion", "readingquestion", "kinestheticquestion")
	ordering = ('scenarionum',)

class BaseSkillAdmin(admin.ModelAdmin):
	list_display=("keyword", "subject", "topic", "skill", "description")
	ordering = ('subject', 'topic', 'keyword',)

class SkillTestQuestionsAdmin(admin.ModelAdmin):
	list_display=("skill", "question", "imgurl", "answer")
	ordering = ('skill',)

class UserReportsAdmin(admin.ModelAdmin):
	list_display = ("user", "skill", "finishdate", "q1pretestscore", "q1posttestscore", "q2pretestscore", "q2posttestscore", "q3pretestscore", "q3posttestscore", "posttestavg")
	ordering = ('user',)

class ProfilePictureAdmin(admin.ModelAdmin):
	list_display = ("user", "pfp")
	ordering = ('user',)

class LearningToolAdmin(admin.ModelAdmin):
	list_display=("skill", "modality", "title", "clicked", "url")
	ordering=('skill',)

class ClickedLinkAdmin(admin.ModelAdmin):
	list_display=("skill", "modality", "url")
	ordering=("skill", "modality")
		
class AppIssueAdmin(admin.ModelAdmin):
	list_display=("shortdesc", "longdesc", "issuedate")
	ordering=("issuedate", "shortdesc")
		

admin.site.register(LearningStyle, LearningStyleAdmin)
admin.site.register(LearningAssessment, LearningQuestionsAdmin)
admin.site.register(BaseSkill, BaseSkillAdmin)
admin.site.register(SkillTestQuestions, SkillTestQuestionsAdmin)
admin.site.register(UserReports, UserReportsAdmin)
admin.site.register(ProfilePicture, ProfilePictureAdmin)
admin.site.register(LearningTool, LearningToolAdmin)
admin.site.register(ClickedLink, ClickedLinkAdmin)
admin.site.register(AppIssue, AppIssueAdmin)
