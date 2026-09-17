#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import os
import re
import sys
from collections import Counter

# Lista padrão de stopwords em Português e Inglês
STOPWORDS_PT = {
    'a', 'o', 'que', 'e', 'do', 'da', 'em', 'um', 'para', 'é', 'com', 'não', 'uma', 'os', 'as', 'no', 'na', 
    'por', 'mais', 'ao', 'aos', 'se', 'umas', 'uns', 'como', 'mas', 'ou', 'foi', 'me', 'para', 'te', 'nos', 
    'esta', 'este', 'isso', 'isto', 'aquilo', 'aquele', 'aquela', 'ele', 'ela', 'eles', 'elas', 'de', 'do', 
    'da', 'dos', 'das', 'com', 'por', 'sobre', 'sob', 'entre', 'atrás', 'depois', 'antes', 'muito', 'pouco',
    'também', 'você', 'vocês', 'eu', 'nós', 'minha', 'meu', 'seus', 'sua', 'seu', 'suas', 'meus', 'minhas',
    'está', 'estão', 'estava', 'estavam', 'ser', 'sendo', 'ter', 'tendo', 'tem', 'têm', 'tinha', 'tinham',
    'são', 'era', 'eram', 'um', 'uma', 'uns', 'umas', 'pelo', 'pela', 'pelos', 'pelas', 'num', 'numa', 'neste',
    'nesta', 'naquele', 'naquela', 'dele', 'dela', 'deles', 'delas', 'só', 'ja', 'já', 'tudo', 'outra', 'outro',
    'outras', 'outros', 'muita', 'muito', 'muitas', 'muitos', 'qual', 'quais', 'quem', 'cujo', 'cuja', 'tambem'
}

STOPWORDS_EN = {
    'the', 'a', 'an', 'and', 'of', 'to', 'in', 'is', 'that', 'it', 'for', 'on', 'with', 'as', 'this', 'at', 
    'by', 'be', 'are', 'was', 'were', 'have', 'has', 'had', 'do', 'does', 'did', 'but', 'not', 'or', 'if', 
    'then', 'else', 'some', 'any', 'no', 'out', 'up', 'down', 'about', 'into', 'over', 'after', 'before', 
    'above', 'below', 'from', 'than', 'too', 'very', 'only', 'own', 'same', 'so', 'can', 'will', 'just',
    'should', 'would', 'could', 'about', 'here', 'there', 'who', 'how', 'why', 'what', 'which'
}

ALL_STOPWORDS = STOPWORDS_PT.union(STOPWORDS_EN)

# Dicionários de sentimento local (Português e Inglês)
LEXICON_POSITIVE = {
    # Português
    'bom', 'boa', 'otimo', 'ótimo', 'otima', 'ótima', 'excelente', 'perfeito', 'perfeita', 'top', 
    'maravilhoso', 'maravilhosa', 'parabens', 'parabéns', 'melhor', 'melhores', 'incrivel', 'incrível', 
    'sensacional', 'legal', 'valeu', 'obrigado', 'obrigada', 'super', 'gostei', 'gosto', 'sucesso', 
    'lindo', 'linda', 'amei', 'adorei', 'recomendo', 'recomendadíssimo', 'recomendo', 'fantastico', 
    'fantástico', 'espetacular', 'genial', 'parabem', 'rapido', 'rápido', 'eficiente', 'facil', 'fácil',
    'util', 'útil', 'prestativo', 'prestativa', 'solucionou', 'resolveu', 'gostando', 'agradavel', 'agradável',
    # Inglês
    'good', 'great', 'awesome', 'excellent', 'perfect', 'amazing', 'love', 'liked', 'thanks', 'thank',
    'best', 'nice', 'cool', 'beautiful', 'wonderful', 'fast', 'easy', 'fantastic', 'superb', 'useful'
}

LEXICON_NEGATIVE = {
    # Português
    'ruim', 'pessimo', 'péssimo', 'pessima', 'péssima', 'horrivel', 'horrível', 'erro', 'bug', 'falha', 
    'odeio', 'chato', 'chata', 'quebrado', 'quebrada', 'lento', 'lenta', 'lixo', 'estragado', 'estragada', 
    'dificil', 'difícil', 'caro', 'cara', 'absurdo', 'absurda', 'decepcao', 'decepção', 'decepcionado', 
    'decepcionada', 'pior', 'piores', 'nao funciona', 'problema', 'problemas', 'demora', 'demorado', 
    'demorada', 'ruins', 'horriveis', 'horríveis', 'complicado', 'complicada', 'dificuldade', 'dificuldades',
    'lamentavel', 'triste', 'decepcionante', 'enganoso', 'fraude', 'pessimamente', 'descaso', 'incompetente',
    'atraso', 'atrasado', 'atrasada', 'perda', 'perdi', 'falhou', 'esquecido', 'esquecida', 'vergonha',
    # Inglês
    'bad', 'worst', 'horrible', 'error', 'bug', 'fail', 'failure', 'hate', 'broken', 'slow', 'garbage', 
    'expensive', 'disappointment', 'disappointed', 'problem', 'problems', 'difficult', 'hard', 'useless',
    'fraud', 'scam', 'terrible', 'annoying'
}

def check_dependencies():
    try:
        import pandas as pd
        import openpyxl
    except ImportError:
        print("Erro: As dependências 'pandas' e/ou 'openpyxl' não estão instaladas.", file=sys.stderr)
        print("Por favor, instale executando: pip install pandas openpyxl", file=sys.stderr)
        sys.exit(1)

def find_columns(df):
    text_col = None
    likes_col = None
    author_col = None
    date_col = None
    
    text_synonyms = {'comentário', 'comentario', 'texto', 'post', 'conteúdo', 'conteudo', 'text', 'comment', 'content', 'body', 'tweet', 'mensagem', 'publication', 'publicação'}
    likes_synonyms = {'curtidas', 'likes', 'reações', 'reacoes', 'reactions', 'claps', 'upvotes', 'curtida', 'like', 'engajamento', 'engagement', 'rt', 'retweets', 'favs'}
    author_synonyms = {'autor', 'usuário', 'usuario', 'username', 'author', 'user', 'profile', 'perfil', 'nome', 'handler'}
    date_synonyms = {'data', 'date', 'timestamp', 'publicado em', 'created at', 'created_at', 'datetime', 'time', 'dia'}
    
    for col in df.columns:
        col_lower = str(col).strip().lower()
        if col_lower in text_synonyms and text_col is None:
            text_col = col
        elif col_lower in likes_synonyms and likes_col is None:
            likes_col = col
        elif col_lower in author_synonyms and author_col is None:
            author_col = col
        elif col_lower in date_synonyms and date_col is None:
            date_col = col
            
    # Fallback inteligente para a coluna de texto
    if text_col is None:
        for col in df.columns:
            non_nulls = df[col].dropna()
            if not non_nulls.empty and non_nulls.apply(lambda x: isinstance(x, str)).mean() > 0.7:
                text_col = col
                break
        if text_col is None:
            text_col = df.columns[0]
            
    return text_col, likes_col, author_col, date_col

def detect_and_parse_vertical(df):
    # Verifica se a coluna 0 tem indicação de publicações empilhadas verticalmente
    first_col = df.iloc[:, 0].dropna()
    is_vertical = False
    
    # Se nas primeiras 50 linhas não nulas encontrarmos strings que comecem com "publicação" ou "publicao"
    sample_size = min(50, len(first_col))
    for val in first_col.head(sample_size):
        val_str = str(val).strip().lower()
        if val_str.startswith('publicação') or val_str.startswith('publicao'):
            is_vertical = True
            break
            
    if not is_vertical:
        return None, None
        
    print("Detecção de Layout: Planilha em formato VERTICAL estruturado identificada.")
    
    publications = []
    comments_list = []
    current_pub = None
    
    for idx, row in df.iterrows():
        val0 = str(row.iloc[0]).strip()
        val1 = str(row.iloc[1]).strip()
        
        val0_lower = val0.lower()
        val1_lower = val1.lower()
        
        # Identifica o início de um bloco de publicação
        if val0_lower.startswith('publicação') or val0_lower.startswith('publicao'):
            current_pub = {
                'id': val0,
                'period': row.iloc[1] if val1 != 'nan' else 'Não especificado',
                'content': '',
                'comments_count': 0
            }
            publications.append(current_pub)
        elif current_pub is not None:
            # Ignora cabeçalhos de seção e vazios
            if val0_lower in {'contexto da publicação', 'contexto da publicao'}:
                continue
            elif val0_lower == 'username' and val1_lower in {'comment', 'comentário', 'comentario', 'texto'}:
                continue
            elif val0_lower == 'nan' and val1_lower == 'nan':
                continue
            # Se for texto de post (coluna 1 é nan)
            elif current_pub['content'] == '' and val1_lower == 'nan':
                current_pub['content'] = row.iloc[0]
            # Se a coluna 1 tiver texto, é um comentário!
            elif val1_lower != 'nan':
                comments_list.append({
                    'Comentário': row.iloc[1],
                    'Autor': row.iloc[0] if val0_lower != 'nan' else 'Anônimo',
                    'Publicação_ID': current_pub['id'],
                    'Publicação_Texto': current_pub['content']
                })
                current_pub['comments_count'] += 1
                
    import pandas as pd
    comments_df = pd.DataFrame(comments_list)
    return comments_df, publications

def analyze_sentiment(text):
    if not isinstance(text, str):
        return 'Neutro', 0.0
    
    text_clean = re.sub(r'[^\w\s]', ' ', text.lower())
    words = text_clean.split()
    
    score = 0.0
    negations = {'não', 'nao', 'nunca', 'jamais', 'nem', 'not', 'no', 'never', 'sem', 'without'}
    
    for i, word in enumerate(words):
        if word in LEXICON_POSITIVE:
            if i > 0 and words[i-1] in negations:
                score -= 1.0
            elif i > 1 and words[i-2] in negations and words[i-1] in {'ser', 'e', 'is', 'a', 'o', 'um', 'uma'}:
                score -= 1.0
            else:
                score += 1.0
        elif word in LEXICON_NEGATIVE:
            if i > 0 and words[i-1] in negations:
                score += 0.5
            elif i > 1 and words[i-2] in negations and words[i-1] in {'ser', 'e', 'is', 'a', 'o', 'um', 'uma'}:
                score += 0.5
            else:
                score -= 1.0
                
    if score > 0:
        return 'Positivo', score
    elif score < 0:
        return 'Negativo', score
    else:
        return 'Neutro', 0.0

def extract_ngrams(texts, weights=None, n=1):
    ngram_counter = Counter()
    for idx, text in enumerate(texts):
        if not isinstance(text, str):
            continue
        
        weight = 1
        if weights is not None:
            import pandas as pd
            w_val = weights[idx]
            if w_val and not pd.isna(w_val):
                try:
                    weight = int(w_val) + 1
                except:
                    weight = 1
        
        words = [w for w in re.sub(r'[^\w\s]', ' ', text.lower()).split() if w not in ALL_STOPWORDS and len(w) > 2]
        
        if n == 1:
            for w in words:
                ngram_counter[w] += weight
        elif n == 2:
            for i in range(len(words) - 1):
                bigram = f"{words[i]} {words[i+1]}"
                ngram_counter[bigram] += weight
                
    return ngram_counter

def main():
    parser = argparse.ArgumentParser(description="Script de análise semântica e social listening (puramente descritivo)")
    parser.add_argument('--xlsx', required=True, help="Caminho do arquivo Excel (.xlsx) contendo as publicações/comentários")
    parser.add_argument('--out', required=True, help="Caminho do arquivo Markdown (.md) a ser gerado")
    
    args = parser.parse_args()
    
    check_dependencies()
    import pandas as pd
    
    if not os.path.exists(args.xlsx):
        print(f"Erro: Arquivo {args.xlsx} não encontrado.", file=sys.stderr)
        sys.exit(1)
        
    try:
        df = pd.read_excel(args.xlsx)
    except Exception as e:
        print(f"Erro ao ler a planilha: {e}", file=sys.stderr)
        sys.exit(1)
        
    if df.empty:
        print("Erro: A planilha está vazia.", file=sys.stderr)
        sys.exit(1)
        
    # Tenta detectar layout vertical
    comments_df, publications = detect_and_parse_vertical(df)
    
    if comments_df is not None:
        # Layout vertical estruturado
        text_col = 'Comentário'
        author_col = 'Autor'
        likes_col = None
        date_col = None
        analysis_df = comments_df
    else:
        # Layout plano convencional
        print("Detecção de Layout: Planilha em formato PLANO convencional identificada.")
        text_col, likes_col, author_col, date_col = find_columns(df)
        analysis_df = df
        
    if analysis_df.empty:
        print("Erro: Nenhum comentário ou texto foi extraído para análise.", file=sys.stderr)
        sys.exit(1)
        
    # Processamento de sentimentos
    sentiments = []
    scores = []
    
    for _, row in analysis_df.iterrows():
        text_val = row[text_col]
        label, score = analyze_sentiment(text_val)
        sentiments.append(label)
        scores.append(score)
        
    analysis_df['sentiment_label'] = sentiments
    analysis_df['sentiment_score'] = scores
    
    total_records = len(analysis_df)
    sentiment_counts = analysis_df['sentiment_label'].value_counts()
    
    pos_count = sentiment_counts.get('Positivo', 0)
    neg_count = sentiment_counts.get('Negativo', 0)
    neu_count = sentiment_counts.get('Neutro', 0)
    
    pos_pct = (pos_count / total_records) * 100
    neg_pct = (neg_count / total_records) * 100
    neu_pct = (neu_count / total_records) * 100
    
    # Calcula engajamento total
    total_likes = 0
    if likes_col and likes_col in analysis_df.columns:
        total_likes = int(analysis_df[likes_col].fillna(0).sum())
        
    # Extrai termos e bigrams mais frequentes
    weights = analysis_df[likes_col].values if likes_col and likes_col in analysis_df.columns else None
    unigrams_freq = extract_ngrams(analysis_df[text_col].values, weights, n=1).most_common(15)
    bigrams_freq = extract_ngrams(analysis_df[text_col].values, weights, n=2).most_common(15)
    
    # Agrupamentos temáticos baseados nos unigramas principais
    top_terms = [item[0] for item in unigrams_freq[:5]]
    topic_groups = {}
    
    for term in top_terms:
        mask = analysis_df[text_col].fillna('').astype(str).str.lower().str.contains(term, regex=False)
        sub_df = analysis_df[mask]
        
        if not sub_df.empty:
            sub_total = len(sub_df)
            sub_sent_counts = sub_df['sentiment_label'].value_counts()
            sub_pos = sub_sent_counts.get('Positivo', 0)
            sub_neg = sub_sent_counts.get('Negativo', 0)
            sub_neu = sub_sent_counts.get('Neutro', 0)
            
            topic_groups[term] = {
                'total': sub_total,
                'pos_pct': (sub_pos / sub_total) * 100,
                'neg_pct': (sub_neg / sub_total) * 100,
                'neu_pct': (sub_neu / sub_total) * 100
            }
            
    # Coleta de amostras representativas
    def get_representative_comments(sentiment, count=3):
        sent_df = analysis_df[analysis_df['sentiment_label'] == sentiment]
        if sent_df.empty:
            return []
        
        if likes_col and likes_col in sent_df.columns:
            sent_df = sent_df.sort_values(by=likes_col, ascending=False)
            
        comments = []
        for _, row in sent_df.head(count).iterrows():
            author_val = row[author_col] if author_col and author_col in sent_df.columns and not pd.isna(row[author_col]) else "Anônimo"
            likes_val = int(row[likes_col]) if likes_col and likes_col in sent_df.columns and not pd.isna(row[likes_col]) else 0
            text_val = str(row[text_col]).strip().replace('\n', ' ')
            # Trunca comentários excessivamente longos para manter legibilidade do relatório
            if len(text_val) > 400:
                text_val = text_val[:400] + "..."
            comments.append({
                'author': author_val,
                'likes': likes_val,
                'text': text_val
            })
        return comments

    pos_samples = get_representative_comments('Positivo', 3)
    neg_samples = get_representative_comments('Negativo', 3)
    neu_samples = get_representative_comments('Neutro', 3)
    
    # Inicia a geração do Relatório Markdown
    markdown_content = f"""# Relatório de Social Listening e Análise Semântica

Este relatório apresenta um panorama descritivo e analítico extraído a partir da base de dados de publicações e comentários. A análise foi processada localmente com foco em neutralidade informativa.

## 📊 Panorama Geral

* **Total de Registros Analisados (Comentários):** {total_records}
"""
    if publications is not None:
        markdown_content += f"* **Total de Publicações/Posts:** {len(publications)}\n"
    if likes_col and likes_col in analysis_df.columns:
        markdown_content += f"* **Engajamento Total Computado:** {total_likes}\n"
    
    markdown_content += """* **Método de Análise:** Heurística semântica local (dicionário de sentimentos + extração de frequência de termos ponderada).

---
"""

    # Se for vertical estruturado, adiciona a tabela de publicações
    if publications is not None:
        markdown_content += """## 📢 Publicações Monitoradas

Abaixo está o resumo das publicações processadas verticalmente no banco de dados e a respectiva volumetria de interações:

| ID da Publicação | Mês/Período | Comentários | Conteúdo Resumido do Post |
|------------------|-------------|-------------|---------------------------|
"""
        # Ordena as publicações pelo número de comentários (decrescente)
        sorted_pubs = sorted(publications, key=lambda x: x['comments_count'], reverse=True)
        for pub in sorted_pubs:
            resumo_post = pub['content'].replace('\n', ' ').strip()
            if len(resumo_post) > 80:
                resumo_post = resumo_post[:80] + "..."
            markdown_content += f"| **{pub['id']}** | {pub['period']} | {pub['comments_count']} | {resumo_post} |\n"
            
        markdown_content += "\n---\n"

    markdown_content += f"""## 🎭 Distribuição Geral de Sentimentos

Abaixo consta a distribuição de sentimentos identificada nos comentários analisados:

| Sentimento | Quantidade Absoluta | Percentual |
|------------|---------------------|------------|
| **🟢 Positivo** | {pos_count} | {pos_pct:.2f}% |
| **🟡 Neutro** | {neu_count} | {neu_pct:.2f}% |
| **🔴 Negativo** | {neg_count} | {neg_pct:.2f}% |

---

## 🔍 Termos e Expressões Mais Frequentes

Frequência de termos e termos compostos identificada nos textos (ponderada pelo engajamento, se disponível):

### Termos Individuais (Unigramas)
| Termo | Frequência Ponderada |
|-------|----------------------|
"""
    for term, freq in unigrams_freq:
        markdown_content += f"| `{term}` | {freq} |\n"
        
    markdown_content += """
### Expressões Compostas (Bigramas)
| Expressão | Frequência Ponderada |
|-----------|----------------------|
"""
    for bigram, freq in bigrams_freq:
        markdown_content += f"| `{bigram}` | {freq} |\n"
        
    markdown_content += """
---

## 📂 Agrupamentos Temáticos Recorrentes

Distribuição de sentimentos dentro dos temas que mais se destacaram nas menções:

| Tema / Palavra-Chave | Menções Associadas | Positivo (%) | Neutro (%) | Negativo (%) |
|----------------------|--------------------|--------------|------------|--------------|
"""
    for topic, stats in topic_groups.items():
        markdown_content += f"| **{topic}** | {stats['total']} | {stats['pos_pct']:.2f}% | {stats['neu_pct']:.2f}% | {stats['neg_pct']:.2f}% |\n"
        
    markdown_content += """
---

## 💬 Amostras de Registros Representativos

Amostra de publicações e comentários que exemplificam cada categoria de percepção identificada:

### Exemplos Classificados como Positivos
"""
    if pos_samples:
        for idx, sample in enumerate(pos_samples, 1):
            likes_str = f" ({sample['likes']} curtidas)" if likes_col and likes_col in analysis_df.columns else ""
            markdown_content += f"{idx}. **@{sample['author']}**{likes_str}: *\"{sample['text']}\"*\n"
    else:
        markdown_content += "*Nenhuma amostra positiva identificada.*\n"
        
    markdown_content += """
### Exemplos Classificados como Negativos
"""
    if neg_samples:
        for idx, sample in enumerate(neg_samples, 1):
            likes_str = f" ({sample['likes']} curtidas)" if likes_col and likes_col in analysis_df.columns else ""
            markdown_content += f"{idx}. **@{sample['author']}**{likes_str}: *\"{sample['text']}\"*\n"
    else:
        markdown_content += "*Nenhuma amostra negativa identificada.*\n"
        
    markdown_content += """
### Exemplos Classificados como Neutros
"""
    if neu_samples:
        for idx, sample in enumerate(neu_samples, 1):
            likes_str = f" ({sample['likes']} curtidas)" if likes_col and likes_col in analysis_df.columns else ""
            markdown_content += f"{idx}. **@{sample['author']}**{likes_str}: *\"{sample['text']}\"*\n"
    else:
        markdown_content += "*Nenhuma amostra neutra identificada.*\n"
        
    markdown_content += "\n---\n*Relatório gerado automaticamente pelo Social Listening Analyst.*\n"
    
    try:
        os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
        with open(args.out, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        print(f"Sucesso! Relatório gerado em: {args.out}")
    except Exception as e:
        print(f"Erro ao salvar o arquivo markdown: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
