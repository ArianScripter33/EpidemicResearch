#!/usr/bin/env python3
import asyncio
import argparse
import os
import json
import sys
from pydantic import BaseModel, Field
from typing import List, Optional

# Aseguramos que el PYTHONPATH incluya la raíz del proyecto para importar esquemas
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from google.antigravity import Agent, LocalAgentConfig
from src.schemas.scientific import PaperReference, Hypothesis, TournamentRating

# Constantes de configuración
OUTPUT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data/processed/scientific"))
os.makedirs(OUTPUT_DIR, exist_ok=True)

async def run_brainstorm(query: str, output_path: str):
    """
    Generation Agent: Formula hipótesis iniciales buscando literatura científica
    en PubMed u OpenAlex y las valida usando las skills de Antigravity.
    """
    print(f"🧬 [Generation Agent] Iniciando descubrimiento bibliográfico para: '{query}'...")
    
    # Configurar el agente con instrucciones de rigor metodológico
    config = LocalAgentConfig(
        system_instructions=(
            "Eres el Generation Agent, un científico senior de Google DeepMind especializado en Biología Molecular y "
            "Medicina Zoonótica. Tu misión es proponer hipótesis científicas novedosas y rigurosas.\n\n"
            "INSTRUCCIONES:\n"
            "1. Usa tus skills científicas (`pubmed-database` o `literature-search-openalex`) para buscar artículos reales.\n"
            "2. Nunca inventes artículos científicos ni PMIDs. Si no encuentras evidencia, decláralo abiertamente.\n"
            "3. Estructura tu respuesta estrictamente para cumplir con el esquema JSON de una Hipótesis Científica."
        ),
        model="gemini-3.1-flash-lite",
        response_schema=Hypothesis
    )
    
    prompt = (
        f"Investiga y formula una hipótesis científica rigurosa sobre el siguiente tema: '{query}'.\n"
        "Debes realizar una búsqueda en PubMed sobre artículos reales y extraer al menos 2 referencias con sus PMIDs y hallazgos clave.\n"
        "Retorna la hipótesis en un bloque JSON estructurado que cumpla exactamente con el modelo 'Hypothesis' "
        "con campos: 'title', 'mechanism', 'evidence' (lista de objetos con 'pmid', 'title', 'authors', 'relevance_score', 'key_finding') y 'confidence_level'."
    )
    
    async with Agent(config) as agent:
        # Enviar la consulta al agente
        response = await agent.chat(prompt)
        content = await response.text()
        
        # Intentar extraer el JSON de la respuesta
        try:
            # Limpiar posibles delimitadores de markdown en la respuesta
            clean_content = content
            if "```json" in content:
                clean_content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                clean_content = content.split("```")[1].split("```")[0].strip()
                
            data = json.loads(clean_content)
            
            # Guardar la hipótesis estructurada
            with open(output_path, "w") as f:
                json.dump(data, f, indent=2)
                
            print(f"✅ [Generation Agent] Hipótesis formulada y guardada en: {output_path}")
            print(f"🔬 Título: {data.get('title')}")
            print(f"📊 Certidumbre: {data.get('confidence_level')}")
        except Exception as e:
            print(f"❌ Error al procesar structured output del agente: {e}")
            print(f"Respuesta cruda del agente:\n{content}")

async def run_debate(hypothesis_path: str, output_path: str):
    """
    Critique/Reflection Agent: Somete la hipótesis a una severa revisión por pares socrática
    usando un nivel de pensamiento alto (Thinking Level: HIGH) y bases de datos genómicas.
    """
    if not os.path.exists(hypothesis_path):
        print(f"❌ Archivo de hipótesis no encontrado: {hypothesis_path}")
        return
        
    with open(hypothesis_path, "r") as f:
        hypothesis_data = json.load(f)
        
    print(f"🧐 [Critique Agent] Sometiendo a revisión la hipótesis: '{hypothesis_data.get('title')}'...")
    
    # Configurar el revisor con High Thinking para análisis profundo
    # Nota: El SDK maneja de forma óptima el test-time compute
    config = LocalAgentConfig(
        system_instructions=(
            "Eres el Critique/Reflection Agent, un revisor ciego de la revista Nature especializado en evaluar "
            "hipótesis de biología molecular y resistencia antimicrobiana con escepticismo extremo.\n\n"
            "INSTRUCCIONES:\n"
            "1. Analiza la viabilidad del mecanismo molecular propuesto.\n"
            "2. Si la hipótesis carece de evidencia robusta, haz una interrogación socrática proactiva proponiendo vías alternativas.\n"
            "3. Evalúa si hay riesgos de falsos positivos biológicos o sesgos de muestreo.\n"
            "4. Consulta tus skills (`ensembl-database` o `uniprot-database`) si necesitas verificar la viabilidad de genes de resistencia o proteínas."
        ),
        model="gemini-3.5-flash"
    )
    
    prompt = (
        f"Evalúa críticamente la siguiente hipótesis científica:\n\n"
        f"Título: {hypothesis_data.get('title')}\n"
        f"Mecanismo: {hypothesis_data.get('mechanism')}\n"
        f"Nivel de Confianza Inicial: {hypothesis_data.get('confidence_level')}\n"
        f"Evidencia Científica Provista: {json.dumps(hypothesis_data.get('evidence'), indent=2)}\n\n"
        "Escribe una crítica socrática severa, desglosando:\n"
        "1. Consistencia molecular del mecanismo (¿tiene sentido biológico?).\n"
        "2. Debilidades de la evidencia o brechas de datos (¿los papers realmente prueban el punto?).\n"
        "3. Preguntas desafiantes para el científico (Interrogación Socrática).\n"
        "4. Rutas alternativas proactivas de investigación si detectas debilidades."
    )
    
    async with Agent(config) as agent:
        response = await agent.chat(prompt)
        critique = await response.text()
        
        # Guardar la crítica
        with open(output_path, "w") as f:
            f.write(critique)
            
        print(f"✅ [Critique Agent] Análisis crítico guardado en: {output_path}")
        print("\n--- CRÍTICA SOCRÁTICA DESTILADA ---")
        # Mostrar los primeros 500 caracteres de la crítica
        print(critique[:600] + "...\n----------------------------------")

async def run_tournament(ideas_dir: str, output_path: str):
    """
    Tournament/Ranking Agent: Enfrenta hipótesis y críticas en una arena de debate Elo
    para seleccionar la propuesta con mayor solidez científica.
    """
    print(f"⚔️ [Tournament Agent] Iniciando arena de confrontación de hipótesis en: '{ideas_dir}'...")
    
    # Cargar todas las hipótesis y sus críticas en el directorio
    files = [f for f in os.listdir(ideas_dir) if f.endswith(".json")]
    if len(files) < 2:
        print("⚠ Se requieren al menos 2 hipótesis estructuradas (.json) en el directorio para correr un torneo Elo.")
        return
        
    hypotheses = []
    for file in files:
        file_path = os.path.join(ideas_dir, file)
        with open(file_path, "r") as f:
            hypotheses.append(json.load(f))
            
    config = LocalAgentConfig(
        system_instructions=(
            "Eres el Tournament/Ranking Agent de Google Labs. Tu rol es actuar como juez imparcial y cuantitativo "
            "en una arena de confrontación científica. Debes comparar hipótesis y decidir cuál posee el mayor "
            "rigor metodológico y factibilidad de negocio/One Health.\n\n"
            "INSTRUCCIONES:\n"
            "1. Compara las propuestas científicas emparejándolas cara a cara.\n"
            "2. Calcula el score Elo de la ganadora (base inicial 1500, variando ±30 según consistencia).\n"
            "3. Retorna un JSON estructurado que cumpla con el modelo 'TournamentRating'."
        ),
        model="gemini-3.5-flash",
        response_schema=TournamentRating
    )
    
    prompt = (
        f"Compara y evalúa las siguientes hipótesis científicas que compiten en el torneo:\n\n"
        f"{json.dumps(hypotheses, indent=2)}\n\n"
        "Determina cuál es la hipótesis ganadora. Justifica tu decisión basándote en la evidencia empírica provista y el mecanismo molecular.\n"
        "Retorna un bloque JSON estructurado con los campos:\n"
        "- 'winner_title': Título de la hipótesis ganadora.\n"
        "- 'loser_title': Título de la hipótesis perdedora.\n"
        "- 'elo_rating': Score Elo de la ganadora (ej. 1532.0).\n"
        "- 'critique_summary': Resumen del debate y por qué venció a la otra.\n"
        "- 'alternative_pathways': Lista de sugerencias proactivas de investigación."
    )
    
    async with Agent(config) as agent:
        response = await agent.chat(prompt)
        content = await response.text()
        
        try:
            clean_content = content
            if "```json" in content:
                clean_content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                clean_content = content.split("```")[1].split("```")[0].strip()
                
            data = json.loads(clean_content)
            
            with open(output_path, "w") as f:
                json.dump(data, f, indent=2)
                
            print(f"🏆 [Tournament Agent] ¡Torneo finalizado! Resultados guardados en: {output_path}")
            print(f"🥇 Ganadora: {data.get('winner_title')}")
            print(f"📈 Elo Score: {data.get('elo_rating')}")
        except Exception as e:
            print(f"❌ Error al procesar structured output del torneo: {e}")
            print(f"Respuesta cruda:\n{content}")

async def run_synthesize(tournament_path: str, critique_path: str, output_path: str):
    """
    Meta-Review Agent: Compila los debates, ratings Elo y críticas en un reporte final
    Markdown Nature-grade con enlaces clickeables a PubMed.
    """
    print("✍ [Meta-Review Agent] Sintetizando reporte científico final...")
    
    if not os.path.exists(tournament_path):
        print(f"❌ Archivo de torneo no encontrado: {tournament_path}")
        return
        
    with open(tournament_path, "r") as f:
        tournament_data = json.load(f)
        
    critique_content = ""
    if os.path.exists(critique_path):
        with open(critique_path, "r") as f:
            critique_content = f.read()
            
    config = LocalAgentConfig(
        system_instructions=(
            "Eres el Meta-Review Agent. Tu tarea es compilar las discusiones científicas, críticas y scores Elo "
            "en un artículo de revisión científica impecable, estructurado y publicable en formato Markdown.\n\n"
            "INSTRUCCIONES:\n"
            "1. Presenta la hipótesis ganadora con una estructura clara: Resumen, Mecanismo Molecular, y Discusión de Evidencia.\n"
            "2. Destaca los scores Elo de la arena de debate.\n"
            "3. Incorpora la crítica socrática de forma constructiva.\n"
            "4. Asegura que los enlaces a PubMed tengan el formato markdown clickeable: [PMID: XXXXX](https://pubmed.ncbi.nlm.nih.gov/XXXXX)."
        ),
        model="gemini-3.5-flash"
    )
    
    prompt = (
        f"Genera el reporte científico de revisión por pares basado en los siguientes datos:\n\n"
        f"Datos del Torneo Elo:\n{json.dumps(tournament_data, indent=2)}\n\n"
        f"Crítica Socrática de Respaldo:\n{critique_content}\n\n"
        "Crea un artículo en Markdown pulido y listo para inyectarse en el Tercer Avance del proyecto 'Ganado Saludable'."
    )
    
    async with Agent(config) as agent:
        response = await agent.chat(prompt)
        report = await response.text()
        
        with open(output_path, "w") as f:
            f.write(report)
            
        print(f"📄 [Meta-Review Agent] Reporte final sintetizado con éxito en: {output_path}")

def main():
    parser = argparse.ArgumentParser(
        description="co-scientist-local: Motor Científico Multi-Agente impulsado por Google Antigravity SDK.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Comandos disponibles")
    
    # Subcomando brainstorm
    parser_brain = subparsers.add_parser("brainstorm", help="Generar hipótesis grounded en PubMed")
    parser_brain.add_argument("--query", required=True, help="Pregunta o meta de investigación científica")
    parser_brain.add_argument("--output", default=os.path.join(OUTPUT_DIR, "hypothesis_alpha.json"), help="Ruta de salida JSON")
    
    # Subcomando debate
    parser_debate = subparsers.add_parser("debate", help="Someter hipótesis a crítica socrática en High Thinking Level")
    parser_debate.add_argument("--hypothesis_file", required=True, help="Ruta al archivo JSON de la hipótesis")
    parser_debate.add_argument("--output", default=os.path.join(OUTPUT_DIR, "critique_alpha.txt"), help="Ruta de salida de la crítica")
    
    # Subcomando tournament
    parser_tourn = subparsers.add_parser("tournament", help="Correr torneo Elo entre múltiples hipótesis")
    parser_tourn.add_argument("--ideas_dir", required=True, help="Directorio con hipótesis JSON")
    parser_tourn.add_argument("--output", default=os.path.join(OUTPUT_DIR, "tournament_results.json"), help="Ruta de salida JSON del torneo")
    
    # Subcomando synthesize
    parser_synth = subparsers.add_parser("synthesize", help="Compilar debates y scores en un reporte final Markdown")
    parser_synth.add_argument("--tournament_file", required=True, help="Ruta al JSON de resultados del torneo")
    parser_synth.add_argument("--critique_file", required=True, help="Ruta al TXT de la crítica socrática")
    parser_synth.add_argument("--output", default=os.path.join(OUTPUT_DIR, "co_scientist_final_report.md"), help="Ruta de salida Markdown")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
        
    loop = asyncio.get_event_loop()
    if args.command == "brainstorm":
        loop.run_until_complete(run_brainstorm(args.query, args.output))
    elif args.command == "debate":
        loop.run_until_complete(run_debate(args.hypothesis_file, args.output))
    elif args.command == "tournament":
        loop.run_until_complete(run_tournament(args.ideas_dir, args.output))
    elif args.command == "synthesize":
        loop.run_until_complete(run_synthesize(args.tournament_file, args.critique_file, args.output))

if __name__ == "__main__":
    main()
