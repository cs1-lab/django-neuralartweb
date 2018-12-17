from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView
)
from django.urls import reverse_lazy
from .forms import (
    UserCreationForm, PassWordChangeForm
)
from django.contrib import messages


def signup(request):
    """
    新規登録するビュー
    :param request:
    :return:
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # ログインしてあげる
            return redirect('cms:home')
    else:
        form = UserCreationForm()

    return render(request, 'accounts/signup.html', {'form': form})


class OriginalPasswordChange(PasswordChangeView):
    """
    パスワード変更ビュー
    """
    from_class = PassWordChangeForm
    success_url = reverse_lazy('cms:home')
    template_name = 'accounts/password_change.html'

    def form_valid(self, form):
        logout(self.request)
        messages.success(self.request,
                         "パスワードの変更が完了しました。再度ログインしてください。",
                         extra_tags="check")
        return super(OriginalPasswordChange, self).form_valid(form)
