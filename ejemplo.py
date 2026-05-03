from transformers import pipeline

# Load a question-answering pipeline:
#  Importa la función pipeline de la biblioteca transformers, que es una forma fácil y rápida de usar modelos preentrenados
#. para tareas como clasificación, traducción, generación de texto, etc.
qa = pipeline("question-answering", model="deepset/roberta-base-squad2")

# Context where the answer is found
#  Se crea un pipeline de pregunta-respuesta ("question-answering").
#  El modelo deepset/roberta-base-squad2 está basado en RoBERTa, y ha sido entrenado con el dataset SQuAD 2.0, el cual contiene preguntas con contexto.
#  Esto significa que el modelo está preparado para: a) Leer un contexto, b) Entender una pregunta y c) Extraer la respuesta directamente del contexto

# Este es el texto de contexto donde el modelo buscará la respuesta.
context = "Las células eucariotas (del griego eu, 'buen', y karyon, 'nuez', en referencia al núcleo) son las células que se caracterizan por tener un núcleo celular definido, cubierto por una envoltura nuclear de doble membrana.[1] Este núcleo celular contiene el ácido desoxirribonucleico —conocido por las siglas ADN— que constituye el material genético necesario para el desarrollo, funcionamiento y reproducción del organismo.[2] Las células eucariotas se distinguen así de las células procariotas, que carecen de núcleo definido y cuyo material genético se encuentra disperso en el citoplasma.Las células eucariotas forman organismos denominados eucariontes, que constituyen uno de los dos o tres grandes dominios utilizados como categorías taxonómicas en la taxonomía biológica. La aparición de células eucariotas a partir de procariotas significó el gran salto en complejidad de la vida y el más importante después del origen de la vida. Sin la complejidad que adquirieron las células eucariotas, no habrían sido posibles fenómenos posteriores como la aparición de los organismos pluricelulares; la vida, probablemente, se habría limitado a constituirse en un conglomerado de bacterias. De hecho, a excepción de procariontes (del que proceden), los cuatro reinos restantes (animales, plantas, hongos y protistas) son el resultado de ese salto cualitativo. El éxito de estas células eucariotas posibilitó las posteriores radiaciones adaptativas de la vida, que han desembocado en la gran variedad de especies que existen en la actualidad."

# Ask a question
# Aquí se define la pregunta que queremos hacer.
# Es una cadena de texto que será analizada junto con el contexto.
question = "Qué es endosimbiosis seriada?"

# Get the answer
# El pipeline recibe el context y la question.
# El modelo procesa ambos textos y devuelve un resultado que contiene:
result = qa(question=question, context=context)

# Show result
# Imprime la respuesta encontrada por el modelo.
print(result["answer"])
