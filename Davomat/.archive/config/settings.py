from fastapi.templating import Jinja2Templates

templates = Jinja2Templates("admin/")

TORTOISE_ORM = {
    "connections": {
        "default": "sqlite://db.sqlite3"
    },
    "apps": {
        "models": {
            "models": ["app.models"],
            "default_connection": "default",
        }
    },
}
