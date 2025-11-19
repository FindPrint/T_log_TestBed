#!/usr/bin/env python3
"""
convert_ipynb_to_pdf.py

Usage:
  python convert_ipynb_to_pdf.py /chemin/vers/mon_notebook.ipynb

Fonctions principales :
- crée un kernel Jupyter temporaire lié à l'interpréteur Python courant
- exécute le notebook avec nbconvert.preprocessors.ExecutePreprocessor en utilisant ce kernel
- tente la conversion PDF via nbconvert (LaTeX), sinon fallback HTML -> Chrome headless
- nettoie le kernel temporaire à la fin
"""

import sys
import subprocess
import shutil
import uuid
from pathlib import Path
import locale

def run_command(cmd, check=False):
    try:
        proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8', errors='replace')
        if check and proc.returncode != 0:
            raise subprocess.CalledProcessError(proc.returncode, cmd, output=proc.stdout, stderr=proc.stderr)
        return proc.returncode, proc.stdout, proc.stderr
    except FileNotFoundError:
        return 127, "", f"Commande introuvable: {cmd[0]}"

def ensure_python_pkg(pkg):
    """Installe un paquet Python via pip si absent."""
    try:
        __import__(pkg)
        return True
    except ImportError:
        py = sys.executable
        cmd = [py, "-m", "pip", "install", pkg]
        code, out, err = run_command(cmd)
        if code == 0:
            try:
                __import__(pkg)
                return True
            except ImportError:
                return False
        return False

def install_ipykernel_and_create_kernel(kernel_name):
    """Installe ipykernel si besoin puis crée un kernel jupyter temporaire."""
    if not ensure_python_pkg("ipykernel"):
        return False
    py = sys.executable
    cmd = [py, "-m", "ipykernel", "install", "--user", "--name", kernel_name, "--display-name", f"tmp-{kernel_name}"]
    code, out, err = run_command(cmd)
    if code == 0:
        # Vérifier que le kernel a été créé
        import json
        import os
        kernel_dir = Path.home() / ".local" / "share" / "jupyter" / "kernels" / kernel_name
        if kernel_dir.exists() and (kernel_dir / "kernel.json").exists():
            return True
    return False

def remove_kernel(kernel_name):
    # Vérifier si le kernel existe avant de tenter de le supprimer
    import os
    from pathlib import Path
    kernel_dir = Path.home() / ".local" / "share" / "jupyter" / "kernels" / kernel_name
    if not kernel_dir.exists():
        return True  # Considérer comme supprimé si inexistant
    ks = shutil.which("jupyter-kernelspec") or shutil.which("jupyter")
    # Prefer jupyter kernelspec remove -f <name>
    cmd = ["jupyter", "kernelspec", "remove", "-f", kernel_name]
    code, out, err = run_command(cmd)
    return code == 0

def execute_notebook_with_temp_kernel(src_path: Path, executed_path: Path, kernel_name: str, timeout=1200):
    if not ensure_python_pkg("nbformat"):
        raise ImportError("nbformat non disponible")
    if not ensure_python_pkg("nbconvert"):
        raise ImportError("nbconvert non disponible")
    import nbformat
    from nbconvert.preprocessors import ExecutePreprocessor
    nb = nbformat.read(str(src_path), as_version=nbformat.NO_CONVERT)
    ep = ExecutePreprocessor(timeout=timeout, kernel_name=kernel_name)
    print(f"Exécution du notebook : {src_path} avec kernel '{kernel_name}'")
    # Essayer d'exécuter sans les cellules problématiques (cellules avec erreurs Unicode)
    try:
        ep.preprocess(nb, {'metadata': {'path': str(src_path.parent)}})
    except Exception as e:
        print(f"Avertissement : Erreur lors de l'exécution du notebook : {e}")
        print("Tentative de conversion sans exécution des cellules...")
        # Si échec, on continue avec le notebook non exécuté
        nbformat.write(nb, str(executed_path))
        print(f"Notebook non exécuté sauvegardé sous : {executed_path}")
        return
    nbformat.write(nb, str(executed_path))
    print(f"Notebook exécuté sauvegardé sous : {executed_path}")

def convert_with_nbconvert(executed_path: Path, to_format: str = "pdf"):
    # Essayer plusieurs chemins possibles pour jupyter
    jupyter_cmd = shutil.which("jupyter")
    if not jupyter_cmd:
        # Essayer avec python -m jupyter
        jupyter_cmd = sys.executable
        cmd = [jupyter_cmd, "-m", "jupyter", "nbconvert", "--to", to_format, str(executed_path)]
    else:
        cmd = [jupyter_cmd, "nbconvert", "--to", to_format, str(executed_path)]
    print(f"Lancement de nbconvert : {' '.join(cmd)}")
    code, out, err = run_command(cmd)
    if code != 0:
        print(f"Erreur nbconvert (format={to_format}) :\n{err}")
    else:
        print(f"Conversion réussie (format={to_format}).")
    return code == 0

def html_to_pdf_with_chrome(html_path: Path, pdf_out: Path):
    # Essayer d'abord Chrome/Chromium
    chrome_path = shutil.which("google-chrome") or shutil.which("chromium") or shutil.which("chrome") or shutil.which("chrome.exe")
    if chrome_path:
        # Assurer que le répertoire de sortie existe
        pdf_out.parent.mkdir(parents=True, exist_ok=True)
        cmd = [chrome_path, "--headless", "--disable-gpu", "--no-sandbox", "--disable-dev-shm-usage", f"--print-to-pdf={str(pdf_out)}", str(html_path)]
        print("Utilisation de Chrome headless pour générer le PDF.")
        code, out, err = run_command(cmd)
        if code == 0 and pdf_out.exists():
            print("PDF généré via Chrome headless :", pdf_out)
            return True
        print("Échec Chrome headless :", err)

    # Fallback vers playwright si pyppeteer échoue
    try:
        from playwright.sync_api import sync_playwright
        print("Utilisation de Playwright pour générer le PDF.")

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True, args=['--no-sandbox', '--disable-dev-shm-usage'])
            page = browser.new_page()
            page.goto(f'file://{html_path.resolve()}')
            page.pdf(path=str(pdf_out), format='A4')
            browser.close()

        if pdf_out.exists():
            print("PDF généré via Playwright :", pdf_out)
            return True
    except Exception as e:
        print("Échec Playwright :", e)

    print("Aucun outil de conversion HTML->PDF disponible.")
    return False

def main():
    if len(sys.argv) < 2:
        print("Usage: python convert_ipynb_to_pdf.py /chemin/vers/mon_notebook.ipynb")
        sys.exit(2)

    src = Path(sys.argv[1]).expanduser().resolve()
    if not src.exists():
        print(f"Fichier introuvable : {src}")
        sys.exit(1)
    if src.suffix.lower() != ".ipynb":
        print("Le fichier fourni n'est pas un .ipynb")
        sys.exit(1)

    executed = src.with_name(src.stem + "_executed.ipynb")
    kernel_name = f"tmp_kernel_{uuid.uuid4().hex[:8]}"

    # 1) Créer kernel temporaire lié à cet interpréteur Python
    print("Création d'un kernel Jupyter temporaire lié à l'interpréteur Python courant...")
    ok_kernel = install_ipykernel_and_create_kernel(kernel_name)
    if not ok_kernel:
        print("Impossible de créer le kernel temporaire. Vérifiez que 'ipykernel' est installable.")
        # On peut encore tenter d'exécuter avec le kernel 'python3' par défaut ; continuer quand même
        kernel_name = "python3"

    try:
        # 2) Exécuter le notebook avec ExecutePreprocessor en utilisant le kernel choisi
        try:
            execute_notebook_with_temp_kernel(src, executed, kernel_name)
        except Exception as e:
            print("Erreur lors de l'exécution du notebook :", e)
            # Si échec avec kernel temporaire, essayer avec python3
            if kernel_name != "python3":
                print("Tentative avec le kernel 'python3' par défaut...")
                try:
                    execute_notebook_with_temp_kernel(src, executed, "python3")
                except Exception as e2:
                    print("Échec également avec 'python3' :", e2)
                    sys.exit(1)
            else:
                sys.exit(1)

        # 3) Conversion PDF via nbconvert (LaTeX)
        print("Tentative de conversion directe en PDF via nbconvert + LaTeX...")
        ok_pdf = convert_with_nbconvert(executed, to_format="pdf")
        if ok_pdf:
            print("PDF généré avec succès via nbconvert + LaTeX.")
            # Nettoyer le fichier exécuté intermédiaire
            if executed.exists():
                executed.unlink()
            sys.exit(0)

        # 4) Fallback HTML
        print("Conversion en PDF via LaTeX a échoué. Essai de conversion en HTML comme contournement.")
        ok_html = convert_with_nbconvert(executed, to_format="html")
        html_file = executed.with_suffix(".html")
        if not ok_html or not html_file.exists():
            print("La conversion en HTML a échoué. Voir les messages ci-dessus.")
            # Essayer de convertir directement en PDF sans exécution si nbconvert est disponible
            print("Tentative de conversion directe du notebook original en PDF...")
            ok_direct_pdf = convert_with_nbconvert(src, to_format="pdf")
            if ok_direct_pdf:
                pdf_direct = src.with_suffix(".pdf")
                print("PDF généré directement depuis le notebook original :", pdf_direct)
                sys.exit(0)
            sys.exit(1)

        # 5) Tenter Chrome headless pour imprimer l'HTML en PDF
        pdf_out = src.with_suffix(".pdf")
        ok_chrome = html_to_pdf_with_chrome(html_file, pdf_out)
        if ok_chrome:
            print("PDF final généré :", pdf_out)
            # Nettoyer les fichiers intermédiaires
            if executed.exists():
                executed.unlink()
            if html_file.exists():
                html_file.unlink()
            sys.exit(0)

        # 6) Dernier message et instructions manuelles
        print("Aucune méthode automatisée n'a réussi à produire le PDF final.")
        print("Fichiers intermédiaires disponibles :", executed, html_file)
        print("Si vous avez pdflatex installé, exécutez manuellement : jupyter nbconvert --to pdf", executed)
        # Nettoyer les fichiers intermédiaires si demandé ou en cas d'échec
        if executed.exists():
            print(f"Suppression du fichier intermédiaire : {executed}")
            executed.unlink()
        if html_file.exists():
            print(f"Suppression du fichier intermédiaire : {html_file}")
            html_file.unlink()
        sys.exit(1)

    finally:
        # Nettoyage : suppression du kernel temporaire si créé
        if kernel_name.startswith("tmp_kernel_"):
            print(f"Suppression du kernel temporaire '{kernel_name}'...")
            removed = remove_kernel(kernel_name)
            if removed:
                print("Kernel temporaire supprimé.")
            else:
                print("Échec suppression kernel temporaire. Vous pouvez le supprimer manuellement : jupyter kernelspec remove -f", kernel_name)

if __name__ == "__main__":
    # Forcer l'encodage UTF-8 pour éviter les problèmes d'encodage sur Windows
    if sys.platform == "win32":
        import os
        os.environ["PYTHONIOENCODING"] = "utf-8"
        # Rediriger stdout et stderr vers UTF-8
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
    main()
