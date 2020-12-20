from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View, TemplateView
from django.http import HttpResponse
from django.template.loader import render_to_string
from .models import CheckList
from weasyprint import *


class CheckListView(TemplateView, LoginRequiredMixin):
    template_name = 'Check_list/check_list.html'

    def get(self, request, *args, **kwargs):
        check_lists = CheckList.objects.filter(author=request.user.profile)
        return render(request, self.template_name, {'check_lists': check_lists})


# @staff_member_required
@login_required
def check_list_pdf(request, key):
    check = get_object_or_404(CheckList, private_key=key)
    html = render_to_string('Check_list/check_list_pdf.html', {'check': check})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Dispositions'] = f'filename=check_{check.id}.pdf'
    HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(response, stylesheets=[CSS(
        'static/css/bootstrap.css'), CSS('static/css/check_list_pdf.css')], presentational_hints=True)
    return response
