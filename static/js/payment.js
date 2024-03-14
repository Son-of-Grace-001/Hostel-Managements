const paymentForm = document.getElementById('paymentForm');
paymentForm.addEventListener("submit", payWithPaystack, false);

function payWithPaystack(amount, e) {
  e.preventDefault();
  let handler = PaystackPop.setup({
    key: 'pk_test_5aa432c04f51f0aea49610d8a1f2c59f1ccdf1d6', // Replace with your public key
    email: document.getElementById("email-address").value,
    amount: amount * 100,
    currency: "NGN",
    ref: ''+Math.floor((Math.random() * 1000000000) + 1), // generates a pseudo-unique reference. Please replace with a reference you generated. Or remove the line entirely so our API will generate one for you
    // label: "Optional string that replaces customer email"
    onClose: function(){
      alert('Window closed.');
    },
    callback: function(response){
      let message = 'Payment complete! Reference: ' + response.reference;
      if (response.status === 'success') {
        window.location.href = '/book_room/';
    }
    }
  });
  // 312975964

  handler.openIframe();
}
