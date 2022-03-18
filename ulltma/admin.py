from django.contrib import admin
from .models import *
from django.contrib.admin.models import LogEntry

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

class SkillTestQuestionAdmin(admin.ModelAdmin):
	list_display=("skill", "question", "answer")
	ordering = ('skill', 'question',)

class UserReportsAdmin(admin.ModelAdmin):
	list_display = ("user", "skill", "finishdate", "q1pretestscore", "q1posttestscore", "q2pretestscore", "q2posttestscore", "q3pretestscore", "q3posttestscore", "posttestavg")
	ordering = ('user',)

class ProfilePictureAdmin(admin.ModelAdmin):
	list_display = ("user", "pfp")
	ordering = ('user',)

class LearningToolAdmin(admin.ModelAdmin):
	list_display=("skill", "modality", "title", "clicked", "url")
	ordering=('skill',)
		
class AppIssueAdmin(admin.ModelAdmin):
	list_display=("shortdesc", "longdesc", "issuedate")
	ordering=("issuedate", "shortdesc")
		
class LogEntryAdmin(admin.ModelAdmin):
    # to have a date-based drilldown navigation in the admin page
    date_hierarchy = 'action_time'

    # to filter the results by users, content types and action flags
    list_filter = [
        'user',
        'content_type',
        'action_flag'
    ]

    # when searching the user will be able to search in both object_repr and change_message
    search_fields = [
        'object_repr',
        'change_message'
    ]

    list_display = [
        'action_time',
        'user',
        'content_type',
        'action_flag',
    ]

class ProfileAdmin(admin.ModelAdmin):
   list_display=("user", "email_confirmed", "first_time_taken_modality_test", "otp_secret")

admin.site.register(LearningStyle, LearningStyleAdmin)
admin.site.register(LearningAssessment, LearningQuestionsAdmin)
admin.site.register(BaseSkill, BaseSkillAdmin)
admin.site.register(SkillTestQuestion, SkillTestQuestionAdmin)
admin.site.register(UserReports, UserReportsAdmin)
admin.site.register(ProfilePicture, ProfilePictureAdmin)
admin.site.register(LearningTool, LearningToolAdmin)
admin.site.register(AppIssue, AppIssueAdmin)
admin.site.register(LogEntry, LogEntryAdmin)
admin.site.register(Profile, ProfileAdmin)
