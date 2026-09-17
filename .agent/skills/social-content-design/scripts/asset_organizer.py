#!/usr/bin/env python3
"""
Asset Organizer - Social Content Design Skill
=============================================
Manages directories, files, and copy metadata for social media posts and carousels.

Usage:
    python asset_organizer.py create <slug> [--slides N] [--title "Title"]
    python asset_organizer.py status <slug>
"""

import os
import sys
import argparse
from datetime import datetime
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

def get_post_dir(slug: str) -> Path:
    base = Path("assets/posts")
    return base / slug

def create_post(slug: str, slides: int = 1, title: str = ""):
    post_dir = get_post_dir(slug)
    post_dir.mkdir(parents=True, exist_ok=True)
    
    copy_file = post_dir / "copy.md"
    date_str = datetime.now().strftime("%Y-%m-%d")
    post_title = title if title else slug.replace("-", " ").title()
    
    if not copy_file.exists():
        content = f"""# Post: {post_title}

> **Data de Criação:** {date_str}  
> **Status:** Rascunho / Em Produção  
> **Tipo:** {"Carrossel (" + str(slides) + " slides)" if slides > 1 else "Post Estático (Tela Única)"}  
> **Diretório:** `assets/posts/{slug}/`

---

## 📝 Legenda do Post (Caption)

[Escreva aqui a legenda persuasiva do post para o feed do Instagram / LinkedIn]

---

## 🏷️ Hashtags

#AnankeOS #Tech #SoftwareEngineering #AI

---

## 🖼️ Especificações de Slides & Prompts Visuais

"""
        for i in range(1, slides + 1):
            slide_name = f"slide-{i:02d}.png"
            content += f"""### Slide {i:02d} (`{slide_name}`)
* **Objetivo Visual:** {"Gancho de Alta Atenção (Hook)" if i == 1 else ("Chamada para Ação Final (CTA)" if i == slides else f"Desenvolvimento - Ponto {i-1}")}
* **Texto Renderizado na Imagem:** "[Texto curto e legível para a imagem]"
* **Direção de Arte & Elementos:** [Fundo, cores hex, ícones, iluminação]
* **Prompt para Geração:**
```text
[Prompt refinado para o modelo de geração visual com parâmetros e proporção]
```

---

"""
        with open(copy_file, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✅ Post criado com sucesso em: {post_dir}")
        print(f"📄 Arquivo de roteiro gerado: {copy_file}")
    else:
        print(f"ℹ️  Pasta e roteiro já existem em: {copy_file}")

def status_post(slug: str):
    post_dir = get_post_dir(slug)
    if not post_dir.exists():
        print(f"❌ Post '{slug}' não encontrado em assets/posts/")
        return
    
    images = sorted(list(post_dir.glob("*.png")) + list(post_dir.glob("*.jpg")) + list(post_dir.glob("*.webp")))
    copy_file = post_dir / "copy.md"
    
    print(f"\n=== Status do Post: {slug} ===")
    print(f"📁 Diretório: {post_dir}")
    print(f"📄 Roteiro copy.md: {'Encontrado ✅' if copy_file.exists() else 'Ausente ❌'}")
    print(f"🖼️  Imagens encontradas: {len(images)}")
    for img in images:
        size_kb = img.stat().st_size / 1024
        print(f"   - {img.name} ({size_kb:.1f} KB)")
    print("==============================\n")

def main():
    parser = argparse.ArgumentParser(description="Asset Organizer para Posts e Carrosséis")
    subparsers = parser.add_subparsers(dest="command")
    
    create_parser = subparsers.add_parser("create", help="Criar nova pasta de post")
    create_parser.add_argument("slug", help="Slug único do post (ex: 2026-09-sdd-tutorial)")
    create_parser.add_argument("--slides", type=int, default=1, help="Número de slides (padrão: 1)")
    create_parser.add_argument("--title", type=str, default="", help="Título legível do post")
    
    status_parser = subparsers.add_parser("status", help="Verificar arquivos de um post")
    status_parser.add_argument("slug", help="Slug do post")
    
    args = parser.parse_args()
    
    if args.command == "create":
        create_post(args.slug, args.slides, args.title)
    elif args.command == "status":
        status_post(args.slug)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
