use sha2::{Digest, Sha256};
use std::fs::File;
use std::io::{Read};
use std::path::PathBuf;
use walkdir::WalkDir;

fn sha256_file(p: &PathBuf) -> String {
	let mut file = File::open(p).unwrap();
	let mut hasher = Sha256::new();
	let mut buf = [0u8; 8192];
	loop {
		let n = file.read(&mut buf).unwrap();
		if n == 0 { break; }
		hasher.update(&buf[..n]);
	}
	format!("{:x}", hasher.finalize())
}

fn main() {
	let target = std::env::args().nth(1).expect("path required");
	for entry in WalkDir::new(&target).into_iter().filter_map(|e| e.ok()) {
		if entry.file_type().is_file() {
			let p: PathBuf = entry.path().into();
			let hash = sha256_file(&p);
			println!("{}  {}", hash, p.display());
		}
	}
	println!("Send telemetry to cloud API as needed (omitted in demo)");
}
