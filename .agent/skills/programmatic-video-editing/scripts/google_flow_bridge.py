#!/usr/bin/env python3
"""
==============================================================================
ANANKE OS — GOOGLE FLOW BRIDGE (Veo & Imagen Automation Engine)
Automação do estúdio criativo flow.google.com utilizando sessão persistente
da conta Google Pro do operador.

Funcionalidades:
- --login: Abre navegador interativo para autenticação inicial de sessão única.
- --status: Verifica se a sessão global em ~/.ananke/google_flow_profile está ativa.
- --prompt: Envia instrução de cena e faz download determinístico do clipe gerado.
- Portátil: Aceita caminhos relativos ao diretório atual de qualquer projeto.
==============================================================================
"""

import sys
import os
import argparse
import time
from pathlib import Path

# Fix Windows console UTF-8 encoding
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# ANSI colors
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_step(msg: str):
    print(f"{Colors.BLUE}🔄 {msg}{Colors.ENDC}")

def print_success(msg: str):
    print(f"{Colors.GREEN}✅ {msg}{Colors.ENDC}")

def print_warning(msg: str):
    print(f"{Colors.YELLOW}⚠️  {msg}{Colors.ENDC}")

def print_error(msg: str):
    print(f"{Colors.RED}❌ {msg}{Colors.ENDC}")

def get_profile_dir() -> Path:
    """Retorna o diretório global compartilhado de sessão da conta Google."""
    profile_dir = Path.home() / ".ananke" / "google_flow_profile"
    profile_dir.mkdir(parents=True, exist_ok=True)
    return profile_dir

def interactive_login(flow_url: str = "https://flow.google.com/"):
    """Abre uma janela visível do navegador para o usuário fazer login na sua conta Google Pro."""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print_error("Playwright não encontrado. Instale com: pip install playwright && playwright install chromium")
        sys.exit(1)

    profile_dir = get_profile_dir()
    print_step(f"Iniciando navegador com perfil persistente em: {profile_dir}")
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.YELLOW}🔐 AUTENTICAÇÃO GOOGLE FLOW (Sessão Global Ananke OS){Colors.ENDC}")
    print(f"1. Uma janela do Google Chrome/Chromium será aberta.")
    print(f"2. Faça login na sua conta Google (Google AI Pro/Ultra).")
    print(f"3. Após estar logado no painel do flow.google.com, volte aqui e pressione ENTER.")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.ENDC}\n")

    with sync_playwright() as p:
        browser_context = p.chromium.launch_persistent_context(
            user_data_dir=str(profile_dir),
            headless=False,
            channel="chrome" if os.path.exists("C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe") else None,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--start-maximized"
            ],
            viewport=None
        )

        page = browser_context.pages[0] if browser_context.pages else browser_context.new_page()
        page.goto(flow_url, wait_until="networkidle")

        try:
            input(f"{Colors.BOLD}{Colors.GREEN}Pressione [ENTER] neste terminal após concluir o login no navegador...{Colors.ENDC}")
        except (KeyboardInterrupt, EOFError):
            pass

        print_step("Salvando sessão e encerrando navegador...")
        browser_context.close()
        print_success("Sessão salva com sucesso em ~/.ananke/google_flow_profile!")
        print_success("Agora você pode gerar vídeos a partir de qualquer projeto sem precisar logar de novo.")

def check_status(flow_url: str = "https://flow.google.com/"):
    """Verifica se existe sessão persistente ativa."""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print_error("Playwright não instalado.")
        sys.exit(1)

    profile_dir = get_profile_dir()
    if not any(profile_dir.iterdir()):
        print_warning("Nenhuma sessão encontrada. Execute com --login para autenticar.")
        return False

    print_step("Verificando validade da sessão salva...")
    with sync_playwright() as p:
        browser_context = p.chromium.launch_persistent_context(
            user_data_dir=str(profile_dir),
            headless=True,
            args=["--disable-blink-features=AutomationControlled"]
        )
        page = browser_context.pages[0] if browser_context.pages else browser_context.new_page()
        page.goto(flow_url, wait_until="networkidle", timeout=30000)
        
        current_url = page.url
        browser_context.close()

        if "accounts.google.com" in current_url:
            print_error("A sessão expirou ou não está autenticada. Execute --login novamente.")
            return False
        else:
            print_success(f"Sessão ativa e autenticada no Google Flow! (URL: {current_url})")
            return True

def list_projects(flow_url: str = "https://flow.google.com/", headless: bool = True):
    """Lista todos os projetos e coleções criados pelo usuário no Google Flow."""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print_error("Playwright não instalado.")
        sys.exit(1)

    profile_dir = get_profile_dir()
    print_step("Acessando biblioteca de projetos no Google Flow...")

    with sync_playwright() as p:
        browser_context = p.chromium.launch_persistent_context(
            user_data_dir=str(profile_dir),
            headless=headless,
            args=["--disable-blink-features=AutomationControlled"]
        )
        page = browser_context.pages[0] if browser_context.pages else browser_context.new_page()
        page.goto(flow_url, wait_until="domcontentloaded", timeout=45000)
        time.sleep(4)

        if "accounts.google.com" in page.url:
            print_error("Sessão não autenticada. Execute: python google_flow_bridge.py --login")
            browser_context.close()
            return []

        print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.ENDC}")
        print(f"{Colors.BOLD}📁 BIBLIOTECA DE PROJETOS // GOOGLE FLOW{Colors.ENDC}")
        print(f"{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.ENDC}\n")

        # Busca por cartões de projetos/coleções ou elementos clicáveis de lista
        project_cards = page.query_selector_all(
            "[role='article'], [role='listitem'], .project-card, .collection-card, a[href*='/project'], a[href*='/flow/']"
        )

        projects_found = []
        if project_cards:
            for idx, card in enumerate(project_cards, 1):
                text_content = card.inner_text().strip().replace("\n", " | ")
                href = card.get_attribute("href") or ""
                if text_content:
                    projects_found.append({"index": idx, "title": text_content, "url": href})
                    print(f"[{idx}] {Colors.BOLD}{text_content}{Colors.ENDC}")
                    if href:
                        print(f"    🔗 Link: https://flow.google.com{href}")
        else:
            # Fallback buscando títulos H2, H3 ou spans de lista no painel
            items = page.query_selector_all("h3, h4, [data-project-name]")
            for idx, it in enumerate(items, 1):
                txt = it.inner_text().strip()
                if txt and len(txt) > 2:
                    projects_found.append({"index": idx, "title": txt, "url": ""})
                    print(f"[{idx}] {Colors.BOLD}{txt}{Colors.ENDC}")

        if not projects_found:
            print_warning("Nenhum projeto explícito listado no momento ou o painel inicial está em branco.")
            print("Dica: você pode criar novos projetos ou abrir com --no-headless para inspecionar.")
        else:
            print_success(f"\nTotal de projetos/itens identificados: {len(projects_found)}")

        browser_context.close()
        return projects_found

def download_project_assets(project_name: str, output_dir: str = "./assets/reels/b-rolls", headless: bool = True):
    """Acessa um projeto específico no Flow e faz download de todos os clipes de vídeo existentes."""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print_error("Playwright não instalado.")
        sys.exit(1)

    profile_dir = get_profile_dir()
    target_dir = Path(output_dir).resolve()
    target_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.ENDC}")
    print(f"{Colors.BOLD}📥 SINCRONIZAÇÃO DE CLIPES DO PROJETO // GOOGLE FLOW{Colors.ENDC}")
    print(f"Projeto Alvo: {project_name}")
    print(f"Pasta de Destino: {target_dir}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.ENDC}\n")

    with sync_playwright() as p:
        browser_context = p.chromium.launch_persistent_context(
            user_data_dir=str(profile_dir),
            headless=headless,
            args=["--disable-blink-features=AutomationControlled"]
        )
        page = browser_context.pages[0] if browser_context.pages else browser_context.new_page()
        page.goto("https://flow.google.com/", wait_until="domcontentloaded", timeout=45000)
        time.sleep(3)

        print_step(f"Localizando projeto '{project_name}'...")
        # Clica no projeto pelo nome
        project_link = page.query_selector(f"text='{project_name}', [aria-label*='{project_name}' i]")
        if project_link:
            project_link.click()
            page.wait_for_load_state("domcontentloaded")
            time.sleep(4)
            print_success(f"Projeto '{project_name}' aberto com sucesso!")
        else:
            print_warning(f"Projeto com nome exato '{project_name}' não localizado diretamente na lista inicial.")
            print_step("Tentando busca de vídeos na página atual...")

        # Captura todos os elementos de vídeo e links de download
        video_elements = page.query_selector_all("video[src], video source[src]")
        download_buttons = page.query_selector_all("button[aria-label*='Download' i], a[download]")

        downloaded_count = 0
        # Baixa via botões de download identificados
        for idx, btn in enumerate(download_buttons, 1):
            try:
                dest_file = target_dir / f"flow_{project_name.lower().replace(' ', '_')}_{idx:02d}.mp4"
                print_step(f"Baixando take {idx} para {dest_file.name}...")
                with page.expect_download(timeout=12000) as download_info:
                    btn.click()
                download = download_info.value
                download.save_as(str(dest_file))
                print_success(f"Take {idx} salvo ({dest_file.stat().st_size / (1024*1024):.2f} MB)")
                downloaded_count += 1
            except Exception as e:
                print_warning(f"Não foi possível baixar via botão {idx}: {e}")

        # Fallback baixando via URLs de vídeo encontradas no DOM
        if downloaded_count == 0 and video_elements:
            import urllib.request
            for idx, vel in enumerate(video_elements, 1):
                src = vel.get_attribute("src")
                if src and src.startswith("http"):
                    dest_file = target_dir / f"flow_{project_name.lower().replace(' ', '_')}_{idx:02d}.mp4"
                    print_step(f"Baixando stream {idx} diretamente...")
                    try:
                        urllib.request.urlretrieve(src, str(dest_file))
                        print_success(f"Vídeo {idx} baixado ({dest_file.stat().st_size / (1024*1024):.2f} MB)")
                        downloaded_count += 1
                    except Exception as e:
                        print_warning(f"Erro no download direto {idx}: {e}")

        browser_context.close()
        if downloaded_count > 0:
            print_success(f"\nSincronização concluída! {downloaded_count} takes baixados em:\n{target_dir}")
        else:
            print_warning(f"\nNenhum clipe de vídeo finalizado foi encontrado no projeto '{project_name}'.")

def generate_video(prompt: str, output_path: str, aspect_ratio: str = "9:16", project_name: str = None, headless: bool = True):
    """Executa a automação de envio de prompt e download do vídeo, opcionalmente dentro de um projeto."""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print_error("Playwright não instalado.")
        sys.exit(1)

    profile_dir = get_profile_dir()
    output_file = Path(output_path).resolve()
    output_file.parent.mkdir(parents=True, exist_ok=True)

    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.ENDC}")
    print(f"{Colors.BOLD}🎬 GOOGLE FLOW GENERATOR // ANANKE OS{Colors.ENDC}")
    print(f"Prompt: {prompt}")
    print(f"Aspect Ratio: {aspect_ratio}")
    print(f"Destino: {output_file}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.ENDC}\n")

    print_step("Iniciando navegador com sessão persistente...")

    with sync_playwright() as p:
        browser_context = p.chromium.launch_persistent_context(
            user_data_dir=str(profile_dir),
            headless=headless,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--start-maximized"
            ],
            viewport={"width": 1920, "height": 1080}
        )

        page = browser_context.pages[0] if browser_context.pages else browser_context.new_page()
        print_step("Acessando flow.google.com...")
        page.goto("https://flow.google.com/", wait_until="domcontentloaded", timeout=45000)

        # Checagem de redirecionamento para login
        if "accounts.google.com" in page.url:
            print_error("Login expirado! Execute: python google_flow_bridge.py --login")
            browser_context.close()
            sys.exit(1)

        print_step("Localizando caixa de prompt...")
        # Espera por campo de prompt do estúdio (textarea, contenteditable ou input)
        prompt_selectors = [
            "textarea",
            "div[contenteditable='true']",
            "input[type='text']",
            "[aria-label*='prompt' i]",
            "[placeholder*='prompt' i]",
            "[placeholder*='describe' i]"
        ]

        prompt_element = None
        for sel in prompt_selectors:
            try:
                el = page.wait_for_selector(sel, timeout=4000)
                if el and el.is_visible():
                    prompt_element = el
                    break
            except Exception:
                continue

        if not prompt_element:
            print_warning("Campo de prompt padrão não encontrado de imediato. Aguardando carregamento dos componentes...")
            time.sleep(3)
            # Segunda tentativa com seletor genérico
            prompt_element = page.query_selector("textarea, [contenteditable='true']")

        if not prompt_element:
            print_error("Não foi possível identificar a interface de entrada de prompt do Flow.")
            print_warning("Dica: execute com --no-headless para inspecionar a interface visualmente.")
            browser_context.close()
            sys.exit(1)

        print_step("Inserindo instrução de cena no Flow...")
        prompt_element.click()
        # Formata o prompt adicionando instrução explícita de enquadramento se for vertical
        full_prompt = prompt
        if aspect_ratio == "9:16" and "vertical" not in prompt.lower() and "9:16" not in prompt:
            full_prompt = f"{prompt}, vertical video format, 9:16, high production value, cinematic 4k"

        prompt_element.fill(full_prompt)
        time.sleep(1)

        # Dispara geração
        print_step("Disparando comando de geração (Enter / Create)...")
        prompt_element.press("Enter")

        # Procura por botão de submit/generate alternativo
        submit_btn = page.query_selector("button:has-text('Generate'), button:has-text('Create'), button[aria-label*='Send' i]")
        if submit_btn and submit_btn.is_enabled():
            submit_btn.click()

        print_step("Geração iniciada! Monitorando renderização no Google Flow...")
        print_step("Aguardando buffer de vídeo (estimativa: 30 a 90 segundos)...")

        # Monitoramento de renderização e download
        video_downloaded = False
        start_time = time.time()
        timeout_seconds = 180

        # Listener para capturar requisições de download ou URLs de vídeo geradas
        video_urls = []
        def handle_response(response):
            if "video" in response.headers.get("content-type", "") or ".mp4" in response.url:
                if response.status == 200:
                    video_urls.append(response.url)

        page.on("response", handle_response)

        while time.time() - start_time < timeout_seconds:
            # Verifica se algum elemento de vídeo apareceu na tela
            video_el = page.query_selector("video[src], video source[src]")
            if video_el:
                src = video_el.get_attribute("src")
                if src and src.startswith("http"):
                    video_urls.append(src)

            # Verifica botão de download
            download_btn = page.query_selector("button[aria-label*='Download' i], a[download], [data-tooltip*='Download' i]")
            if download_btn and download_btn.is_visible():
                try:
                    with page.expect_download(timeout=10000) as download_info:
                        download_btn.click()
                    download = download_info.value
                    download.save_as(str(output_file))
                    video_downloaded = True
                    break
                except Exception:
                    pass

            if video_urls:
                # Faz download direto do stream capturado
                print_step("Stream de vídeo gerado detectado! Baixando arquivo...")
                try:
                    import urllib.request
                    urllib.request.urlretrieve(video_urls[-1], str(output_file))
                    video_downloaded = True
                    break
                except Exception as e:
                    print_warning(f"Tentativa de download direto: {e}")

            time.sleep(3)
            elapsed = int(time.time() - start_time)
            print(f"⏳ Processando... ({elapsed}s decorridos)", end="\r")

        browser_context.close()

        if video_downloaded and output_file.exists() and output_file.stat().st_size > 1000:
            print_success(f"\nVídeo gerado e salvo com sucesso em:\n{output_file}")
            print_success(f"Tamanho: {output_file.stat().st_size / (1024*1024):.2f} MB")
            return str(output_file)
        else:
            print_error(f"\nTempo limite excedido ou download incompleto. Verifique o status no painel do flow.google.com.")
            sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description="Ananke OS — Google Flow Bridge (Automação de Vídeos Veo & Imagen)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de Uso:
  1. Autenticação inicial (Executado uma única vez):
     python google_flow_bridge.py --login

  2. Listar projetos existentes na sua conta:
     python google_flow_bridge.py --list-projects

  3. Baixar todos os vídeos de um projeto específico:
     python google_flow_bridge.py --download-project "Nome do Projeto" --output ./assets/reels/b-rolls/

  4. Gerar vídeo dentro de um projeto existente (para consistência):
     python google_flow_bridge.py --project "Cenas Lúdicas" --prompt "Criança sorrindo com blocos" --output ./assets/reels/b-rolls/take1.mp4

  5. Checagem de status de sessão:
     python google_flow_bridge.py --status
        """
    )
    parser.add_argument("--login", action="store_true", help="Abre navegador interativo para autenticação de sessão única")
    parser.add_argument("--status", action="store_true", help="Verifica se a sessão global está ativa")
    parser.add_argument("--list-projects", action="store_true", help="Lista todos os projetos e coleções na sua conta Google Flow")
    parser.add_argument("--project", type=str, help="Nome do projeto existente no Flow para contextualizar a geração ou download")
    parser.add_argument("--download-project", type=str, help="Nome do projeto do qual deseja baixar todos os vídeos gerados")
    parser.add_argument("--prompt", type=str, help="Texto descritivo da cena para o modelo Veo")
    parser.add_argument("--output", type=str, default="./assets/reels/b-rolls/flow_take.mp4", help="Caminho de destino do arquivo MP4 ou pasta de download")
    parser.add_argument("--aspect-ratio", type=str, default="9:16", choices=["9:16", "16:9", "1:1"], help="Proporção do vídeo (Padrão: 9:16 vertical)")
    parser.add_argument("--no-headless", action="store_true", help="Executa o navegador de forma visível")

    args = parser.parse_args()

    if args.login:
        interactive_login()
    elif args.status:
        check_status()
    elif args.list_projects:
        list_projects(headless=not args.no_headless)
    elif args.download_project:
        download_project_assets(
            project_name=args.download_project,
            output_dir=args.output,
            headless=not args.no_headless
        )
    elif args.prompt:
        generate_video(
            prompt=args.prompt,
            output_path=args.output,
            aspect_ratio=args.aspect_ratio,
            project_name=args.project,
            headless=not args.no_headless
        )
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
