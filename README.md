# TraductorEspIng

Agente de Traducción Literaria — **Argentine Spanish → Literary English**

A CLI tool powered by the [Gemini API](https://ai.google.dev/) that translates fragments from Argentine Spanish novels into polished, native-sounding literary English.  
It handles *lunfardo*, *voseo*, cultural references (mate, asado, barrio) and adjusts rhythm and cadence so the prose feels written-in-English rather than translated.

---

## Output format

For every fragment the agent returns:

```
**[Literary Translation]**
The final, publication-ready English text.

**[Translator's Notes]**
Brief explanation of any Argentine idiom or cultural term that required a non-literal adaptation.
```

---

## Setup

### 1. Clone & install dependencies

```bash
git clone https://github.com/justobeyer/TraductorEspIng.git
cd TraductorEspIng
pip install -r requirements.txt
```

### 2. Configure your Gemini API key

```bash
cp .env.example .env
# Edit .env and replace `your_gemini_api_key_here` with your actual key
```

You can obtain a free API key at <https://aistudio.google.com/app/apikey>.

---

## Usage

```bash
python traductor.py
```

Paste the Spanish text fragment when prompted, press **Enter** twice to submit, and the agent will output the literary English translation together with translator's notes.

### Example

**Input (Argentine Spanish):**
```
Dale, che, no me fallés que ese boliche se pone re copado después de las dos.
```

**Output:**
```
**[Literary Translation]**
Come on, man, don't let me down. That club gets seriously good after two.

**[Translator's Notes]**
"Dale, che" — a typical Rioplatense opener combining encouragement and address; rendered
as "Come on, man" to keep the casual urgency.  
"re copado" — lunfardo intensifier meaning "really great/cool"; translated as
"seriously good" to match register without sounding dated.
```
