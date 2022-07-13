from starlette.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")


def create_template(template, request, connector):
    available_connections = connector.get_all_connections()
    query_params = request.query_params
    logging = query_params["logging"] if "logging" in query_params else ""
    return templates.TemplateResponse(template,
                                      {"request": request,
                                       'logging': logging,
                                       'connections': [elem["db_name"] for elem in available_connections],
                                       })