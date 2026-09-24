# La Cocina del Domingo

Planificador semanal de batch cooking para cualquier familia. Todo lo de cada casa (personas, edades, dietas, alergias, comidas libres, tiendas, presupuesto, día de cocina y menú del comedor escolar) se configura en la pestaña «Tu casa»; el menú del cole se puede importar desde un PDF o una foto.

- `PROMPT.md` — el prompt maestro original de la primera familia (Gijón); la app lo construye ahora a partir de los ajustes de cada casa.
- `app/index.html` — la aplicación web: menú semanal generado con IA, lista de la compra por tiendas (Carnicería, Pescadería, Frutería, Mercadona) para marcar en la tienda, plan del domingo, despensa, gustos editables y control del gasto.

La app se publica como Artifact en claude.ai: allí guarda los datos compartidos entre los dos y usa Claude para generar los menús. Abierta fuera de claude.ai funciona en modo local (datos solo en ese navegador, sin IA).

Cada casa necesita su propia copia publicada (su propio enlace), porque los datos se comparten con todas las personas que tienen el enlace.
