# 🚀 DataViz Channel - Automated Financial Content Generator

## 📋 Overview
Sistema automatizado completo para generar contenido diario de análisis financiero cripto (Shorts/Reels/TikToks) con datos en tiempo real, gráficos profesionales y SEO optimizado.

## ✅ Características Implementadas

### 🔄 **Sistema Completo**
- ✅ **API Integration**: CoinGecko para datos en tiempo real
- ✅ **Chart Generation**: QuickChart.io para gráficos profesionales
- ✅ **Text-to-Speech**: Edge TTS para narración natural
- ✅ **Video Composition**: FFmpeg para videos verticales 9:16
- ✅ **Template System**: Múltiples estilos para evitar spam
- ✅ **SEO Optimization**: Títulos y etiquetas automatizados
- ✅ **GitHub Actions**: Automatización programada

### 🎨 **Templates Variados**
- **Backgrounds**: 6 estilos diferentes (solid, gradient)
- **Voces**: 6 voces naturales (inglés)
- **Colores**: 5 estilos de gráficos (neon, fire, etc.)
- **Scripts**: 4 plantillas por tipo de contenido

### 📊 **Tipos de Videos**
1. **Bitcoin Focus**: Análisis diario de Bitcoin
2. **Top Gainers**: Las criptos con mayor subida
3. **Market Summary**: Resumen completo del mercado

## 🚀 Inicio Rápido

### 1. Instalación
```bash
# Clonar el repositorio
git clone <repository-url>
cd DATAVIZCHANNEL

# Instalar dependencias
pip install -r requirements.txt

# Configurar entorno
cp .env.example .env
```

### 2. Requisitos
- **Python 3.11+**
- **FFmpeg** (para composición de video)
- **Opcional**: GitHub para automatización

### 3. Generar Videos

#### **MVP (Prueba básica)**
```bash
python mvp_bitcoin_chart.py
```

#### **Video Simple**
```bash
python generate_video.py bitcoin
python generate_video.py gainers
```

#### **Video Avanzado con Templates**
```bash
# Generar video específico
python generate_advanced_video.py single bitcoin
python generate_advanced_video.py single gainers

# Generar lote de videos
python generate_advanced_video.py batch 5

# Probar templates
python generate_advanced_video.py test
```

## 📁 Estructura del Proyecto

```
├── src/
│   ├── coingecko_api.py      # API de CoinGecko
│   ├── chart_generator.py    # QuickChart integration
│   ├── tts_generator.py      # Text-to-Speech
│   ├── video_composer.py     # FFmpeg video composition
│   └── template_manager.py   # Templates y SEO
├── assets/
│   ├── backgrounds/          # Videos de fondo
│   ├── audio/               # Archivos de voz
│   ├── charts/              # Gráficos generados
│   └── output/              # Videos finales
├── .github/workflows/       # Automatización GitHub Actions
├── mvp_bitcoin_chart.py     # MVP simple
├── generate_video.py        # Generador básico
└── generate_advanced_video.py # Generador completo
```

## 🤖 Automatización con GitHub Actions

### **Programación Automática**
- **Frecuencia**: Cada 6 horas
- **Videos por lote**: 3 videos variados
- **Tipos**: Alternando Bitcoin y Top Gainers

### **Ejecución Manual**
1. Ve a Actions > Generate Daily Crypto Videos
2. Click "Run workflow"
3. Selecciona tipo y cantidad
4. Descarga videos desde Artifacts

### **Características CI/CD**
- ✅ Tests automáticos en cada push
- ✅ Linting con flake8
- ✅ Validación de funcionalidad
- ✅ Cache de dependencias

## 🎯 Estrategias de Contenido

### **Para Evitar Spam**
- ✅ 6 fondos diferentes
- ✅ 6 voces variadas  
- ✅ 5 estilos de gráficos
- ✅ 4 plantillas de script
- ✅ Combinaciones aleatorias

### **SEO Optimizado**
- ✅ Títulos con emojis y palabras clave
- ✅ Etiquetas relevantes automáticamente
- ✅ Metadatos en archivos separados
- ✅ Fechas y sentimientos detectados

### **Tipos de Contenido Viral**
1. **"Bitcoin Explodes X%"** - Gran captura de atención
2. **"Top Crypto Performer"** - Análisis de ganadores
3. **"Market Crash Alert"** - Sentimiento de urgencia

## 📊 Ejemplos de Uso

### **Generación Diaria Programada**
```bash
# Automático cada 6 horas via GitHub Actions
# O manual:
python generate_advanced_video.py batch 3
```

### **Personalización de Templates**
```python
from src.template_manager import TemplateManager

template_manager = TemplateManager()
bg_name, bg_config = template_manager.get_background_template()
voice = template_manager.get_voice_template()
style_name, style_config = template_manager.get_chart_style()
```

### **SEO y Metadatos**
```python
from src.template_manager import SEOGenerator

seo = SEOGenerator()
title = seo.generate_seo_title(coin_data, 'bitcoin')
tags = seo.generate_tags(coin_data)
```

## 🔄 Flujo de Trabajo

1. **Data Extraction**: API CoinGecko obtiene datos
2. **Template Selection**: Sistema aleatorio elige estilos
3. **Chart Generation**: QuickChart crea gráficos
4. **Script Generation**: Template Manager crea narración
5. **TTS**: Edge TTS genera audio
6. **Video Composition**: FFmpeg une todo
7. **SEO**: Genera títulos y etiquetas
8. **Output**: Video + metadatos listos para subir

## 🚀 Próximos Mejoras

- [ ] Integración con APIs de YouTube/TikTok
- [ ] Música de fondo automática
- [ ] Análisis de sentimiento de mercado
- [ ] Videos con múltiples criptos
- [ ] Sistema de trending topics
- [ ] Dashboard de analytics

## 📈 Métricas de Éxito

- **Velocidad**: <2 minutos por video
- **Calidad**: Gráficos profesionales 1080x1920
- **Variedad**: 720+ combinaciones posibles
- **Automatización**: 100% sin intervención manual
- **SEO**: Títulos optimizados algorítmicamente

---

**🎯 Resultado Final**: Sistema completamente automatizado que genera contenido financiero viral a escala, optimizado para SEO y diseñado para crecimiento en redes sociales.