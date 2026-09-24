# La Cocina del Domingo

Planificador semanal de batch cooking para una familia de Gijón (2 adultos y un niño de 5 años).

- `PROMPT.md` — el prompt maestro con las reglas de la familia (hidratos, tiendas, comedor, temporada).
- `app/index.html` — la aplicación web: menú semanal generado con IA, lista de la compra por tiendas (Carnicería, Pescadería, Frutería, Mercadona) para marcar en la tienda, plan del domingo, despensa, gustos editables y control del gasto.

La app se publica como Artifact en claude.ai: allí guarda los datos compartidos entre los dos y usa Claude para generar los menús. Abierta fuera de claude.ai funciona en modo local (datos solo en ese navegador, sin IA).
