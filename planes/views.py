from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from .forms import (
    LoginForm,
    RegisterForm,
    ContractForm,
    SumsBYNForm,
    SumsRURForm,
    PlanningForm, 
)
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.views import View
from datetime import date
from datetime import datetime as dt
from .models import (
    Contract,
    SumsBYN,
    SumsRUR,
    UserActivityJournal,
    Curator, 
    FinanceCosts, 
    Planning,
)
from django.shortcuts import get_object_or_404
from django.forms import model_to_dict
import json


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
        contracts = Contract.objects.filter(
            start_date__contains=self.today_year,
            contract_active=True).order_by('-id')
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


class ContractFabric(View):
    create_or_add = 'contracts/add_new_contract.html'

    def get(self, request, contract_id=None, from_ajax=None):
        ''' ajax methods'''
        if request.GET.__contains__('from_ajax'): # TODO here will be function to delete acontract
            if request.GET['from_ajax'] == 'del_contract':
                contract_id_list = request.GET.getlist('choosed[]')
                Contract.objects.filter(id__in=contract_id_list).update(contract_active=False)
                return HttpResponse('this is delete contract')


        if request.GET.__contains__('pattern_contract_id'): # TODO THIS IS COPY CONTRACT
            contract_id = int(request.GET['pattern_contract_id'])


        instance_contract, \
        instance_sum_byn, \
        instance_sum_rur = self.instances(contract_id)

        contract_form, sum_byn_form, sum_rur_form = self.inst_forms(instance_contract,
                                                                     instance_sum_byn,
                                                                     instance_sum_rur)
        return render(request,
                      template_name=self.create_or_add,
                      context={
                          'contract_form': contract_form,
                          'sum_byn_form': sum_byn_form,
                          'sum_rur_form': sum_rur_form,
                      })

    def post(self, request, contract_id=None):

        instance_contract, \
        instance_sum_byn, \
        instance_sum_rur = self.instances(contract_id)

        contract_form, sum_byn_form, sum_rur_form = self.inst_forms(instance_contract,
                                                                     instance_sum_byn,
                                                                     instance_sum_rur)

        contract_form = ContractForm(request.POST, instance=instance_contract) # TODO push it in def instance()
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


        return render(request,
                      template_name=self.create_or_add,
                      context={
                          'contract_form': contract_form,
                          'sum_byn_form': sum_byn_form,
                          'sum_rur_form': sum_rur_form,
                      })

    def instances(self, contract_id):
        if not contract_id:
            instance_contract = None
            instance_sum_byn = None
            instance_sum_rur = None
        else:
            instance_contract = get_object_or_404(Contract, id=contract_id)
            instance_sum_byn = get_object_or_404(SumsBYN, contract__id=contract_id)
            instance_sum_rur = get_object_or_404(SumsRUR, contract__id=contract_id)
        return instance_contract, instance_sum_byn, instance_sum_rur

    def inst_forms(self,
                    instance_contract,
                    instance_sum_byn,
                    instance_sum_rur):
        contract_form = ContractForm(instance=instance_contract)
        sum_byn_form = SumsBYNForm(instance=instance_sum_byn)
        sum_rur_form = SumsRURForm(instance=instance_sum_rur)
        return contract_form, sum_byn_form, sum_rur_form


def adding_click_to_UserActivityJournal(request):
     counter = UserActivityJournal.objects.get(user=request.user)
     counter.clicks += 1
     counter.save()
     return HttpResponse('add_click')


def plane(request):
    finance_costs = FinanceCosts.objects.all()
    # year = dt.now().year
    send_list = []
    money = None
    for item in finance_costs:
        try:
            money = item.with_planning.get(curator__title="ALL")
        except Planning.DoesNotExist:
            plan = Planning()
            plan.FinanceCosts = FinanceCosts.objects.get(pk = item.id)
            plan.curator = Curator.objects.get(title = "ALL")
            plan.q_1 = 0
            plan.q_2 = 0
            plan.q_3 = 0
            plan.q_4 = 0
            plan.year = dt.now().year
            plan.period = dt.now().date()
            plan.save()
            money = item.with_planning.get(curator__title="ALL")
        send_list.append([item, money])
    print(send_list)

    response = {"finance_costs": finance_costs,'send_list':send_list}
    return render(request, './planes/plane.html', response)


def curators(request, finance_cost_id):
    planning = Planning.objects.filter(FinanceCosts=finance_cost_id).exclude(curator__title='ALL')
    finance_cost_name = FinanceCosts.objects.get(pk=finance_cost_id).title
    response = {
        'planning': planning,
        'finance_cost_name': finance_cost_name,
        'finance_cost_id':finance_cost_id           
    }
    return render (request, './planes/curators.html', response)

  
def from_js(request):
    a = request.body.decode('utf-8')
    jsn = json.loads(a)
    try:
        result_curator = Curator.objects.get(title='ALL')
        id_result_curator = result_curator.id
    except Curator.DoesNotExist:
        print('error')
        result_curator = Curator()
        result_curator.title = 'ALL'
        result_curator.save()
        id_result_curator = result_curator.id


    finance_cost_title = jsn['cost_title']
    id_finance_cost = FinanceCosts.objects.get(title=finance_cost_title).id

    try:
        planing = Planning.objects.filter(FinanceCosts = id_finance_cost)
        result_cur = planing.get(curator__title='ALL')
    except Planning.DoesNotExist:
        plan = Planning()
        plan.FinanceCosts = FinanceCosts.objects.get(pk = id_finance_cost)
        plan.curator = Curator.objects.get(pk = id_result_curator)
        plan.q_1 = jsn['result_money'][0]
        plan.q_2 = jsn['result_money'][1]
        plan.q_3 = jsn['result_money'][2]
        plan.q_4 = jsn['result_money'][3]
        plan.year = dt.now().year
        plan.period = dt.now().date()
        plan.save()
        result_cur = planing.get(curator__title='ALL')
    
    if result_cur.q_1 != jsn['result_money'][0] : 
        result_cur.q_1 = jsn['result_money'][0]
        print('helo')
    if result_cur.q_2 != jsn['result_money'][1]:
        result_cur.q_2 = jsn['result_money'][1]
    if result_cur.q_3 != jsn['result_money'][2]:
        result_cur.q_3 = jsn['result_money'][2]
    if result_cur.q_4 != jsn['result_money'][3]:
        result_cur.q_4 = jsn['result_money'][3]
    result_cur.save()
    return HttpResponse('123')


def edit_plane(request, item_id):
    plan = Planning.objects.get(pk=item_id)
    plan_form = PlanningForm(instance=plan)
    response = {'plan_form':plan_form, 'item_id':item_id}
    print(request.POST)
    if(request.method == 'POST'):
        print('in post')
        plan_form = PlanningForm(request.POST, instance=plan)
        if plan_form.is_valid():
            if plan_form.cleaned_data.get('delete'):
                Planning.objects.get(pk=item_id).delete()
                return redirect(f'/plane/{str(plan.FinanceCosts.id)}/curators' ) 
            plan_form.save()
            return redirect(f'/plane/{str(plan.FinanceCosts.id)}/curators' )
    return render(request, './planes/edit_plane.html', response)

  
def add(request, finance_cost_id):
    plane_form = PlanningForm(initial={
        'FinanceCosts': finance_cost_id,
        'year': dt.now().year,
       'period':dt.now().date()
        })
    response = {
        'plane_form':plane_form,
        'finance_cost_id':finance_cost_id
    }
    if(request.method == 'POST'):
        plane_form = PlanningForm(request.POST)
        if plane_form.is_valid():
            plane_form.save()
            return redirect(f'/plane/{str(finance_cost_id)}/curators' )
    return render(request, './planes/add.html', response)
