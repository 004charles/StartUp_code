from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractUser, Group, Permission


class Usuario(AbstractUser):
    nome = models.CharField(max_length=100)
    sobrenome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=100)
    data_nascimento = models.DateField()

    groups = models.ManyToManyField(Group, related_name="usuario_set", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="usuario_permissions_set", blank=True)

    def __str__(self):
        return self.username





class Administrador(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    permissao_gerenciar_usuarios = models.BooleanField(default=True)
    permissao_gerenciar_cursos = models.BooleanField(default=True)

class Instrutor(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    especializacao = models.CharField(max_length=255)
    bio = models.TextField(blank=True)
    foto_perfil = models.ImageField(upload_to='instrutor_fotos/', blank=True, null=True)

class Aluno(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    nivel_experiencia = models.CharField(max_length=50, choices=[
        ('iniciante', 'Iniciante'),
        ('intermediario', 'Intermediário'),
        ('avancado', 'Avançado'),
    ])
    interesses = models.CharField(max_length=255)

class Perfil(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    foto_perfil = models.ImageField(upload_to='perfil_fotos/', blank=True, null=True)
    telefone = models.CharField(max_length=15, blank=True, null=True)
    endereco = models.TextField(blank=True, null=True)
    cidade = models.CharField(max_length=100, blank=True, null=True)
    estado = models.CharField(max_length=100, blank=True, null=True)
    pais = models.CharField(max_length=100, blank=True, null=True)
    data_nascimento = models.DateField(blank=True, null=True)
    redes_sociais = models.JSONField(default=dict, blank=True)
    preferencias = models.JSONField(default=dict, blank=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Perfil de {self.usuario.username}"
# =======================
# Cursos e Conteúdo
# =======================
class Categoria(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)

class Curso(models.Model):
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    instrutor = models.ForeignKey(Instrutor, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)
    duracao_estimada = models.PositiveIntegerField(help_text="Duração em minutos")
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.BooleanField(default=True)
    data_publicacao = models.DateField(auto_now_add=True)

class Modulo(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200)
    ordem = models.PositiveIntegerField()
    duracao_estimada = models.PositiveIntegerField(help_text="Duração em minutos")

class Aula(models.Model):
    modulo = models.ForeignKey(Modulo, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200)
    conteudo = models.TextField()
    video = models.URLField(blank=True, null=True)

class MaterialComplementar(models.Model):
    aula = models.ForeignKey(Aula, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=50, choices=[
        ('pdf', 'PDF'),
        ('link', 'Link Externo'),
        ('outro', 'Outro')
    ])
    arquivo = models.FileField(upload_to='materiais/', blank=True, null=True)
    url = models.URLField(blank=True, null=True)

# =======================
# Avaliação e Certificação
# =======================
class Avaliacao(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    nota = models.PositiveIntegerField()
    feedback = models.TextField(blank=True)
    data_envio = models.DateField(auto_now_add=True)

class Certificado(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    data_conclusao = models.DateField(auto_now_add=True)
    codigo_validacao = models.CharField(max_length=100, unique=True)

# =======================
# Interatividade
# =======================
class Forum(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    autor = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    data_criacao = models.DateField(auto_now_add=True)

class Postagem(models.Model):
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE)
    autor = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    conteudo = models.TextField()
    data_publicacao = models.DateField(auto_now_add=True)

class Comentario(models.Model):
    postagem = models.ForeignKey(Postagem, on_delete=models.CASCADE)
    autor = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    conteudo = models.TextField()
    data_publicacao = models.DateField(auto_now_add=True)

# =======================
# Blogs
# =======================
class Blog(models.Model):
    titulo = models.CharField(max_length=200)
    autor = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    conteudo = models.TextField()
    data_publicacao = models.DateField(auto_now_add=True)
    imagem_capa = models.ImageField(upload_to='blog_covers/', blank=True, null=True)

class ComentarioBlog(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    autor = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    conteudo = models.TextField()
    data_publicacao = models.DateField(auto_now_add=True)

# =======================
# Pagamentos
# =======================
class PlanoAssinatura(models.Model):
    nome = models.CharField(max_length=100)
    preco_mensal = models.DecimalField(max_digits=10, decimal_places=2)
    preco_anual = models.DecimalField(max_digits=10, decimal_places=2)
    beneficios = models.TextField()
    status = models.BooleanField(default=True)

class Pedido(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=50, choices=[
        ('compra_unica', 'Compra Única'),
        ('assinatura', 'Assinatura')
    ])
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=[
        ('pendente', 'Pendente'),
        ('aprovado', 'Aprovado'),
        ('cancelado', 'Cancelado')
    ])

# =======================
# Gamificação
# =======================
class Pontuacao(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    pontos = models.PositiveIntegerField()
    data = models.DateField(auto_now_add=True)

class Badge(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    imagem = models.ImageField(upload_to='badges/')
    criterios = models.TextField()

# =======================
# Relatórios e Monitoramento
# =======================
class Progresso(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    percentual_conclusao = models.DecimalField(max_digits=5, decimal_places=2)
    ultimo_acesso = models.DateField(auto_now=True)

class RelatorioAcesso(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    data = models.DateField(auto_now_add=True)
    tempo_permanencia = models.PositiveIntegerField(help_text="Tempo em minutos")

# =======================
# Parcerias e Vagas
# =======================
class EmpresaParceira(models.Model):
    nome = models.CharField(max_length=200)
    contato = models.EmailField()
    site = models.URLField(blank=True, null=True)
    area_atuacao = models.CharField(max_length=100)

class Vaga(models.Model):
    empresa = models.ForeignKey(EmpresaParceira, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    requisitos = models.TextField()
    data_limite = models.DateField()



class Projeto(models.Model):
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    data_inicio = models.DateField()
    data_fim = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=[
        ('em_andamento', 'Em Andamento'),
        ('concluido', 'Concluído'),
        ('pausado', 'Pausado'),
        ('cancelado', 'Cancelado')
    ], default='em_andamento')
    responsavel = models.ForeignKey('Usuario', on_delete=models.SET_NULL, null=True, related_name='projetos')
    equipe = models.ManyToManyField('Usuario', related_name='projetos_participando', blank=True)
    data_criacao = models.DateField(auto_now_add=True)
    foto_projeto = models.ImageField(upload_to='projetos/', blank=True, null=True)

    def __str__(self):
        return self.titulo

