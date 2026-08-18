import re

import streamlit as st

st.set_page_config(page_title="Detector de emociones", page_icon="😊", layout="centered")

st.markdown(
    """
    <style>
        :root {
            --vino: #7b1e3a;
            --vino-oscuro: #4d0d22;
            --vino-claro: #f7e3e8;
            --blanco: #ffffff;
            --texto: #2b0a15;
            --gris: #6d4b56;
        }

        .stApp {
            background: linear-gradient(135deg, #fff7f8 0%, #f8e6eb 40%, #f2d5dd 100%);
            color: var(--texto);
        }

        .main .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }

        .titulo {
            color: var(--vino-oscuro);
            font-weight: 800;
            letter-spacing: 0.02em;
        }

        .result-box {
            padding: 1.2rem 1.3rem;
            border-radius: 18px;
            border-left: 8px solid var(--vino);
            background: rgba(123, 30, 58, 0.08);
            box-shadow: 0 8px 18px rgba(123, 30, 58, 0.08);
            margin-top: 1rem;
            margin-bottom: 1rem;
            color: var(--texto);
        }

        .resultado {
            font-size: 2rem;
            font-weight: 800;
            margin: 0;
        }

        .subresultado {
            font-size: 1rem;
            color: var(--gris);
            margin-top: 0.4rem;
        }

        .positiva {
            color: #1f7a45;
        }

        .negativa {
            color: #9b1c1c;
        }

        .neutral {
            color: #5a5a5a;
        }

        div[data-testid="stTextArea"] textarea {
            border: 1px solid rgba(123, 30, 58, 0.35);
            border-radius: 14px;
            background: rgba(255,255,255,0.8);
        }

        .stButton > button {
            background: linear-gradient(135deg, var(--vino) 0%, #9b2d4c 100%);
            color: white;
            border: none;
            border-radius: 12px;
            font-weight: 700;
            padding: 0.5rem 1rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

POSITIVE_WORDS = {
    "feliz", "alegría", "alegre", "contento", "satisfecho", "genial", "maravilloso",
    "bueno", "excelente", "encantado", "optimista", "motivado", "divertido",
    "amor", "increíble", "fantástico", "sonrisa", "triunfo", "éxito", "bien",
    "mejor", "gratitud", "felicidad", "emocionado", "positivo", "entusiasmado"
}

NEGATIVE_WORDS = {
    "triste", "enojo", "enojado", "molesto", "furioso", "miedo", "asustado",
    "decepcionado", "frustrado", "pésimo", "terrible", "horrible", "odio",
    "odioso", "malo", "peor", "nervioso", "angustiado", "deprimido", "tristemente",
    "preocupado", "negativo", "enfadado", "desalentado"
}


def detectar_emocion(texto: str):
    palabras = re.findall(r"[a-záéíóúüñ]+", texto.lower())

    if not palabras:
        return "Neutral", 0, [], []

    positivas = [p for p in palabras if p in POSITIVE_WORDS]
    negativas = [p for p in palabras if p in NEGATIVE_WORDS]

    puntuacion = len(positivas) - len(negativas)

    if puntuacion > 0:
        return "Positiva", puntuacion, positivas, negativas
    if puntuacion < 0:
        return "Negativa", puntuacion, positivas, negativas
    return "Neutral", puntuacion, positivas, negativas


def main():
    st.markdown('<h1 class="titulo">Detector de emociones</h1>', unsafe_allow_html=True)
    st.caption("Escribe una frase y te diré si transmite una emoción positiva, negativa o neutral.")

    texto = st.text_area(
        "Introduce tu frase",
        height=160,
        placeholder="Ejemplo: ¡Hoy me siento muy feliz y motivado para empezar!",
    )

    if st.button("Analizar emoción"):
        if not texto.strip():
            st.warning("Escribe algo antes de analizar la emoción.")
            return

        emocion, puntuacion, positivas, negativas = detectar_emocion(texto)

        if emocion == "Positiva":
            color_class = "positiva"
            emoji = "😊"
            descripcion = "La frase transmite una sensación agradable y optimista."
        elif emocion == "Negativa":
            color_class = "negativa"
            emoji = "😟"
            descripcion = "La frase transmite una sensación incómoda o pesimista."
        else:
            color_class = "neutral"
            emoji = "😐"
            descripcion = "La frase no tiene una carga emocional claramente positiva ni negativa."

        st.markdown(
            f"""
            <div class="result-box">
                <p class="resultado {color_class}">{emoji} {emocion}</p>
                <div class="subresultado">{descripcion}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        col1, col2 = st.columns(2)

        with col1:
            st.info(f"Puntuación: {puntuacion}")

        with col2:
            st.write(f"Frase analizada: {texto}")

        with st.expander("Ver palabras clave detectadas"):
            st.write(f"**Positivas:** {', '.join(positivas) if positivas else 'ninguna'}")
            st.write(f"**Negativas:** {', '.join(negativas) if negativas else 'ninguna'}")

    else:
        st.info("Pulsa el botón para analizar la emoción de la frase.")


if __name__ == "__main__":
    main()
