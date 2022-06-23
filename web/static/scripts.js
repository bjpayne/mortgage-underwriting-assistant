let loanAmountInput = $('#loan-amount')

loanAmountInput.focus(function () {
  let input = $(this);

  if (input.val().length === 0) {
    return;
  }

  input.val(accounting.unformat(input.val()))
});

loanAmountInput.blur(function () {
  let input = $(this);

  input.val(accounting.formatMoney(accounting.unformat(input.val())))
});

(function () {
  'use strict'

  // Fetch all the forms we want to apply custom Bootstrap validation styles to
  var forms = document.querySelectorAll('.needs-validation')

  // Loop over them and prevent submission
  Array.prototype.slice.call(forms)
    .forEach(function (form) {
      form.addEventListener('submit', function (event) {
        if (!form.checkValidity()) {
          event.preventDefault()
          event.stopPropagation()
        }

        form.classList.add('was-validated')
      }, false)
    })
})()