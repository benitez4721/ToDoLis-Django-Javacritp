let task_input = document.querySelector('#task-input')
task_input.addEventListener('keyup', (e) => {
    if (e.keyCode == 13){
        add_task(task_input.value)
    }
})
function add_task(task_body){
   
    if (task_body.length > 0){
        fetch('/add_task', {
            method: 'POST',
            body: JSON.stringify({
                body: task_body
            })
        })
        .then( resp => resp.json())
        .then( task => {
            console.log(task)
            let element = document.createElement('div')
            element.innerHTML = `
                <div class = "form-check">
                    <input type="checkbox" class="form-check-input" id=${task.id} style="margin-right: 10px;">                   
                    <label class="form-check-label" for=${task.id}>${task_body}</label>
                </div>
                <i class="fas fa-trash-alt" style="color: rgb(187, 8, 8); cursor: pointer;" onclick = "delete_task(${task.id})"></i>
            `
            element.classList.add("task")
            element.id = `task${task.id}`
            document.querySelector('#tasks-container').append(element)
        })
    }
}

function check(id){
    fetch(`check/${id}`, {
        method: "PUT"
    })
    .then( resp => resp.json())
    .then( resp => console.log(resp))
}

function delete_task(id){
    fetch(`delete/${id}`)
    .then(resp => resp.json())
    .then(resp => console.log(resp))
    console.log("fsaomefsa");
    document.querySelector(`#task${id}`).remove()

}