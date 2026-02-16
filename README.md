# SellSmartAI

Sistema de gestão comercial desenvolvido com **Django 5.0**, focado em PDV (Ponto de Venda), controle financeiro e gestão de produtos.

## 📋 Funcionalidades

- **PDV (Ponto de Venda)**: Interface para vendas e operações de caixa
- **Gestão de Produtos**: Cadastro de produtos, categorias e marcas
- **Controle Financeiro**: Gestão de entradas, saídas e fluxo de caixa
- **Pedidos**: Controle de pedidos e vendas
- **Dashboard**: Painel administrativo com indicadores
- **API REST**: Endpoints para integração com outros sistemas
- **Admin Personalizado**: Interface administrativa com Jazzmin

## 🛠️ Tecnologias

- **Backend**: Django 5.0
- **API**: Django REST Framework
- **Banco de Dados**: SQLite (desenvolvimento)
- **Frontend**: Templates Django + Bootstrap (tema Minty)
- **Testes**: pytest + pytest-django

## 📦 Instalação

### Pré-requisitos

- Python 3.11 ou superior
- pip (gerenciador de pacotes Python)
- Git

### Passo a passo

1. **Clone o repositório**
   ```bash
   git clone https://github.com/lennon-bitu/SellSmart.git
   cd SellSmartAI
   ```

2. **Crie um ambiente virtual**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # Linux/Mac
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Instale as dependências**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure as variáveis de ambiente (opcional)**
   
   O projeto funciona com configurações padrão, mas você pode personalizar criando um arquivo `.env`:
   ```env
   SECRET_KEY=sua-chave-secreta-aqui
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   ```

5. **Execute as migrações do banco de dados**
   ```bash
   python manage.py migrate
   ```

6. **Crie um superusuário para acessar o admin**
   ```bash
   python manage.py createsuperuser
   ```

7. **Colete os arquivos estáticos (opcional para desenvolvimento)**
   ```bash
   python manage.py collectstatic --noinput
   ```

## 🚀 Execução

### Servidor de Desenvolvimento

Com o ambiente virtual ativado, execute:

```bash
python manage.py runserver
```

O sistema estará disponível em: **http://127.0.0.1:8000**

- **Admin**: http://127.0.0.1:8000/admin/
- **API Docs**: http://127.0.0.1:8000/swagger/ (se configurado)

## 🧪 Testes

O projeto utiliza **pytest** para testes automatizados.

```bash
# Executar todos os testes
pytest

# Executar testes com output detalhado
pytest -v

# Executar apenas testes rápidos
pytest -m fast

# Executar com coverage
pytest --cov=.
```

## 📁 Estrutura do Projeto

```
SellSmartAI/
├── accounts/           # Autenticação e gestão de usuários
├── core/               # Configurações principais do Django
├── dashboard/          # Painel de indicadores
├── financial_control/  # Controle financeiro
├── order/              # Gestão de pedidos
├── pdv/                # Ponto de Venda
├── product/            # Gestão de produtos
├── templates/          # Templates HTML
├── static/             # Arquivos estáticos (CSS, JS, imagens)
├── media/              # Uploads de arquivos
└── manage.py           # Script de gerenciamento Django
```

## 🔐 Segurança

O projeto inclui configurações de segurança para produção:

- **HTTPS/HSTS**: Redirecionamento automático para HTTPS
- **Cookies seguros**: Session e CSRF cookies com flag `secure`
- **Clickjacking protection**: `X_FRAME_OPTIONS = 'DENY'`

Para produção, certifique-se de:
- Definir `DEBUG = False`
- Configurar `SECRET_KEY` forte via variável de ambiente
- Usar banco de dados production-ready (PostgreSQL recomendado)

## 📝 Comandos Úteis

```bash
# Criar novas migrações após mudanças nos models
python manage.py makemigrations

# Aplicar migrações
python manage.py migrate

# Iniciar shell interativo do Django
python manage.py shell

# Verificar problemas de configuração
python manage.py check

# Criar backup do banco (SQLite)
cp db.sqlite3 db_backup.sqlite3
```

## 🤝 Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abra um Pull Request

## 📄 Licença

Sell Smart LTDA

## 📞 Suporte

Para dúvidas ou problemas, abra uma issue no repositório.

---

**Desenvolvido com Django 5.0** 🚀
