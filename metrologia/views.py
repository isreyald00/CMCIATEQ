from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.forms import BaseModelForm, modelformset_factory, formset_factory
from django.views import generic
from django.db import transaction
from django import forms

from .forms import  DetalleControlMetroForm, EspecificacionMetrologicaForm, IncertidumbreForm
from .models import CriteriosMetrologicos, EspecificacionMetrologia, Criterio
from usuarios.views import is_in_allowed_groups
from inventario.models import Equipo

@login_required
def metrologiaView(request):
    return render(request, "metrologia/metrologia.html")

class AgregarEspecificacionMetrologicaView(generic.CreateView):
    model = EspecificacionMetrologia
    form_class = EspecificacionMetrologicaForm
    template_name = 'metrologia/EspecificacionMetrologica.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        formset = None
        
        cal = self.kwargs.get('cal') == "1"
        ver = self.kwargs.get('ver') == "1"

        DetCtrlMetroFormset = modelformset_factory(CriteriosMetrologicos, form=DetalleControlMetroForm, extra = 0)
        initial_values = [{'id_criterio': 'Error'}, {'id_criterio': 'Incertidumbre'}]

        if ver:
            DetCtrlMetroFormset.min_num = 1 
            formset = DetCtrlMetroFormset(self.request.POST or None, queryset=CriteriosMetrologicos.objects.none(),initial=initial_values, prefix='detalle_control_metro')
            if not self.request.POST:
                formset[0].fields['id_criterio'].widget = forms.TextInput(attrs={'readonly': 'readonly'})

        if cal:
            DetCtrlMetroFormset.min_num = 2
            formset = DetCtrlMetroFormset(self.request.POST or None, queryset=CriteriosMetrologicos.objects.none(), initial=initial_values, prefix='detalle_control_metro')
            if not self.request.POST:
                formset[0].fields['id_criterio'].widget = forms.TextInput(attrs={'readonly': 'readonly'})
                formset[1].fields['id_criterio'].widget = forms.TextInput(attrs={'readonly': 'readonly'})

        context['id_equipo'] = self.kwargs.get('equipo')
        context['formset'] = formset
        return context

    def form_valid(self, form):
        with transaction.atomic():
            equipo = get_object_or_404(Equipo, id = self.kwargs.get('equipo'))

            ctrlMetro = form.save(commit=False)
            ctrlMetro.id_equipo = equipo
            ctrlMetro.save()

            # Recuperar el formset del contexto
            formset = self.get_context_data().get('formset')

            if formset and formset.is_valid():
                for detalle_form in formset:
                    if detalle_form.is_valid():
                        detalle = detalle_form.save(commit=False)
                        detalle.id_controlMetro = ctrlMetro
                        if detalle.valor_esperado:
                            detalle.save()
                        else:
                            print("if detalle.valor_esperado:")
                            return super().form_invalid(form)
                    else:
                        print("if detalle_form.is_valid():")
                        return super().form_invalid(form)
            else:
               print("if formset and formset.is_valid():")
               return super().form_invalid(form) 

            return super().form_valid(form)

    def get_success_url(self) -> str:
        cal = self.kwargs.get('cal') == "1"
        ver = self.kwargs.get('ver') == "1"
        equipo = self.kwargs.get('equipo')

        if cal and ver:
            return reverse('calibracion:registrarEsp', kwargs={'equipo': equipo, 'ver': "1"})
        elif cal:
            return reverse('calibracion:registrarEsp', kwargs={'equipo': equipo, 'ver': "0"})
        elif ver:
            return reverse('verificacion:registrarEsp', kwargs={'equipo': equipo})
        else:
            return reverse('inventario:detalles', kwargs={'pk': equipo})


@user_passes_test(is_in_allowed_groups)
def AgregarEspecificacionMetrologicaView0(request, equipo=None, cal = None, ver = None):
    context = {}
    id_equipo = None
    formset = None
    if request.session.get('equipo_id') is not None:
        print("Entro a equipo recogido de la sesión")
        id_equipo = request.session.get('equipo_id')
        cal = request.session.get('calibracion')
        ver = request.session.get('verificacion')
    elif equipo is not None:
        print("Entro a equipo recogido de la URL")
        id_equipo = Equipo.objects.get(id = equipo)
        cal = cal == "1"
        ver = ver == "1"
    
    DetCtrlMetroFormset = modelformset_factory(CriteriosMetrologicos, form=DetalleControlMetroForm, extra=0)

    if ver:
        print("Entro a crear formset con 1 criterio predefinido para verificacion: Error")
        error = get_object_or_404(Criterio, id='Error')
        criterios = [CriteriosMetrologicos(id_criterio=error)]
        DetCtrlMetroFormset.min_num = 1
        initial_values = [{'id_criterio': obj.id_criterio} for obj in criterios]
        formset = DetCtrlMetroFormset(request.POST or None, queryset=CriteriosMetrologicos.objects.none(),initial=initial_values, prefix='detalle_control_metro')
        for form in formset:
            form.fields['id_criterio'].widget = forms.TextInput(attrs={'readonly': 'readonly'})   
    if cal:
        print("Entro a crear formset con criterios predefinidos para calibración: Error e Incertidumbre")
        error = get_object_or_404(Criterio, id='Error')
        incertidumbre = get_object_or_404(Criterio, id='Incertidumbre')
        criterios = [CriteriosMetrologicos(id_criterio=error), CriteriosMetrologicos(id_criterio=incertidumbre),]
        DetCtrlMetroFormset.min_num = 2
        initial_values = [{'id_criterio': obj.id_criterio} for obj in criterios]
        formset = DetCtrlMetroFormset(request.POST or None, queryset=CriteriosMetrologicos.objects.none(),initial=initial_values,prefix='detalle_control_metro')
        for form in formset:
            form.fields['id_criterio'].widget = forms.TextInput(attrs={'readonly': 'readonly'}) 

    form = EspecificacionMetrologicaForm(request.POST or None, initial={'id_equipo':id_equipo})
    form.fields['id_equipo'].widget = forms.TextInput(attrs={'readonly': 'readonly'})

    if request.method == "POST":
        if form.is_valid() and formset.is_valid():
            
            with transaction.atomic():
                especificacion = form.save(commit=False)
                especificacion.save()
                for detalle_form in formset:
                    detalle = detalle_form.save(commit=False)
                    detalle.id_controlMetro = especificacion
                    detalle.save()

            if cal and ver:
                return redirect('calibracion:registrarEsp', equipo=equipo, ver="1")
            elif cal:
                return redirect('calibracion:registrarEsp', equipo=equipo, ver="0")
            elif ver:
                return redirect('verificacion:registrarEsp', equipo=equipo)
            else:
                return redirect('inventario:detalles', pk= equipo)
    
    context['formset'] = formset
    context['form'] = form
    return render(request, 'metrologia/EspecificacionMetrologica.html', context)

@method_decorator(user_passes_test(is_in_allowed_groups), name='dispatch')
class AgregarIncertidumbreView(generic.CreateView):
    model = CriteriosMetrologicos
    form_class = IncertidumbreForm
    template_name = 'metrologia/agregarIncertidumbre.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id_equipo = self.kwargs.get('equipo', None)
        context['id_equipo'] = id_equipo
        context['criterio'] = "Incertidumbre"
        return context

    def form_valid(self, form):
        try:
            equipo = self.kwargs.get('equipo', None)
            print("Equipo: ", equipo)
            incertidumbre = "Incertidumbre"
            ctrlMetro = EspecificacionMetrologia.objects.get(id_equipo = equipo)
            criterio  = form.save(commit=False)
            criterio.id_controlMetro = ctrlMetro
            criterio.id_criterio = incertidumbre
            criterio.save()
            return super().form_valid(form)
        except:
            return super().form_invalid(form)
    
    def get_success_url(self):
        equipo = self.kwargs.get('equipo', None)
        return reverse('calibracion:registrarEsp', args=(equipo,"0"))