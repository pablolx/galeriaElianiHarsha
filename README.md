# Eliani Harsha — site da artista

Site responsivo desenvolvido com Django para apresentar a biografia e as obras de Eliani Harsha, divulgar exposições e receber mensagens de contato. A administração de obras e eventos é feita pelo Django Admin.

## Desenvolvimento local

Requer Docker e Docker Compose:

```sh
cp .env.example .env
# Edite .env antes de usar SMTP ou credenciais próprias.
docker compose up --build
```

Acesse `http://localhost:8000`. O serviço importa as imagens de `IMG/` como obras iniciais na primeira execução. A importação é idempotente; imagens já importadas não são duplicadas. Os arquivos originais em `IMG/` permanecem intactos.

Para criar uma conta administrativa:

```sh
docker compose exec web python manage.py createsuperuser
```

O painel fica em `http://localhost:8000/admin/`. Somente usuários autenticados com acesso de equipe podem entrar. Use contas de superusuário para a artista e o administrador ou conceda a uma conta de equipe apenas as permissões de obras e exposições necessárias.

Para executar sem Docker, instale `requirements.txt` e execute `python manage.py migrate`, `python manage.py load_initial_artworks` e `python manage.py runserver`. Sem `DATABASE_URL`, o Django usa SQLite localmente.

## Obras, eventos e contato

No Admin, cadastre títulos, características, dimensões, materiais, data e local de criação. Marque obras como destaque para escolhê-las na página inicial; se nenhuma estiver marcada, são exibidas as obras publicadas mais recentes. Eventos publicados com data de início futura aparecem na página inicial.

Configure `CONTACT_EMAIL` para receber mensagens do formulário. Para SMTP, defina `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD` e `DEFAULT_FROM_EMAIL`. Sem `EMAIL_HOST`, o Django usa o backend de console. Configure `INSTAGRAM_URL` para exibir o perfil social. O detalhe de cada obra também oferece compartilhamento nativo do dispositivo ou cópia do link para publicá-lo no Instagram.

## Deploy no Render

Crie um **Blueprint** no Render apontando para este repositório. `render.yaml` configura um serviço web Docker, PostgreSQL e disco persistente para imagens cadastradas pelo Admin. O serviço web usa plano pago para suportar o disco persistente. Confira os preços vigentes de banco, serviço e disco no Render antes de implantar.

Configure `CONTACT_EMAIL`, dados SMTP, `DEFAULT_FROM_EMAIL` e `INSTAGRAM_URL` no painel do serviço, conforme necessário. `SECRET_KEY` é gerada pelo Blueprint. Atualize `ALLOWED_HOSTS` se usar um domínio diferente do endereço padrão. Migrações e importação idempotente das imagens iniciais são executadas ao iniciar o container.

Após o primeiro deploy, crie as contas administrativas pelo Shell do serviço:

```sh
python manage.py createsuperuser
```

## Verificação

Execute os testes com:

```sh
python manage.py test
```
