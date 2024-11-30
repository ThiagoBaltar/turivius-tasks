Para rodar o projeto localmente é necessário instalar o Docker e o docker-compose

Com isso feito, clone o projeto e dentro da raíz do projeto, rode os seguintes comandos no terminal, em ordem.

make install
make start
make runserver

Isso irá fazer com que o projeto rode localmente na porta 8000.

Para acessar o admin do django: http://localhost:8000/admin/
As credencias são: admin:admin

Para acessar a documentação do swagger: http://localhost:8000/api/schema/swagger-ui/ ou http://localhost:8000/api/schema/redoc/

O fluxo de chamadas de enpoint para teste é:
Criação de usuário: http://localhost:8000/api/schema/redoc/#tag/users/operation/users_create
Login: http://localhost:8000/api/schema/redoc/#tag/tokens/operation/tokens_create
Criação de task: http://localhost:8000/api/schema/redoc/#tag/tasks/operation/tasks_create
Listagem de tasks: http://localhost:8000/api/schema/redoc/#tag/tasks/operation/tasks_list
Finalizar task: http://localhost:8000/api/schema/redoc/#tag/tasks/operation/tasks_finish_update
Resumir task: http://localhost:8000/api/schema/redoc/#tag/tasks/operation/tasks_resume_update
Deletar task: http://localhost:8000/api/schema/redoc/#tag/tasks/operation/tasks_destroy

Depois de terminar os testes, para liberar espaço na máquina, rode os seguintes comandos, em ordem:

make stop
make uninstall
make clean-layers
