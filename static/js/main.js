// console.log('first')

// document.querySelector(".schedule-btn").addEventListener
// ("click", () => console.log('olaaa'));

document.querySelector('.create-btn').addEventListener('click', showCreateRoute);
document.querySelector('.schedule-btn').addEventListener('click', showScheduleRoute);


function showScheduleRoute(e) {
    e.preventDefault()

    const create = document.querySelector('.create');
    const schedule = document.querySelector('.schedule');
    if (create.classList.contains('show') && !schedule.classList.contains('show')) {
        create.classList.toggle('show')
        schedule.classList.toggle('show')
    }

    document.querySelector('.create').classList.toggle('show')
    document.querySelector('.schedule').classList.toggle('show')
}
function showCreateRoute(e) {
    e.preventDefault()

    const create = document.querySelector('.create');
    const schedule = document.querySelector('.schedule');
    if (!create.classList.contains('show') && schedule.classList.contains('show')) {
        create.classList.toggle('show')
        schedule.classList.toggle('show')
    }

    document.querySelector('.create').classList.toggle('show')
    document.querySelector('.schedule').classList.toggle('show')
}




// document.querySelectorAll('.create-btn').addEventListner
// ('click', showCreateRoute);
// document.querySelectorAll('.create-btn').addEventListner
// ('click', showCreateRoute);
// document.querySelectorAll('.create-btn').addEventListner
// ('click', showCreateRoute);
// document.querySelectorAll('.create-btn').addEventListner
// ('click', showCreateRoute);
