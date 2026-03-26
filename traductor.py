"""
Agente de Traducción Literaria (AR > EN)
Translates Argentine Spanish novels to literary English using the Gemini API.
"""

import os
import sys
import textwrap

import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

SYSTEM_PROMPT = textwrap.dedent("""\
    Actúa como un traductor literario experto, especializado en literatura argentina \
contemporánea y su traducción al inglés (US/UK). Tu objetivo es traducir fragmentos \
de una novela manteniendo el "vibe" porteño/argentino, pero logrando que fluya como \
prosa nativa en inglés.

    ### Directrices de Traducción (AR > EN):
    1. **El Voseo y la Cercanía:** Identifica el uso del "vos" y la confianza entre \
personajes. Traduce esa informalidad usando contracciones y el registro adecuado en \
inglés para que no suene rígido.
    2. **Tratamiento del Lunfardo y Modismos:** No traduzcas expresiones como "che", \
"boludo", "ni en pedo" o "re copado" de forma literal. Busca el equivalente funcional \
en inglés que mantenga la carga emocional y el nivel de agresividad o afecto de la escena.
    3. **Ritmo y Cadencia:** El español tiende a oraciones largas; el inglés literario \
suele ser más directo. Ajusta la puntuación para que el texto tenga "swing" en inglés \
sin perder la voz del autor.
    4. **Contexto Cultural:** Mantén términos como "asado", "mate" o "barrio" si aportan \
a la atmósfera, pero adapta las descripciones para que un lector angloparlante las \
entienda por contexto.

    ### Proceso de Trabajo (Paso a Paso):
    Para cada fragmento que te envíe:
    1. Analiza el subtexto y el tono (¿Es cínico? ¿Es nostálgico? ¿Es bizarro?).
    2. Realiza una traducción de borrador (Draft).
    3. Refina el texto para que sea una "Versión Literaria" pulida.
    4. Incluye una breve sección de "Notas del Traductor" si hubo un argentinismo \
particularmente difícil que tuviste que adaptar.

    ### Formato de Salida:
    ---
    **[Literary Translation]**
    (El texto final pulido en inglés)

    **[Translator's Notes]**
    (Explicación breve de adaptaciones clave de lunfardo o cultura)
""")


def build_model() -> genai.GenerativeModel:
    """Configure and return the Gemini generative model."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not set. Copy .env.example to .env and add your key.")
        sys.exit(1)
    genai.configure(api_key=api_key)
    return genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=SYSTEM_PROMPT,
    )


def translate(model: genai.GenerativeModel, fragment: str) -> str:
    """Send a text fragment to the model and return the literary translation."""
    response = model.generate_content(fragment)
    return response.text


def read_multiline_input(prompt: str) -> str:
    """Read multi-line input from stdin until two consecutive empty lines are entered."""
    print(prompt)
    print("(Press Enter twice when done)")
    lines: list[str] = []
    consecutive_empty = 0
    while True:
        line = input()
        if line == "":
            consecutive_empty += 1
            if consecutive_empty >= 2:
                break
        else:
            consecutive_empty = 0
        lines.append(line)
    # Remove any trailing blank lines accumulated before the sentinel
    while lines and lines[-1] == "":
        lines.pop()
    return "\n".join(lines)


def main() -> None:
    """Interactive CLI loop for the literary translation agent."""
    print("=" * 60)
    print("  Agente de Traducción Literaria  |  AR → EN")
    print("  Argentine Spanish → Literary English")
    print("=" * 60)
    print()

    model = build_model()

    while True:
        try:
            fragment = read_multiline_input("Paste the Spanish fragment to translate:")
        except (EOFError, KeyboardInterrupt):
            print("\nExiting. ¡Hasta luego!")
            break

        if not fragment.strip():
            print("No text entered. Exiting.")
            break

        print("\nTranslating…\n")
        try:
            result = translate(model, fragment)
        except Exception as exc:  # noqa: BLE001
            print(f"Translation error: {exc}")
            print("Common causes: invalid API key, network issue, or rate limit exceeded.")
            continue

        print(result)
        print()

        try:
            again = input("Translate another fragment? [y/N]: ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting. ¡Hasta luego!")
            break

        if again != "y":
            print("¡Hasta luego!")
            break


if __name__ == "__main__":
    main()
