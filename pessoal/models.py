from django.db import models

# Create your models here.
from django.db import models
from django.core.validators import MinLengthValidator
from django.utils import timezone
from django.core.exceptions import ValidationError

class Militar(models.Model):
    # Opções para campos com escolhas limitadas
    POSTO_GRAD_CHOICES = [
        ('Cel PM', 'Cel PM'),
        ('Ten Cel PM', 'Ten Cel'),
        ('Maj PM', 'Maj PM'),
        ('Cap PM', 'Cap PM'),
        ('1º Ten PM', '1º Ten PM'),
        ('2º Ten PM', '2º Ten PM'),
        ('Asp Of PM', 'Asp Of PM'),
        ('Sub Ten PM', 'Sub TeN PM'),
        ('1º Sgt PM', '1º Sgt PM'),
        ('2º Sgt PM', '2º Sgt PM'),
        ('3º Sgt PM', '3º Sgt PM'),
        ('Cb PM', 'Cb PM'),
        ('Sd PM', 'Sd PM'),
    ]

    Unidade = [
        ('5º BPM', '5º BPM'),
        
    ]

    SITUACAO_CHOICES = [
        ('Pronto Emprego', 'Pronto Emprego'),
        ('Férias', 'Férias'),
        ('Licença Prêmio', 'Licença Prêmio'),
        ('Agregado', 'Agregado'),
        ('Em Curso', 'Em Curso'),
        ('Impedido Operacional', 'Impedido Operacional'),
    ]

    # Campos principais
    posto_grad = models.CharField(
        'Posto/Graduação',
        max_length=20,
        choices=POSTO_GRAD_CHOICES
    )
    
    nome = models.CharField(
        'Nome Completo',
        max_length=100
    )
    
    qra = models.CharField(
        'QRA',
        max_length=20,
        unique=True,
        help_text='Identificação única do militar'
    )
    
    rgpm = models.CharField(
        'RGPM',
        max_length=15,
        unique=True,
        validators=[MinLengthValidator(6)]
    )
    
    validade_rgpm = models.DateField(
        'Validade RGPM',
        null=True,
        blank=True
    )
    
    cpf = models.CharField(
        'CPF',
        max_length=14,
        unique=True,
        validators=[MinLengthValidator(11)]
    )
    
    cnh = models.CharField(
        'CNH',
        max_length=20,
        null=True,
        blank=True
    )
    
    validade_cnh = models.DateField(
        'Validade CNH',
        null=True,
        blank=True
    )
    
    matricula = models.CharField(
        'Matrícula',
        max_length=20,
        unique=True
    )
    
    unidade = models.CharField(
        'unidade',
        max_length=20,
        choices=Unidade
    )
    
    sub_lotacao_funcao = models.CharField(
        'Sub Lotação/Função',
        max_length=100,
        null=True,
        blank=True
    )
    
    situacao_atual = models.CharField(
        'Situação Atual',
        max_length=20,
        choices=SITUACAO_CHOICES,
        default='Ativo'
    )
    
    detalhes_situacao = models.TextField(
        'Detalhes da Situação',
        max_length=500,
        null=True,
        blank=True
    )

    telefone = models.CharField(
        'Telefone', 
        max_length=15, 
        blank=True, 
        null=True,
        help_text='Formato: (DDD) 99999-9999'
    )

    # Metadados
    class Meta:
        verbose_name = 'Militar'
        verbose_name_plural = 'Militares'
        ordering = ['posto_grad', 'nome']

    def __str__(self):
        return f'{self.posto_grad} {self.nome} ({self.qra})'

    # Validação adicional (opcional)
    def clean(self):

        # Validação da validade do RGPM (original)
        if self.validade_rgpm and self.validade_rgpm < timezone.now().date():
            raise ValidationError({'validade_rgpm': 'A validade do RGPM está expirada.'})

        # Validações para CNH
        if self.cnh or self.validade_cnh:
            # Validação 1: Se tem CNH, deve ter validade
            if self.cnh and not self.validade_cnh:
                raise ValidationError({
                    'validade_cnh': 'É obrigatório informar a validade quando há CNH.'
                })

            # Validação 2: Se tem validade, deve ter número da CNH
            if self.validade_cnh and not self.cnh:
                raise ValidationError({
                    'cnh': 'É obrigatório informar o número da CNH quando há validade.'
                })

            # Validação 3: CNH não pode ter menos de 11 dígitos
            if self.cnh and len(self.cnh.replace('.', '').replace('-', '')) < 11:
                raise ValidationError({
                    'cnh': 'CNH deve conter pelo menos 11 dígitos.'
                })

            # Validação 4: Data de validade não pode ser no passado
            if self.validade_cnh and self.validade_cnh < timezone.now().date():
                raise ValidationError({
                    'validade_cnh': 'A validade da CNH está expirada.'
                })

        # Validação extra: Se não tem CNH, não pode ter validade
        if not self.cnh and self.validade_cnh:
            raise ValidationError({
                'cnh': 'Informe o número da CNH pois a validade foi preenchida.',
                'validade_cnh': 'Informe a CNH primeiro.'
            })
