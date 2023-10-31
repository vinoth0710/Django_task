from django.contrib import admin
from .models import Question, Answer, Like

# Create an admin class for the Question model
class QuestionAdmin(admin.ModelAdmin):
    # Specify the fields to display in the list view of the admin page for Question
    list_display = ("user", "text", "created_at", "updated_at")

# Create an admin class for the Answer model
class AnswerAdmin(admin.ModelAdmin):
    # Specify the fields to display in the list view of the admin page for Answer
    list_display = ("user", "text", "question", "created_at", "updated_at")

# Create an admin class for the Like model
class LikeAdmin(admin.ModelAdmin):
    # Specify the fields to display in the list view of the admin page for Like
    list_display = ("user", "answer", "created_at")

# Register the models with their respective admin classes
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Like, LikeAdmin)
