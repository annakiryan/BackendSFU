from pydantic import BaseModel
from pydantic import PostgresDsn
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class RunConfig(BaseModel):
    host: str = "127.0.0.1"
    port: int = 8000


class ApiV1Prefix(BaseModel):
    prefix: str = "/v1"
    auth: str = "/auth"
    users: str = "/users"
    tasks: str = "/tasks"
    brands: str = "/brands"
    cars: str = "/cars"
    customer_cars: str = "/customer_cars"
    order_service: str = "/order_service"
    orders: str = "/orders"
    role_user: str = "/role_user"
    roles: str = "/roles"
    services: str = "/services"


class ApiPrefix(BaseModel):
    prefix: str = "/api"
    v1: ApiV1Prefix = ApiV1Prefix()

    @property
    def bearer_token_url(self) -> str:
        # api/v1/auth/login
        parts = (self.prefix, self.v1.prefix, self.v1.auth, "/login")
        path = "".join(parts)
        # return path[1:]
        return path.removeprefix("/")


# class DatabaseConfig(BaseModel):
#     url: PostgresDsn
#     echo: bool = False
#     echo_pool: bool = False
#     pool_size: int = 50
#     max_overflow: int = 10

#     naming_convention: dict[str, str] = {
#         "ix": "ix_%(column_0_label)s",
#         "uq": "uq_%(table_name)s_%(column_0_N_name)s",
#         "ck": "ck_%(table_name)s_%(constraint_name)s",
#         "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
#         "pk": "pk_%(table_name)s",
#     }


class DatabaseConfig(BaseModel):
    url: str
    echo: bool = False
    future: bool = True

    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }


class AccessToken(BaseModel):
    lifetime_seconds: int = 3600
    reset_password_token_secret: str
    verification_token_secret: str


class StageEnv(BaseModel):
    name: str


class SMTPConfig(BaseModel):
    host: str
    port: int
    username: str
    password: str
    sender: str


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env.template", ".env"),
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
    )
    run: RunConfig = RunConfig()
    api: ApiPrefix = ApiPrefix()
    db: DatabaseConfig
    stage: StageEnv
    access_token: AccessToken

    smtp: SMTPConfig


settings = Settings()
