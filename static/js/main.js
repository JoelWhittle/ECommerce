var modalBtns = document.getElementsByClassName('modalview')
var modalId = 0


var productTitleText =""
for(var i = 0; i < modalBtns.length; i++)
{
modalBtns[i].addEventListener('click', function()
{
	var productId = this.dataset.product;
	var modalInner = document.getElementsByClassName("modalInner");

for (var i = 0, max = modalInner.length; i < max; i++) {
    modalInner[i].style.display = "none";
}

	var modelToLoad = document.getElementById("modal"+productId);
	modelToLoad.style.display = "block";
	console.log('productId', productId);


})
}


