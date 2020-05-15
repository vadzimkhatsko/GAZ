from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from .forms import (
    LoginForm,
    RegisterForm,
    ContractForm,
    SumsBYNForm,
    SumsRURForm,
)
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.views import View
from datetime import date
from .models import (
    Contract,
    SumsBYN,
    SumsRUR,
    UserActivityJournal,
)
from django.shortcuts import get_object_or_404
from django.forms import model_to_dict


@login_required
def index(request):
    return render(request, 'planes/index.html')


@login_required
def logout_view(request):
    logout(request)
    return render(request, 'planes/index.html')


def login_view(request,):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('/')
                else:
                    return HttpResponse('disable account')
            else:
                return redirect('/login/')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})


@login_required
def register_view(request):
    form = None
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        email = request.POST.get('email')
        username = request.POST.get('username')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Пользователь с таким адресом уже существует')
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Пользователь с таким именем уже существует')
        else:
            if form.is_valid():
                username = form.cleaned_data['username']
                email = email
                password = User.objects.make_random_password(4)
                user = User.objects.create_user(
                    username,
                    email,
                    password
                )
                user.save()
                create_journal = UserActivityJournal.objects.create(user=user)
                create_journal.save()
                send_mail(
                    'Hello from GAZ',
                    'Ваш пароль: ' + str(password),
                    'gazprombelgaz@gmail.com',
                    [email],
                    fail_silently=False
                )
                return HttpResponse(("Регистрация прошла успешна, пароль отправлен на почту: %s") % str(email))
    else:
        form = RegisterForm()
    context = {'form': form}
    return render(request, 'registration/register.html', context)


class ContractView(View):
    template_name = 'contracts/contract_main.html'
    today_year = date.today().year

    def get(self, request):
        contracts = Contract.objects.filter(start_date__contains=self.today_year).order_by('-id')
        contract_and_sum = []
        for contract in contracts:
            sum_byn = SumsBYN.objects.get(contract=contract)
            sum_rur = SumsRUR.objects.get(contract=contract)
            contract_and_sum.append(
                {
                    'contract':contract,
                    'sum_byn':sum_byn,
                    'sum_rur':sum_rur,
                }
            )
        return render(request,
                      template_name=self.template_name,
                      context={'contracts':contracts,
                               'contract_and_sum':contract_and_sum,
                               })


@login_required
def fabricate_contract(request, contract_id=None):
    if not contract_id:
        instance_contract = None
        instance_sum_byn = None
        instance_sum_rur = None
    else:
        instance_contract = get_object_or_404(Contract, id=contract_id)
        instance_sum_byn = get_object_or_404(SumsBYN, contract__id=contract_id)
        instance_sum_rur = get_object_or_404(SumsRUR, contract__id=contract_id)

    if request.method == 'POST':
        contract_form = ContractForm(request.POST, instance=instance_contract)
        sum_byn_form = SumsBYNForm(request.POST, instance=instance_sum_byn)
        sum_rur_form = SumsRURForm(request.POST, instance=instance_sum_rur)
        if \
                contract_form.is_valid() \
                        and sum_byn_form.is_valid() \
                        and sum_rur_form.is_valid():
            new_contract = contract_form.save()
            contract_sum_b = sum_byn_form.save(commit=False)
            contract_sum_b.contract = new_contract
            contract_sum_b.save()
            contract_sum_r = sum_rur_form.save(commit=False)
            contract_sum_r.contract = new_contract
            contract_sum_r.save()
            return HttpResponse('saved')

    contract_form = ContractForm(instance=instance_contract)
    sum_byn_form = SumsBYNForm(instance=instance_sum_byn)
    sum_rur_form = SumsRURForm(instance=instance_sum_rur)
    return render(request,
                  template_name='contracts/add_new_contract.html',
                  context={
                      'contract_form': contract_form,
                      'sum_byn_form': sum_byn_form,
                      'sum_rur_form': sum_rur_form,
                  })


def adding_click_to_UserActivityJournal(request):
     counter = UserActivityJournal.objects.get(user=request.user)
     counter.clicks += 1
     counter.save()
     return HttpResponse('add_click')
