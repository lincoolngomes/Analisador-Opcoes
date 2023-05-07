import streamlit as st

# Config página
st.set_page_config(
    page_title="Inicio",
    page_icon='',
)

st.title("Seja bem vindo(a)!")

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 


st.write(
    """
    Essa página está em desenvolvimento, o objetivo da página é facilitar na busca, estudo e análise de ações. Nosso objetivo é fornecer uma plataforma intuitiva e fácil de usar para investidores iniciantes e experientes. Estamos trabalhando duro para trazer recursos úteis para ajudar a tornar o processo de análise de ações mais fácil e acessível para todos.

Nossa plataforma contará com ferramentas de pesquisa avançadas, dados em tempo real e gráficos interativos para que você possa tomar decisões informadas sobre seus investimentos. Também estamos desenvolvendo recursos de compartilhamento de informações para que você possa colaborar com outros investidores e discutir estratégias de investimento.

Agradecemos antecipadamente pela sua paciência enquanto trabalhamos para aprimorar nossa plataforma e adicionar novos recursos. Estamos sempre abertos a feedbacks e sugestões, portanto, se você tiver alguma ideia para melhorar nossa plataforma, não hesite em entrar em contato conosco. Obrigado por escolher nossa plataforma para ajudá-lo a alcançar seus objetivos de investimento.**.
    """
)

st.write(
    """
      

    """
)

c1, c2, c3 = st.columns(3)
with c1:
    st.info('**Site: [lincoolngomes.com](https://lincolngomes.com)**', icon="🧠")
with c2:
    st.info('**GitHub: [@lincoolngomes](https://github.com/lincoolngomes)**', icon="💻")
with c3:
    st.info('**Linkedin: [@lincoolngomes](https://www.linkedin.com/in/lincoln-gomes/)**', icon="💡")