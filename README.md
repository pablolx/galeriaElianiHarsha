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

O formulário e o link de contato usam `pablo.pinheiro@gmail.com` por padrão; altere `CONTACT_EMAIL` para outro endereço se necessário. Para entregar mensagens por e-mail, configure também `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD` e `DEFAULT_FROM_EMAIL`. Sem `EMAIL_HOST`, o Django usa o backend de console. Configure `INSTAGRAM_URL` para exibir o perfil social. O detalhe de cada obra também oferece compartilhamento nativo do dispositivo ou cópia do link para publicá-lo no Instagram.

## Deploy no Render via Blueprint

1. Envie este projeto para um repositório GitHub.
2. No Render, escolha **New > Blueprint**, conecte o repositório e selecione a branch que contém `render.yaml` (neste repositório, `master`).
3. Revise os recursos propostos e confirme a criação. O Blueprint provisiona o serviço web `eliani-harsha`, um banco PostgreSQL e um disco persistente para imagens enviadas pelo Admin.
4. Aguarde o primeiro deploy ficar saudável. O endpoint `/health/` é usado pelo Render para verificar o serviço.
5. Crie as contas de administração no Shell do serviço (instruções abaixo) e entre em `/admin/`.

O serviço web usa o plano `starter` e o banco usa `basic-256mb`; ambos são pagos. O disco persistente requer uma instância compatível e aumenta o custo. Confira os preços e a disponibilidade atuais na sua região e workspace antes de confirmar.

`SECRET_KEY` é gerada pelo Blueprint. `ALLOWED_HOSTS` inclui automaticamente o hostname padrão do Render (`RENDER_EXTERNAL_HOSTNAME`). Se conectar um domínio próprio, adicione seu hostname à variável `ALLOWED_HOSTS` no painel do serviço. O endereço de contato inicial é `pablo.pinheiro@gmail.com`.

Imagens que já estão no repositório são importadas para o disco na primeira inicialização, sem alterar os originais. O disco preserva novas imagens cadastradas pelo Admin entre deploys; mantenha-o anexado ao serviço. Migrações e importação idempotente das imagens iniciais são executadas na inicialização.

Para que o formulário realmente entregue e-mails, configure no painel do serviço `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD` e `DEFAULT_FROM_EMAIL` com as credenciais de um provedor SMTP. Sem SMTP, o Django usa o backend de console e não entrega a mensagem a uma caixa de entrada. `INSTAGRAM_URL` também pode ser definida no painel para exibir o perfil da artista.

Após o primeiro deploy, crie as contas administrativas pelo Shell do serviço:

```sh
python manage.py createsuperuser
```

## Verificação

Execute os testes com:

```sh
python manage.py test
```
