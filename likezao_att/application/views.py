from unicodedata import decimal
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required, user_passes_test

from application.forms import BankDetailForm, RuleForm, UserForm, VarForm
from .models import User, BankDetail, Rule, Var
from django.conf import settings

from django.contrib import messages
import json
import random
import decimal
import pdb

def estrelas(request):
    rule = Rule.objects.last()
    return(Var.number_star) 

@login_required
def open_insta(request):
    rule = Rule.objects.last()
    if request.user.today_earning < request.user.maximum_earning_per_day:
        make_earning(request)
        return redirect("https://www.instagram.com/")
    messages.error(request, "Limite diário atingido!", render(home.html)) 
    return render(request, "home.html", {"type": "Instagram"})

@login_required
def open_tiktok(request):
    rule = Rule.objects.last()
    if request.user.today_earning < request.user.maximum_earning_per_day:
        make_earning(request)
        return redirect("https://www.tiktok.com/")
    messages.error(request, "Limite diário atingido!")
    return render(request, "open_page.html", {"type": "Tiktok"})

@login_required
def open_youtube(request):
    rule = Rule.objects.last()
    if request.user.today_earning < request.user.maximum_earning_per_day:
        make_earning(request)
        return redirect("https://www.youtube.com/")
    messages.error(request, "Limite diário atingido!")
    return render(request, "open_page.html", {"type": "YouTube"})

def make_earning(request):
    user = request.user
    rule = Rule.objects.last()
    earning = random.uniform(rule.minimum_per_click, rule.maximum_per_click)
    new_today_earning = user.today_earning + decimal.Decimal(earning)
    bank_detail = user.bank_details.last()
    bank_detail.total_earning = bank_detail.total_earning + decimal.Decimal(earning)
    user.today_earning=new_today_earning
    user.save()
    bank_detail.save()

def can_withdraw(user):
    rule = Rule.objects.last()
    if user.bank_details.last().total_earning >= rule.minimum_withdrawl:
        return True
    return False

def create_bank_details(user):
    user.bank_details.create()

@login_required
def bank_detail_update(request):
    bank_detail = request.user.bank_details.last()
    form = BankDetailForm(request.POST, instance=bank_detail)
    if form.is_valid():
        form.instance.user = request.user
        form.save()
        request.user.bank_details.create(branch=form.instance.branch, 
                                         account_number=form.instance.account_number, 
                                         name=form.instance.name,
                                         account_type=form.instance.account_type,
                                         bank_number=form.instance.bank_number)
        messages.success(request, 'Pedido de saque realizado, aguarde até 5 dias úteis.')
    else:
        messages.error(request, form.errors)
    return redirect(f"/home")
    
@login_required
def instagram(request):
    return render(request, "open_page.html", {"type": "Instagram"})

@login_required
def youtube(request):
    return render(request, "open_page.html", {"type": "YouTube"})

@login_required
def tiktok(request):
    return render(request, "open_page.html", {"type": "Tiktok"})


@login_required
def home(request):
    if request.user.is_superuser:
        return HttpResponseRedirect(reverse('admin:index'))
    try:
        rule = Rule.objects.last()
        width = request.user.bank_details.last().total_earning / decimal.Decimal(rule.minimum_withdrawl) * 100
        bank_detail = request.user.bank_details.last()
        start = Var.number_star
    except:
        rule = Rule.objects.last()
        width = request.user.bank_details.last().total_earning / decimal.Decimal(rule.minimum_withdrawl) * 100
        bank_detail = BankDetail()
        start = Var.number_star
    return render(request, "home.html", {'can_withdraw': can_withdraw(request.user), "bank_detail": bank_detail, "rule": rule, "width": width, start: "start"})

@csrf_exempt
def register(request):
    if request.method == 'POST':
        try:
            user = json.loads(request.body)["Customer"]
            if user:
                user = User.objects.create(full_name=user.get("full_name"), cpf=user.get("CPF"),
                                    email=user.get("email"), phone=user.get("mobile"), username=user.get("CPF"))
                if user:
                    create_bank_details(user)
                    return HttpResponse({"success": True})
        except:
            print(f"parsing error: {request.body}")
            return HttpResponse({"not saved": False})
    return HttpResponse({"success": False})

@csrf_exempt
def register_perfectpay(request):
    if request.method == 'POST':
        try:
            user = json.loads(request.body)["customer"]
            if user:
                user = User.objects.create(full_name=user.get("full_name"), cpf=user.get("identification_number"),
                                    email=user.get("email"), phone=user.get("phone_formated"), username=user.get("identification_number"))
                if user:
                    create_bank_details(user)
                    return HttpResponse({"success": True})
        except:
            print(f"parsing error: {request.body}")
            return HttpResponse({"not saved": False})
    return HttpResponse({"success": False})

@csrf_exempt
def register_orbita(request):
    if request.method == 'POST':
        try:
            user = request.POST
            if user:
                user = User.objects.create(full_name=user.get("cus_name"), cpf=user.get("cus_taxnumber"),
                                    email=user.get("cus_email"), phone=user.get("cus_tel"), username=user.get("cus_taxnumber"))
                if user:
                    create_bank_details(user)
                    return HttpResponse({"success": True})
        except Exception as e:
            print(f"parsing error: {request.body}: {e}")
            return HttpResponse({"not saved": False})
    return HttpResponse({"Não registrado": False})

def register_braip(request):
    if request.method == 'POST':
        try:
            user = json.loads(request.body)
            if user:
                user = User.objects.create(full_name=user.get("client_name"), cpf=user.get("client_documment"),
                                    email=user.get("client_email"), phone=user.get("client_cel"), username=user.get("client_documment"))
                if user:
                    create_bank_details(user)
                    return HttpResponse({"success": True})
        except Exception as e:
            print(f"parsing error: {request.body}: {e}")
            return HttpResponse({"not saved": False})
    return HttpResponse({"success": False})

@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        try:
            user = User.objects.get(cpf=request.POST.get('cpf'))
            user.backend = settings.AUTHENTICATION_BACKENDS[0]
            login(request, user)
            try:
                rule = Rule.objects.last()
                width = request.user.bank_details.last().total_earning / decimal.Decimal(rule.minimum_withdrawl) * 100
                bank_detail = user.bank_details.last()
            except:
                bank_detail = BankDetail()
                width = request.user.bank_details.last().total_earning / decimal.Decimal(rule.minimum_withdrawl) * 100
            return render(request, "home.html", {'can_withdraw': can_withdraw(user), "bank_detail": bank_detail, "rule": rule, "width": width})
        except User.DoesNotExist:
            messages.error(request, "CPF Invalido.")
            return redirect(request.META['HTTP_REFERER'])
    elif request.method == 'GET':
        if request.user.is_authenticated:
            return redirect("/home")
        return render(request, "registration/login.html", {})
    
@user_passes_test(lambda u: u.is_superuser)
def users_list(request):
    users = User.objects.all().filter(is_superuser=False)
    context = {
        'users': users,
        'rule': Rule.objects.last()
    }
    return render(request, 'users_list.html', context)

@user_passes_test(lambda u: u.is_superuser)
def user_insert(request):
    form = UserForm(request.POST)
    if form.is_valid():
        form.instance.username = form.instance.cpf
        form.save()
        create_bank_details(form.instance)
        messages.success(request, 'Usuário adicionado com sucesso')
    else:
        messages.error(request, form.errors)
    return redirect(f"/admin/users")

@user_passes_test(lambda u: u.is_superuser)
def user_detail(request, id):
    user = get_object_or_404(User, pk=id)
    bank_details = user.bank_details.all() if user else []
    if user:
        context = {
            'userr': user,
            'details': bank_details.reverse(),
            'rule': Rule.objects.last()
        }
        return render(request, 'user_detail.html', context)
    else:
        messages.error(request, "Not Found.")
        return redirect(request.META['HTTP_REFERER'])

@user_passes_test(lambda u: u.is_superuser)
def user_delete(request, id):
    try:
        user = User.objects.all().filter(is_superuser=False).get(id=id)  
        if user.delete():
            messages.success(request, 'Usuário excluído com sucesso')
        else:
            messages.error(request, 'Exclusão de usuário malsucedida')
        return redirect(f"/admin/users")
    except:
        messages.error(request, 'Usuário não encontrado.')
        return redirect(f"/admin/users")

@user_passes_test(lambda u: u.is_superuser)
def rule_detail(request):
    rule = Rule.objects.last()
    if rule is None: messages.error(request, "Nenhuma regra encontrada, você pode adicionar uma nova.")
    return render(request, 'rule_detail.html', {"rule": rule})

@user_passes_test(lambda u: u.is_superuser)
def password_change(request):
    return HttpResponseRedirect(reverse('admin:password_change'))

@user_passes_test(lambda u: u.is_superuser)
def rule_create_or_update(request):
    rule = Rule.objects.last()
    if rule:
        form = RuleForm(request.POST, instance=rule)
    else:
        form = RuleForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, 'Regra atualizada com sucesso')
    else:
        messages.error(request, form.errors)
    return redirect(f"/admin/rule")

@user_passes_test(lambda u: u.is_superuser)
def user_update(request, id):
    user = get_object_or_404(User, pk=id)
    form = UserForm(request.POST, instance=user)
    if form.is_valid():
        form.save()
        try:
            bank_detail = user.bank_details.last()
            bank_detail.total_earning = decimal.Decimal(float(request.POST['total_earning']))
            bank_detail.save()
        except:
            messages.error(request, "ganho não atualizado")
        messages.success(request, 'Usuário adicionado com sucesso')
    else:
        messages.error(request, form.errors)
    return redirect(f"/admin/user/{id}")

def page_not_found_view(request, exception):
    return render(request, '404.html', status=404)
