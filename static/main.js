// Obtener los enlaces de la barra de navegación
const homeLink = document.getElementById("home-link");
const semanticoLink = document.getElementById("semantico-link");
const sintacticoLink = document.getElementById("sintactico-link");
const lexicoLink = document.getElementById("lexico-link");

// Obtener los contenedores de contenido dinámico
const semanticoContent = document.getElementById("semantico-content");
const sintacticoContent = document.getElementById("sintactico-content");
const lexicoContent = document.getElementById("lexico-content");

// Función para cambiar el contenido en respuesta a un clic en el enlace
function cambiarContenido(event) {
  event.preventDefault(); // Evitar que se produzca la navegación estándar

  // Ocultar todos los contenedores de contenido
  semanticoContent.style.display = "none";
  sintacticoContent.style.display = "none";
  lexicoContent.style.display = "none";
  console.log(event.target);

  // Mostrar el contenedor de contenido correspondiente al enlace clicado
  if (event.target === semanticoLink || event.target === homeLink) {
    semanticoContent.style.display = "block";
  } else if (event.target === sintacticoLink) {
    sintacticoContent.style.display = "block";
  } else if (event.target === lexicoLink) {
    lexicoContent.style.display = "block";
  }
}

// Agregar oyentes de clic a los enlaces de navegación
homeLink.addEventListener("click", cambiarContenido);
semanticoLink.addEventListener("click", cambiarContenido);
sintacticoLink.addEventListener("click", cambiarContenido);
lexicoLink.addEventListener("click", cambiarContenido);

const textarea = document.getElementById("entradaText");
const textareaButton = document.getElementById("textareaSintactico");
const render = document.getElementById("render");

const onChange = async () => {
  const sintaxys = await fetch("http://127.0.0.1:5000/sintactico", {
    method: "POST",
    body: textarea.value,
  });

  const data = await sintaxys.text();

  render.innerHTML = data;
};

textarea.addEventListener("input", onChange);
