# IC – Calculadora de coeficiente de understeer (Fórmula SAE)

Ferramenta, desenvolvida em Iniciação Científica junto ao time de Fórmula SAE, para calcular o gradiente de
understeer (K_us) de um protótipo a combustão e apoiar a definição de setup a partir do layout da pista.

## Escopo deste módulo
Calcula K_us, LLTD, balanço e sensibilidades. Os parâmetros de outras ICs (aerodinâmica, suspensão, diferencial etc.)
entram apenas como **entrada**, listados em `data/parametros/parametros_carro.csv`.

## Estrutura
```
understeer/   código-fonte (modelo bicicleta, pista, otimização)
data/         pistas de exemplo e tabela compartilhada de parâmetros
notebooks/    exploração e testes
docs/         referências e diário da IC
tests/        testes automatizados
```

## Como rodar
```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m understeer.modelo_bicicleta
python -m pytest
```

## Convenções
- Unidades do SI (kg, m, N, rad); saídas de K_us em graus por g.
- K_us > 0: understeer; K_us < 0: oversteer.
- Valores no código são **placeholders** até serem trocados por dados reais do carro.
- Commits em português, no imperativo curto (ex.: "Adiciona cálculo de curvatura").
- Trabalho em branches (`feature/nome-curto`) e merge na `main` após revisão.

## Status
Em fase de proposta e modelagem inicial.
