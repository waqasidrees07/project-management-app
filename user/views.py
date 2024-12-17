from django.shortcuts import render, HttpResponse
from .forms import SignupForm
from django.views.generic import View
from django.shortcuts import redirect
from django.contrib.auth import logout
# Create your views here.


class SignupView(View):
    def get(self, request):
        form = SignupForm()
        return render(request, "signup.html", {"form": form})

    def post(self, request):
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()

            return redirect("login")

        else:
            form = SignupForm()
        return render(request, "signup.html", {"form": form})


def custom_logout(request):
    logout(request)
    return redirect('login')
