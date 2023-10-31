from django.db import models
from django.contrib.auth.models import User

# Define the Question model
class Question(models.Model):
    # User who posted the question
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # The text of the question
    text = models.TextField()
    
    # Date and time when the question was created
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Date and time when the question was last updated
    updated_at = models.DateTimeField(auto_now=True)

# Define the Answer model
class Answer(models.Model):
    # User who posted the answer
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # The question to which this answer is posted
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    
    # The text of the answer
    text = models.TextField()
    
    # Date and time when the answer was created
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Date and time when the answer was last updated
    updated_at = models.DateTimeField(auto_now=True)

# Define the Like model
class Like(models.Model):
    # User who liked the answer
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # The answer that is liked
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    
    # Date and time when the like was created
    created_at = models.DateTimeField(auto_now_add=True)
