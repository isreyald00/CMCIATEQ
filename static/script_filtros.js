
String.prototype.capitalize = function() {
    return this.charAt(0).toUpperCase() + this.slice(1);
};

function mostrarSublista() {
    // Obtener el valor seleccionado
    var filtroSeleccionado = document.getElementById("filtroPrincipal");
    var filtroSeleccionadoValue = filtroSeleccionado.value;

    // Obtener la posición del elemento seleccionado
    var filtroSeleccionadoRect = filtroSeleccionado.getBoundingClientRect();
    var topPosition = filtroSeleccionadoRect.bottom + window.scrollY;

    // Ocultar todas las sublistas
    ocultarSublistas();

    // Mostrar la sublista correspondiente al valor seleccionado y ajustar la posición
    var sublista = document.getElementById("sublista" + filtroSeleccionadoValue.capitalize());  // Asegúrate de que la primera letra esté en mayúscula
    if (sublista) {
        sublista.style.display = "block";
        sublista.style.top = topPosition + "px";
    }
}

function ocultarSublistas() {
    // Ocultar todas las sublistas
    document.getElementById("sublistaDireccion").style.display = "none";
    document.getElementById("sublistaSede").style.display = "none";
    document.getElementById("sublistaClasificacion").style.display = "none";
}

function actualizarListaEquipos(superF, filtro) {
    // Obtener todos los elementos de la tabla
    var filas = document.querySelectorAll(".table_main tbody tr");
    var registrosCoincidentes = 0;
    // Mostrar u ocultar filas según el filtro
    filas.forEach(function (fila) {
        // Obtener el valor del atributo "data-direccion-especialidad" en la fila actual
        var direccionEspecialidad = fila.getAttribute("dir_e");
        var sede = fila.getAttribute("sede");
        var clasificacion = fila.getAttribute("clasif");
        var estatus = $(fila).find(".clase-estatus").text();
        var dictamen = $(fila).find(".clase-dictamen").text();
        var tipo_comp = $(fila).find(".clase-tipo").text();
        var tipo = tipo_comp.split('-');
        if (int_ext !== undefined){
            var int_ext = tipo[0].trim();
        }
        if (int_ext !== undefined){
            var corr_prev = tipo[1].trim();
        }

        // Comparar el valor con el filtro y mostrar u ocultar la fila en consecuencia
        if (direccionEspecialidad === filtro || filtro === "") {
            fila.style.display = "table-row";
            registrosCoincidentes++;
        } else if (sede === filtro || filtro === "") {
            fila.style.display = "table-row";
            registrosCoincidentes++;
        } else if (clasificacion === filtro || filtro === "") {
            fila.style.display = "table-row";
            registrosCoincidentes++;
        } else if (estatus === filtro || filtro === "") {
            fila.style.display = "table-row";
            registrosCoincidentes++;
        } else if (dictamen === filtro || filtro === "") {
            fila.style.display = "table-row";
            registrosCoincidentes++;
        } else if (int_ext === filtro || filtro === "") {
            fila.style.display = "table-row";
            registrosCoincidentes++;
        } else if (corr_prev === filtro || filtro === "") {
            fila.style.display = "table-row";
            registrosCoincidentes++;
        } else {
            fila.style.display = "none";
        }
    });
    
    $("#numeroRegistros").text(registrosCoincidentes + " equipos coinciden con el filtro: '" +superF +">"+ filtro +"'");
}

$(document).ready(function () {
    $("#inputBusqueda").on("input", function () {
        // Obtener el valor actual del campo de búsqueda
        var valorBusqueda = $(this).val().toLowerCase();

        // Filtrar las filas de la tabla según el valor de búsqueda
        var registrosCoincidentes = 0;
        

        // Filtrar las filas de la tabla según el valor de búsqueda
        $("#tablaEquipos tbody tr").each(function () {

            console.log("Buscando")

            var cod_cer_cal = $(this).find(".cod_cer_cal").text().toLowerCase();;
            console.log("CodCerCal: ", cod_cer_cal)
            var folio = $(this).find(".folio").text();
            var idEquipo = $(this).find("td:first").text().toLowerCase(); // asumiendo que el ID está en la primera columna
            var n_responsable = $(this).attr("n_resp").toLowerCase(); // asumiendo que el atributo "n_resp" contiene el responsable
            var e_responsable = $(this).attr("e_resp").toLowerCase(); // asumiendo que el atributo "e_resp" contiene el responsable
            var fecha = $(this).attr("fecha");

            if (cod_cer_cal !== undefined){
                cod_cer_cal.toLowerCase();
            }
            if (fecha !== undefined){
                fecha.toLowerCase();
            }
            if (folio !== undefined){
                folio.toLowerCase();
            }

            //console.log("Folio: ", folio,"n_resp:", n_responsable);

            // Mostrar u ocultar la fila según el valor de búsqueda
            if (
                (idEquipo && idEquipo.includes(valorBusqueda)) || 
                (n_responsable && n_responsable.includes(valorBusqueda)) || 
                (e_responsable && e_responsable.includes(valorBusqueda)) || 
                (cod_cer_cal && cod_cer_cal.includes(valorBusqueda)) || 
                (fecha && fecha.includes(valorBusqueda)) || 
                (folio && folio.includes(valorBusqueda))
            ){ 
                $(this).show();
                registrosCoincidentes++;
            } else {
                $(this).hide();
            }
        });

        // Actualizar el número de registros coincidentes
        if (valorBusqueda === ""){
            $("#numeroRegistros").text("Sin filtros seleccinados");
        } else{
            $("#numeroRegistros").text(registrosCoincidentes + " registros coinciden con el filtro: '" + $(this).val() +"'");
        }
        });
});
