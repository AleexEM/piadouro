document.addEventListener('DOMContentLoaded', function() {
  var elems = document.querySelectorAll('select');
  var instances = M.FormSelect.init(elems, {});
  var comentario_forms = document.querySelectorAll('.piar');
  var clickable_icons = document.querySelectorAll('i[href]');
  var piados_content = document.querySelectorAll('.piado-conteudo');

  comentario_forms.forEach(comentario_form => {
    comentario_form.addEventListener('submit', function (event) {
      if (event.target.querySelector('textarea').value === '') {
        M.toast({html: 'Escreva alguma coisa vacilão!'});
        event.stopPropagation();
        event.preventDefault();
      }
    });
    comentario_form.addEventListener('keypress', function (event) {
      if(event.key === 'Enter'){
        event.preventDefault();
        event.stopPropagation();
        comentario_form.submit();
      }
    });
  });

  clickable_icons.forEach(icon => {
    icon.addEventListener('click', event => {
      location.href = event.target.getAttribute('href');
    })
  })

  piados_content.forEach(piado => {
    var new_content = document.createElement('span');
    piado.textContent.split(' ').forEach(word => {
      if (word.startsWith('#')){
        var anchor = document.createElement('a');
        anchor.innerText = word + ' ';
        anchor.setAttribute('href', `/piado/hashtags/${word.substr(1)}`)
        new_content.appendChild(anchor);
      } else  {
        new_content.appendChild(document.createTextNode(word + ' '))
      }
    });
    piado.innerHTML = '';
    piado.appendChild(new_content);
  });

  // Modal
  var elems = document.querySelectorAll('.modal');
  var instances = M.Modal.init(elems, {});

  // Materialize Jquery
  $('.sidenav').sidenav();
  $(".dropdown-trigger").dropdown();
});
