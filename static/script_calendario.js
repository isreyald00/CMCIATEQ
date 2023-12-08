document.addEventListener('DOMContentLoaded', function(){
    var calendarUI = document.getElementById('calendar');
    var calendar = new FullCalendar.Calendar(calendarUI, {
        headerToolbar:{
            left: 'prev next today',
            center: 'title',
            right:  'dayGridMonth,dayGridDay,dayGridWeek,listMonth'
        },
        events: [
            {% for evento in eventos %}
                {
                    title: "{{ evento.tipo }}: {{ evento.id_equipo }}",
                    start: "{{ evento.proxima|date:'Y-m-d' }}",
                    allDay: true,
                    color: "{{ evento.color }}",
                    textColor: '#000000',
                    responsable: '{{ evento.responsable }}'
                },
            {% endfor %}
        ],
        eventClick: function(info) {
            // Construye un mensaje personalizado con información detallada del evento
            var mensaje = info.event.title + '\n'+
                'Fecha: ' + info.event.start.toLocaleDateString() + '\n' +
                'Responsable: ' + info.event.extendedProps.responsable;

            // Muestra un modal con información detallada del evento
            alert(mensaje);
        },
    });
    calendar.render();
    calendar.setOption('locale','es');
});