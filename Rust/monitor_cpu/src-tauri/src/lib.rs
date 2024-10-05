use sysinfo::{CpuRefreshKind, RefreshKind, System};
use std::{fs::OpenOptions, io::Write, thread, time, env, sync::{Arc, Mutex}};
use chrono::Local;
use tauri::State;

struct MonitorState {
    running: Arc<Mutex<bool>>,
}

#[tauri::command]
fn monitor_cpu(name: &str, state: State<MonitorState>) -> String {
    let file_path = format!("{}.csv", name);
    let running = Arc::clone(&state.running);

    let file_path_clone = file_path.clone();

    std::thread::spawn(move || {
        let mut sys = System::new_with_specifics(RefreshKind::new().with_cpu(CpuRefreshKind::everything()));
        let mut file = match OpenOptions::new()
            .append(true)
            .create(true)
            .open(&file_path_clone)
        {
            Ok(file) => file,
            Err(e) => {
                eprintln!("Erro ao abrir o arquivo: {}", e);
                return;
            }
        };

        if file.metadata().unwrap().len() == 0 {
            writeln!(file, "Uso da CPU (%),Data e Hora,Nome do Programa").expect("Erro ao escrever no arquivo");
        }

        while *running.lock().unwrap() {
            sys.refresh_all();
            let cpu_usage = sys.global_cpu_usage();
            let timestamp = Local::now().to_string();

            let current_process = sys.processes()
                .iter()
                .max_by_key(|(_, p)| p.cpu_usage() as u32)
                .map(|(_, p)| p.name().to_string_lossy().to_string())
                .unwrap_or_else(|| "Desconhecido".to_string());

            writeln!(file, "{:.2},{:?},{}", cpu_usage, timestamp, current_process).expect("Erro ao escrever no arquivo");
            println!("Uso da CPU: {:.2}%, Programa: {}", cpu_usage, current_process);

            let one_second = time::Duration::from_secs(1);
            thread::sleep(one_second);
        }
    });

    format!("Monitoramento da CPU iniciado para o arquivo: {}", file_path)
}

#[tauri::command]
fn stop_monitoring(state: State<MonitorState>) -> String {
    let mut running = state.running.lock().unwrap();
    *running = false;
    
    std::process::exit(0);
}

#[tauri::command]
fn get_file_path(name: &str) -> String {
    let file_path = format!("{}.csv", name);
    let absolute_path = env::current_dir().unwrap().join(file_path);
    format!("O arquivo foi salvo em: {:?}", absolute_path)
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    let monitor_state = MonitorState {
        running: Arc::new(Mutex::new(true)),
    };

    tauri::Builder::default()
        .plugin(tauri_plugin_shell::init())
        .manage(monitor_state)
        .invoke_handler(tauri::generate_handler![monitor_cpu, stop_monitoring, get_file_path])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
