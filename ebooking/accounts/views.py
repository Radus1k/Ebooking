from django.contrib.auth import login
from django.shortcuts import render, redirect
from .forms import MyUserCreationForm
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect

def register(request):
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = MyUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


class MyLoginView(LoginView):
    template_name = 'registration/login.html'

    def get_success_url(self):
        user = self.request.user
        if user.is_superuser:
            # Redirect to the admin page if the user is a superuser
            return reverse_lazy('admin:index')
        else:
            # Otherwise, redirect to the homepage
            return reverse_lazy('home')

    def form_valid(self, form):
        # Call the parent implementation to log the user in
        response = super().form_valid(form)

        # Redirect the user to the appropriate page
        return HttpResponseRedirect(self.get_success_url())




