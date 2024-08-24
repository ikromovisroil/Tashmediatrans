from django.shortcuts import render,redirect,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages
from django.shortcuts import get_object_or_404
from users.models import *
from .models import *
from .forms import *
from django.db import connection
from django.db.models import Max
from django.db.models import F, Q, Sum, Value, Case, When, IntegerField
from django.db.models.functions import Coalesce
import datetime
# Create your views here.

@login_required
def profil(request):
    if request.method == 'POST':
        form = Userprofilform(request.POST, files=request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.info(request, "Saqlandi ")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            messages.success(request, "Yaroqsiz maʼlumot !")
    else:
        form = Userprofilform(instance=request.user)
    context = {
        'form': form,
        'user': request.user,
    }
    return render(request, 'main/profil.html',context)


@login_required
def index(request):
    istemolchi_max = Istemolchi.objects.aggregate(Max('id'))
    istemolchi_max_id = istemolchi_max['id__max']
    if request.method == 'POST':
        form = NewIshchiForm(data=request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.author = request.user
            if istemolchi_max_id is not None:
                user.id = istemolchi_max_id + 1
            user.save()
            messages.info(request, "Saqlandi")
            return redirect(reverse('index'))
        else:
            messages.error(request, "Yaroqsiz maʼlumot.")
    else:
        form = NewIshchiForm()
    if request.user.is_superuser:
        istemolchi = Istemolchi.objects.all().annotate(
            summa=Sum(
                Case(
                    When(qarz__status=False, then='qarz__summa'),
                    default=0,
                    output_field=IntegerField()
                )
            )
        ).order_by('-id')
    else:
        istemolchi = Istemolchi.objects.filter(author=request.user).annotate(
            summa=Sum(
                Case(
                    When(qarz__status=False, then='qarz__summa'),
                    default=0,
                    output_field=IntegerField()
                )
            )
        ).order_by('-id')
    jami_sum = istemolchi.aggregate(Sum('summa'))['summa__sum']
    context = {
        'istemolchi': istemolchi,
        'form': form,
        'user': request.user,
        'jami_sum': jami_sum,
    }
    return render(request, 'main/index.html', context)


@login_required
def detail(request,pk):
    istemolchi_id = get_object_or_404(Istemolchi, id=pk)
    if request.method == 'POST':
        form = QarzForm(request.POST)
        if form.is_valid():
            qarz = form.save(commit=False)
            qarz.istemolchi = istemolchi_id
            qarz.author = request.user
            qarz.save()
            messages.info(request, "Saqlandi ")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            messages.success(request, "Yaroqsiz maʼlumot !")
    else:
        form = QarzForm()
    context = {
        'form':form,
        'istemolchi_id':istemolchi_id,
        'qarzlar':Qarz.objects.filter(istemolchi=istemolchi_id,status=False)[::-1],
        'user': request.user,
    }
    return render(request, 'main/detail.html',context)

@login_required
def qarz_delete(request, pk):
    qarz = get_object_or_404(Qarz, id=pk)
    qarz.status = True
    qarz.save()
    messages.info(request, "O'chirildi!")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def Xaydovchilar(request):
    if request.method == 'POST':
        sana = request.POST.get('sana')
        try:
            sana = datetime.datetime.strptime(sana, "%Y-%m-%d").date()
        except (ValueError, TypeError):
            sana = datetime.date.today()
    else:
        sana = datetime.date.today()

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT i.id, i.full_name, a.nomi, a.raqami, i.tel, t.naxt, t.karta, t.izox
            FROM istemolchi i
            INNER JOIN aftomabil a ON i.aftomabil_id = a.id
            LEFT JOIN tolov t ON t.istemolchi_id = i.id AND t.date = %s
            WHERE i.status = True;
        """, [sana])
        istemolchi = cursor.fetchall()

    context = {
        'sana': sana,
        'istemolchi': istemolchi,
        'user': request.user,
    }
    return render(request, 'main/Xaydovchilar.html', context)


@login_required
def payment(request,pk):
    istemolchi_id = get_object_or_404(Istemolchi, id=pk)
    if request.method == 'POST':
        form = TolovForm(request.POST)
        if form.is_valid():
            tolov = form.save(commit=False)
            tolov.istemolchi = istemolchi_id
            tolov.author = request.user
            tolov.save()
            messages.info(request, "Saqlandi ")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            messages.success(request, "Yaroqsiz maʼlumot !")
    else:
        form = TolovForm()
    context = {
        'form': form,
        'tolov': Tolov.objects.filter(istemolchi=istemolchi_id).order_by('-date')[:60],
        'istemolchi_id': istemolchi_id,
        'user': request.user,
    }
    return render(request, 'main/payment.html',context)


@login_required
def payment_edit(request, pk):
    tolov_id = get_object_or_404(Tolov, id=pk)
    if request.method == 'POST':
        naxt = request.POST.get('naxt')
        karta = request.POST.get('karta')
        izox = request.POST.get('izox')
        if naxt and karta:
            tolov_id.karta = karta
            tolov_id.naxt = naxt
            tolov_id.izox = izox
            tolov_id.save()
            messages.info(request, "Saqlandi")
        elif karta:
            tolov_id.karta = karta
            tolov_id.izox = izox
            tolov_id.save()
            messages.info(request, "Saqlandi")
        elif naxt:
            tolov_id.naxt = naxt
            tolov_id.izox = izox
            tolov_id.save()
            messages.info(request, "Saqlandi")
        else:
            messages.error(request, "Yaroqsiz ma'lumot.")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect(reverse('login'))


@login_required
def employee(request):
    context = {
        'xodimlar' : Xodim.objects.all(),
        'user': request.user,
    }
    return render(request, 'main/employee.html',context)

@login_required
def avans(request,pk):
    xodim_id = get_object_or_404(Xodim, id=pk)
    if request.method == 'POST':
        form = MaoshForm(request.POST)
        if form.is_valid():
            maosh = form.save(commit=False)
            maosh.xodim = xodim_id
            maosh.author = request.user
            maosh.save()
            messages.info(request, "Saqlandi ")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            messages.success(request, "Yaroqsiz maʼlumot !")
    else:
        form = MaoshForm()
    context = {
        'form': form,
        'maosh':Maosh.objects.filter(xodim=xodim_id),
        'xodim_id': xodim_id,
        'user': request.user,
    }
    return render(request, 'main/avans.html',context)

@login_required
def avans_edit(request, pk):
    maosh = get_object_or_404(Maosh, id=pk)
    if request.method == 'POST':
        summa = request.POST.get('summa')
        izox = request.POST.get('izox')
        if summa:
            maosh.summa = summa
            maosh.izox = izox
            maosh.save()
            messages.info(request, "Saqlandi")
        else:
            messages.error(request, "Yaroqsiz ma'lumot.")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect(reverse('login'))
    
@login_required
def aftomabil(request):
    context = {
        'aftomabil': Aftomabil.objects.all(),
        'user': request.user,
    }
    return render(request, 'main/aftomabil.html',context)

@login_required
def xarajatlar(request,pk):
    aftomabil_id = get_object_or_404(Aftomabil, id=pk)
    if request.method == 'POST':
        form = Car_costForm(request.POST)
        if form.is_valid():
            xarajat = form.save(commit=False)
            xarajat.aftomabil = aftomabil_id
            xarajat.author = request.user
            xarajat.save()
            messages.info(request, "Saqlandi ")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            messages.success(request, "Yaroqsiz maʼlumot !")
    else:
        form = Car_costForm()
    context = {
        'form':form,
        'xarajatlar': Car_cost.objects.filter(aftomabil=aftomabil_id)[::-1],
        'aftomabil_id': aftomabil_id,
        'user': request.user,
    }
    return render(request, 'main/xarajatlar.html',context)


@login_required
def car_aktiv(request,pk):
    aftomabil_id = get_object_or_404(Aftomabil, id=pk)
    if aftomabil_id.status == True:
        aftomabil_id.status=False
    else:
        aftomabil_id.status = True
    aftomabil_id.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
    
    
    
