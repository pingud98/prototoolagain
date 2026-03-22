#!/usr/bin/env python3
import os
import subprocess
import sqlite3
import sys
from pathlib import Path


def install_deps():
    subprocess.run(
        [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True
    )


def generate_cert():
    cert_dir = Path("certs")
    cert_dir.mkdir(exist_ok=True)
    subprocess.run(
        [
            "openssl",
            "req",
            "-newkey",
            "rsa:2048",
            "-nodes",
            "-keyout",
            "certs/key.pem",
            "-x509",
            "-days",
            "365",
            "-out",
            "certs/cert.pem",
        ],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def create_db():
    db_path = "instance/inspection.db"
    os.makedirs("instance", exist_ok=True)
    conn = sqlite3.connect(db_path)
    # TODO: Initialize schema (users, inspections, etc.)
    conn.close()


def create_admin_user():
    # TODO: Prompt for credentials and insert into users table
    pass


def main():
    install_deps()
    generate_cert()
    create_db()
    create_admin_user()
    print("Setup complete. Access the app at https://localhost:5000")


if __name__ == "__main__":
    main()
