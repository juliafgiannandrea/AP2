#Frontend da aba DOCUMTENTAÇÃO: 

#Importação das bibliotecas:
import streamlit as st
import pandas as pd

#textos explicativos: 
def render_doc():
    st.subheader("""
                 Uma aplicação para gerenciar e visualizar dados financeiros de forma simples e intuitiva.
                 """)
    st.subheader("OBJETIVO")
    st.write(
        """
Esta aplicação foi desenvolvida para oferecer uma experiência prática e intuitiva na gestão e visualização de dados financeiros, servindo como uma ferramenta interativa para análise de indicadores financeiros de empresas.
O objetivo é permitir que o usuário explore métricas essenciais de rentabilidade e desconto, importantes para o monitoramento da performance de uma empresa no mercado. Indicadores financeiros, como ROE, ROIC, ROC earning yield, p_pv e dividend yield, são amplamente usados por corretoras de investimentos e bolsas de valores para avaliar o desempenho financeiro e o potencial de valorização das empresas. Aqui, o usuário pode selecionar e visualizar esses dados de forma dinâmica, facilitando a tomada de decisões embasadas e estratégicas.
Permitindo que decisões de investimentos sejam pautadas em critérios objetivos e concretos e não meramente em suposições.

        """)
    st.subheader("PLANILHÃO")
    st.write(
        """
Planilha retirada do site do laboratório das finanças () com todas as ações negociadas na bolsa brasileira (B3) com seus respectivos indicadores fundamentalistas calculados a partir de uma data base consulta. Permitindo você analisar, comparar e tomar as melhores decisões de investimento.
"""
    )

    st.subheader("OS INDICADORES")
    st.write(
        """
Indicadores financeiros são métricas que coletam e geram informações sobre um determinado aspecto das demonstrações financeiras de uma empresa. Fornece dados relevantes para o gestor e para o investidor, sobretudo acerca da saúde financeira da organização e o quão rentável ela pode ser.
São importantes para monitorar a performance de uma empresa no mercado: por meio do desempenho passado, o gestor da organização consegue traçar uma previsibilidade futura da empresa. Fica mais fácil delinear com clareza os pontos frágeis do negócio, bem como seus principais potenciais.

"""
    )

    st.subheader("DE RENTABILIDADE:")
    st.write("""
Avalia o desempenho de uma empresa por meio da análise de lucros da mesma. Desse modo, essa métrica dá ao investidor informações a respeito de quanto uma companhia gera de retorno financeiro.
""")
    
    st.subheader("ROE")
    st.write("""
O termo ROE significa “Return on Equity”, também conhecido como o Retorno sobre o Patrimônio Líquido. Ele é considerado um dos indicadores financeiros mais importantes para a análise fundamentalista pois avalia se uma empresa está sendo rentável ou não. É possível descobrir o ROE por meio da fórmula:
ROE = Lucro Líquido ÷ Patrimônio Líquido x 100.
Quanto mais alto for o ROE, mais eficiente a empresa será. Mas atenção, o ROE não deve ser comparado entre empresas de setores diferentes.
""")
    
    st.subheader("ROIC")
    st.subheader("ROC")

    st.subheader("DE DESCONTO: ")

    st.subheader("EARNING YIELD")
    st.write("""
O earnings yield (EY) é o rendimento dos lucros/ganhos. Representa o retorno gerado pelos lucros de uma empresa em relação ao preço de suas ações. Ele mostra aos investidores uma noção dos ganhos obtidos para cada real investido. Quanto maior o valor do earnings yield, maior é o retorno gerado pelos lucros em relação ao preço da ação. Isso indica que a empresa está gerando um bom retorno em relação ao capital investido
É calculado por:
Earning yield (EY) = (lucro por ação nos últimos 12 meses ÷ cotação atual) × 100
Esse indicador entra na “fórmula mágica” do Joel Greenblach.

             """)
    
    st.subheader("DIVIDEND YIELD")
    st.write(
        """
O Dividend Yield, ou rendimento dos dividendos, é uma métrica que representa a relação entre os dividendos pagos por uma empresa e o preço de suas ações. Esse indicador auxilia na comparação entre diferentes empresas, ajudando o investidor a identificar quais delas possuem um histórico de pagamentos de dividendos mais atrativo e consistente.
Ele é calculado da seguinte maneira:
Dividend Yield = Dividendos pagos por ação / cotação da ação × 100
Um Dividend Yield elevado pode indicar que uma empresa é uma boa pagadora de dividendos, proporcionando um retorno adicional ao investidor além da valorização das ações. 
OBS: dividendos são parte do lucro líquido de uma empresa, que é distribuído diretamente aos acionistas, de acordo com o volume de investimento de cada um.
"""
    )

    st.subheader("P/VP")
    st.write(
        """
P/VP, abreviação de Preço sobre Valor Patrimonial, é um indicador que compara o preço de mercado de uma ação com o valor patrimonial correspondente. Ele mostra o quanto investidores estão dispostos a pagar pelo patrimônio líquido da empresa por ação.
P/VP = Preço (da ação) / Valor Patrimonial (da ação)

Se o resultado for superior a 1, significa que o mercado está disposto a pagar mais pelo patrimônio da empresa do que o valor registrado em seus livros.
Se for inferior a 1 sugere que a ação está sendo negociada por menos que o valor do patrimônio líquido da empresa.
"""
    )
    st.write("""
Os conteúdos e textos apresentados acima foram todos retirados e/ou adaptados dos seguintes sites: 
             
https://conteudos.xpi.com.br/
             
https://blog.pagseguro.uol.com.br/p-vp/
             
https://blog.toroinvestimentos.com.br/bolsa/earnings-yield/
             
https://laboratoriodefinancas.com/home

""" 
    )

    st.subheader("DOCUMENTAÇÃO DO CÓDIGO:")
    st.write("Esta seção contém informações sobre como a aplicação foi desenvolvida e manipulada.")


