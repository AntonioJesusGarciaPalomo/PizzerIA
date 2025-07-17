# 🍕 Pizzería Inteligente con Semantic Kernel

Una aplicación de demostración que utiliza **Semantic Kernel** en Python para crear un asistente inteligente de pizzería impulsado por Azure OpenAI. Este proyecto muestra cómo implementar un sistema de plugins para manejar menús, carritos de compra y procesamiento de pagos mediante conversación natural.

## 🚀 Características

- **Asistente conversacional** que entiende lenguaje natural
- **Sistema de plugins** modular con Semantic Kernel:
  - `PizzaMenuPlugin`: Gestión del menú de pizzas
  - `ShoppingCartPlugin`: Manejo del carrito de compras
  - `PaymentPlugin`: Procesamiento de pagos
- **Integración con Azure OpenAI** para procesamiento de lenguaje natural
- **Function Calling automático** para ejecutar acciones basadas en la intención del usuario

## 📋 Requisitos Previos

- Python 3.8 o superior
- Cuenta de Azure con servicio Azure OpenAI desplegado
- Un modelo de chat desplegado en Azure OpenAI (GPT-3.5-turbo o GPT-4)

## 🛠️ Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/pizzeria-semantic-kernel.git
cd pizzeria-semantic-kernel
```

### 2. Crear entorno virtual

**En Windows:**
```bash
python -m venv pizzaenv
pizzaenv\Scripts\activate
```

**En macOS/Linux:**
```bash
python3 -m venv pizzaenv
source pizzaenv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

Copia el archivo `.example.env` a `.env`:

```bash
cp .example.env .env
```

Edita el archivo `.env` con tus credenciales de Azure OpenAI:

```env
AZURE_OPENAI_ENDPOINT=https://tu-recurso.openai.azure.com/
AZURE_OPENAI_API_KEY=tu-api-key
AZURE_OPENAI_DEPLOYMENT_NAME=nombre-de-tu-deployment
AZURE_OPENAI_API_VERSION=2024-02-01
```

## 🎮 Uso

Ejecuta la aplicación:

```bash
python pizzeria.py
```

### Ejemplos de conversación:

```
🧑 User > Hola, ¿qué pizzas tienen disponibles?
🤖 AI > [El asistente mostrará el menú de pizzas disponibles]

🧑 User > Quiero pedir una pizza Margherita y una Pepperoni
🤖 AI > [El asistente agregará las pizzas al carrito]

🧑 User > ¿Qué tengo en mi carrito?
🤖 AI > [El asistente mostrará el contenido del carrito]

🧑 User > Quiero pagar con tarjeta
🤖 AI > [El asistente procesará el pago y limpiará el carrito]
```

Para salir de la aplicación, escribe `exit`, `quit` o `salir`.

## 🏗️ Arquitectura

### Estructura del Proyecto

```
pizzeria-semantic-kernel/
├── pizzeria.py          # Aplicación principal
├── .env                 # Variables de entorno (no incluido en git)
├── .example.env         # Plantilla de variables de entorno
├── requirements.txt     # Dependencias del proyecto
├── .gitignore          # Archivos ignorados por git
├── LICENSE             # Licencia MIT
└── README.md           # Este archivo
```

### Componentes Principales

1. **Kernel de Semantic Kernel**: Orquesta la comunicación entre el modelo de IA y los plugins
2. **Plugins**:
   - `PizzaMenuPlugin`: Proporciona información sobre pizzas disponibles
   - `ShoppingCartPlugin`: Gestiona operaciones CRUD del carrito
   - `PaymentPlugin`: Simula el procesamiento de pagos
3. **CartService**: Servicio singleton para mantener el estado del carrito
4. **Chat History**: Mantiene el contexto de la conversación

## 🔧 Personalización

### Agregar nuevas pizzas

Modifica el método `get_available_pizzas` en `PizzaMenuPlugin`:

```python
async def get_available_pizzas(self):
    return [
        {"name": "Nueva Pizza", "ingredients": "Ingredientes", "price": 15},
        # ... más pizzas
    ]
```

### Agregar nuevos métodos de pago

Actualiza la lista `valid_methods` en `PaymentPlugin.process_payment`:

```python
valid_methods = ["tarjeta", "efectivo", "paypal", "transferencia"]
```

### Crear nuevos plugins

Sigue el patrón de los plugins existentes:

```python
class NuevoPlugin:
    @kernel_function(name="nombre_funcion", description="Descripción clara")
    async def mi_funcion(self, parametro: str):
        # Implementación
        return "resultado"
```

## 🐛 Solución de Problemas

### Error de conexión con Azure OpenAI

- Verifica que las credenciales en `.env` sean correctas
- Asegúrate de que el endpoint incluya `https://` y termine con `/`
- Confirma que el deployment name corresponda a un modelo de chat

### El asistente no ejecuta las funciones

- Asegúrate de usar un modelo que soporte function calling (GPT-3.5-turbo o GPT-4)
- Verifica que la versión de la API sea compatible (`2024-02-01` o posterior)

## 📚 Recursos Adicionales

- [Documentación de Semantic Kernel](https://learn.microsoft.com/en-us/semantic-kernel/)
- [Azure OpenAI Service](https://azure.microsoft.com/en-us/products/cognitive-services/openai-service)
- [Semantic Kernel Python SDK](https://github.com/microsoft/semantic-kernel/tree/main/python)

## 📝 Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea tu rama de características (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 👤 Autor

Antonio Jesús García Palomo

---

⭐ Si este proyecto te resulta útil, considera darle una estrella en GitHub!