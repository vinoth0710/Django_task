# Import necessary modules and classes
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from Quora.models import Question, Like, Answer
from django.contrib import messages
from django.http import JsonResponse

# User Registration View
def registration(request):
    if request.method == 'POST':
        # Get user registration details from the form
        first_name = request.POST['first_name']
        username = request.POST['username']
        password = request.POST['password']

        # Create a new user
        user = User.objects.create_user(username=username, password=password, first_name=first_name)

        # Redirect to the login page after successful registration
        return redirect('Quora:login')
    
    # Render the registration form page
    return render(request, 'auth/registration.html')

# User Login View
def user_login(request):
    if request.method == 'POST':
        # Get user login details from the form
        username = request.POST['username']
        password = request.POST['password']

        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # If authentication is successful, log in the user and redirect to the user dashboard
            login(request, user)
            return redirect('Quora:user_dashboard')
        else:
            # If authentication fails, display an error message
            messages.error(request, 'Username or password is incorrect.')

    # Render the login form page
    return render(request, 'auth/login.html')

# User Logout View
def user_logout(request):
    # Log out the user and redirect to the login page
    logout(request)
    return redirect('Quora:login')

# User Dashboard View
def user_dashboard(request):
    if request.method == 'POST':
        question_id = request.POST.get('question_id')
        # Get the question object or return a 404 page if it doesn't exist
        question = get_object_or_404(Question, id=question_id)
        answers = Answer.objects.filter(question=question)
        
        if request.user.is_authenticated:
            for answer in answers:
                # Check if the user has liked the answer and update the 'liked' attribute
                if answer.like_set.filter(user=request.user).exists():
                    answer.liked = True
                else:
                    answer.liked = False
                    
        questions = Question.objects.all()
        
        # Prepare context data to pass to the template
        context = {
            "answers": answers,
            "questions": questions,
        }
        
        # Render the user dashboard page with the context data
        return render(request, "users/user_dashboard.html", context)

    questions = Question.objects.all()

    # Prepare context data to pass to the template
    context = {
        "questions": questions,
    }
    
    # Render the user dashboard page with the context data
    return render(request, "users/user_dashboard.html", context)

# Save Question Details View (Handles question creation)
@csrf_exempt
def save_question_details(request):
    if request.method == 'POST':
        try:
            user = request.user  
            text = request.POST.get('text', '')
            if text:
                # Create a new question and save it
                question = Question(user=user, text=text)
                question.save()
                response_data = {'success': True, 'message': 'Question saved successfully.'}
            else:
                response_data = {'success': False, 'message': 'Question text is required.'}
        except Exception as e:
            response_data = {'success': False, 'message': str(e)}
    else:
        response_data = {'success': False, 'message': 'Invalid request method.'}

    # Return a JSON response with the response data
    return JsonResponse(response_data)

# Add Answer View (Handles answer creation)
def add_answer(request):
    if request.method == 'POST':
        question_id = request.POST.get('question_id')
        answer_text = request.POST.get('answer_text')
        try:
            # Create a new answer and save it
            answer = Answer(user=request.user, question_id=question_id, text=answer_text)
            answer.save()
            return JsonResponse({'status': 'success', 'message': 'Answer added successfully.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

# Get Answers View (Retrieve the last answer for a question)
def get_answers(request):
    if request.method == 'GET':
        question_id = request.GET.get('question_id')
        try:
            # Retrieve the last answer by ordering in descending order by ID
            last_answer = Answer.objects.filter(question_id=question_id).order_by('-id').first()
            
            if last_answer is not None:
                answer_data = {'text': last_answer.text}
                return JsonResponse(answer_data)
            else:
                return JsonResponse({}, safe=False)
        except Answer.DoesNotExist:
            return JsonResponse({}, safe=False)
    
    return JsonResponse({}, safe=False)

# Like/Unlike Answer View (Handles liking and unliking answers)
@login_required
def like_unlike_answer(request, answer_id):
    if request.method == 'POST':
        answer = Answer.objects.get(pk=answer_id)
        user = request.user
        try:
            # Check if the user has already liked the answer
            like = Like.objects.get(user=user, answer=answer)
            # Unlike the answer
            like.delete()
            liked = False
        except Like.DoesNotExist:
            # Like the answer
            Like.objects.create(user=user, answer=answer)
            liked = True
        
        # Return a JSON response indicating whether the answer was liked or unliked
        return JsonResponse({'liked': liked})
