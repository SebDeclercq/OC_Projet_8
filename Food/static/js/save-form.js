function submit_form() {
    let form = document.querySelector('form.save');
    form.addEventListener('submit', (event) => {
        event.preventDefault();
        let data = new FormData();
        data.append('csrfmiddlewaretoken', form.querySelector('input[name=csrfmiddlewaretoken]').value);
        data.append('substitute', form.querySelector('input[name=substitute]').value);
        data.append('substituted', form.querySelector('input[name=substituted]').value);
        let xhr = new XMLHttpRequest();
        xhr.open('POST', form.getAttribute('action'));
        xhr.addEventListener('load', () => {
            const answer = JSON.parse(xhr.responseText);
            if (xhr.status == 200) {
                let status = answer.status;
                if (status == 'success') {
                    alert('Favori sauvegardé !');
                }
                else {
                    alert('Une erreur est survenue');
                }
            }
            else {
                alert('Une erreur est survenue');
            }
        });
        xhr.send(data);
    });
}
window.onload = submit_form();
