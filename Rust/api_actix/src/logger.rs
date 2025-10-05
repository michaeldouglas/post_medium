use tracing_subscriber::fmt::time::UtcTime;
use tracing_subscriber::EnvFilter;

pub fn init_logger() {
    let filter = EnvFilter::try_from_default_env()
        .unwrap_or_else(|_| EnvFilter::new("info"));

    tracing_subscriber::fmt()
        .with_env_filter(filter)
        .json() // logs no formato JSON
        .with_current_span(true)
        .with_span_list(true)
        .with_timer(UtcTime::rfc_3339())
        .with_file(true)
        .with_line_number(true)
        .with_level(true)
        .with_target(true)
        .init();
}
