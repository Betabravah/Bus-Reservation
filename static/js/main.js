
document.querySelector('.create-btn').addEventListener('click', showCreateRoute);
document.querySelector('.schedule-btn').addEventListener('click', showScheduleRoute);
document.querySelector('.scheduled-btn').addEventListener('click', showScheduledRoutes);


const create = document.querySelector('.create');
const schedule = document.querySelector('.schedule');
const scheduled = document.querySelector('.scheduled');

function showCreateRoute(e) {
    e.preventDefault()

    if (create.classList.contains('show')){
        create.classList.toggle('show');
    }
    if (!schedule.classList.contains('show')) {
        schedule.classList.toggle('show')
    }
    if (!scheduled.classList.contains('show')) {
        scheduled.classList.toggle('show')
    }
}

function showScheduleRoute(e) {
    e.preventDefault()

    if (!create.classList.contains('show')) {
        create.classList.toggle('show')
    }
    if (schedule.classList.contains('show')) {
        schedule.classList.toggle('show')
    }
    if (!scheduled.classList.contains('show')) {
        scheduled.classList.toggle('show')
    }

}



function showScheduledRoutes(e) {
    e.preventDefault()

    if (!create.classList.contains('show')) {
        create.classList.toggle('show')
    }
    if (!schedule.classList.contains('show')) {
        schedule.classList.toggle('show')
    }
    if (scheduled.classList.contains('show')) {
            scheduled.classList.toggle('show')

    }
}


