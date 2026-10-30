# -*- coding: utf-8 -*-
r"""
build_svgs.py
Genera dark_mode.svg y light_mode.svg con el estilo auténtico de Windows Command Prompt (CMD),
utilizando la tipografía exacta de Bloc de Notas del usuario (Consolas Regular 15pt / 20px, paso 23px),
con la versión mejorada del rostro ASCII (ojos mirando al frente, izquierda (o_)(o_), pestañeo, y puente nasal alineado),
y las estadísticas y datos de educación en inglés para @BlueberryMauro.
"""
import os

def escape_xml(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

raw_ascii_top = [
    """    ."``````'.        """,
    """   /          \\       """,
    """  /   ________/       """,
    """  | .' ==  ==|        """
]

raw_eyes = {
    "center": """  \\(\\=(_o)^(o)        """,
    "left":   """  \\(\\=(o_)(o_)        """,
    "blink":  """  \\(\\=(__)^(_)        """
}

raw_ascii_bottom = [
    """   |\\      | |        """,
    """   | \\     _)|        """,
    """   |\\ \\  ━_━/         """,
    """.'`| '.`__.'          """,
    """   \\     |_           """,
    """    '-__ / `-         """
]

def generate_svg(theme="dark", username="Mauro"):
    is_dark = (theme == "dark")
    
    # Windows CMD Palette (Minimalista, auténtica de Command Prompt)
    bg_color = "#0c0c0c" if is_dark else "#ffffff"
    title_bg = "#181818" if is_dark else "#e8e8e8"
    title_text = "#cccccc" if is_dark else "#1f1f1f"
    border_color = "#2d2d2d" if is_dark else "#d0d7de"
    btn_color = "#999999" if is_dark else "#555555"
    prompt_color = "#cccccc" if is_dark else "#1f1f1f"
    cmd_color = "#ffffff" if is_dark else "#000000"
    prop_color = "#4fa6d8" if is_dark else "#0066cc"
    text_color = "#cccccc" if is_dark else "#24292f"
    muted_color = "#444444" if is_dark else "#d0d7de"
    ascii_color = "#cccccc" if is_dark else "#24292f"

    start_y = 66
    line_step = 23
    ascii_tspans = []
    
    curr = 0
    # Top 4 líneas
    for line in raw_ascii_top:
        y = start_y + curr * line_step
        ascii_tspans.append(f'<tspan x="28" y="{y:.1f}">{escape_xml(line)}</tspan>')
        curr += 1

    # Animación de ojos (solo centro, izquierda y pestañeo)
    y_eyes = start_y + curr * line_step
    c_esc = escape_xml(raw_eyes["center"])
    l_esc = escape_xml(raw_eyes["left"])
    b_esc = escape_xml(raw_eyes["blink"])
    ascii_tspans.append(f"""<tspan x="28" y="{y_eyes:.1f}" class="eye-center">{c_esc}</tspan>
<tspan x="28" y="{y_eyes:.1f}" class="eye-left">{l_esc}</tspan>
<tspan x="28" y="{y_eyes:.1f}" class="eye-blink">{b_esc}</tspan>""")
    curr += 1

    # Bottom 6 líneas
    for line in raw_ascii_bottom:
        y = start_y + curr * line_step
        esc = escape_xml(line)
        ascii_tspans.append(f'<tspan x="28" y="{y:.1f}">{esc}</tspan>')
        curr += 1

    ascii_block = "\n".join(ascii_tspans)

    svg = f"""<?xml version='1.0' encoding='UTF-8'?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 330" width="800px" height="330px">
<style>
.bg {{ fill: {bg_color}; }}
.border {{ stroke: {border_color}; stroke-width: 1.5; }}
.title {{ fill: {title_text}; font-size: 12px; font-family: 'Segoe UI', -apple-system, sans-serif; }}
.prompt {{ fill: {prompt_color}; font-size: 14px; font-family: Consolas, 'Lucida Console', monospace; }}
.cmd {{ fill: {cmd_color}; font-weight: bold; font-size: 14px; font-family: Consolas, 'Lucida Console', monospace; }}
.prop {{ fill: {prop_color}; font-size: 14px; font-family: Consolas, 'Lucida Console', monospace; }}
.text {{ fill: {text_color}; font-size: 14px; font-family: Consolas, 'Lucida Console', monospace; }}
.muted {{ fill: {muted_color}; font-size: 14px; font-family: Consolas, 'Lucida Console', monospace; }}

/* Configuración idéntica a Bloc de Notas: Consolas Regular a 15pt (20px) */
.ascii {{
  fill: {ascii_color};
  font-size: 20px;
  font-family: Consolas, 'Lucida Console', monospace;
  font-weight: normal;
}}
text, tspan {{ white-space: pre; }}

/* Animación de Ojos (centro, izquierda, pestañeo) */
.eye-left, .eye-blink {{ opacity: 0; }}
.eye-center {{ opacity: 1; }}

.eye-center {{ animation: eyeCenter 8s infinite; }}
.eye-left   {{ animation: eyeLeft 8s infinite; }}
.eye-blink  {{ animation: eyeBlink 8s infinite; }}

@keyframes eyeCenter {{
  0%, 37.49%     {{ opacity: 1; }}
  37.5%, 56.24%  {{ opacity: 0; }}
  56.25%, 81.24% {{ opacity: 1; }}
  81.25%, 83.74% {{ opacity: 0; }}
  83.75%, 87.49% {{ opacity: 1; }}
  87.5%, 89.99%  {{ opacity: 0; }}
  90.0%, 100%    {{ opacity: 1; }}
}}

@keyframes eyeLeft {{
  0%, 37.49%     {{ opacity: 0; }}
  37.5%, 56.24%  {{ opacity: 1; }}
  56.25%, 100%   {{ opacity: 0; }}
}}

@keyframes eyeBlink {{
  0%, 81.24%     {{ opacity: 0; }}
  81.25%, 83.74% {{ opacity: 1; }}
  83.75%, 87.49% {{ opacity: 0; }}
  87.5%, 89.99%  {{ opacity: 1; }}
  90.0%, 100%    {{ opacity: 0; }}
}}
</style>

<!-- Ventana Command Prompt -->
<rect width="800px" height="330px" fill="{bg_color}" rx="8" class="border"/>

<!-- Barra de Título Windows CMD -->
<rect width="800px" height="32px" fill="{title_bg}" rx="8" />
<rect y="24" width="800px" height="8px" fill="{title_bg}" />
<line x1="0" y1="32" x2="800" y2="32" stroke="{border_color}" stroke-width="1"/>

<!-- Título de Ventana (sin icono, alineado a la izquierda) -->
<text x="16" y="20" class="title">Command Prompt</text>

<!-- Botones de Control de Ventana Windows (Minimizar, Maximizar, Cerrar) -->
<line x1="710" y1="16" x2="720" y2="16" stroke="{btn_color}" stroke-width="1.2"/>
<rect x="736" y="11" width="10" height="10" stroke="{btn_color}" stroke-width="1.2" fill="none"/>
<line x1="764" y1="11" x2="774" y2="21" stroke="{btn_color}" stroke-width="1.2"/>
<line x1="774" y1="11" x2="764" y2="21" stroke="{btn_color}" stroke-width="1.2"/>

<!-- LADO IZQUIERDO: Retrato ASCII Mejorado (Consolas 15pt / 20px exacta a Bloc de Notas) -->
<text x="28" y="66" class="ascii">
{ascii_block}
</text>

<!-- LADO DERECHO: Formato CMD (Exactamente 11 líneas simétricas) -->
<text x="270" y="66" fill="{text_color}">
<tspan x="270" y="66.0"><tspan class="prompt">C:\\Users\\{username}&gt;</tspan> <tspan class="cmd">whoami</tspan></tspan>
<tspan x="270" y="89.0" class="muted">----------------------------------------------------</tspan>
<tspan x="270" y="112.0"><tspan class="prop">Degree</tspan>      : <tspan class="text">B.S. in Intelligent Computing Engineering</tspan></tspan>
<tspan x="270" y="135.0"><tspan class="prop">University</tspan>  : <tspan class="text">Autonomous University of Aguascalientes</tspan></tspan>
<tspan x="270" y="158.0"><tspan class="prop">Stack</tspan>       : <tspan class="text">Python, Rust, TypeScript, PHP, MySQL</tspan></tspan>
<tspan x="270" y="181.0"><tspan class="prop">CoreSkills</tspan>  : <tspan class="text">Backend, Systems, Fullstack &amp; DB</tspan></tspan>
<tspan x="270" y="204.0" class="muted">----------------------------------------------------</tspan>
<tspan x="270" y="227.0"><tspan class="prop">Repos</tspan>       : <tspan class="text" id="repos_val">5</tspan></tspan>
<tspan x="270" y="250.0"><tspan class="prop">Commits</tspan>     : <tspan class="text" id="commits_val">149</tspan></tspan>
<tspan x="270" y="273.0"><tspan class="prop">Stars</tspan>       : <tspan class="text" id="stars_val">6</tspan></tspan>
<tspan x="270" y="296.0"><tspan class="prop">TotalLOC</tspan>    : <tspan class="text" id="loc_val">1,457,475</tspan></tspan>
</text>
</svg>
"""
    return svg

def main():
    target_dir = r"c:\Users\Lomeli\Downloads\pagit"
    os.makedirs(target_dir, exist_ok=True)
    
    dark_svg = generate_svg("dark", "Mauro")
    light_svg = generate_svg("light", "Mauro")
    
    with open(os.path.join(target_dir, "dark_mode.svg"), "w", encoding="utf-8") as f:
        f.write(dark_svg)
    with open(os.path.join(target_dir, "light_mode.svg"), "w", encoding="utf-8") as f:
        f.write(light_svg)
        
    print("Regenerados dark_mode.svg y light_mode.svg con el nuevo ASCII mejorado!")

if __name__ == "__main__":
    main()
