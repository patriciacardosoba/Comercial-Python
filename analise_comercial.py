import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def executar_analise_completa():
  print('=== 1. EXTRAÇÃO E CARREGAMENTO ===')
  cal = pd.read_excel('calendario.xlsx', sheet_name='Calendario')
  filiais = pd.read_excel('Filiais.xlsx', sheet_name='Estrutura')
  vendas = pd.read_excel('Vendas.xlsx')
  vendedores = pd.read_excel('Vendedores.xlsx')
  visitas = pd.read_excel('Visitas.xlsx')
  print('-> Ficheiros carregados com sucesso.')

  print('\n=== 2. TRANSFORMAÇÃO E LIMPEZA (ETL) ===')
  # Padronização de datas
  vendas['DATA VENDA'] = pd.to_datetime(
      vendas['DATA VENDA'], format='%d/%m/%Y', errors='coerce'
  )

  # Criar coluna Mês/Ano para análises temporais
  vendas['Mês/Ano'] = vendas['DATA VENDA'].dt.to_period('M').astype(str)

  # Cruzamento de dados comerciais com as filiais (para obter o tipo de estabelecimento)
  # Identifica automaticamente a coluna de ligação correta
  col_filial_vendas = (
      'CÓDIGO FILIAL' if 'CÓDIGO FILIAL' in vendas.columns else 'FILIAL'
  )
  col_filial_estrut = (
      'CÓDIGO FILIAL' if 'CÓDIGO FILIAL' in filiais.columns else 'FILIAL'
  )

  if col_filial_vendas in vendas.columns and col_filial_estrut in filiais.columns:
    vendas_completa = vendas.merge(
        filiais, left_on=col_filial_vendas, right_on=col_filial_estrut, how='left'
    )
  else:
    vendas_completa = vendas.copy()

  print('-> Transformações e cruzamentos aplicados com sucesso.')

  # Garantir que a pasta PYTHON existe para guardar os gráficos atualizados
  os.makedirs('PYTHON', exist_ok=True)

  print('\n=== 3. ANÁLISE: Tendência Temporal de Vendas ===')
  vendas_mensal = (
      vendas.groupby('Mês/Ano').size().reset_index(name='Total de Vendas')
  )

  plt.figure(figsize=(10, 5))
  plt.plot(
      vendas_mensal['Mês/Ano'],
      vendas_mensal['Total de Vendas'],
      marker='o',
      linestyle='-',
      color='#1f77b4',
      linewidth=2,
  )
  plt.title('Tendência Temporal - Volume de Vendas Mensal', fontsize=12, pad=10)
  plt.xlabel('Mês/Ano')
  plt.ylabel('Total de Vendas')
  plt.xticks(rotation=45)
  plt.grid(True, linestyle='--', alpha=0.6)
  plt.tight_layout()
  plt.savefig('PYTHON/tendencia_vendas_mensal.png')
  plt.close()
  print('-> Gráfico de tendência mensal atualizado e guardado.')

  print('\n=== 4. ANÁLISE: Distribuição por Tipo de Estabelecimento ===')
  # Procura dinâmica pela coluna de tipo de estabelecimento
  col_tipo = None
  for col in vendas_completa.columns:
    if any(
        termo in col.upper() for termo in ['TIPO', 'ESTABELECIMENTO', 'SEGMENTO']
    ):
      col_tipo = col
      break

  if col_tipo:
    estab_counts = (
        vendas_completa[col_tipo]
        .value_counts(normalize=True)
        .mul(100)
        .reset_index(name='Percentagem')
    )
    estab_counts.columns = [col_tipo, 'Percentagem']

    plt.figure(figsize=(9, 5))
    plt.bar(
        estab_counts[col_tipo].astype(str),
        estab_counts['Percentagem'],
        color='#2ca02c',
        edgecolor='black',
        alpha=0.85,
    )
    plt.title(
        'Distribuição Percentual por Tipo de Estabelecimento',
        fontsize=12,
        pad=10,
    )
    plt.xlabel('Tipo de Estabelecimento')
    plt.ylabel('Percentagem (%)')
    plt.xticks(rotation=30)
    plt.grid(axis='y', linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.savefig('PYTHON/percentagem_estabelecimentos.png')
    plt.close()
    print('-> Gráfico de percentagem de estabelecimentos gerado com sucesso.')
  else:
    print(
        '-> Aviso: Coluna de tipo de estabelecimento não identificada'
        ' automaticamente.'
    )

  print('\n=== 5. TOP 5 VENDEDORES ===')
  if 'MATRÍCULA' in vendas.columns:
    top_vendedores = (
        vendas.groupby('MATRÍCULA').size().reset_index(name='Vendas_Totais')
    )
    top_vendedores = top_vendedores.sort_values(
        by='Vendas_Totais', ascending=False
    )
    print('Top 5 Vendedores (Matrícula) por Volume de Vendas:')
    print(top_vendedores.head(5).to_string(index=False))

  print(
      '\n=== Processo Automatizado de ETL e Análise Concluído com Sucesso! ==='
  )


if __name__ == '__main__':
  executar_analise_completa()