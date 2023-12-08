from django.shortcuts import render, redirect
from reports.main import report
from django.contrib import messages
from users.models import Config

import json
from reports.models import FluxoChoice, AgrupadoPorChoice


def user_authentication(request):
    #messages.error(request, 'Usuário não logado')
    return redirect('login')

def reports(request, loogbook=None):
    if not request.user.is_authenticated:
        return user_authentication(request)

    context = {'fluxo_choices': FluxoChoice.choices,
               'agrupado_por_choices': AgrupadoPorChoice.choices,}

    if (request.method == 'POST'):
        data_update = request.POST.get('submit_button') == 'update'

        fluxo = request.POST.get('fluxo')
        agrupado_por = request.POST.get('agrupado_por')

        # Recupere o valor do campo oculto
        context_user_dict = request.POST.get('context_user_dict')
        if context_user_dict:
            # Atualize o contexto com o valor do campo oculto
            context['user_dict'] = json.loads(context_user_dict)

        

        user_dict = report(request, fluxo, agrupado_por, data_update)

        if not isinstance(user_dict, dict):
            messages.error(request, user_dict)
            context = {}
        else:

            config = Config.objects.get(fk_user=request.user)

            context = {
                'user_dict': user_dict,
                'fluxo_choices': FluxoChoice.choices,
                'agrupado_por_choices': AgrupadoPorChoice.choices,
                'fluxo_selected': fluxo,
                'agrupado_por_selected': agrupado_por,
                'jira_url':config.jira_url
            }

    return render(request, 'reports/report-up-down.html', context)
