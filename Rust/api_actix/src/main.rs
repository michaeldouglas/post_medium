mod logger;

use actix_web::{get, post, web, App, HttpResponse, HttpServer, Responder};
use tracing::{info, debug};
use utoipa::OpenApi;
use utoipa_swagger_ui::SwaggerUi;

#[utoipa::path(
    get,
    path = "/",
    responses(
        (status = 200, description = "Retorna hello world")
    )
)]
#[get("/")]
async fn hello() -> impl Responder {
    info!("Rota / foi chamada");
    HttpResponse::Ok().body("Hello, world!")
}

#[utoipa::path(
    post,
    path = "/echo",
    request_body = String,
    responses(
        (status = 200, description = "Retorna o mesmo body enviado")
    )
)]
#[post("/echo")]
async fn echo(req_body: String) -> impl Responder {
    debug!(body = %req_body, "Recebi um POST em /echo");
    HttpResponse::Ok().body(req_body)
}

#[utoipa::path(
    get,
    path = "/greet/{name}",
    params(
        ("name" = String, Path, description = "Nome para cumprimentar")
    ),
    responses(
        (status = 200, description = "Cumprimenta o usuário")
    )
)]
async fn greet(name: web::Path<String>) -> impl Responder {
    let greeting = format!("Hello, {}!", name);
    info!(%name, "Rota greet chamada");
    HttpResponse::Ok().body(greeting)
}

#[derive(OpenApi)]
#[openapi(
    paths(
        hello,
        echo,
        greet
    )
)]
struct ApiDoc;

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    logger::init_logger();

    info!("Servidor iniciando...");

    HttpServer::new(|| {
        App::new()
            .service(hello)
            .service(echo)
            .route("/greet/{name}", web::get().to(greet))
            .service(
                SwaggerUi::new("/swagger-ui/{_:.*}")
                    .url("/api-doc/openapi.json", ApiDoc::openapi()),
            )
    })
    .bind("127.0.0.1:8080")?
    .run()
    .await
}
