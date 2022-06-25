let dollarAmountInput = $('input.dollar-amount')

dollarAmountInput.focus(function () {
  let input = $(this);

  if (input.val().length === 0) {
    return;
  }

  input.val(accounting.unformat(input.val()))
});

dollarAmountInput.blur(function () {
  let input = $(this);

  input.val(accounting.formatMoney(accounting.unformat(input.val())))
});

$('#loan-amount, #property-value').blur(function (e) {
  let loanAmount = $('#loan-amount');

  let loanAmountValue = accounting.unformat(loanAmount.val());

  let propertyValue = $('#property-value');

  let propertyValueValue = accounting.unformat(propertyValue.val())

  let ltv = $('#ltv');

  if (loanAmountValue > 0 && propertyValueValue > 0) {
    ltv.val(Math.min((loanAmountValue / propertyValueValue) * 100, 100));

    ltv.val(accounting.toFixed(ltv.val(), 2));

    return;
  }

  ltv.val(0);
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
})();

(function () {
  let tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))

  let tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {

  return new bootstrap.Tooltip(tooltipTriggerEl)
})
})()