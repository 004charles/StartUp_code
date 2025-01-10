from django.contrib import admin
from .models import (
    Usuario, Administrador, Instrutor, Aluno, Perfil,
    Categoria, Curso, Modulo, Aula, MaterialComplementar,
    Avaliacao, Certificado, Forum, Postagem, Comentario,
    Blog, ComentarioBlog, PlanoAssinatura, Pedido,
    Pontuacao, Badge, Progresso, RelatorioAcesso,
    EmpresaParceira, Vaga, Projeto
)

# Registra os modelos
admin.site.register(Usuario)
admin.site.register(Administrador)
admin.site.register(Instrutor)
admin.site.register(Aluno)
admin.site.register(Perfil)

# Registra os modelos de Cursos e Conteúdo
admin.site.register(Categoria)
admin.site.register(Curso)
admin.site.register(Modulo)
admin.site.register(Aula)
admin.site.register(MaterialComplementar)

# Registra os modelos de Avaliação e Certificação
admin.site.register(Avaliacao)
admin.site.register(Certificado)

# Registra os modelos de Interatividade
admin.site.register(Forum)
admin.site.register(Postagem)
admin.site.register(Comentario)

# Registra os modelos de Blogs
admin.site.register(Blog)
admin.site.register(ComentarioBlog)

# Registra os modelos de Pagamentos
admin.site.register(PlanoAssinatura)
admin.site.register(Pedido)

# Registra os modelos de Gamificação
admin.site.register(Pontuacao)
admin.site.register(Badge)

# Registra os modelos de Relatórios e Monitoramento
admin.site.register(Progresso)
admin.site.register(RelatorioAcesso)

# Registra os modelos de Parcerias e Vagas
admin.site.register(EmpresaParceira)
admin.site.register(Vaga)

# Registra o modelo de Projetos
admin.site.register(Projeto)
