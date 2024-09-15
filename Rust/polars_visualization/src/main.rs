use polars::prelude::*;
use std::fs::File;
use std::time::Instant;

fn main() -> Result<(), polars::error::PolarsError> {
    // Registra o tempo de início da execução
    let start = Instant::now();

    // Abre o arquivo CSV
    let file =
        File::open("../DataFrame/tipo_sanguineo.csv").expect("Não foi possível abrir o arquivo");

    // Cria um novo leitor de CSV e carrega o DataFrame
    let mut df = CsvReader::new(file)
        .infer_schema(None)
        .has_header(true)
        .finish()?;

    // Renomear a coluna "Tipo Sanguíneo" para "tipo_sanguineo"
    let df = df.rename("Tipo Sanguíneo", "tipo_sanguineo")?;

    // Exibe as primeiras 10 linhas do DataFrame para visualização
    println!("{:?}", df.head(Some(10)));

    // Retorna o nome da coluna e o tipo
    for col in df.get_columns() {
        let name = col.name();
        let dtype = col.dtype();
        println!("Coluna: {}, Tipo de dado: {:?}", name, dtype);
    }

    // Verifica o tipo da coluna de agrupamento
    let tipo_col = df.column("tipo_sanguineo")?;
    println!("Tipo da coluna 'tipo_sanguineo': {:?}", tipo_col.dtype());

    // Agrupar pelo tipo sanguíneo e contar as ocorrências
    let lazy_df = df.clone().lazy();
    let grouped_df = lazy_df
        .groupby([col("tipo_sanguineo")])
        .agg([col("Nome").count().alias("count")])
        .collect()?;

    // Mostrar o resultado
    println!("{}", grouped_df);

    // Filtra os dados com base na coluna "tipo_sanguineo" igual a "A+" e na coluna "d" que não deve ser nula
    let lazy_filter_df = df.clone().lazy();
    let filtered_df = lazy_filter_df
        .filter(
            col("tipo_sanguineo")
                .eq(lit("A+"))
                .and(col("tipo_sanguineo").is_not_null()),
        )
        .collect()?;

    // Mostrar o resultado do DataFrame filtrado
    println!("{}", filtered_df);

    // Calcula e exibe o tempo total de execução
    let duration = start.elapsed();
    println!("Tempo total de execução: {:?}", duration);

    // Retorna Ok para indicar que a execução foi bem-sucedida
    Ok(())
}
