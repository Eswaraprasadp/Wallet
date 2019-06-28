function sort(expenses){
	var select = document.getElementById('sort-expenses');
	var latestExpenses = document.getElementById('latest-expenses');
	var amountExpenses = document.getElementById('amount-expenses');
	var index = select.selectedIndex;
	if(index == 0){
		latestExpenses.style.display = "block";
		amountExpenses.style.display = "none";
	}
	else if(index == 1){
		latestExpenses.style.display = "none";
		amountExpenses.style.display = "block";
	}
}