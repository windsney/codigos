from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.db.models import Count
from .models import Militar
from django.views.generic import ListView
from django.db.models import Count, Q
from django.http import JsonResponse,HttpResponse
from django.views import View
from django.template.loader import render_to_string
from weasyprint import HTML
from django.utils import timezone

def dashboard(request):
    # Estatísticas por situação
    situacao_stats = Militar.objects.values('situacao_atual').annotate(total=Count('id'))
    
    # Contagem por unidade
    unidades = Militar.objects.values('unidade').annotate(total=Count('id')).order_by('-total')
    
    # Contagem por posto/grad
    postos = Militar.objects.values('posto_grad').annotate(total=Count('id')).order_by('posto_grad')
    
    # Contagem por função
    funcoes = Militar.objects.values('sub_lotacao_funcao').annotate(total=Count('id')).order_by('-total')[:10]

    # contagem inativoas
    total_inativos = Militar.objects.filter(
        Q(situacao_atual='Agregado') | 
        Q(situacao_atual='Em Curso') |
        Q(situacao_atual='Afastado/Licença') |
        Q(situacao_atual='Impedido Operacional')
    ).count()

    # contagem pronto emprego
    total_pronto = Militar.objects.filter(
        situacao_atual='Pronto Emprego'
        
    ).count()
    
   

    context = {
        'situacao_stats': situacao_stats,
        'unidades': unidades,
        'postos': postos,
        'funcoes': funcoes,
        'total_militares': Militar.objects.count(),
        'total_inativos': total_inativos,
        'total_pronto': total_pronto,

    }
    return render(request, 'pessoal/dashboard.html', context)

# views.py
from django.views.generic import ListView
from django.db.models import Q

class BaseMilitarListView(ListView):
    # Estatísticas por situação
    situacao_stats = Militar.objects.values('situacao_atual').annotate(total=Count('id'))
    
    # Contagem por unidade
    unidades = Militar.objects.values('unidade').annotate(total=Count('id')).order_by('-total')
    
    # Contagem por posto/grad
    postos = Militar.objects.values('posto_grad').annotate(total=Count('id')).order_by('posto_grad')
    
    # Contagem por função
    funcoes = Militar.objects.values('sub_lotacao_funcao').annotate(total=Count('id')).order_by('-total')[:10]

    # contagem inativoas
    total_inativos = Militar.objects.filter(
        Q(situacao_atual='Agregado') | 
        Q(situacao_atual='Em Curso') |
        Q(situacao_atual='Afastado/Licença') |
        Q(situacao_atual='Impedido Operacional')
    ).count()

    # contagem pronto emprego
    total_pronto = Militar.objects.filter(
        situacao_atual='Pronto Emprego'
        
    ).count()
    """
    View base para listagem de militares com filtros comuns
    """
    model = Militar
    template_name = 'pessoal/lista_militares.html'
    context_object_name = 'militares'
    paginate_by = 20
    titulo = 'Lista de Militares'
    filtro_situacoes = None
    filtro_pronto_emprego = None
    ordering = ['posto_grad', 'nome']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filtro por situações
        if self.filtro_situacoes:
            if isinstance(self.filtro_situacoes, str):
                self.filtro_situacoes = [self.filtro_situacoes]
            queryset = queryset.filter(situacao_atual__in=self.filtro_situacoes)
        
        # Filtro por pronto emprego
        if self.filtro_pronto_emprego is not None:
            queryset = queryset.filter(pronto_emprego=self.filtro_pronto_emprego)
        
        # Ordenação
        if self.ordering:
            queryset = queryset.order_by(*self.ordering)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'titulo': self.titulo,
            'total_militares': self.get_queryset().count()
        })
        return context


class ProntoEmpregoListView(BaseMilitarListView):
    titulo = 'Militares em Pronto Emprego'
    filtro_situacoes = 'Pronto Emprego'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()  # Obter o queryset filtrado
        
        context.update({
            'titulo': self.titulo,
            'total_militares': queryset.count(),  # Contagem após filtro
            # Garante que is_paginated está definido
            'is_paginated': self.paginate_by is not None and queryset.count() > self.paginate_by
        })
        return context
    

class BuscarValoresFiltroView(View):
    def get(self, request):
        campo = request.GET.get('campo')
        valores = []

        if campo:
            # Remove duplicatas e ordena os valores
            valores = Militar.objects.values_list(campo, flat=True).distinct().order_by(campo)
        
        return JsonResponse({'valores': list(valores)})

class PesquisarMilitaresListView(ListView):
    model = Militar
    template_name = 'pessoal/pesquisa_militares.html'
    context_object_name = 'militares'

    def get_queryset(self):
        queryset = super().get_queryset()
        
        campo = self.request.GET.get('campo_filtro')
        valor = self.request.GET.get('valor_filtro')
        
        if campo and valor:
            # Filtra os militares com base nos parâmetros
            filtro = {campo: valor}
            queryset = queryset.filter(**filtro)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now().date()  # Adiciona data atual ao contexto
        return context


def exportar_pdf(request):
    # Obtém os mesmos filtros da pesquisa
    campo = request.GET.get('campo_filtro')
    valor = request.GET.get('valor_filtro')
    
    # Filtra os militares (igual à view de pesquisa)
    militares = Militar.objects.all()
    if campo and valor:
        militares = militares.filter(**{campo: valor})
    
    # Renderiza o HTML como PDF
    html_string = render_to_string('pessoal/relatorio_pdf.html', {
        'militares': militares,
        'total': militares.count(),
        'filtro': f"{campo}: {valor}" if campo and valor else "Nenhum filtro aplicado"
    })
    
    html = HTML(string=html_string)
    pdf = html.write_pdf()
    
    # Retorna o PDF como download
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="militares_filtrados.pdf"'
    return response