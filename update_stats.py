# -*- coding: utf-8 -*-
"""
update_stats.py
Calcula estadísticas reales de GitHub para @BlueberryMauro
e inyecta los valores actualizados en dark_mode.svg y light_mode.svg.
"""

import os
import sys
import re
import json
import urllib.request
import urllib.error
from datetime import datetime

GITHUB_USERNAME = os.environ.get("GITHUB_USERNAME", "BlueberryMauro")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")

def fetch_rest(endpoint):
    url = f"https://api.github.com/{endpoint.lstrip('/')}"
    headers = {
        "User-Agent": "GitHub-Stats-WindowsTerminal",
        "Accept": "application/vnd.github.v3+json"
    }
    if GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        print(f"Error REST API ({url}): {e}", file=sys.stderr)
        return None

def get_stats(username):
    stats = {
        "username": username,
        "repos": 5,
        "commits": 159,
        "stars": 6,
        "loc": 1457475
    }

    # Datos básicos de usuario
    user_info = fetch_rest(f"users/{username}")
    if user_info:
        stats["repos"] = user_info.get("public_repos", stats["repos"])

    # Repositorios públicos para contar estrellas y commits
    repos = fetch_rest(f"users/{username}/repos?per_page=100")
    if repos and isinstance(repos, list):
        total_stars = 0
        total_commits = 0
        approx_loc = 0
        
        for r in repos:
            total_stars += r.get("stargazers_count", 0)
            repo_name = r.get("name")
            size_kb = r.get("size", 0)
            approx_loc += int(size_kb * 25) # Estimación de líneas por tamaño de código
            
            # Contar commits por repo
            commits_data = fetch_rest(f"repos/{username}/{repo_name}/commits?per_page=100")
            if commits_data and isinstance(commits_data, list):
                total_commits += len(commits_data)
                
        if total_stars > 0:
            stats["stars"] = total_stars
        if total_commits > 0:
            stats["commits"] = total_commits
        if approx_loc > 0:
            stats["loc"] = approx_loc

    return stats

def update_svg_file(file_path, stats):
    if not os.path.exists(file_path):
        print(f"Archivo no encontrado: {file_path}")
        return

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Inyección de estadísticas reales
    content = re.sub(r'(id="repos_val">)[^<]+(<)', rf'\g<1>{stats["repos"]}\g<2>', content)
    content = re.sub(r'(id="commits_val">)[^<]+(<)', rf'\g<1>{stats["commits"]:,}\g<2>', content)
    content = re.sub(r'(id="stars_val">)[^<]+(<)', rf'\g<1>{stats["stars"]:,}\g<2>', content)
    content = re.sub(r'(id="loc_val">)[^<]+(<)', rf'\g<1>{stats["loc"]:,}\g<2>', content)


    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Actualizado: {file_path}")

def update_gif_file(file_path, stats):
    if not os.path.exists(file_path):
        return
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    content = re.sub(r'("prop",\s*"Repos",\s*")[^"]+(")', rf'\g<1>      : {stats["repos"]}\g<2>', content)
    content = re.sub(r'("prop",\s*"Commits",\s*")[^"]+(")', rf'\g<1>    : {stats["commits"]:,}\g<2>', content)
    content = re.sub(r'("prop",\s*"Stars",\s*")[^"]+(")', rf'\g<1>      : {stats["stars"]:,}\g<2>', content)
    content = re.sub(r'("prop",\s*"TotalLOC",\s*")[^"]+(")', rf'\g<1>   : {stats["loc"]:,}\g<2>', content)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Actualizado: {file_path}")

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    username = sys.argv[1] if len(sys.argv) > 1 else GITHUB_USERNAME

    print(f"Obteniendo métricas reales para @{username}...")
    stats = get_stats(username)
    print("Métricas obtenidas:")
    for k, v in stats.items():
        print(f"  {k}: {v}")

    dark_svg = os.path.join(script_dir, "dark_mode.svg")
    light_svg = os.path.join(script_dir, "light_mode.svg")
    gif_file = os.path.join(script_dir, "generate_gif.py")

    update_svg_file(dark_svg, stats)
    update_svg_file(light_svg, stats)
    update_gif_file(gif_file, stats)
    print("¡Archivos actualizados con éxito!")

if __name__ == "__main__":
    main()
