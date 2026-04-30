from django.http import HttpResponse
from django.contrib.auth.models import User
from django.db import connection

def home(request):
    return HttpResponse("Home page")

def profile(request, user_id):
    # VULNERABLE: user can access any profile by changing URL
    user = User.objects.get(id=user_id)

    # fix would be:
    # if request.user.id != user_id:
    #     return HttpResponse("Forbidden", status=403)
    # user = request.user

    return HttpResponse(f"Username: {user.username}")

def search(request):
    query = request.GET.get('q', '')

    # VULNERABLE: raw SQL injection
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT username FROM auth_user WHERE username LIKE '%{query}%'")
        results = cursor.fetchall()

    # fix would be:
    # cursor.execute("SELECT username FROM auth_user WHERE username LIKE %s", [f"%{query}%"])

    return HttpResponse(str(results))

def login_view(request):
    username = request.GET.get('username')
    password = request.GET.get('password')

    # VULNERABLE: no real authentication
    if username == "admin" and password == "admin":
        return HttpResponse("Logged in as admin")

    # fix would be:
    # from django.contrib.auth import authenticate
    # user = authenticate(request, username=username, password=password)
    # if user:
    #     return HttpResponse("Logged in")

    return HttpResponse("Login failed")
def transfer(request):
    amount = int(request.GET.get("amount", "0"))

    balance = 100

    # VULNERABLE: negative amounts are accepted
    new_balance = balance - amount

    # fix would be:
    # if amount <= 0:
    #     return HttpResponse("Invalid transfer amount", status=400)
    # new_balance = balance - amount

    return HttpResponse(f"Old balance: {balance}, transfer amount: {amount}, new balance: {new_balance}")