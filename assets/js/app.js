console.log("FactoryFlow Loaded Successfully");

const ctx = document.getElementById('revenueChart');

if(ctx){

new Chart(ctx,{

type:'bar',

data:{

labels:[
'Jan',
'Feb',
'Mar',
'Apr',
'May',
'Jun'
],

datasets:[

{
label:'Income',
data:[
90000,
120000,
100000,
150000,
130000,
125000
],
backgroundColor:'#2563eb',
borderRadius:8
},

{
label:'Expenses',
data:[
60000,
75000,
70000,
80000,
76000,
78500
],
backgroundColor:'#ef4444',
borderRadius:8
}

]

},

options:{

responsive:true,

plugins:{
legend:{
position:'top'
}
},

scales:{
y:{
beginAtZero:true
}
}

}

});

}